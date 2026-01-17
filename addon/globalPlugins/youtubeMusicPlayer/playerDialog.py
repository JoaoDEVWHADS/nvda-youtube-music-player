

"""
Janela do player com controles de teclado para volume, velocidade, pitch e navegação.
"""

import wx
import ui
import threading
from logHandler import log

import addonHandler
addonHandler.initTranslation()


class PlayerDialog(wx.Dialog):
    """Janela do player de áudio com controles de teclado."""

    def __init__(self, parent, videoData, playerManager):
        super().__init__(
            parent,
            title=_("Player - {}").format(videoData.get('title', _('Sem título'))),
            style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        )
        self.resultsDialog = parent
        self.playerManager = playerManager
        self.videoData = videoData
        self.history = []


        self.volume = 100
        self.speed = 1.0
        self.pitch = 0
        self.position = 0
        self.duration = 0
        self.isPlaying = False
        self.repeatEnabled = False
        self._destroyed = False
        self._next_request_id = 0
        self._loading_next = False

        self._createControls()
        self._bindEvents()
        self._startPlayback()

        self.SetSize((450, 200))
        self.CentreOnScreen()
        self.Raise()
        self.SetFocus()

    def _createControls(self):
        """Cria os controles do diálogo - design simplificado."""
        mainSizer = wx.BoxSizer(wx.VERTICAL)


        self.titleLabel = wx.StaticText(
            self,
            label=self.videoData.get('title', _('Sem título'))
        )
        mainSizer.Add(self.titleLabel, flag=wx.ALL | wx.EXPAND, border=10)


        self.statusLabel = wx.StaticText(self, label=_("Carregando..."))
        mainSizer.Add(self.statusLabel, flag=wx.LEFT | wx.RIGHT, border=10)


        self.infoLabel = wx.StaticText(self, label="")
        mainSizer.Add(self.infoLabel, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)


        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.prevButton = wx.Button(self, label=_("&Anterior"))
        self.prevButton.Bind(wx.EVT_BUTTON, self.onPrevTrack)
        buttonSizer.Add(self.prevButton, flag=wx.ALL, border=5)

        self.playPauseButton = wx.Button(self, label=_("&Pausar"))
        self.playPauseButton.Bind(wx.EVT_BUTTON, lambda e: self._togglePlayPause())
        buttonSizer.Add(self.playPauseButton, flag=wx.ALL, border=5)

        self.nextButton = wx.Button(self, label=_("&Próxima"))
        self.nextButton.Bind(wx.EVT_BUTTON, self.onNextTrack)
        buttonSizer.Add(self.nextButton, flag=wx.ALL, border=5)

        self.resultsButton = wx.Button(self, label=_("&Resultados"))
        self.resultsButton.Bind(wx.EVT_BUTTON, lambda e: self._backToResults())
        buttonSizer.Add(self.resultsButton, flag=wx.ALL, border=5)


        ap_label = _("&Desabilitar Auto-Play") if self.playerManager.autoplay_enabled else _("&Habilitar Auto-Play")
        self.autoplayButton = wx.Button(self, label=ap_label)
        self.autoplayButton.Bind(wx.EVT_BUTTON, self.onToggleAutoplay)
        buttonSizer.Add(self.autoplayButton, flag=wx.ALL, border=5)


        rep_label = _("&Repetir: Ligado") if self.repeatEnabled else _("&Repetir: Desligado")
        self.repeatButton = wx.Button(self, label=rep_label)
        self.repeatButton.Bind(wx.EVT_BUTTON, self.onToggleRepeat)
        buttonSizer.Add(self.repeatButton, flag=wx.ALL, border=5)

        mainSizer.Add(buttonSizer, flag=wx.CENTER)

        self.SetSizer(mainSizer)


    def _bindEvents(self):
        """Vincula eventos de teclado."""
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def loadVideo(self, videoData, addToHistory=True):
        """Carrega um novo vídeo na mesma janela (reduz verbosidade)."""

        if addToHistory and hasattr(self, 'videoData') and self.videoData:
             if not hasattr(self, 'history'): self.history = []

             if not self.history or self.history[-1]['id'] != self.videoData['id']:
                 self.history.append(self.videoData)

                 if len(self.history) > 50:
                     self.history.pop(0)

        self.videoData = videoData


        title = videoData.get('title', _('Sem título'))
        channel = videoData.get('channel', '')

        self.SetTitle(_("Player - {}").format(title))
        self.titleLabel.SetLabel(title)


        if channel:
            ui.message(f"{title} - {channel}")
        else:
            ui.message(title)


        self.statusLabel.SetLabel(_("Carregando..."))
        self.isPlaying = False
        self.position = 0
        self.duration = 0


        self._startPlayback()

    def _startPlayback(self):
        """Inicia a reprodução do vídeo."""
        try:
            video_id = self.videoData.get('id', '')
            source = self.videoData.get('source', 'youtube')
            if video_id:

                self.playerManager.play(
                    video_id,
                    self._onPlaybackUpdate,
                    self._onAutoNextTrack,
                    source
                )
                self.isPlaying = True
                self._updateStatus()


                if self.resultsDialog and hasattr(self.resultsDialog, 'updatePlayerButton'):

                    wx.CallAfter(self.resultsDialog.updatePlayerButton, self.videoData)

        except Exception as e:
            log.error(f"Erro ao iniciar reprodução: {e}")
            ui.message(_("Erro ao carregar áudio"))

    def _onAutoNextTrack(self):
        """Chamado quando a música atual termina."""
        log.info("PlayerDialog._onAutoNextTrack chamado")
        ui.message(_("Tocando próxima..."))


        threading.Thread(target=self._playNext).start()

    def _playNextWithId(self, request_id):
        """Executa busca de próxima música com ID para cancelamento."""
        try:
            if request_id != self._next_request_id:
                log.info(f"Request {request_id} cancelado (atual: {self._next_request_id})")
                return
            self._playNextInternal(request_id)
        finally:
            if request_id == self._next_request_id:
                self._loading_next = False

    def _playNext(self):
        self._playNextInternal(self._next_request_id)

    def _playNextInternal(self, request_id):
        try:
            log.info("PlayerDialog._playNext iniciando busca de recomendação")

            if self.repeatEnabled:
                log.info("Modo repetição ativo - recarregando mesma faixa")
                if request_id == self._next_request_id:
                    wx.CallAfter(self.loadVideo, self.videoData, False)
                return

            from .youtubeSearch import YouTubeSearch
            searcher = YouTubeSearch()

            current_id = self.videoData.get('id')
            current_title = self.videoData.get('title', '')
            current_channel = self.videoData.get('channel', '')
            source = self.videoData.get('source', 'youtube_music')
            log.info(f"Buscando recomendação para ID: {current_id} na fonte: {source}")

            exclude_ids = []
            if hasattr(self, 'history'):
                exclude_ids = [item.get('id') for item in self.history[-20:] if item.get('id')]

            if current_id and current_id not in exclude_ids:
                exclude_ids.append(current_id)

            if request_id != self._next_request_id:
                log.info(f"Request {request_id} cancelado antes da busca")
                return

            rec_item = searcher.get_recommendation(
                current_id,
                source=source,
                current_title=current_title,
                exclude_ids=exclude_ids,
                current_channel=current_channel
            )

            if request_id != self._next_request_id:
                log.info(f"Request {request_id} cancelado após busca")
                return

            if rec_item:
                log.info(f"Recomendação encontrada: {rec_item.get('title')}")
                wx.CallAfter(self.loadVideo, rec_item, True)


                if self.resultsDialog and hasattr(self.resultsDialog, 'updatePlayerButton'):
                    wx.CallAfter(self.resultsDialog.updatePlayerButton, rec_item)

            else:
                log.info("Nenhuma recomendação encontrada")
                wx.CallAfter(ui.message, _("Fim da lista"))

        except Exception as e:
            log.error(f"Erro auto-next: {e}")

    def _updateTrackUI(self, title):
        """Atualiza a UI com o novo título da música."""
        if self._destroyed:
            return
        self.SetTitle(_("Player - {}").format(title))
        self.titleLabel.SetLabel(title)
        self.statusLabel.SetLabel(_("Carregando..."))
        self.position = 0
        self.duration = 0

        ui.message(title)


    def _onPlaybackUpdate(self, position, duration, status):
        """Callback para atualizações do player."""
        self.position = position
        self.duration = duration
        wx.CallAfter(self._updateStatus)

    def _updateStatus(self):
        """Atualiza o status na interface."""

        if self._destroyed:
            return
        try:
            if not self or not self.statusLabel:
                return
        except RuntimeError:
            return

        if self.isPlaying:
            status = _("Reproduzindo")
        else:
            status = _("Pausado")

        pos_min = int(self.position // 60)
        pos_sec = int(self.position % 60)
        dur_min = int(self.duration // 60)
        dur_sec = int(self.duration % 60)

        self.statusLabel.SetLabel(
            f"{status} - {pos_min}:{pos_sec:02d} / {dur_min}:{dur_sec:02d}"
        )

        self.infoLabel.SetLabel(
            _("Volume: {}% | Velocidade: {}x | Tom: {}").format(
                self.volume,
                f"{self.speed:.1f}",
                f"+{self.pitch}" if self.pitch > 0 else str(self.pitch)
            )
        )

    def onKeyPress(self, event):
        """Trata comandos de teclado."""
        keyCode = event.GetKeyCode()
        ctrl = event.ControlDown()
        shift = event.ShiftDown()
        alt = event.AltDown()

        if shift and keyCode in [wx.WXK_PAGEUP, wx.WXK_PAGEDOWN]:

            pass


        if keyCode == ord('D'):
            self.onSelectDevice()
            return


        if keyCode == wx.WXK_ESCAPE:

            results = self.resultsDialog
            self._closePlayer()

            if results:
                try:
                    results.Show()
                    results.Raise()
                    results.resultsList.SetFocus()
                except:
                    pass
            return


        if keyCode == wx.WXK_TAB:
            event.Skip()
            return


        if keyCode == wx.WXK_SPACE:
            self._togglePlayPause()
            return


        if keyCode == wx.WXK_UP:
            if ctrl:

                self._changeSpeed(0.1)
            else:

                self._changeVolume(5)
            return


        if keyCode == wx.WXK_DOWN:
            if ctrl:

                self._changeSpeed(-0.1)
            else:

                self._changeVolume(-5)
            return


        if keyCode == wx.WXK_RIGHT:
            if ctrl:

                self._seek(60)
            elif shift:

                self._seek(10)
            else:

                self._seek(1)
            return


        if keyCode == wx.WXK_LEFT:
            if ctrl:

                self._seek(-60)
            elif shift:

                self._seek(-10)
            else:

                self._seek(-1)
            return


        if keyCode == wx.WXK_PAGEUP:
            if ctrl and shift:

                self._changePitch(1)
            elif alt:

                self._changeSpeed(0.1)
            else:

                self._changeSpeedAndPitch(0.1)
            return


        if keyCode == wx.WXK_PAGEDOWN:
            if ctrl and shift:

                self._changePitch(-1)
            elif alt:

                self._changeSpeed(-0.1)
            else:

                self._changeSpeedAndPitch(-0.1)
            return

        event.Skip()

    def _changeVolume(self, delta):
        """Altera o volume."""
        self.volume = max(0, min(100, self.volume + delta))
        self.playerManager.setVolume(self.volume)
        ui.message(_("Volume: {}%").format(self.volume))
        self._updateStatus()

    def _changeSpeed(self, delta):
        """Altera a velocidade (sem alterar pitch)."""
        self.speed = max(0.5, min(2.0, round(self.speed + delta, 1)))
        self.playerManager.setSpeed(self.speed)
        ui.message(_("Velocidade: {}x").format(f"{self.speed:.1f}"))
        self._updateStatus()

    def _changePitch(self, delta):
        """Altera a tonalidade (sem alterar velocidade)."""
        self.pitch = max(-12, min(12, self.pitch + delta))
        self.playerManager.setPitch(self.pitch)
        pitch_str = f"+{self.pitch}" if self.pitch > 0 else str(self.pitch)
        ui.message(_("Tom: {}").format(pitch_str))
        self._updateStatus()

    def _changeSpeedAndPitch(self, delta):
        """Altera velocidade e pitch juntos (como WMP Rate)."""
        self.speed = max(0.5, min(2.0, round(self.speed + delta, 1)))


        pitch_delta = int(round(delta * 16))
        self.pitch = max(-12, min(12, self.pitch + pitch_delta))
        self.playerManager.setSpeedAndPitch(self.speed, self.pitch)
        ui.message(_("Vel+Tom: {}x / {} semitons").format(
            f"{self.speed:.1f}",
            f"+{self.pitch}" if self.pitch > 0 else str(self.pitch)
        ))
        self._updateStatus()


    def _seek(self, seconds):
        """Avança ou retrocede a reprodução usando busca relativa."""

        self.playerManager.seekRelative(seconds)


        self.position = max(0, min(self.duration, self.position + seconds))

        if seconds > 0:
            ui.message(_("Avançou {} segundos").format(abs(seconds)))
        else:
            ui.message(_("Retrocedeu {} segundos").format(abs(seconds)))
        self._updateStatus()

    def _togglePlayPause(self):
        """Pausa ou continua a reprodução."""
        if self.isPlaying:
            self.playerManager.pause()
            self.isPlaying = False
            ui.message(_("Pausado"))
            self.playPauseButton.SetLabel(_("&Continuar"))
        else:
            self.playerManager.resume()
            self.isPlaying = True
            ui.message(_("Reproduzindo"))
            self.playPauseButton.SetLabel(_("&Pausar"))
        self._updateStatus()

    def onNextTrack(self, event=None):
        """Botão Próxima - vai para próxima música."""
        if self._loading_next:
            ui.message(_("Aguarde, já está carregando..."))
            return
        
        self._next_request_id += 1
        current_request = self._next_request_id
        
        if self.playerManager.next_track_callback:
            ui.message(_("Carregando próxima..."))
            self._loading_next = True
            threading.Thread(target=self._playNextWithId, args=(current_request,)).start()
        else:
            ui.message(_("Sem próxima faixa"))

    def onPrevTrack(self, event=None):
        """Botão Anterior - volta no histórico ou reinicia."""

        if self.playerManager.position > 3:
            self.playerManager.seek(0)
            ui.message(_("Reiniciando música"))
        else:

            if self.history:
                try:
                    prev_item = self.history.pop()
                    ui.message(_("Voltando para anterior..."))

                    self.loadVideo(prev_item, addToHistory=False)


                    if self.resultsDialog:
                         wx.CallAfter(self.resultsDialog.updatePlayerButton, prev_item)
                except Exception as e:
                    log.error(f"Erro ao voltar histórico: {e}")
                    self.playerManager.seek(0)
            else:
                self.playerManager.seek(0)
                ui.message(_("Início da lista"))

        self._updateStatus()


    def _backToResults(self):
        """Volta para a lista de resultados (música continua!)."""
        from logHandler import log
        log.info("_backToResults chamado - escondendo player, NÃO parando música")

        self.Hide()

        if self.resultsDialog:
            try:
                self.resultsDialog.Show()
                self.resultsDialog.Raise()
                self.resultsDialog.resultsList.SetFocus()
                log.info("Foco movido para resultsDialog")
            except (RuntimeError, AttributeError) as e:
                log.error(f"Erro ao mostrar resultsDialog: {e}")

                if hasattr(self.resultsDialog, 'searchDialog') and self.resultsDialog.searchDialog:
                    self.resultsDialog.searchDialog.Show()
                    self.resultsDialog.searchDialog.SetFocus()

    def _closePlayer(self):
        """Fecha o player e para a reprodução."""

        self.Close()

    def onSelectDevice(self):
        """Abre diálogo para selecionar dispositivo de áudio."""
        devices = self.playerManager.get_audio_devices()
        if not devices:
            ui.message(_("Nenhum dispositivo encontrado"))
            return


        names = [f"{desc}" for dev_id, desc in devices]


        current_idx = 0

        dlg = wx.SingleChoiceDialog(
            self,
            _("Escolha o dispositivo de saída:"),
            _("Dispositivo de Áudio"),
            names,
            wx.CHOICEDLG_STYLE
        )

        dlg.SetSelection(current_idx)

        if dlg.ShowModal() == wx.ID_OK:
            sel_idx = dlg.GetSelection()
            dev_id = devices[sel_idx][0]
            dev_name = devices[sel_idx][1]

            self.playerManager.set_audio_device(dev_id)
            ui.message(_("Dispositivo alterado para: {}").format(dev_name))

        dlg.Destroy()

    def onToggleAutoplay(self, event):
        """Alterna o estado do auto-play."""
        self.playerManager.autoplay_enabled = not self.playerManager.autoplay_enabled

        if self.playerManager.autoplay_enabled:
            ui.message(_("Auto-Play Habilitado"))
            self.autoplayButton.SetLabel(_("&Desabilitar Auto-Play"))
        else:
            ui.message(_("Auto-Play Desabilitado"))
            self.autoplayButton.SetLabel(_("&Habilitar Auto-Play"))

    def onToggleRepeat(self, event):
        """Alterna o modo de repetição da faixa atual."""
        self.repeatEnabled = not self.repeatEnabled

        if self.repeatEnabled:
            ui.message(_("Repetir Faixa: Ligado"))
            self.repeatButton.SetLabel(_("&Repetir: Ligado"))
        else:
            ui.message(_("Repetir Faixa: Desligado"))
            self.repeatButton.SetLabel(_("&Repetir: Desligado"))

    def onClose(self, event):
        """Evento de fechamento (X da janela, Alt+F4, ou ESC)."""
        if not self._destroyed:
            self._destroyed = True
            self._next_request_id += 1
            self._loading_next = False
            self.playerManager.stop()
            self.playerManager.cleanup()
            self.isPlaying = False
            log.info("PlayerDialog fechado, MPV encerrado")

        if event:
            event.Skip(False)
        self.Destroy()

