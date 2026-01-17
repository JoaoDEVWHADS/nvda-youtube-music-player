

"""
Módulo de busca no YouTube e YouTube Music.
- YouTube: usa yt-dlp
- YouTube Music: usa ytmusicapi
"""

import json
import subprocess
import os
from logHandler import log

import addonHandler
addonHandler.initTranslation()


class YouTubeSearch:
    """Classe para buscar vídeos no YouTube e músicas no YouTube Music."""

    def __init__(self):
        self.results_per_page = 10
        self._ytmusic = None
        self._cookies_path = None
        self._load_cookie_paths()
        self._init_ytmusic()

    def _load_cookie_paths(self):
        """Carrega o caminho do arquivo de cookies das configurações do NVDA."""
        try:
            from .settingsPanel import YouTubeMusicPlayerSettings
            settings = YouTubeMusicPlayerSettings.get()

            cookies_path = settings.cookiesFilePath
            if cookies_path and os.path.isfile(cookies_path):
                self._cookies_path = cookies_path
                log.info(f"Cookies carregado: {cookies_path}")
        except Exception as e:
            log.warning(f"Não foi possível carregar configurações de cookies: {e}")

    def _init_ytmusic(self):
        """Inicializa o cliente ytmusicapi."""
        try:
            from ytmusicapi import YTMusic


            if self._cookies_path:
                try:

                    self._ytmusic = YTMusic(self._cookies_path)
                    log.info("ytmusicapi inicializado com cookies")
                except Exception:

                    self._ytmusic = YTMusic()
                    log.info("ytmusicapi inicializado sem autenticação (cookies incompatível)")
            else:
                self._ytmusic = YTMusic()
                log.info("ytmusicapi inicializado com sucesso")
        except ImportError:
            log.warning("ytmusicapi não disponível")
            self._ytmusic = None
        except Exception as e:
            log.error(f"Erro ao inicializar ytmusicapi: {e}")
            self._ytmusic = None

    def _get_ytdlp_path(self):
        """Retorna o caminho do yt-dlp."""
        addon_path = os.path.dirname(os.path.abspath(__file__))
        ytdlp_local = os.path.join(addon_path, 'lib', 'yt-dlp.exe')

        if os.path.exists(ytdlp_local):
            return ytdlp_local

        return 'yt-dlp'

    def _get_ytdlp_base_cmd(self):
        """Retorna a base do comando yt-dlp com cookies se configurados."""
        cmd = [self._get_ytdlp_path()]


        if self._cookies_path:
            cmd.extend(['--cookies', self._cookies_path])

            cmd.extend(['--extractor-args', 'youtube:player_client=web'])

        return cmd


    def search_youtube(self, query, page=1):
        """
        Busca vídeos no YouTube usando yt-dlp.

        Args:
            query: Termo de busca
            page: Número da página (1-indexed)

        Returns:
            Lista de dicionários com resultados
        """
        try:

            search_count = self.results_per_page * page

            cmd = self._get_ytdlp_base_cmd() + [
                '--flat-playlist',
                '--dump-json',
                '--no-warnings',
                '--quiet',
                f'ytsearch{search_count}:{query}'
            ]

            log.debug(f"Executando yt-dlp: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode != 0:
                log.error(f"yt-dlp error: {result.stderr}")
                return self._get_youtube_mock_results()

            results = []
            lines = result.stdout.strip().split('\n')


            start_idx = (page - 1) * self.results_per_page
            end_idx = page * self.results_per_page
            page_lines = lines[start_idx:end_idx]

            for line in page_lines:
                if line:
                    try:
                        data = json.loads(line)

                        log.info(f"YT-DLP raw: channel={data.get('channel')}, uploader={data.get('uploader')}, title={data.get('title')}")
                        results.append({
                            'id': data.get('id', ''),
                            'title': data.get('title', _('Sem título')),
                            'duration': self._format_duration(data.get('duration')),
                            'channel': data.get('channel', data.get('uploader', '')),
                            'url': f"https://www.youtube.com/watch?v={data.get('id', '')}",
                            'source': 'youtube'
                        })
                    except json.JSONDecodeError:
                        continue

            return results if results else self._get_youtube_mock_results()

        except FileNotFoundError:
            log.warning("yt-dlp não encontrado")
            return self._get_youtube_mock_results()
        except subprocess.TimeoutExpired:
            log.error("Timeout na busca YouTube")
            return self._get_youtube_mock_results()
        except Exception as e:
            log.error(f"Erro na busca YouTube: {e}")
            return self._get_youtube_mock_results()


    def search_youtube_music(self, query, page=1):
        """
        Busca músicas no YouTube Music usando ytmusicapi.

        Args:
            query: Termo de busca
            page: Número da página (1-indexed)

        Returns:
            Lista de dicionários com resultados
        """
        if not self._ytmusic:
            log.warning("ytmusicapi não disponível, usando fallback yt-dlp")
            return self._search_ytmusic_fallback(query, page)

        try:

            search_results = self._ytmusic.search(query, filter='songs', limit=self.results_per_page * page)


            start_idx = (page - 1) * self.results_per_page
            end_idx = page * self.results_per_page
            page_results = search_results[start_idx:end_idx]

            results = []
            for item in page_results:

                video_id = item.get('videoId', '')
                title = item.get('title', _('Sem título'))


                duration = ''
                if 'duration' in item:
                    duration = item['duration']
                elif 'duration_seconds' in item:
                    duration = self._format_duration(item['duration_seconds'])


                artists = item.get('artists', [])
                if artists:
                    channel = ', '.join([a.get('name', '') for a in artists if a.get('name')])
                else:
                    channel = ''

                results.append({
                    'id': video_id,
                    'title': title,
                    'duration': duration,
                    'channel': channel,
                    'url': f"https://music.youtube.com/watch?v={video_id}",
                    'source': 'youtube_music'
                })

            return results if results else self._get_ytmusic_mock_results()

        except Exception as e:
            log.error(f"Erro na busca YouTube Music: {e}")
            return self._search_ytmusic_fallback(query, page)

    def _search_ytmusic_fallback(self, query, page=1):
        """Fallback para busca no YouTube Music usando yt-dlp."""
        try:
            search_count = self.results_per_page * page

            cmd = self._get_ytdlp_base_cmd() + [
                '--flat-playlist',
                '--dump-json',
                '--no-warnings',
                '--quiet',
                f'https://music.youtube.com/search?q={query}'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode != 0:
                return self._get_ytmusic_mock_results()

            results = []
            lines = result.stdout.strip().split('\n')
            start_idx = (page - 1) * self.results_per_page
            end_idx = page * self.results_per_page

            for line in lines[start_idx:end_idx]:
                if line:
                    try:
                        data = json.loads(line)
                        results.append({
                            'id': data.get('id', ''),
                            'title': data.get('title', _('Sem título')),
                            'duration': self._format_duration(data.get('duration')),
                            'channel': data.get('channel', data.get('uploader', '')),
                            'url': f"https://music.youtube.com/watch?v={data.get('id', '')}",
                            'source': 'youtube_music'
                        })
                    except json.JSONDecodeError:
                        continue

            return results if results else self._get_ytmusic_mock_results()

        except Exception as e:
            log.error(f"Erro no fallback YTMusic: {e}")
            return self._get_ytmusic_mock_results()


    def _format_duration(self, seconds):
        """Formata duração em segundos para mm:ss."""
        if not seconds:
            return ""

        try:
            seconds = int(seconds)
            minutes = seconds // 60
            secs = seconds % 60

            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60
                return f"{hours}:{minutes:02d}:{secs:02d}"

            return f"{minutes}:{secs:02d}"
        except (ValueError, TypeError):
            return str(seconds) if seconds else ""

    def get_audio_url(self, video_id, source='youtube'):
        """
        Obtém a URL de áudio de um vídeo.

        Args:
            video_id: ID do vídeo
            source: 'youtube' ou 'youtube_music'

        Returns:
            URL do stream de áudio ou None
        """
        try:
            if source == 'youtube_music':
                url = f'https://music.youtube.com/watch?v={video_id}'
            else:
                url = f'https://www.youtube.com/watch?v={video_id}'

            cmd = self._get_ytdlp_base_cmd() + [
                '-f', 'bestaudio/best',
                '-g',
                '--no-warnings',
                '--quiet',
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode == 0 and result.stdout.strip():
                audio_url = result.stdout.strip()
                log.info(f"Audio URL obtida ({source}): {audio_url[:80]}...")
                return audio_url

            log.error(f"Erro ao obter URL de áudio: {result.stderr}")
            return None

        except Exception as e:
            log.error(f"Erro ao obter URL de áudio: {e}")
            return None

    def get_duration_seconds(self, video_id, source='youtube'):
        """
        Obtém a duração de um vídeo em segundos.

        Args:
            video_id: ID do vídeo
            source: 'youtube' ou 'youtube_music'

        Returns:
            Duração em segundos (int) ou 0 se falhar
        """
        try:
            if source == 'youtube_music':
                url = f'https://music.youtube.com/watch?v={video_id}'
            else:
                url = f'https://www.youtube.com/watch?v={video_id}'

            cmd = self._get_ytdlp_base_cmd() + [
                '-j',
                '--no-warnings',
                '--quiet',
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout.strip())
                duration = int(data.get('duration', 0))
                log.info(f"Duração obtida: {duration}s")
                return duration

            return 0

        except Exception as e:
            log.error(f"Erro ao obter duração: {e}")
            return 0


    def get_recommendation(self, video_id, source="youtube_music", current_title=None, exclude_ids=None, current_channel=None):
        """
        Obtém recomendação (próxima faixa).
        :param video_id: ID do vídeo atual
        :param source: 'youtube_music' ou 'youtube'
        :param current_title: Título atual para busca fallback (YouTube)
        :param exclude_ids: Lista de IDs para excluir (histórico recente)
        :param current_channel: Canal atual para busca mais variada
        """
        log.info(f"get_recommendation: ID={video_id}, Source={source}")

        if exclude_ids is None:
            exclude_ids = []


        if video_id and video_id not in exclude_ids:
            exclude_ids.append(video_id)


        if source == 'youtube_music' and self._ytmusic:
            try:

                watch_playlist = self._ytmusic.get_watch_playlist(videoId=video_id, limit=5)
                tracks = watch_playlist.get('tracks', [])

                track = None
                for t in tracks:

                    if t.get('videoId') in exclude_ids:
                        continue

                    track = t
                    break

                if track:

                    log.info(f"Raw track data: {track}")

                    item = {
                        'id': track.get('videoId'),
                        'title': track.get('title', _("Próxima Música")),
                        'channel': ', '.join([a.get('name', '') for a in track.get('artists', []) if a.get('name')]),
                        'source': 'youtube_music'
                    }
                    if not item['channel']:
                         item['channel'] = track.get('byline', '')

                    log.info(f"Recomendação (YTM): {item['title']} - {item['channel']}")
                    return item
            except Exception as e:
                log.error(f"Erro ao buscar related (ytmusic): {e}")


        if source == 'youtube':
            try:
                log.info("Tentando recomendação via YouTube Radio Mix...")


                radio_url = f"https://www.youtube.com/watch?v={video_id}&list=RD{video_id}"

                cmd = self._get_ytdlp_base_cmd() + [
                    '--flat-playlist',
                    '--dump-json',
                    '--no-warnings',
                    '--quiet',
                    '--playlist-items', '1-15',
                    radio_url
                ]

                log.info(f"Extraindo Radio Mix: RD{video_id}")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )

                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')

                    for line in lines:
                        try:
                            data = json.loads(line)
                            item_id = data.get('id', '')


                            if item_id in exclude_ids:
                                continue


                            item = {
                                'id': item_id,
                                'title': data.get('title', _("Próxima Música")),
                                'channel': data.get('channel', data.get('uploader', '')),
                                'source': 'youtube'
                            }
                            log.info(f"Recomendação (YouTube Radio): {item['title']} - {item['channel']}")
                            return item

                        except json.JSONDecodeError:
                            continue
                else:
                    log.warning(f"Radio Mix falhou, tentando busca fallback...")

            except Exception as e:
                log.error(f"Erro ao extrair Radio Mix: {e}")


            try:
                log.info("Fallback: Buscando via query...")
                query = f"{current_channel} mix" if current_channel else f"Mix {current_title}"
                results = self.search_youtube(query)

                from difflib import SequenceMatcher
                for res in results:
                    if res.get('id') in exclude_ids:
                        continue

                    if current_title:
                        ratio = SequenceMatcher(None, current_title.lower(), res['title'].lower()).ratio()
                        if ratio > 0.6:
                            continue

                    log.info(f"Recomendação (fallback): {res['title']}")
                    return res

            except Exception as e:
                log.error(f"Erro ao buscar related (youtube): {e}")

        return None


    def _get_youtube_mock_results(self):
        """Resultados mock para YouTube."""
        return [
            {
                'id': 'dQw4w9WgXcQ',
                'title': 'Rick Astley - Never Gonna Give You Up',
                'duration': '3:33',
                'channel': 'Rick Astley',
                'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'source': 'youtube'
            },
            {
                'id': 'kJQP7kiw5Fk',
                'title': 'Luis Fonsi - Despacito ft. Daddy Yankee',
                'duration': '4:42',
                'channel': 'Luis Fonsi',
                'url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
                'source': 'youtube'
            },
            {
                'id': '9bZkp7q19f0',
                'title': 'PSY - GANGNAM STYLE',
                'duration': '4:13',
                'channel': 'officialpsy',
                'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0',
                'source': 'youtube'
            },
        ]

    def _get_ytmusic_mock_results(self):
        """Resultados mock para YouTube Music."""
        return [
            {
                'id': 'JGwWNGJdvx8',
                'title': 'Shape of You',
                'duration': '4:24',
                'channel': 'Ed Sheeran',
                'url': 'https://music.youtube.com/watch?v=JGwWNGJdvx8',
                'source': 'youtube_music'
            },
            {
                'id': 'RgKAFK5djSk',
                'title': 'See You Again',
                'duration': '3:58',
                'channel': 'Wiz Khalifa ft. Charlie Puth',
                'url': 'https://music.youtube.com/watch?v=RgKAFK5djSk',
                'source': 'youtube_music'
            },
            {
                'id': 'fRh_vgS2dFE',
                'title': 'Sorry',
                'duration': '3:26',
                'channel': 'Justin Bieber',
                'url': 'https://music.youtube.com/watch?v=fRh_vgS2dFE',
                'source': 'youtube_music'
            },
        ]
