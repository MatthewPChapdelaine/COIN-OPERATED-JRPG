# Deployment Guide for Linux and Steam

This guide explains how to test and deploy the Coin-Operated JRPG on Linux and Steam.

## Table of Contents
- [System Requirements](#system-requirements)
- [Linux Setup](#linux-setup)
- [Testing on Linux](#testing-on-linux)
- [Steam Preparation](#steam-preparation)
- [Steam Deployment](#steam-deployment)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 18.04+, Fedora 30+, or equivalent)
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Storage**: 100 MB free space
- **Dependencies**: Pillow (PIL) 9.0.0 or higher

### Recommended Requirements
- **OS**: Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 1 GB
- **Storage**: 500 MB free space

## Linux Setup

### 1. First-Time Setup

Run the automated setup script to install all dependencies:

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

This script will:
- Verify Python 3.8+ is installed
- Check for pip3
- Install Pillow (PIL) for graphics generation
- Make all shell scripts executable

### 2. Manual Setup (Alternative)

If you prefer manual installation:

```bash
# Check Python version (must be 3.8+)
python3 --version

# Install dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x setup_linux.sh verify.sh build_steam.sh
```

## Testing on Linux

### 1. Verify Installation

Run the verification script to check all systems:

```bash
chmod +x verify.sh
./verify.sh
```

This comprehensive test will:
- ✓ Check Python version (>= 3.8)
- ✓ Verify Pillow installation
- ✓ Check all game files are present
- ✓ Verify SNES graphics system (if installed)
- ✓ Check Steam deployment files
- ✓ Test Python syntax in all modules
- ✓ Test game engine imports
- ✓ Check disk space

### 2. Run the Game

Once verification passes, start the game:

```bash
python3 play.py
```

### 3. Test Graphics Systems

To test the procedural graphics generation:

```bash
# Test SNES-style graphics
python3 snes_demo.py

# Test modern graphics (if installed)
python3 graphics_demo.py
```

Generated graphics will be saved to:
- SNES graphics: `generated_sprites/snes/`
- Modern graphics: `generated_sprites/modern/`

### 4. Run Unit Tests

If you want to run the game's unit tests:

```bash
python3 python-core/tests/test_game.py
```

## Steam Preparation

### 1. Get Your Steam Credentials

Before deploying to Steam, you need:
- **Steam App ID**: Obtain from Steamworks Partner portal
- **Depot ID**: Created in your app's configuration
- **Steam account**: With appropriate publishing permissions

### 2. Configure Steam Files

Update the Steam configuration files with your App ID:

#### `steam_appid.txt`
Replace `480` with your actual Steam App ID:
```
YOUR_APP_ID_HERE
```

#### `steam_app_build.vdf`
Update the appid and depot ID:
```vdf
"appbuild"
{
  "appid" "YOUR_STEAM_APP_ID_HERE"
  "desc" "Coin-Operated JRPG Build"
  
  "depots"
  {
    "YOUR_DEPOT_ID_HERE"
    {
      // ... rest of config
    }
  }
}
```

#### `steam_depot_build.vdf`
Update the depot ID:
```vdf
"DepotBuildConfig"
{
  "DepotID" "YOUR_DEPOT_ID_HERE"
  // ... rest of config
}
```

### 3. Generate Game Assets

Create icons and other assets for Steam:

```bash
python3 generate_icon.py
```

This generates:
- Multiple icon sizes (16x16 to 512x512)
- Windows ICO file
- Steam store icon (512x512)

Icons are saved to: `assets/icons/`

### 4. Build for Steam

Run the Steam build script:

```bash
chmod +x build_steam.sh
./build_steam.sh
```

This script will:
1. Clean previous builds
2. Verify Python dependencies
3. Generate game icons
4. Run tests
5. Create Steam build directory
6. Copy all game files
7. Create Steam launcher script
8. Verify build integrity

The Steam-ready build will be in: `steam_build/`

## Steam Deployment

### 1. Install SteamCMD

If not already installed, download and install SteamCMD:

```bash
# For Ubuntu/Debian
sudo apt-get install steamcmd

# Or download manually
mkdir ~/steamcmd
cd ~/steamcmd
curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
```

### 2. Upload to Steam

Using SteamCMD, upload your build:

```bash
cd ~/steamcmd
./steamcmd.sh +login YOUR_USERNAME +run_app_build /path/to/steam_app_build.vdf +quit
```

Replace:
- `YOUR_USERNAME`: Your Steam username
- `/path/to/steam_app_build.vdf`: Full path to your build config

### 3. Set to Live

After upload completes:
1. Log into Steamworks Partner portal
2. Navigate to your app's build section
3. Select the uploaded build
4. Set it live on your desired release branch

## Troubleshooting

### Python Version Issues

**Problem**: `Python 3.8+ required`

**Solution**:
```bash
# Check version
python3 --version

# If too old, update (Ubuntu)
sudo apt-get update
sudo apt-get install python3.10
```

### Pillow Installation Fails

**Problem**: `error: command 'gcc' not found`

**Solution**:
```bash
# Install build dependencies (Ubuntu)
sudo apt-get install python3-dev python3-pip
sudo apt-get install libjpeg-dev zlib1g-dev

# Then retry
pip3 install Pillow>=9.0.0
```

### Permission Denied

**Problem**: `Permission denied` when running scripts

**Solution**:
```bash
chmod +x setup_linux.sh verify.sh build_steam.sh play.py
```

### Graphics Don't Generate

**Problem**: No sprites appear or generation fails

**Solution**:
```bash
# Ensure Pillow is installed
pip3 install --upgrade Pillow

# Try generating manually
python3 generate_icon.py
python3 snes_demo.py
```

### SteamCMD Login Issues

**Problem**: Authentication fails or Steam Guard required

**Solution**:
- Use your Steam Guard code when prompted
- For automated builds, set up Steam Guard Mobile Authenticator
- Consider using shared_config files for CI/CD

### Build Verification Fails

**Problem**: `./verify.sh` reports errors

**Solution**:
1. Read the error messages carefully
2. Fix any missing files or dependencies
3. Run verification again
4. Check Python syntax if syntax errors reported

### Game Won't Launch on Linux

**Problem**: Game crashes or won't start

**Solution**:
```bash
# Check error messages
python3 play.py

# Verify all imports work
python3 -c "import sys; sys.path.insert(0, 'python-core'); from core.game_engine import GameEngine"

# Check file permissions
ls -la python-core/
```

## Additional Resources

### File Structure for Steam Build

```
steam_build/
├── launch.sh           # Main launcher script
├── play.py             # Game entry point
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT license
├── README.md          # Player documentation
├── python-core/        # Core game code
│   ├── main.py
│   ├── core/
│   ├── systems/
│   ├── content/
│   └── graphics/
├── assets/             # Generated assets
│   └── icons/
└── docs/               # Documentation
```

### Testing Checklist

Before publishing to Steam, ensure:
- [ ] Verification script passes (`./verify.sh`)
- [ ] Game launches successfully
- [ ] All 10 episodes are playable
- [ ] Combat system works
- [ ] Save/load functionality works
- [ ] Graphics generate properly
- [ ] Steam overlay works (if integrated)
- [ ] Icons display correctly
- [ ] All dependencies are included

### Performance Notes

- **Load times**: First launch may be slower due to graphics generation
- **Save files**: Stored in JSON format in game directory
- **Generated assets**: Cached after first generation
- **Memory usage**: ~50-100 MB during gameplay

## Support

For issues specific to:
- **Game bugs**: Check `python-core/tests/test_game.py`
- **Graphics issues**: See `docs/SNES_GRAPHICS.md`
- **Steam integration**: Consult Steamworks documentation
- **Linux compatibility**: Test on Ubuntu 20.04+ first

## License

This game is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

**Ready to publish?** Run `./verify.sh` to ensure everything is ready!
