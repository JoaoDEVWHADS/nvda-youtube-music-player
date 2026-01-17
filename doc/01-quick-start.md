# Quick Start Guide

Get the add-on running in 5 minutes.

## Option 1: Download Pre-built Package (Users)

1. Go to [Releases](https://github.com/JoaoDEVWHADS/nvda-youtube-music-player/releases)
2. Download the latest `.nvda-addon` file
3. Double-click to install
4. Restart NVDA
5. Press `NVDA+Alt+Y` to open

## Option 2: Automated Build (Developers)

```bash
# Clone repository
git clone https://github.com/JoaoDEVWHADS/nvda-youtube-music-player.git
cd nvda-youtube-music-player

# Run setup and build
bash install_dependencies.sh
```

The script will:
- ✅ Install system dependencies
- ✅ Download Python libraries
- ✅ Download yt-dlp.exe and mpv.exe
- ✅ Run integrity check
- ✅ Build the .nvda-addon package

## Option 3: Manual Build

See [Manual Build](04-manual-build.md) for step-by-step instructions without using the script.

## First Run

1. Install the generated `.nvda-addon` file
2. Restart NVDA
3. Press `NVDA+Alt+Y`
4. A welcome dialog will appear on first run
5. Start searching for music!

## Basic Controls

| Key | Action |
|-----|--------|
| `NVDA+Alt+Y` | Open player |
| `↑` / `↓` | Volume |
| `←` / `→` | Seek |
| `Space` | Play/Pause |
| `Escape` | Close |
