# Configuration

Build configuration options and settings.

## buildVars.py

The main configuration file for the add-on build.

```python
addon_info = {
    "addon_name": "youtubeMusicPlayer",
    "addon_summary": _("YouTube Music Player"),
    "addon_description": _("..."),
    "addon_version": "2026.01.17",
    "addon_author": "JoaoDEVWHADS",
    "addon_url": None,
    "addon_docFileName": "readme.html",
    "addon_minimumNVDAVersion": "2023.1.0",
    "addon_lastTestedNVDAVersion": "2025.1.0",
    "addon_updateChannel": None,
}
```

### Key Options

| Option | Description |
|--------|-------------|
| `addon_name` | Technical name (no spaces) |
| `addon_summary` | Display name |
| `addon_version` | Version string |
| `addon_minimumNVDAVersion` | Minimum NVDA version |
| `addon_lastTestedNVDAVersion` | Last tested version |

## manifest.ini

Generated automatically by SCons from buildVars.py.

```ini
name = youtubeMusicPlayer
summary = YouTube Music Player
version = 2026.01.17
author = JoaoDEVWHADS
minimumNVDAVersion = 2023.1.0
lastTestedNVDAVersion = 2025.1.0
```

## Update Checker Configuration

In `updateChecker.py`:

```python
GITHUB_API_URL = "https://api.github.com/repos/USER/REPO/releases/latest"
ADDON_NAME = "YouTube Music Player"
CURRENT_VERSION = "2026.01.17"
```

Update these when:
- Changing repository location
- Releasing a new version

## Settings Panel

User-configurable settings in NVDA preferences:
- Cookies file path (for authenticated access)

Stored in NVDA's config:
```
[youtubeMusicPlayer]
cookiesFilePath = ""
welcome_shown = True
```

### Troubleshooting Cookies
If authentication fails or causes errors, simply **clear the path** from the generic 'Cookies File' field in the settings panel to reset and disable authentication.
