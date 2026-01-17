# Package Distribution Guide

## Building Distribution Packages

COIN:OPERATED can be packaged in multiple formats for easy distribution.

---

## 🐧 Debian Package (.deb)

### Build

```bash
bash build_deb.sh
```

### Install

```bash
sudo dpkg -i coin-operated-jrpg_1.0.0_all.deb
sudo apt-get install -f  # Fix dependencies if needed
```

Or double-click the .deb file in your file manager.

### Uninstall

```bash
sudo apt remove coin-operated-jrpg
```

### What's Included

- Game files in `/opt/coin-operated/`
- Launcher script in `/usr/bin/coin-operated`
- Desktop entry in `/usr/share/applications/`
- Icon in `/usr/share/pixmaps/`
- Automatic dependency installation

---

## 📦 RPM Package (.rpm)

### Build

```bash
bash build_package.sh
# Select option 2
```

### Install

```bash
sudo rpm -i coin-operated-jrpg-1.0.0-1.noarch.rpm
```

Or use your package manager (dnf, yum, zypper).

### Uninstall

```bash
sudo rpm -e coin-operated-jrpg
```

---

## 📚 Universal Tarball (.tar.gz)

### Build

```bash
bash build_package.sh
# Select option 3
```

### Install

```bash
tar xzf coin-operated-jrpg-1.0.0.tar.gz
cd coin-operated-jrpg-1.0.0
bash setup.sh
```

### What's Included

- Complete game source
- Automated installer
- README and documentation
- No system integration (portable)

---

## 💾 Windows ZIP (.zip)

### Build

```bash
bash build_package.sh
# Select option 4
```

### Install

1. Extract the ZIP file
2. Double-click `setup.bat`
3. Follow prompts

### What's Included

- Complete game files
- Windows batch installer
- Desktop shortcut creation
- All documentation

---

## 🚀 AppImage (Universal Linux)

### Build

```bash
bash build_package.sh
# Select option 5
```

Requires `appimagetool` (download from https://appimage.github.io/)

### Install

```bash
chmod +x coin-operated-jrpg-1.0.0-x86_64.AppImage
./coin-operated-jrpg-1.0.0-x86_64.AppImage
```

No installation needed - runs directly!

---

## 🎯 All Formats at Once

```bash
bash build_package.sh
# Select option 6
```

Builds all available formats automatically.

---

## 📊 Package Comparison

| Format | Best For | Size | Installation |
|--------|----------|------|--------------|
| .deb | Ubuntu/Debian | ~5MB | System package |
| .rpm | Fedora/RHEL/SUSE | ~5MB | System package |
| .tar.gz | Any Linux | ~4MB | Manual/portable |
| .zip | Windows | ~4MB | Manual/portable |
| .AppImage | Any Linux | ~8MB | No install needed |

---

## 📋 Package Contents

All packages include:

- ✅ Complete game engine
- ✅ All Python source code
- ✅ Graphics system
- ✅ Character & combat systems
- ✅ Content (Acts I-IV)
- ✅ Documentation
- ✅ Launcher scripts
- ✅ Desktop integration files

---

## 🔧 Build Requirements

### For .deb:
- `dpkg-deb` (usually pre-installed on Debian/Ubuntu)

### For .rpm:
- `rpmbuild` package
- Ubuntu: `sudo apt install rpm`
- Fedora: `sudo dnf install rpm-build`

### For .tar.gz and .zip:
- `tar` and `zip` (usually pre-installed)

### For .AppImage:
- `appimagetool` from https://appimage.github.io/

---

## 🎨 Customization

### Change Version

Edit the `VERSION` variable in build scripts:
```bash
VERSION="1.0.0"  # Change this
```

### Change Package Name

Edit the `PACKAGE_NAME` variable:
```bash
PACKAGE_NAME="coin-operated-jrpg"  # Change this
```

### Add Files

Modify the copy commands in the build script to include additional files.

---

## 📤 Distribution

### Upload Locations

**GitHub Releases:**
```bash
# After building
gh release create v1.0.0 \
  coin-operated-jrpg_1.0.0_all.deb \
  coin-operated-jrpg-1.0.0.tar.gz \
  coin-operated-jrpg-1.0.0.zip
```

**itch.io:**
- Upload .zip for Windows
- Upload .tar.gz for Linux
- Upload .deb as bonus download

**Steam:**
- Use the Steam SDK build pipeline
- Reference: `build_steam.sh`

---

## 📝 User Instructions by Package

### .deb (Ubuntu/Debian)
```
Download coin-operated-jrpg_1.0.0_all.deb
Double-click to install, or:
  sudo dpkg -i coin-operated-jrpg_1.0.0_all.deb
Launch from applications menu
```

### .rpm (Fedora/RHEL)
```
Download coin-operated-jrpg-1.0.0-1.noarch.rpm
Double-click to install, or:
  sudo rpm -i coin-operated-jrpg-1.0.0-1.noarch.rpm
Launch from applications menu
```

### .tar.gz (Any Linux)
```
Download coin-operated-jrpg-1.0.0.tar.gz
Extract: tar xzf coin-operated-jrpg-1.0.0.tar.gz
Install: cd coin-operated-jrpg-1.0.0 && bash setup.sh
```

### .zip (Windows)
```
Download coin-operated-jrpg-1.0.0.zip
Extract the ZIP file
Run setup.bat
```

### .AppImage (Any Linux)
```
Download coin-operated-jrpg-1.0.0-x86_64.AppImage
Make executable: chmod +x coin-operated-jrpg-1.0.0-x86_64.AppImage
Run: ./coin-operated-jrpg-1.0.0-x86_64.AppImage
```

---

## 🚀 Quick Build Cheat Sheet

```bash
# Just .deb (most common)
bash build_deb.sh

# Interactive menu for any format
bash build_package.sh

# All formats at once
bash build_package.sh
# (choose option 6)
```

---

## 🔍 Verify Package

### Test .deb before distribution:

```bash
# Install in test environment
sudo dpkg -i coin-operated-jrpg_1.0.0_all.deb

# Verify launcher
which coin-operated

# Test desktop entry
ls /usr/share/applications/coin-operated.desktop

# Test game launch
coin-operated

# Uninstall when done
sudo apt remove coin-operated-jrpg
```

---

## 📊 Expected Sizes

- .deb: ~5-6 MB
- .rpm: ~5-6 MB  
- .tar.gz: ~3-4 MB (compressed)
- .zip: ~3-4 MB (compressed)
- .AppImage: ~7-9 MB (includes runtime)

---

## 🎯 Recommended Distribution

For maximum reach, provide:

1. **.deb** - Ubuntu/Debian users (majority)
2. **.tar.gz** - Universal Linux (advanced users)
3. **.zip** - Windows users
4. **.AppImage** - Linux users who want portability

This covers ~95% of potential users.

---

**From coin to goddess, from tool to deity** 🪙✨
