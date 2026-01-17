

"""
Gerenciador do player de áudio usando MPV com suporte IPC.
Permite controle em tempo real de Volume, Speed e Pitch.
"""

import subprocess
import threading
import time
import os
import json
import random
from logHandler import log
import wx
import ui

import addonHandler
addonHandler.initTranslation()


class PlayerManager:
    """Gerencia a reprodução de áudio usando MPV e IPC."""

    def __init__(self):
        self.current_video_id = None
        self.audio_url = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 100
        self.speed = 1.0
        self.pitch = 0
        self.position = 0
        self.duration = 0
        self.update_callback = None
        self.next_track_callback = None
        self._process = None
        self._update_thread = None
        self._stop_update = False
        self._lock = threading.RLock()
        self._source = None
        self._start_time = None
        self._start_position = 0
        self._ipc_thread = None
        self._loading_new_track = False
        self._pipe_handle = None
        self._autoplay_timer = None
        self._track_duration_seconds = 0
        self.autoplay_enabled = True
        self._load_request_id = 0


        self.audio_devices = []
        self.current_device_idx = 0


        self._ipc_path = f"\\\\.\\pipe\\mpv-nvda-{os.getpid()}-{random.randint(1000,9999)}"
        self._mpv_path = self._get_mpv_path()


        self._start_mpv_process()

    def _get_mpv_path(self):
        """Obtém o caminho do mpv.exe."""
        addon_path = os.path.dirname(os.path.abspath(__file__))
        mpv = os.path.join(addon_path, 'lib', 'mpv.exe')
        if os.path.exists(mpv):
            return mpv
        return "mpv"

    def _start_mpv_process(self):
        """Inicia processo MPV em modo Idle."""
        self._kill_process()

        cmd = [
            self._mpv_path,
            '--no-video',
            '--really-quiet',
            '--idle=yes',
            '--keep-open=yes',
            f'--input-ipc-server={self._ipc_path}',
            f'--volume={self.volume}',
            f'--speed={self.speed}',
        ]

        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            self._process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )


            self._start_ipc_thread()
            self._start_update_thread()


            threading.Thread(target=self._refresh_audio_devices, daemon=True).start()

        except Exception as e:
            log.error(f"Erro ao iniciar MPV Idle: {e}")

    def _start_ipc_thread(self):
        """Thread para ler eventos JSON do MPV via named pipe."""
        self._ipc_thread = threading.Thread(target=self._ipc_loop)
        self._ipc_thread.daemon = True
        self._ipc_thread.start()

    def _ipc_loop(self):
        """Loop de leitura de eventos IPC via named pipe."""
        import time


        time.sleep(1.0)

        retry_count = 0
        max_retries = 5

        while self._process and retry_count < max_retries:
            try:

                self._pipe_handle = open(self._ipc_path, 'r+b', buffering=0)
                log.info(f"Conectado ao pipe MPV: {self._ipc_path}")
                break
            except FileNotFoundError:
                log.warning(f"Pipe não encontrado, tentativa {retry_count+1}/{max_retries}")
                retry_count += 1
                time.sleep(0.5)
            except Exception as e:
                log.error(f"Erro ao conectar ao pipe: {e}")
                retry_count += 1
                time.sleep(0.5)
        else:
            log.error("Não foi possível conectar ao pipe MPV para eventos")
            return

        buffer = b""
        while self._process and self._pipe_handle:
            try:

                byte = self._pipe_handle.read(1)
                if not byte:
                    time.sleep(0.05)
                    continue

                buffer += byte


                if byte == b'\n':
                    try:
                        line = buffer.strip()
                        if line:
                            event = json.loads(line.decode('utf-8'))
                            self._handle_ipc_event(event)
                    except json.JSONDecodeError:
                        pass
                    except Exception as e:
                        log.error(f"Erro processando evento IPC: {e}")
                    finally:
                        buffer = b""

            except Exception as e:
                log.error(f"Erro no loop IPC: {e}")
                time.sleep(0.1)

        try:
            if self._pipe_handle:
                self._pipe_handle.close()
                self._pipe_handle = None
        except:
            pass


    def _handle_ipc_event(self, event):
        """Trata eventos do MPV."""
        evt_type = event.get('event')
        request_id = event.get('request_id')


        if request_id is not None and 'data' in event:
            data = event.get('data')
            if request_id == 10 and data is not None:
                self.position = float(data)
            elif request_id == 11 and data is not None:
                self.duration = float(data)
            return

        if evt_type == 'end-file':
            reason = event.get('reason', '')
            log.info(f"MPV end-file reason: {reason}")


            if reason in ('eof', 0, 'stop', 'redirect') and not self._loading_new_track:
                self._on_track_end()
            elif reason == 'stop' and self._loading_new_track:
                log.info("end-file stop ignorado (carregando nova faixa)")

        elif evt_type == 'idle':

            if self.is_playing and not self._loading_new_track:
                log.info("MPV idle detectado enquanto is_playing=True - música acabou naturalmente")
                self._on_track_end()

        elif evt_type == 'seek':


            threading.Timer(0.5, self._recalculate_timer_after_seek).start()

        elif evt_type == 'property-change':
            name = event.get('name')
            data = event.get('data')
            if name == 'time-pos' and data is not None:
                self.position = float(data)
            elif name == 'duration' and data is not None:
                self.duration = float(data)
            elif name == 'eof-reached' and data == True:

                log.info("eof-reached detectado - stream terminou naturalmente")
                if not self._loading_new_track:
                    self._on_track_end()


    def _on_track_end(self):
        """Chamado quando a faixa termina."""

        self._cancel_autoplay_timer()

        self.is_playing = False
        self.is_paused = False


        if self.next_track_callback:

            if self.autoplay_enabled:
                log.info("Faixa terminou. Chamando next_track_callback (autoplay habilitado)")

                wx.CallAfter(self.next_track_callback)
            else:
                log.info("Faixa terminou mas auto-play está desabilitado")
        else:

            log.info("Faixa terminou mas callback já foi limpo (player parado)")


    def _start_autoplay_timer(self, duration_seconds):
        """Inicia timer para auto-play após duração da faixa."""
        self._cancel_autoplay_timer()

        if duration_seconds <= 0:
            log.warning("Duração <= 0, timer não iniciado")
            return


        wait_time = duration_seconds + 2.0
        log.info(f"Timer de auto-play iniciado: {wait_time:.1f}s")

        self._autoplay_timer = threading.Timer(wait_time, self._timer_triggered)
        self._autoplay_timer.daemon = True
        self._autoplay_timer.start()

    def _cancel_autoplay_timer(self):
        """Cancela timer de auto-play se existir."""
        if self._autoplay_timer:
            self._autoplay_timer.cancel()
            self._autoplay_timer = None
            log.info("Timer de auto-play cancelado")

    def _timer_triggered(self):
        """Chamado quando o timer de auto-play dispara."""
        log.info("Timer de auto-play disparou!")
        if self.is_playing and not self._loading_new_track:
            self._on_track_end()
        else:
            log.info("Timer ignorado (não está tocando ou carregando nova faixa)")

    def _recalculate_timer_after_seek(self):
        """Recalcula timer após seek (usuário avançou no slider)."""
        if not self.is_playing or self._loading_new_track:
            return


        duration = self._track_duration_seconds
        position = self.position

        if duration <= 0:
            log.warning("Não foi possível recalcular timer - duração desconhecida")
            return


        if position <= 0:
            log.info("Seek detectado mas posição desconhecida, mantendo timer atual")
            return

        remaining = duration - position
        if remaining <= 0:

            log.info(f"Seek para perto do fim - disparando auto-play (pos={position:.1f}, dur={duration:.1f})")
            self._on_track_end()
        else:

            log.info(f"Recalculando timer após seek: pos={position:.1f}, dur={duration:.1f}, restante={remaining:.1f}s")
            self._start_autoplay_timer(remaining)

    def play(self, video_id, callback=None, next_callback=None, source='youtube'):
        """Inicia reprodução de um vídeo."""
        self.current_video_id = video_id
        self._source = source
        self.update_callback = callback
        self.next_track_callback = next_callback


        if not self._process or self._process.poll() is not None:
            self._start_mpv_process()
            time.sleep(0.5)


        self._load_request_id += 1
        current_load_id = self._load_request_id
        
        thread = threading.Thread(target=self._load_and_play, args=(video_id, source, current_load_id))
        thread.daemon = True
        thread.start()

    def _load_and_play(self, video_id, source, load_id):
        try:
            if load_id != self._load_request_id:
                log.info(f"Load {load_id} cancelado (atual: {self._load_request_id})")
                return
                
            from .youtubeSearch import YouTubeSearch
            searcher = YouTubeSearch()
            self.audio_url = searcher.get_audio_url(video_id, source)

            if load_id != self._load_request_id:
                log.info(f"Load {load_id} cancelado após get_audio_url")
                return

            if not self.audio_url:
                ui.message(_("Erro: Link de áudio indisponível"))
                log.error("URL de áudio não encontrada")
                self.is_playing = False
                return


            self._loading_new_track = True


            cmd = {"command": ["loadfile", self.audio_url]}
            self._send_ipc(cmd)


            time.sleep(0.3)
            self._send_ipc({"command": ["set_property", "pause", False]})


            time.sleep(0.2)
            self._loading_new_track = False


            self._update_audio_filters()

            self.is_playing = True
            self.is_paused = False


            self._send_ipc({"command": ["observe_property", 1, "time-pos"]})
            self._send_ipc({"command": ["observe_property", 2, "duration"]})
            self._send_ipc({"command": ["observe_property", 3, "eof-reached"]})

            if load_id != self._load_request_id:
                log.info(f"Load {load_id} cancelado antes do timer")
                return


            try:
                duration = searcher.get_duration_seconds(video_id, source)
                if duration > 0:
                    self._track_duration_seconds = duration
                    self._start_autoplay_timer(duration)
                else:
                    log.warning("Duração não obtida, timer não iniciado")
            except Exception as e:
                log.error(f"Erro ao obter/iniciar timer: {e}")


        except Exception as e:
            self._loading_new_track = False
            msg = _("Erro de conexão ao carregar música")
            ui.message(msg)
            log.error(f"{msg}: {e}")
            self.is_playing = False


    def get_related_video_id(self):
        """Busca ID de vídeo relacionado (Simulado ou Real)."""


        try:
            from .youtubeSearch import YouTubeSearch
            searcher = YouTubeSearch()
            if self._source == 'youtube_music':


                pass
        except:
            pass
        return None

    def _send_ipc(self, command):
        """Envia comando JSON para o pipe (conexão separada)."""
        if not self._process:
            return

        try:

            with open(self._ipc_path, 'wb') as f:
                cmd_bytes = json.dumps(command).encode('utf-8') + b'\n'
                f.write(cmd_bytes)
                f.flush()
        except Exception as e:
            pass


    def _kill_process(self):
        self._stop_update = True
        with self._lock:
            if self._process:
                try:
                    self._process.terminate()
                    self._process.wait(timeout=1)
                except:
                    try:
                        self._process.kill()
                    except:
                        pass
                self._process = None

    def _start_update_thread(self):

        self._stop_update = False
        self._update_thread = threading.Thread(target=self._update_loop)
        self._update_thread.daemon = True
        self._update_thread.start()

    def _update_loop(self):
        while not self._stop_update:
            if not self._process:
                break

            if self.update_callback and self.is_playing:
                try:

                    wx.CallAfter(self.update_callback, self.position, self.duration, self.is_playing)
                except:
                    pass

            time.sleep(0.5)


    def pause(self):
        cmd = {"command": ["set_property", "pause", True]}
        self._send_ipc(cmd)
        self.is_paused = True
        self.is_playing = False

    def resume(self):
        cmd = {"command": ["set_property", "pause", False]}
        self._send_ipc(cmd)
        self.is_paused = False
        self.is_playing = True

    def stop(self):
        """Para a reprodução e limpa callbacks para evitar auto-play fantasma."""
        self._load_request_id += 1
        self.next_track_callback = None
        self.update_callback = None

        self._cancel_autoplay_timer()

        cmd = {"command": ["stop"]}
        self._send_ipc(cmd)
        self.is_playing = False
        self.is_paused = False
        log.info(f"Player parado, load_request_id={self._load_request_id}")

    def seek(self, position):
        cmd = {"command": ["seek", position, "absolute"]}
        self._send_ipc(cmd)

    def seekRelative(self, delta):
        """Avança ou retrocede a reprodução."""
        cmd = {"command": ["seek", delta, "relative"]}
        self._send_ipc(cmd)


        duration = self._track_duration_seconds
        if duration > 0:
            self.position = max(0, min(duration, self.position + delta))
            log.info(f"Seek: delta={delta}s, nova posição estimada={self.position:.1f}s")


            remaining = duration - self.position
            if remaining <= 0:

                log.info("Seek passou do fim, disparando auto-play")
                self._on_track_end()
            elif remaining < self._track_duration_seconds:
                self._start_autoplay_timer(remaining)


    def setVolume(self, volume):
        self.volume = max(0, min(100, volume))
        cmd = {"command": ["set_property", "volume", self.volume]}
        self._send_ipc(cmd)

    def change_volume(self, delta):
        """Altera volume relativo (+/-)."""
        new_vol = self.volume + delta
        self.setVolume(new_vol)

    def setSpeed(self, speed):
        self.speed = max(0.5, min(2.0, speed))
        cmd = {"command": ["set_property", "speed", self.speed]}
        self._send_ipc(cmd)
        if self.pitch != 0:
             self._update_audio_filters()

    def setPitch(self, pitch):
        self.pitch = max(-12, min(12, pitch))
        self._update_audio_filters()

    def setSpeedAndPitch(self, speed, pitch):
        self.speed = speed
        self.pitch = pitch
        cmd_speed = {"command": ["set_property", "speed", self.speed]}
        self._send_ipc(cmd_speed)
        self._update_audio_filters()

    def _get_audio_filters(self):
        """Gera string de filtros de áudio para pitch e speed."""
        pitch_factor = 2 ** (self.pitch / 12.0)

        if self.pitch == 0:
            return ""

        if self.speed == 1.0:
            return f"asetrate=44100*{pitch_factor:.4f},aresample=44100,atempo={1/pitch_factor:.4f}"
        else:
            combined = pitch_factor * self.speed
            return f"asetrate=44100*{combined:.4f},aresample=44100"

    def _update_audio_filters(self):
        filters = self._get_audio_filters()
        if filters:
             cmd = {"command": ["af", "set", filters]}
        else:
             cmd = {"command": ["af", "set", ""]}
        self._send_ipc(cmd)


    def _refresh_audio_devices(self):
        """Carrega lista de dispositivos via mpv --audio-device=help."""
        try:
            cmd = [self._mpv_path, '--no-config', '--audio-device=help']

            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                startupinfo=startupinfo
            )

            if proc.returncode == 0:
                lines = proc.stdout.split('\n')
                devices = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('List of'):
                        continue


                    parts = line.split("'", 2)
                    if len(parts) >= 3:
                        dev_id = parts[1]

                        description = parts[2].strip()
                        if description.startswith('(') and description.endswith(')'):
                            description = description[1:-1]

                        devices.append((dev_id, description))

                self.audio_devices = devices
                log.info(f"Dispositivos de áudio carregados: {len(devices)}")
        except Exception as e:
            log.error(f"Erro ao listar dispositivos: {e}")
            self.audio_devices = [('auto', 'Auto')]

    def get_audio_devices(self):
        """Retorna lista de (id, nome)."""
        if not self.audio_devices:
            self._refresh_audio_devices()
        return self.audio_devices

    def set_audio_device(self, device_id):
        """Define o dispositivo de saída."""
        log.info(f"Definindo dispositivo de áudio: {device_id}")

        dev = device_id if device_id else 'auto'


        cmd = {"command": ["set_property", "audio-device", dev]}
        self._send_ipc(cmd)

    def cleanup(self):
        self._kill_process()
