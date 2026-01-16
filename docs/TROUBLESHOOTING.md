# COIN-OPERATED JRPG: Troubleshooting Guide

## Quick Diagnostic

Before diving into specific issues, run the diagnostic tool:

```bash
python3 diagnose.py
```

This will check your system and identify most common problems automatically.

---

## Common Issues

### Installation Problems

#### Issue: "ModuleNotFoundError: No module named 'pygame'"

**Symptoms:**
- Error when trying to launch graphics or SNES mode
- Import errors mentioning pygame

**Solution:**
```bash
pip install pygame
# or
pip install -r requirements.txt
```

**If that doesn't work:**
```bash
# Try upgrading pip first
python3 -m pip install --upgrade pip

# Then install pygame
python3 -m pip install pygame
```

---

#### Issue: "ModuleNotFoundError: No module named 'PIL'"

**Symptoms:**
- Error when trying to use SNES mode
- Import errors mentioning PIL or Pillow

**Solution:**
```bash
pip install Pillow
# or
pip install -r requirements.txt
```

---

#### Issue: "Python version too old"

**Symptoms:**
- Syntax errors with type hints
- "Type annotations require Python 3.8+"

**Solution:**
1. Check your Python version:
   ```bash
   python3 --version
   ```

2. If < 3.8, upgrade Python:
   - **Ubuntu/Debian:** `sudo apt install python3.10`
   - **macOS:** `brew install python@3.10`
   - **Windows:** Download from python.org

3. Create new virtual environment with correct version:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

---

### Graphics/Display Issues

#### Issue: "pygame.error: No available video device"

**Symptoms:**
- Error when trying to launch graphics mode
- "No available video device" or similar

**Solution:**

**On Linux:**
```bash
# Check if X11 is running
echo $DISPLAY

# If empty, you're in a headless environment
# Use text mode instead:
python3 launch_game.py --mode text
```

**On WSL/WSL2:**
```bash
# Install VcXsrv or X410 on Windows
# Set DISPLAY variable
export DISPLAY=:0

# Or use WSLg (Windows 11)
# Should work automatically
```

**On Remote Server:**
```bash
# Use virtual display (xvfb)
sudo apt install xvfb
xvfb-run python3 launch_game.py --mode graphics
```

---

#### Issue: "Display freezes or stutters"

**Symptoms:**
- Low frame rate
- Choppy animation
- Screen tearing

**Solutions:**

1. **Check FPS:**
   ```python
   # Run profiler
   python3 profile_graphics.py
   ```

2. **Reduce resolution:**
   ```python
   # In python-core/config.py or via launcher
   python3 launch_game.py --mode graphics
   # Then edit config: Set graphics.width=640, graphics.height=480
   ```

3. **Enable VSync:**
   ```python
   # Edit config.json
   {
     "graphics": {
       "vsync": true
     }
   }
   ```

4. **Lower FPS cap:**
   ```python
   # Edit config.json
   {
     "graphics": {
       "fps": 30  # Instead of 60
     }
   }
   ```

---

#### Issue: "Colors look wrong in SNES mode"

**Symptoms:**
- Washed out colors
- Incorrect palette
- Modern-looking colors instead of retro

**Solution:**

1. **Check SNES palette is being used:**
   ```bash
   # Generate palette reference
   python3 generate_assets.py
   # Check assets/palettes/snes_palette.png
   ```

2. **Verify SNES mode is actually active:**
   ```python
   # Check config
   from python-core.config import ConfigManager
   config = ConfigManager()
   print(config.get('graphics.mode'))  # Should be 'snes'
   ```

3. **Force palette refresh:**
   ```bash
   # Delete config and restart
   rm ~/.coin-operated-jrpg/config.json
   python3 launch_game.py --mode snes
   ```

---

### Save File Issues

#### Issue: "Can't load save file"

**Symptoms:**
- Error when loading game
- "Corrupted save" message
- Lost progress

**Solutions:**

1. **Check save file exists:**
   ```bash
   ls ~/.coin-operated-jrpg/saves/
   ```

2. **Validate save file:**
   ```bash
   python3 automation/validate_save_files.py
   ```

3. **Restore from backup:**
   ```bash
   # If backup exists
   cp ~/.coin-operated-jrpg/saves/slot1.json.bak ~/.coin-operated-jrpg/saves/slot1.json
   ```

