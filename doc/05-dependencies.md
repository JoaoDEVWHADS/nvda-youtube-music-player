# Dependencies

Managing external libraries and executables.

## Python Libraries

### ytmusicapi
- **Purpose**: YouTube Music search API
- **Source**: https://github.com/sigma67/ytmusicapi
- **License**: MIT

### requests
- **Purpose**: HTTP library
- **Source**: https://github.com/psf/requests
- **License**: Apache 2.0

### Installation
```bash
pip install --target=addon/globalPlugins/youtubeMusicPlayer/lib \
    ytmusicapi requests
```

## Executables

### yt-dlp.exe
- **Purpose**: YouTube video/audio extraction
- **Source**: https://github.com/yt-dlp/yt-dlp
- **License**: Unlicense

Download:
```bash
curl -L -o addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe \
    https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
```

### mpv.exe
- **Purpose**: Audio playback engine
- **Source**: https://github.com/shinchiro/mpv-winbuild-cmake
- **License**: GPL v2

Download:
```bash
# See 04-manual-build.md for full instructions
```

## Updating Dependencies

### Update yt-dlp
```bash
rm addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe
curl -L -o addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe \
    https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
```

### Update Python Libraries
```bash
rm -rf addon/globalPlugins/youtubeMusicPlayer/lib/ytmusicapi
rm -rf addon/globalPlugins/youtubeMusicPlayer/lib/requests
pip install --target=addon/globalPlugins/youtubeMusicPlayer/lib \
    ytmusicapi requests --upgrade
```

## Dependency Tree

```
ytmusicapi
├── requests
│   ├── charset_normalizer
│   ├── idna
│   ├── urllib3
│   └── certifi
└── (no other dependencies)
```

All sub-dependencies are automatically installed by pip.
