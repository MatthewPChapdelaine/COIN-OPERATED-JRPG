# COIN:OPERATED JRPG - Automated Installation Guide

## Zero-Technical-Knowledge Installation

We've made installation as simple as possible. Choose your platform:

---

## 🐧 Linux (Easiest)

### One-Command Installation

Open a terminal in the game folder and run:

```bash
bash setup.sh
```

**That's it!** The script will:
- ✓ Check Python and pip
- ✓ Install all dependencies automatically
- ✓ Create application menu shortcut
- ✓ Optionally create desktop icon
- ✓ Offer to launch the game

**No technical knowledge required!**

---

## 🪟 Windows

### One-Click Installation

1. Double-click **`setup.bat`**
2. Follow the prompts
3. Done!

The script will:
- ✓ Check Python installation
- ✓ Install all dependencies
- ✓ Create desktop shortcut
- ✓ Create quick launch script
- ✓ Offer to launch the game

**No typing required!**

---

## 🍎 macOS

### Simple Terminal Command

Open Terminal in the game folder and run:

```bash
python3 auto_setup.py
```

The script will:
- ✓ Check everything
- ✓ Install dependencies
- ✓ Create launch script
- ✓ Set up shortcuts
- ✓ Offer to launch the game

---

## 🌐 Cross-Platform Python Installer

If the above don't work, use the universal installer:

```bash
python3 auto_setup.py
```

This works on **any** platform with Python 3.8+

---

## ⚡ Super Quick Start (If You're Impatient)

### Linux/macOS:
```bash
bash setup.sh
```
Press Enter twice, then type `y` to launch!

### Windows:
Double-click `setup.bat`, press Enter twice, then type `y`!

---

## 🎮 After Installation

Launch the game any of these ways:

### Linux:
- **Applications menu**: Search for "COIN:OPERATED"
- **Desktop icon**: Double-click (if created)
- **Terminal**: `./play.sh` or `python3 coin_operated.py`

### Windows:
- **Desktop shortcut**: Double-click (if created)
- **File**: Double-click `play.bat`
- **Command**: `python coin_operated.py`

### macOS:
- **Terminal**: `./play.sh` or `python3 coin_operated.py`

---

## 🆘 Troubleshooting

### "Python not found"

**Linux:**
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora
sudo pacman -S python python-pip      # Arch
```

**Windows:**
Download from: https://www.python.org/downloads/
✅ Make sure to check "Add Python to PATH" during installation!

**macOS:**
```bash
brew install python3  # If you have Homebrew
```
Or download from: https://www.python.org/downloads/

### "Permission denied"

**Linux/macOS:**
```bash
chmod +x setup.sh
bash setup.sh
```

### "Dependencies failed to install"

Try manual installation:
```bash
pip3 install pygame Pillow
```

Or:
```bash
pip3 install -r requirements.txt
```

---

## 📋 What Each Installer Does

All installers do the same thing automatically:

1. ✓ **Check Python** (version 3.8+)
2. ✓ **Check/Install pip** (Python package manager)
3. ✓ **Install pygame** (graphics library)
4. ✓ **Install Pillow** (image library)
5. ✓ **Create shortcuts** (desktop & menu)
6. ✓ **Make launcher executable**
7. ✓ **Offer to launch game**

**Total time: 1-2 minutes** (depending on internet speed)

---

## 🎯 For Non-Technical Users

### You Don't Need To Know:
- ❌ How to use terminal/command prompt
- ❌ What pip or Python modules are
- ❌ How to edit configuration files
- ❌ What dependencies are
- ❌ How desktop integration works

### You Just Need To:
- ✅ Run **ONE** command or script
- ✅ Press Enter when asked
- ✅ Type 'y' if you want shortcuts
- ✅ Play the game!

---

## 🪙 What You'll Get

After installation, you'll have:

- 🎮 **Application Menu Shortcut** - Find it in your apps
- 🖥️ **Desktop Icon** - Quick access (optional)
- 📜 **Launch Scripts** - `play.sh` or `play.bat`
- ✨ **Beautiful Splash Screen** - Golden Coin logo
- 🎨 **16-bit JRPG Graphics** - Retro authentic style
- 🪙 **Play as Coin** - Golden mystical protagonist

---

## 💡 Pro Tips

- **First launch takes ~2 seconds** (loading modules)
- **No internet needed after installation** (all offline)
- **No terminal window** (pure GUI game)
- **Save files auto-created** in game folder
- **Press ESC to quit** anytime (auto-saves)

---

## 🎪 Installation Comparison

| Method | Difficulty | Time | Works On |
|--------|-----------|------|----------|
| `setup.sh` | ⭐ Easiest | 1-2 min | Linux |
| `setup.bat` | ⭐ Easiest | 1-2 min | Windows |
| `auto_setup.py` | ⭐⭐ Easy | 1-2 min | All platforms |
| Manual | ⭐⭐⭐ Medium | 3-5 min | All platforms |

---

## ✨ Success Indicators

You'll know installation succeeded when you see:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              ✨ Installation Complete! ✨                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

Then you're ready to play!

---

## 🚀 Quick Command Reference

```bash
# Install (choose one):
bash setup.sh              # Linux (recommended)
setup.bat                  # Windows (double-click)
python3 auto_setup.py      # Any platform

# Launch (after install):
./play.sh                  # Linux/macOS
play.bat                   # Windows
python3 coin_operated.py   # Any platform
```

---

**From coin to goddess, from tool to deity** 🪙✨  
*A Universe Beyond the Universe*
