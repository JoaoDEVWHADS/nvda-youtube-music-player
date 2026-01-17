# Prerequisites

System requirements for building the add-on.

## Operating System

| OS | Support |
|----|---------|
| Linux | ✅ Full support (recommended for building) |
| Windows WSL | ✅ Supported |
| Windows (native) | ⚠️ Partial (use WSL for building) |
| macOS | ⚠️ Untested |

## Required Software

### For Building

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Build scripts and SCons |
| SCons | Latest | Build system |
| gettext | Any | Translation compilation |
| curl | Any | Downloading dependencies |
| p7zip | Any | Extracting mpv |

### Installation (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-pip scons gettext curl p7zip-full
pip install markdown
```

### Installation (Arch Linux)

```bash
sudo pacman -S python python-pip scons gettext curl p7zip
pip install markdown
```

### Installation (Fedora)

```bash
sudo dnf install python3 python3-pip scons gettext curl p7zip
pip install markdown
```

## For Running the Add-on

| Software | Version |
|----------|---------|
| NVDA | 2023.1 or later |
| Windows | 10 or 11 |
| Internet | Required for streaming |

## Verify Installation

```bash
# Check Python
python3 --version

# Check SCons
scons --version

# Check gettext
msgfmt --version

# Check curl
curl --version
```

All commands should return version information without errors.
