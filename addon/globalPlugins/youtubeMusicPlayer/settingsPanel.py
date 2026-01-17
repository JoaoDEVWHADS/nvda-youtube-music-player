

"""
Painel de configurações do YouTube Music Player nas preferências do NVDA.
"""

import os
import wx
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel
from logHandler import log
import config

import addonHandler
addonHandler.initTranslation()


confspec = {
    "cookiesFilePath": "string(default='')",
    "welcome_shown": "boolean(default=False)",
}

class YouTubeMusicPlayerSettings:
    """Gerencia as configurações do add-on."""

    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):

        if "youtubeMusicPlayer" not in config.conf:
            config.conf.spec["youtubeMusicPlayer"] = confspec
            config.conf["youtubeMusicPlayer"] = {}

    @property
    def cookiesFilePath(self):
        """Retorna o caminho do arquivo de cookies (Netscape format)."""
        try:
            return config.conf["youtubeMusicPlayer"]["cookiesFilePath"]
        except KeyError:
            return ""

    @cookiesFilePath.setter
    def cookiesFilePath(self, value):
        config.conf["youtubeMusicPlayer"]["cookiesFilePath"] = value

    @property
    def welcome_shown(self):
        try:
            return config.conf["youtubeMusicPlayer"]["welcome_shown"]
        except KeyError:
            return False

    @welcome_shown.setter
    def welcome_shown(self, value):
        config.conf["youtubeMusicPlayer"]["welcome_shown"] = value


class YouTubeMusicPlayerSettingsPanel(SettingsPanel):
    """Painel de configurações do YouTube Music Player no NVDA."""


    title = _("YouTube Music Player")

    def makeSettings(self, settingsSizer):
        """Constrói os controles do painel."""
        helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        settings = YouTubeMusicPlayerSettings.get()


        authGroup = guiHelper.BoxSizerHelper(
            self,
            sizer=wx.StaticBoxSizer(
                wx.StaticBox(self, label=_("Autenticação (Opcional)")),
                wx.VERTICAL
            )
        )


        cookiesLabel = _("Arquivo de cookies (cookies.txt - formato Netscape):")
        self.cookiesPathEdit = authGroup.addLabeledControl(
            cookiesLabel,
            wx.TextCtrl,
            value=settings.cookiesFilePath
        )


        browseCookiesBtn = wx.Button(self, label=_("Procurar..."))
        browseCookiesBtn.Bind(wx.EVT_BUTTON, self.onBrowseCookies)
        authGroup.addItem(browseCookiesBtn)

        helper.addItem(authGroup)


        helpText = _(
            "Dica: Utilize extensões como 'Get cookies.txt LOCALLY' para exportar "
            "cookies do navegador. Isso ajuda a contornar bloqueios regionais do YouTube."
        )
        helper.addItem(wx.StaticText(self, label=helpText))

    def onBrowseCookies(self, evt):
        """Abre diálogo para selecionar arquivo de cookies."""

        dlg = wx.FileDialog(
            self,
            _("Selecione o arquivo de cookies"),
            wildcard="Arquivos de texto (*.txt)|*.txt|Todos os arquivos (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.cookiesPathEdit.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onSave(self):
        """Salva as configurações."""
        settings = YouTubeMusicPlayerSettings.get()

        cookiesPath = self.cookiesPathEdit.GetValue().strip()


        if cookiesPath and not os.path.isfile(cookiesPath):

            gui.messageBox(
                _("O arquivo de cookies especificado não existe."),
                _("Erro"),
                wx.OK | wx.ICON_ERROR
            )
            return

        settings.cookiesFilePath = cookiesPath
        log.info(f"YouTube Music Player: Cookies path salvo: {cookiesPath}")
