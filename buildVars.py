

from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries
from site_scons.site_tools.NVDATool.utils import _


addon_info = AddonInfo(
	addon_name="youtubeMusicPlayer",
	addon_summary=_("YouTube Music Player"),
	addon_description=_("""Pesquise e reproduza músicas do YouTube e YouTube Music diretamente no NVDA.
Interface acessível com controles de volume, velocidade e tonalidade."""),
	addon_version="2026.01.17",
	addon_changelog=_("""Versão 2026.01.17:
- Nova funcionalidade de busca no YouTube e YouTube Music
- Player acessível completo com controles de reprodução
- Suporte a playlists e reprodução contínua (Auto-Play)
- Controles avançados de velocidade e tonalidade
- Radio Mix para descoberta de novas músicas"""),
	addon_author="JoaoDEVWHADS",
	addon_url="https://github.com/JoaoDEVWHADS/nvda-youtube-music-player",
	addon_sourceURL="https://github.com/JoaoDEVWHADS/nvda-youtube-music-player",
	addon_docFileName="readme.html",
	addon_minimumNVDAVersion="2024.1",
	addon_lastTestedNVDAVersion="2025.1",
	addon_updateChannel=None,
	addon_license="GPL v2",
	addon_licenseURL=None,
)

pythonSources: list[str] = ["addon/globalPlugins/**/*.py"]
i18nSources: list[str] = pythonSources + ["buildVars.py"]
excludedFiles: list[str] = []
baseLanguage: str = "pt_BR"
markdownExtensions: list[str] = []
brailleTables: BrailleTables = {}
symbolDictionaries: SymbolDictionaries = {}
