# 🎮 Quick Start Guide

## Choose Your Mode

COIN-OPERATED JRPG supports three gameplay modes:

### 🎨 Retro16 Mode (Recommended)
**Authentic 16-bit graphics with modern interface**
```bash
pip install pygame Pillow
python3 launch_game.py --mode retro16
```
- 256x224 resolution (scaled 3x)
- Authentic Retro16-style graphics
- Procedurally generated sprites
- Classic JRPG battle screen

### 🖼️ Graphics Mode
**Modern 2D graphics renderer**
```bash
pip install pygame
python3 launch_game.py --mode graphics
```
- 800x600 resolution
- Clean modern interface
- Full pygame rendering
- Smooth animations

### 📖 Text Mode
**Original interactive fiction experience**
```bash
python3 launch_game.py --mode text
```
- No graphics dependencies
- Terminal-based gameplay
- Rich narrative focus
- Works everywhere

## Installation

### Quick Install (All Modes)
```bash
# Clone repository
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG

# Install all dependencies
pip install -r requirements.txt

# Launch game (Retro16 mode)
python3 launch_game.py
```

### Linux Quick Setup
```bash
chmod +x setup_linux.sh
./setup_linux.sh
python3 launch_game.py
```

### Text Mode Only
```bash
# No dependencies needed!
python3 launch_game.py --mode text
```

## Controls

### Graphics/Retro16 Modes
```
Arrow Keys    Move character
Space/Enter   Interact with NPCs
A             Attack (in combat)
S             Save game
I             Inventory
ESC           Quit
```

### Text Mode
```
Type commands or select numbered options
help          Show available commands
quit          Exit game
```

## Game Modes Comparison

| Feature | Text | Graphics | Retro16 |
|---------|------|----------|------|
| Resolution | Terminal | 800x600 | 768x672 |
| Graphics | None | Modern 2D | 16-bit Retro |
| Dependencies | None | pygame | pygame + Pillow |
| Performance | Instant | Fast | Fast |
| Authenticity | Original | Modern | Authentic 16-bit |
| Best For | Narrative | General | Retro fans |

## Troubleshooting

### "No module named pygame"
```bash
pip install pygame
```

### "No module named PIL"
```bash
pip install Pillow
```

### Graphics won't start
1. Check Python version: `python3 --version` (need 3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Try text mode: `python3 launch_game.py --mode text`

### Game runs too slowly
- Try graphics mode instead of Retro16: `python3 launch_game.py --mode graphics`
- Or use text mode: `python3 launch_game.py --mode text`

## List All Modes
```bash
python3 launch_game.py --list-modes
```

## Development

### Running Tests
```bash
python3 test_system.py
python3 test_graphics.py
```

### Validation
```bash
python3 automation/validate_interfaces.py
python3 automation/validate_no_redundancy.py
```

### Generate Retro16 Graphics Samples
```bash
python3 snes_demo.py
```

## Advanced Usage

### Custom Scale Factor (Retro16 Mode)
Edit `launch_game.py` and change:
```python
renderer = Retro16PygameRenderer(adapter, scale=3)  # 3x scaling
```
Options: 2 (512x448), 3 (768x672), 4 (1024x896)

### Custom Resolution (Graphics Mode)
Edit `launch_game.py` and change:
```python
renderer = PygameRenderer(adapter, width=1024, height=768)
```

## Architecture

All three modes use the **same game logic**:
```
Text Mode     ─┐
Graphics Mode ─┼─→ Game Engine → Game Logic
Retro16 Mode  ─┘
```

Benefits:
- ✅ Save files work across all modes
- ✅ Same quests, combat, story
- ✅ Zero data duplication
- ✅ Interface-based architecture

## Next Steps

1. **Play the game!** Start with Retro16 mode for authentic experience
2. **Read the docs** - See `docs/GRAPHICS_INTEGRATION.md`
3. **Check examples** - Run `python3 snes_demo.py` (still uses old filename)
4. **Contribute** - See `docs/DEVELOPMENT.md`

## Quick Links

- [Full Documentation](docs/)
- [Graphics System Guide](docs/GRAPHICS_INTEGRATION.md)
- [Retro16 Graphics](docs/SNES_GRAPHICS.md) (file not yet renamed)
- [Development Guide](docs/DEVELOPMENT.md)

## Support

Having issues? Check:
1. Python 3.8+ installed
2. Dependencies installed: `pip install -r requirements.txt`
3. Run validation: `./verify.sh`
4. Try text mode as fallback

Enjoy your adventure! 🎮✨
