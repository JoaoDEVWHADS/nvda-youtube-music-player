

"""
Diálogo de busca simplificado: campo de texto + menu de seleção.
"""

import wx
import ui
from logHandler import log

import addonHandler
addonHandler.initTranslation()


class SearchDialog(wx.Dialog):
    """Diálogo de busca para YouTube/YouTube Music."""

    def __init__(self, parent, playerManager):
        super().__init__(
            parent,
            title=_("YouTube Music Player"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        )
        self.playerManager = playerManager
        self.resultsDialog = None

        self._createControls()
        self._bindEvents()
        self.searchText.SetFocus()

        self.CentreOnScreen()
        self.Raise()
        self.SetFocus()

    def _createControls(self):
        """Cria os controles do diálogo."""
        mainSizer = wx.BoxSizer(wx.VERTICAL)


        lbl = wx.StaticText(self, label=_("Pesquisar"))
        mainSizer.Add(lbl, flag=wx.LEFT | wx.TOP, border=10)


        self.searchText = wx.TextCtrl(
            self,
            style=wx.TE_PROCESS_ENTER,
            size=(400, -1),
            name=_("Pesquisar")
        )
        mainSizer.Add(self.searchText, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def _bindEvents(self):
        """Vincula eventos aos controles."""
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.onSearchEnter)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

    def onKeyPress(self, event):
        """Trata pressionamento de teclas."""
        keyCode = event.GetKeyCode()


        if keyCode == wx.WXK_TAB:
            if self._showPlayerIfActive():
                return
            event.Skip()
            return


        if keyCode == wx.WXK_ESCAPE:
            if self.resultsDialog:
                try:
                    self.resultsDialog.Show()
                    self.resultsDialog.Raise()
                    self.resultsDialog.resultsList.SetFocus()
                    self.Hide()
                    return
                except:
                    pass

            return

        event.Skip()

    def _showPlayerIfActive(self):
        """Se tiver player ativo, mostra ele. Retorna True se mostrou."""
        if self.resultsDialog and self.resultsDialog.playerDialog:
            try:
                player = self.resultsDialog.playerDialog
                if not player._destroyed and self.playerManager.is_playing:
                    self.Hide()
                    player.Show()
                    player.Raise()
                    player.SetFocus()
                    return True
            except:
                pass
        return False

    def onSearchEnter(self, event):
        """Mostra menu de seleção de fonte quando pressiona Enter."""
        query = self.searchText.GetValue().strip()
        if not query:
            ui.message(_("Digite algo para buscar"))
            return


        self.last_search_from_menu = True
        menu = wx.Menu()
        youtubeItem = menu.Append(wx.ID_ANY, _("YouTube"))
        youtubeMusicItem = menu.Append(wx.ID_ANY, _("YouTube Music"))


        self.Bind(wx.EVT_MENU, lambda e: self.doSearch("youtube"), youtubeItem)
        self.Bind(wx.EVT_MENU, lambda e: self.doSearch("youtube_music"), youtubeMusicItem)


        pos = self.searchText.GetPosition()
        pos.y += self.searchText.GetSize().height
        self.PopupMenu(menu, pos)
        menu.Destroy()

    def doSearch(self, source):
        """Executa a busca."""
        query = self.searchText.GetValue().strip()
        if not query:
            ui.message(_("Digite algo para buscar"))
            self.searchText.SetFocus()
            return

        ui.message(_("Buscando..."))
        log.info(f"Buscando '{query}' no {source}")


        from .resultsDialog import ResultsDialog
        from .youtubeSearch import YouTubeSearch

        try:
            searcher = YouTubeSearch()
            if source == "youtube":
                results = searcher.search_youtube(query)
            else:
                results = searcher.search_youtube_music(query)

            if not results:
                ui.message(_("Nenhum resultado encontrado"))
                return


            self.Hide()


            oldResultsDialog = self.resultsDialog
            oldPlayerDialog = None

            if oldResultsDialog:
                try:
                    oldPlayerDialog = oldResultsDialog.playerDialog


                    if oldPlayerDialog and not oldPlayerDialog._destroyed:

                        oldResultsDialog.playerDialog = None
                        oldResultsDialog.Hide()
                    else:

                        oldPlayerDialog = None
                        oldResultsDialog.Destroy()

                except Exception:
                    oldPlayerDialog = None


            self.resultsDialog = ResultsDialog(
                self,
                results=results,
                query=query,
                source=source,
                playerManager=self.playerManager
            )


            if oldPlayerDialog and not oldPlayerDialog._destroyed:
                self.resultsDialog.playerDialog = oldPlayerDialog
                oldPlayerDialog.resultsDialog = self.resultsDialog


                if self.playerManager.is_playing:
                    title = oldPlayerDialog.videoData.get('title', '')
                    self.resultsDialog.updatePlayerButton(title)

            self.resultsDialog.Show()

        except Exception as e:
            log.error(f"Erro na busca: {e}")
            ui.message(_("Erro ao buscar: {}").format(str(e)))

    def showFromResults(self):
        """Mostra o diálogo quando volta dos resultados."""
        self.Show()
        self.searchText.SetFocus()


        if getattr(self, 'last_search_from_menu', False):


             wx.CallAfter(self.onSearchEnter, None)

    def onClose(self, event):
        """Fecha o diálogo."""
        self.Destroy()
