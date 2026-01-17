# Project Structure

Understanding the codebase organization.

## Directory Layout

```
nvda-youtube-music-player/
├── addon/                          # Add-on package
│   ├── globalPlugins/
│   │   └── youtubeMusicPlayer/
│   │       ├── __init__.py         # Main plugin entry point
│   │       ├── playerManager.py    # MPV audio control
│   │       ├── playerDialog.py     # Player GUI
│   │       ├── searchDialog.py     # Search GUI
│   │       ├── resultsDialog.py    # Search results
│   │       ├── youtubeSearch.py    # YouTube API
│   │       ├── updateChecker.py    # Auto-update
│   │       ├── settingsPanel.py    # NVDA settings
│   │       └── lib/                # Bundled dependencies
│   │           ├── mpv.exe
│   │           ├── yt-dlp.exe
│   │           ├── ytmusicapi/
│   │           └── requests/
│   ├── doc/                        # User documentation
│   │   ├── en/readme.md
│   │   ├── pt_BR/readme.md
│   │   └── .../
│   ├── locale/                     # Translations
│   │   ├── en/LC_MESSAGES/nvda.po
│   │   ├── pt_BR/LC_MESSAGES/nvda.po
│   │   └── .../
│   └── manifest.ini                # Add-on metadata
├── doc/                            # Developer documentation
│   ├── readme.md
│   ├── 01-quick-start.md
│   └── .../
├── buildVars.py                    # Build configuration
├── sconstruct                      # SCons build script
├── install_dependencies.sh         # Setup script
└── readme.md                       # GitHub README
```

## Key Files

### `__init__.py`
Main entry point. Defines `GlobalPlugin` class with:
- Initialization and cleanup
- Keyboard shortcut handler
- Welcome dialog
- Update checker integration

### `playerManager.py`
Controls MPV audio playback:
- Start/stop playback
- Volume, speed, pitch control
- Position seeking
- Audio device management

### `youtubeSearch.py`
Handles YouTube API:
- YouTube Music search (ytmusicapi)
- YouTube search (yt-dlp)
- Audio URL extraction

### `playerDialog.py`
Accessible player interface:
- Playback controls
- Progress display
- Keyboard navigation

### `updateChecker.py`
Automatic updates:
- GitHub release checking
- Download and install
- Version comparison