4. **Manual repair:**
   ```bash
   # Open in text editor
   nano ~/.coin-operated-jrpg/saves/slot1.json
   # Check for valid JSON syntax
   ```

---

#### Issue: "Save not compatible between modes"

**Symptoms:**
- Can't load text mode save in graphics mode
- Data mismatch errors

**Solution:**

This shouldn't happen - all modes use the same save format. If it does:

1. **Run validation:**
   ```bash
   python3 automation/validate_save_files.py
   ```

2. **Check save file format:**
   ```bash
   # Should have these keys:
   cat ~/.coin-operated-jrpg/saves/slot1.json
   # Look for: player, location, inventory, quests
   ```

3. **Report bug:**
   This indicates an architecture violation. Please report with:
   - Save file content (sensitive data removed)
   - Modes involved
   - Error message

---

### Performance Issues

#### Issue: "Slow startup"

**Symptoms:**
- Takes long time to launch
- Hangs on loading screen

**Solutions:**

1. **Profile startup:**
   ```bash
   python3 -m cProfile launch_game.py --mode text > profile.txt
   ```

2. **Clear cache:**
   ```bash
   # Remove Python cache
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

---

#### Issue: "High memory usage"

**Symptoms:**
- System slowing down
- Out of memory errors

**Solutions:**

1. **Profile memory:**
   ```bash
   python3 profile_graphics.py
   ```

2. **Reduce asset cache:**
   ```python
   # In config.json
   {
     "graphics": {
       "cache_size": 50  # Reduce from default
     }
   }
   ```

3. **Use text mode for low-memory systems:**
   ```bash
   python3 launch_game.py --mode text
   ```

---

### Import Errors

#### Issue: "Can't import from graphics module"

**Symptoms:**
- ImportError for graphics.adapter, etc.
- "No module named 'graphics'"

**Solution:**

1. **Check file structure:**
   ```bash
   ls python-core/graphics/
   # Should see: adapter.py, pygame_renderer.py, etc.
   ```

2. **Check PYTHONPATH:**
   ```bash
   # Add python-core to path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/python-core"
   ```

3. **Use launcher instead of direct import:**
   ```bash
   # Don't: python3 python-core/graphics/pygame_renderer.py
   # Do: python3 launch_game.py --mode graphics
   ```

---

#### Issue: "Circular import detected"

**Symptoms:**
- ImportError about circular dependencies
- "Cannot import name X from partially initialized module"

**Solution:**

This indicates an architecture violation. Check:

1. **Graphics modules should only import from interfaces.py:**
   ```bash
   python3 automation/validate_interfaces.py
   ```

2. **No direct imports from core/systems/content:**
   ```bash
   grep -r "from core" python-core/graphics/
   grep -r "from systems" python-core/graphics/
   grep -r "from content" python-core/graphics/
   # Should return nothing
   ```

3. **If violations found:**
   - Review [ARCHITECTURE_DIAGRAM.md](docs/ARCHITECTURE_DIAGRAM.md)
   - Fix imports to use adapter instead

---

### Configuration Issues

#### Issue: "Config file won't save"

**Symptoms:**
- Changes don't persist
- Config resets every launch

**Solutions:**

1. **Check file permissions:**
   ```bash
   ls -la ~/.coin-operated-jrpg/config.json
   # Should be writable
   ```

2. **Check disk space:**
   ```bash
   df -h ~
   ```

3. **Manual config creation:**
   ```bash
   mkdir -p ~/.coin-operated-jrpg
   cat > ~/.coin-operated-jrpg/config.json << 'EOF'
   {
     "graphics": {
       "mode": "text",
       "width": 800,
       "height": 600,
       "fps": 60
     }
   }
   EOF
   ```

---

#### Issue: "Invalid configuration"

**Symptoms:**
- Error parsing config
- "Invalid JSON" messages

**Solution:**

1. **Validate JSON:**
   ```bash
   cat ~/.coin-operated-jrpg/config.json | python3 -m json.tool
   ```

2. **Reset to defaults:**
   ```bash
   rm ~/.coin-operated-jrpg/config.json
   python3 launch_game.py
   ```

---

## Platform-Specific Issues

### Linux

#### Issue: "Audio not working"

**Solution:**
```bash
# Install audio dependencies
sudo apt install libasound2-dev pulseaudio

