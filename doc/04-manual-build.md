# Manual Build Guide

Build the add-on step-by-step without using the automated script.

## Step 1: Clone the Repository

```bash
git clone https://github.com/JoaoDEVWHADS/nvda-youtube-music-player.git
cd nvda-youtube-music-player
```

## Step 2: Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip scons gettext curl p7zip-full
pip install markdown
```

## Step 3: Create lib Directory

```bash
mkdir -p addon/globalPlugins/youtubeMusicPlayer/lib
```

## Step 4: Install Python Libraries

```bash
pip install --target=addon/globalPlugins/youtubeMusicPlayer/lib \
    ytmusicapi requests
```

## Step 5: Download yt-dlp

```bash
curl -L -o addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe \
    https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
```

## Step 6: Download mpv

```bash
# Get latest mpv release URL
MPV_URL=$(curl -s https://api.github.com/repos/shinchiro/mpv-winbuild-cmake/releases/latest \
    | grep "browser_download_url.*x86_64.*7z" \
    | head -1 \
    | cut -d '"' -f 4)

# Download and extract
curl -L -o /tmp/mpv.7z "$MPV_URL"
cd addon/globalPlugins/youtubeMusicPlayer/lib
7z e /tmp/mpv.7z mpv.exe -y
cd -
```

## Step 7: Verify Files

Check that these files exist:
```bash
ls -la addon/globalPlugins/youtubeMusicPlayer/lib/mpv.exe
ls -la addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe
ls -d addon/globalPlugins/youtubeMusicPlayer/lib/ytmusicapi
ls -d addon/globalPlugins/youtubeMusicPlayer/lib/requests
```

## Step 8: Build with SCons

```bash
scons
```

## Step 9: Find the Package

The built add-on will be in the project root:
```bash
ls -la *.nvda-addon
```

## Troubleshooting

### SCons not found
```bash
pip install scons
```

### msgfmt not found
```bash
sudo apt install gettext
```

### 7z not found
```bash
sudo apt install p7zip-full
```

### Build fails
Check that all files in Step 7 exist and are not empty.
