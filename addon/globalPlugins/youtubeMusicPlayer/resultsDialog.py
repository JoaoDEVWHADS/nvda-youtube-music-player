

"""
Lista de resultados da busca com navegação por páginas.
Tab = próxima página, Shift+Tab = página anterior
Enter = tocar, Escape = voltar à busca
"""

import wx
import ui
from logHandler import log

import addonHandler
addonHandler.initTranslation()


class ResultsDialog(wx.Dialog):
    """Diálogo com lista de resultados da busca."""

    def __init__(self, parent, results, query, source, playerManager):
        super().__init__(
            parent,
            title=_("Resultados da Busca"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.STAY_ON_TOP
        )
        self.searchDialog = parent
        self.playerManager = playerManager
        self.results = results
        self.query = query
        self.source = source
        self.currentPage = 1
        self.playerDialog = None

        self._createControls()
        self._bindEvents()
        self._populateResults()

        self.SetSize((900, 450))
        self.CentreOnScreen()

    def _createControls(self):
        """Cria os controles do diálogo."""
        mainSizer = wx.BoxSizer(wx.VERTICAL)


        self.txtNowPlaying = wx.TextCtrl(
            self,
            value=_("Parado"),
            style=wx.TE_READONLY | wx.TE_CENTRE | wx.TE_NO_VSCROLL
        )


        mainSizer.Add(self.txtNowPlaying, flag=wx.EXPAND | wx.ALL, border=10)


        self.pageLabel = wx.StaticText(self, label="")
        mainSizer.Add(self.pageLabel, flag=wx.LEFT | wx.RIGHT, border=10)


        self.resultsList = wx.ListBox(
            self,
            style=wx.LB_SINGLE,
            size=(480, 250)
        )
        mainSizer.Add(self.resultsList, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)


        instructions = wx.StaticText(
            self,
            label=_("Enter: Tocar | Tab: Navegar | Escape: Voltar")
        )


        navSizer = wx.BoxSizer(wx.HORIZONTAL)


        self.btnPrev = wx.Button(self, label=_("< Página Anterior"))
        self.btnPrev.Bind(wx.EVT_BUTTON, lambda e: self.onPreviousPage())


        self.btnPlayer = wx.Button(self, label=_("Player"))
        self.btnPlayer.Bind(wx.EVT_BUTTON, lambda e: self.onOpenPlayer())


        self.btnNext = wx.Button(self, label=_("Próxima Página >"))
        self.btnNext.Bind(wx.EVT_BUTTON, lambda e: self.onNextPage())


        navSizer.Add(self.btnPrev, flag=wx.RIGHT, border=5)
        navSizer.Add(self.btnPlayer, flag=wx.LEFT | wx.RIGHT, border=5)
        navSizer.Add(self.btnNext, flag=wx.LEFT, border=5)

        mainSizer.Add(navSizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        mainSizer.Add(instructions, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.SetSizer(mainSizer)

    def _bindEvents(self):
        """Vincula eventos."""
        self.resultsList.Bind(wx.EVT_LISTBOX_DCLICK, self.onPlaySelected)
        self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
        self.Bind(wx.EVT_CLOSE, self.onClose)


        self.btnPlayer.Bind(wx.EVT_KEY_DOWN, self.onPlayerButtonKey)

    def onPlayerButtonKey(self, event):
        """Controles inline quando o foco está no botão Player."""
        keyCode = event.GetKeyCode()

        if not self.playerManager or not self.playerManager.is_playing:
            event.Skip()
            return


        if keyCode == wx.WXK_SPACE:
            self.playerManager.play_pause()
            return


        if keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.onOpenPlayer()
            return


        if keyCode == wx.WXK_LEFT:
            self.playerManager.seek_relative(-10)
        elif keyCode == wx.WXK_RIGHT:
            self.playerManager.seek_relative(10)
        elif keyCode == wx.WXK_UP:
            self.playerManager.change_volume(5)
        elif keyCode == wx.WXK_DOWN:
            self.playerManager.change_volume(-5)
        else:
            event.Skip()

    def onOpenPlayer(self, event=None):
        """Reabre o player."""
        if self.playerDialog:
            try:

                if self.playerDialog._destroyed:
                    self.playerDialog = None
                    ui.message(_("Player não está ativo"))
                    return

                self.Hide()
                self.playerDialog.Show()
                self.playerDialog.SetFocus()
            except (RuntimeError, AttributeError):

                self.playerDialog = None
                ui.message(_("Player não está ativo"))
        else:
            ui.message(_("Player não está ativo"))

    def _populateResults(self):
        """Popula a lista com os resultados."""
        self.resultsList.Clear()

        for item in self.results:
            title = item.get('title', _('Sem título'))
            duration = item.get('duration', '')
            channel = item.get('channel', '')

            if duration:
                display = f"{title} - {duration}"
            else:
                display = title

            if channel:
                display += f" ({channel})"

            self.resultsList.Append(display, item)

        if self.resultsList.GetCount() > 0:
            self.resultsList.SetSelection(0)
            self.resultsList.SetFocus()

        self._updatePageLabel()

    def _updatePageLabel(self):
        """Atualiza o label da página."""
        count = self.resultsList.GetCount()
        self.pageLabel.SetLabel(
            _("Página {page} - {count} resultados para '{query}'").format(
                page=self.currentPage,
                count=count,
                query=self.query
            )
        )

    def onCharHook(self, event):
        """Trata teclas globais do diálogo."""
        keyCode = event.GetKeyCode()
        focusObj = self.FindFocus()


        if focusObj == self.btnPlayer:

            if self.playerManager and self.playerManager.is_playing:

                if keyCode == wx.WXK_SPACE:
                    log.info("Inline: Play/Pause")
                    self.playerManager.play_pause()
                    return
                elif keyCode == wx.WXK_LEFT:
                    self.playerManager.seek_relative(-10)
                    return
                elif keyCode == wx.WXK_RIGHT:
                    self.playerManager.seek_relative(10)
                    return
                elif keyCode == wx.WXK_UP:
                    self.playerManager.change_volume(5)
                    return
                elif keyCode == wx.WXK_DOWN:
                    self.playerManager.change_volume(-5)
                    return


            if keyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
                self.onOpenPlayer()
                return

        if keyCode == wx.WXK_ESCAPE:
            self.onBackToSearch()
        elif keyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):

            if focusObj == self.resultsList:
                self.onPlaySelected(event)
            else:
                event.Skip()
        else:
            event.Skip()

    def _showPlayerIfActive(self):
        """Se tiver player ativo, mostra ele. Retorna True se mostrou."""
        if self.playerDialog:
            try:
                if not self.playerDialog._destroyed and self.playerManager.is_playing:
                    self.Hide()
                    self.playerDialog.Show()
                    self.playerDialog.Raise()
                    self.playerDialog.SetFocus()
                    return True
            except:
                pass
        return False

    def onNextPage(self):
        """Carrega próxima página de resultados."""
        from .youtubeSearch import YouTubeSearch

        ui.message(_("Carregando próxima página..."))
        self.currentPage += 1

        try:
            searcher = YouTubeSearch()
            if self.source == "youtube":
                results = searcher.search_youtube(self.query, page=self.currentPage)
            else:
                results = searcher.search_youtube_music(self.query, page=self.currentPage)

            if results:
                self.results = results
                self._populateResults()
                ui.message(_("Página {} carregada").format(self.currentPage))
            else:
                self.currentPage -= 1
                ui.message(_("Não há mais resultados"))

        except Exception as e:
            self.currentPage -= 1
            log.error(f"Erro ao carregar página: {e}")
            ui.message(_("Erro ao carregar página"))

    def onPreviousPage(self):
        """Carrega página anterior de resultados."""
        if self.currentPage <= 1:
            ui.message(_("Já está na primeira página"))
            return

        from .youtubeSearch import YouTubeSearch

        ui.message(_("Carregando página anterior..."))
        self.currentPage -= 1

        try:
            searcher = YouTubeSearch()
            if self.source == "youtube":
                results = searcher.search_youtube(self.query, page=self.currentPage)
            else:
                results = searcher.search_youtube_music(self.query, page=self.currentPage)

            if results:
                self.results = results
                self._populateResults()
                ui.message(_("Página {} carregada").format(self.currentPage))

        except Exception as e:
            self.currentPage += 1
            log.error(f"Erro ao carregar página: {e}")
            ui.message(_("Erro ao carregar página"))

    def onPrevTrack(self):
        """Toca a música anterior da lista."""
        selection = self.resultsList.GetSelection()
        if selection == wx.NOT_FOUND or selection <= 0:
            ui.message(_("Início da lista"))
            return

        self.resultsList.SetSelection(selection - 1)
        self.onPlaySelected()

    def onNextTrack(self):
        """Toca a próxima recomendação (Smart Shuffle)."""

        current_id = None


        if self.playerManager and self.playerManager.current_video_id:
            current_id = self.playerManager.current_video_id


        if not current_id:
            selection = self.resultsList.GetSelection()
            if selection != wx.NOT_FOUND:
                item = self.resultsList.GetClientData(selection)
                current_id = item.get('id')

        if not current_id:
            ui.message(_("Tocar algo primeiro para recomendações"))
            return

        ui.message(_("Buscando próxima..."))

        from .youtubeSearch import YouTubeSearch
        import threading

        def _fetch_and_play():
            try:
                searcher = YouTubeSearch()

                rec_item = searcher.get_recommendation(current_id)

                if rec_item:


                    if 'source' not in rec_item:
                         rec_item['source'] = self.source

                    self._play_item(rec_item, switch_focus=False)

                else:

                    wx.CallAfter(self._play_next_sequential)
            except Exception as e:
                log.error(f"Erro smart next: {e}")
                wx.CallAfter(self._play_next_sequential)

        threading.Thread(target=_fetch_and_play).start()

    def _play_next_sequential(self):
        """Fallback: Toca próxima da lista."""
        selection = self.resultsList.GetSelection()
        count = self.resultsList.GetCount()
        if selection != wx.NOT_FOUND and selection < count - 1:
            self.resultsList.SetSelection(selection + 1)
            self.onPlaySelected()
        else:
            ui.message(_("Fim da lista"))

    def _play_item(self, item, switch_focus=True):
        """Helper para tocar um item (usado por thread)."""
        wx.CallAfter(self._play_item_ui, item, switch_focus)

    def _play_item_ui(self, item, switch_focus=True):
        """Executa a ação de tocar na UI thread."""
        from .playerDialog import PlayerDialog

        title = item.get('title', '')


        self.updatePlayerButton(title)


        if self.playerDialog:
            try:

                if self.playerDialog._destroyed:
                    self.playerDialog = None
                else:
                    self.playerDialog.loadVideo(item)
                    if switch_focus:
                        self.playerDialog.Show()
                        self.playerDialog.SetFocus()
                        self.Hide()
                    else:


                        self.playerDialog.Show()
                        self.Raise()
                        self.resultsList.SetFocus()
                    return
            except (RuntimeError, AttributeError):
                self.playerDialog = None


        self.playerDialog = PlayerDialog(
            self,
            videoData=item,
            playerManager=self.playerManager
        )

        if switch_focus:
            self.playerDialog.Show()
            self.Hide()
        else:

            self.playerDialog.Show()
            self.Raise()
            self.resultsList.SetFocus()

    def onPlaySelected(self, event=None):
        """Toca o item selecionado."""
        selection = self.resultsList.GetSelection()
        if selection == wx.NOT_FOUND:
            ui.message(_("Selecione um item para tocar"))
            return

        item = self.resultsList.GetClientData(selection)
        if not item:
            return

        self._play_item_ui(item, switch_focus=True)

    def onBackToSearch(self):
        """Volta para a busca (ESC)."""
        self.Hide()
        self.searchDialog.showFromResults()

    def onClose(self, event):
        """Fecha tudo (Alt+F4)."""

        self._cleanupPlayer()


        if self.searchDialog:
            self.searchDialog.Close()
        self.Destroy()

    def _cleanupPlayer(self):
        """Limpa o player antes de destruir este diálogo."""
        if self.playerDialog:
            try:

                self.playerDialog.playerManager.stop()
                self.playerDialog._destroyed = True
                self.playerDialog.Destroy()
            except:
                pass
            finally:
                self.playerDialog = None

    def showFromPlayer(self):
        """Mostra os resultados quando volta do player."""
        self.Show()
        self.resultsList.SetFocus()

        if self.playerManager and self.playerManager.is_playing:
             pass
        else:
             self.updatePlayerButton(None)

    def updatePlayerButton(self, info):
        """Atualiza o texto do botão Player com a música atual.
           info: pode ser string (titulo) ou dict (videoData)
        """
        title = ""
        channel = ""

        if isinstance(info, dict):
            title = info.get('title', _('Sem título'))
            channel = info.get('channel', '') or info.get('author', '')
        elif isinstance(info, str):
            title = info

        if title:

            if channel:
                display_full = f"{title} - {channel}"
            else:
                display_full = title


            self.txtNowPlaying.SetValue(_("Tocando: {}").format(display_full))


            if len(display_full) > 30:
                short_display = display_full[:27] + "..."
            else:
                short_display = display_full

            self.btnPlayer.SetLabel(_("Player ({})").format(short_display))
        else:
            self.txtNowPlaying.SetValue(_("Parado"))
            self.btnPlayer.SetLabel(_("Player"))

    def onBackToSearch(self):
        """Volta para a busca (música continua em background)."""

        self.Hide()
        self.searchDialog.showFromResults()