# Check audio
speaker-test -t wav -c 2
```

#### Issue: "Permission denied for display"

**Solution:**
```bash
# Allow X11 connection
xhost +local:

# Or run as correct user
sudo -u $USER python3 launch_game.py
```

---

### macOS

#### Issue: "App not signed/verified"

**Solution:**
```bash
# Allow unsigned apps
xattr -d com.apple.quarantine launch_game.py

# Or in System Preferences:
# Security & Privacy → Allow apps from: Anywhere
```

#### Issue: "Pygame window appears behind others"

**Solution:**
```python
# Add to pygame initialization
import pygame
pygame.init()
pygame.display.set_caption("COIN-OPERATED JRPG")
# Then window should focus properly
```

---

### Windows

#### Issue: "Python not found"

**Solution:**
```batch
# Use py launcher
py -3 launch_game.py

# Or add Python to PATH in System Environment Variables
```

#### Issue: "DLL load failed"

**Solution:**
```batch
# Install Visual C++ Redistributables
# Download from: https://aka.ms/vs/16/release/vc_redist.x64.exe

# Then reinstall pygame
pip uninstall pygame
pip install pygame
```

---

## Advanced Troubleshooting

### Debug Mode

Enable debug output:

```bash
# Set environment variable
export COIN_JRPG_DEBUG=1

# Then run normally
python3 launch_game.py --mode graphics
```

### Verbose Logging

```python
# Add to top of launch_game.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Profiling

```bash
# CPU profiling
python3 -m cProfile -o profile.stats launch_game.py
python3 -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"

# Memory profiling (requires memory_profiler)
pip install memory_profiler
python3 -m memory_profiler launch_game.py
```

### Network Issues (Future Features)

For online features (when implemented):

```bash
# Check connectivity
ping api.coin-operated-jrpg.com

# Check DNS
nslookup api.coin-operated-jrpg.com

# Test with proxy
export HTTP_PROXY=http://proxy:8080
python3 launch_game.py
```

---

## Getting Help

### Before Asking for Help

1. Run diagnostic tool: `python3 diagnose.py`
2. Check this guide for your specific issue
3. Search existing GitHub issues
4. Try text mode to isolate graphics issues

### Reporting Bugs

Include:
1. Output from `python3 diagnose.py`
2. Python version: `python3 --version`
3. OS and version: `uname -a` (Linux) or `ver` (Windows)
4. Steps to reproduce
5. Expected vs actual behavior
6. Error messages and stack traces

### Community Support

- GitHub Issues: [Report bugs](https://github.com/your-repo/issues)
- Discussions: [Ask questions](https://github.com/your-repo/discussions)
- Discord: [Join community](#) (if available)

---

## Validation Scripts

Run these to check system health:

```bash
# Check architecture compliance
python3 automation/validate_interfaces.py

# Check for data duplication
python3 automation/validate_no_redundancy.py

# Check save file compatibility
python3 automation/validate_save_files.py

# Check feature parity between modes
python3 automation/validate_feature_parity.py
```

All should pass (exit code 0) on a healthy system.

---

## Performance Benchmarks

Expected performance on reference hardware:

**Reference System:**
- CPU: Intel i5 (4 cores, 2.5GHz)
- RAM: 8GB
- GPU: Integrated graphics
- OS: Ubuntu 22.04

**Benchmarks:**
- Text mode: < 1% CPU, < 50MB RAM
- Graphics mode: < 5% CPU, < 150MB RAM, 60 FPS
- SNES mode: < 8% CPU, < 180MB RAM, 60 FPS
- Startup time: < 3 seconds
- Save/load: < 0.1 seconds

If your performance is significantly worse, see Performance Issues section.

---

## Emergency Recovery

### Nuclear Option: Complete Reset

```bash
# Backup saves
cp -r ~/.coin-operated-jrpg/saves ~/saves-backup

# Remove all config and cache
rm -rf ~/.coin-operated-jrpg

# Reinstall dependencies
pip uninstall pygame Pillow
pip install -r requirements.txt

# Restore saves
mkdir -p ~/.coin-operated-jrpg/saves
cp ~/saves-backup/* ~/.coin-operated-jrpg/saves/

# Run in text mode first
python3 launch_game.py --mode text
```

---

**Last Updated:** December 2024  
**Version:** 1.0

For issues not covered here, please [open an issue](https://github.com/your-repo/issues) with output from `python3 diagnose.py`.
