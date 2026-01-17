# Testing

Testing your changes before release.

## Quick Test with Scratchpad

NVDA's Scratchpad allows testing without building:

1. Enable Developer Scratchpad:
   - NVDA → Preferences → Settings → Advanced
   - Enable "Developer Scratchpad"

2. Copy files:
   ```
   %APPDATA%\nvda\scratchpad\globalPlugins\
   ```

3. Restart NVDA

## Testing Checklist

### Basic Functionality
- [ ] Add-on loads without errors
- [ ] `NVDA+Alt+Y` opens search dialog
- [ ] Search returns results
- [ ] Playback starts correctly
- [ ] Volume controls work
- [ ] Speed/pitch controls work
- [ ] Seek controls work
- [ ] Player closes properly

### Edge Cases
- [ ] No internet connection
- [ ] Empty search query
- [ ] Very long search query
- [ ] Special characters in query
- [ ] Cancel during playback
- [ ] Multiple rapid commands

### Update Checker
- [ ] Checks on startup (5s delay)
- [ ] Handles 404 gracefully
- [ ] Shows dialog when update available
- [ ] Download works correctly

### Settings
- [ ] Settings panel appears
- [ ] Cookies path saves
- [ ] Settings persist after restart

## View NVDA Log

1. NVDA → Tools → View Log
2. Or press: `NVDA+F1` on focused object
3. Check for errors with "YouTube Music Player"

## Debug Mode

Enable debug logging:
1. NVDA → Preferences → Settings → General
2. Set "Logging level" to "Debug"
3. Restart NVDA

## Python Console

Interactive debugging:
1. Press `NVDA+Ctrl+Z`
2. Test commands:
```python
import globalPlugins.youtubeMusicPlayer
plugin = globalPlugins.youtubeMusicPlayer.GlobalPlugin
```

## Common Test Scenarios

### Scenario 1: First Run
1. Uninstall add-on
2. Clear config: delete `[youtubeMusicPlayer]` from nvda.ini
3. Install fresh
4. Welcome dialog should appear

### Scenario 2: Update Check
1. Set `CURRENT_VERSION = "0.0.1"` in updateChecker.py
2. Restart NVDA
3. Update dialog should appear (if release exists)
