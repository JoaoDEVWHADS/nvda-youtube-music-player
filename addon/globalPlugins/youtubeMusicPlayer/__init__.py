

"""
Global Plugin para pesquisar e reproduzir músicas do YouTube/YouTube Music.
Atalho principal: NVDA+Alt+Y
"""


import os
import sys
_lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if _lib_path not in sys.path:
    sys.path.insert(0, _lib_path)

import globalPluginHandler
import scriptHandler
import ui
import gui
import wx
from logHandler import log

import addonHandler
addonHandler.initTranslation()

from .searchDialog import SearchDialog
from .playerManager import PlayerManager
from .settingsPanel import YouTubeMusicPlayerSettingsPanel, YouTubeMusicPlayerSettings
from .updateChecker import UpdateChecker, show_update_dialog, CURRENT_VERSION


class WelcomeDialog(wx.Dialog):
    """Diálogo de boas-vindas exibido na primeira execução."""

    def __init__(self, parent):
        super().__init__(
            parent,
            title=_("Bem-vindo ao YouTube Music Player!"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        )

        self._init_ui()
        self.CenterOnScreen()
        self.Raise()
        self.SetFocus()

    def _init_ui(self):
        """Inicializa a interface do diálogo."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        message = _(
            "Obrigado por instalar o YouTube Music Player!\n\n"
            "Este add-on permite pesquisar e reproduzir músicas do YouTube\n"
            "e YouTube Music diretamente no NVDA.\n\n"
            "Atalho: NVDA+Alt+Y\n\n"
            "⚠️ Nota sobre Cookies:\n"
            "O YouTube atualiza constantemente suas políticas de segurança,\n"
            "o que pode causar instabilidade no uso de cookies para autenticação.\n"
            "O add-on funciona sem cookies para conteúdos públicos."
        )

        message_label = wx.StaticText(self, label=message)
        message_label.Wrap(450)
        main_sizer.Add(message_label, flag=wx.ALL, border=15)


        tip_label = wx.StaticText(
            self,
            label=_("Pressione NVDA+Alt+Y para começar a usar!")
        )
        font = tip_label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        tip_label.SetFont(font)
        main_sizer.Add(tip_label, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)


        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ok_btn = wx.Button(self, wx.ID_OK, _("&OK"))
        ok_btn.SetDefault()
        ok_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_OK))
        button_sizer.Add(ok_btn)

        main_sizer.Add(button_sizer, flag=wx.ALL | wx.ALIGN_CENTER, border=15)

        self.SetSizer(main_sizer)
        self.Fit()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """Plugin global para YouTube Music Player."""

    scriptCategory = _("YouTube Music Player")

    def __init__(self):
        super().__init__()


        self.settings = YouTubeMusicPlayerSettings.get()


        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
            YouTubeMusicPlayerSettingsPanel
        )

        self.playerManager = PlayerManager()
        log.info("YouTube Music Player inicializado")


        log.info(f"YouTubeMusicPlayer: welcome_shown = {self.settings.welcome_shown}")
        if not self.settings.welcome_shown:
            log.info("YouTubeMusicPlayer: Agendando diálogo de boas-vindas em 2 segundos...")

            wx.CallLater(2000, self._show_welcome_message)
        else:
            log.info("YouTubeMusicPlayer: Diálogo de boas-vindas já foi mostrado anteriormente.")


        self.update_checker = UpdateChecker(
            on_update_available_callback=self._on_update_available
        )
        self.update_checker.start()

    def _on_update_available(self, version, download_url, release_info):
        """Callback chamado quando uma atualização está disponível."""
        show_update_dialog(CURRENT_VERSION, version, download_url, release_info)

    def _show_welcome_message(self):
        """Mostra mensagem de boas-vindas na primeira execução."""
        import winsound


        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            pass


        try:
            log.info("YouTubeMusicPlayer: Exibindo diálogo de boas-vindas...")
            dialog = WelcomeDialog(gui.mainFrame)
            gui.mainFrame.prePopup()
            dialog.ShowModal()
            dialog.Destroy()
            gui.mainFrame.postPopup()
            log.info("YouTubeMusicPlayer: Diálogo de boas-vindas fechado.")
        except Exception as e:
            log.error(f"YouTubeMusicPlayer: Error showing welcome dialog: {e}")

        self.settings.welcome_shown = True

    def terminate(self):
        """Limpeza ao descarregar o plugin."""

        try:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
                YouTubeMusicPlayerSettingsPanel
            )
        except ValueError:
            pass

        if self.playerManager:
            self.playerManager.cleanup()
        super().terminate()
        log.info("YouTube Music Player finalizado")

    @scriptHandler.script(
        description=_("Abre o YouTube Music Player"),
        gesture="kb:NVDA+Alt+Y",
        category=_("YouTube Music Player")
    )
    def script_openYouTubePlayer(self, gesture):
        """Abre a interface ou player se estiver tocando."""

        if self.playerManager and self.playerManager.is_playing:
            try:
                def openPlayer():
                    from .playerDialog import PlayerDialog

                    videoData = {
                        'id': self.playerManager.current_video_id,
                        'title': _("Reproduzindo..."),
                        'source': 'unknown'
                    }
                    dlg = PlayerDialog(gui.mainFrame, videoData, self.playerManager)
                    dlg.Show()
                    dlg.Raise()
                    dlg.SetFocus()
                wx.CallAfter(openPlayer)
                return
            except:
                pass


        def openDialog():
            dialog = SearchDialog(
                gui.mainFrame,
                playerManager=self.playerManager
            )
            dialog.Show()
            dialog.Raise()
            dialog.SetFocus()
        wx.CallAfter(openDialog)
