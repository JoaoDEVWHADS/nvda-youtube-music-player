# Troubleshooting

Common issues and solutions.

## Build Issues

### "scons: command not found"
```bash
pip install scons
# Or add to PATH if already installed
```

### "msgfmt: command not found"
```bash
sudo apt install gettext
```

### "7z: command not found"
```bash
sudo apt install p7zip-full
```

### Build fails with missing files
Run integrity check:
```bash
ls -la addon/globalPlugins/youtubeMusicPlayer/lib/mpv.exe
ls -la addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe
```
Re-download if missing.

## Runtime Issues

### Add-on doesn't load
Check NVDA log for errors:
- NVDA → Tools → View Log
- Search for "YouTube Music Player"

### "ImportError: No module named 'ytmusicapi'"
Libraries not installed correctly:
```bash
pip install --target=addon/globalPlugins/youtubeMusicPlayer/lib \
    ytmusicapi requests --force-reinstall
```

### Shortcut doesn't work
1. Check if add-on is enabled
2. Check Input Gestures for conflicts
3. Restart NVDA

### Search returns no results
- Check internet connection
- Try YouTube search instead of YouTube Music
- Check NVDA log for API errors

### Playback doesn't start
- Check if mpv.exe exists and is not corrupted
- Check NVDA log for MPV errors
- Try re-downloading mpv

### Update checker shows 404
- Repository doesn't exist yet
- No releases published
- Check GitHub URL in updateChecker.py

## NVDA Compatibility

### "Add-on not compatible"
Check `addon_minimumNVDAVersion` in buildVars.py matches your NVDA version.

### API deprecated warnings
Update code for newer NVDA API:
- `controlTypes.ROLE_X` → `controlTypes.Role.X`
- `controlTypes.STATE_X` → `controlTypes.State.X`

## Performance Issues

### Slow startup
Update checker runs 5 seconds after startup. This is normal.

### High memory usage
MPV process runs separate from NVDA. Close player when not in use.

## Getting Help

1. Check NVDA log first
2. Search existing issues on GitHub
3. Open new issue with:
   - NVDA version
   - Windows version
   - Add-on version
   - Error message/log
   - Steps to reproduce
