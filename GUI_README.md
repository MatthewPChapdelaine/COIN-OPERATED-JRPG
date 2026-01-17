# COIN:OPERATED - GUI-Based JRPG

**A 16-bit Retro JRPG where you play as Coin - a sentient being created from mystical Domminnian coins**

## 🎮 Launch from Desktop (No Terminal Required!)

This game is designed to run as a **GUI application** - just like any other desktop game.

### Quick Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Desktop Integration:**
   ```bash
   python3 install.py
   ```

3. **Launch the Game:**
   - Click the "COIN:OPERATED" icon in your applications menu
   - OR double-click the desktop icon
   - OR run: `python3 coin_operated.py`

### What Makes This Special

✨ **No Terminal Required** - Launches directly as a GUI application  
🎨 **Authentic 16-bit Graphics** - Inspired by SNES-era JRPGs like Final Fantasy VI & Chrono Trigger  
🪙 **Unique Protagonist** - Play as Coin, a magical being made of enchanted coins  
🌌 **Deep Spiritual Narrative** - Themes from Gnostic Christianity and Wicca  
⚔️ **Strategic Combat** - Turn-based JRPG battles  
🎭 **Multiple Endings** - Your choices shape the story  

## 🎨 Graphics Style

The graphics are designed to match:
- **Coin's Character**: Golden, mystical, coin-like appearance with magical aura
- **16-bit Aesthetic**: Inspired by SNES Final Fantasy, Chrono Trigger, Secret of Mana
- **Mystical Theme**: Dark mystical stones, purple/gold magical effects, spiritual atmosphere
- **The Setting**: Planet Acadmium, magical vs technology conflict

### Character Design

**Coin** (Protagonist):
- Golden circular body (like a magical coin)
- Mystical purple eyes
- Glowing magical aura
- Small head coin above main body
- Transforms from young to adult to Time Goddess throughout the story

**Other Characters**:
- **Jinn-Lir**: Blue wizard robes, staff wielder (Light Cabal)
- **Orbius**: Ancient mystical master (Light Cabal leader)
- **Coireena**: Knight/warrior with armor (former victim, now protector)
- **Typhus**: Mysterious creature (Dark Cabal affinity)

## 🎯 The Story

You are **Coin** - created by the wizard Jinn-Lir from Domminnian Coins and magical essence. Originally intended as a tool for war between the Light Cabal (magic faction) and the Drift Empire (technology faction), you must discover your own agency and destiny.

**Your Journey**:
- **Act I**: Origins & Exploitation - Discover you're more than a tool
- **Act II**: Independence & Conflict - Break free and find your power
- **Act III**: Temporal Awakening - Unlock time magic and goddess powers
- **Act IV**: Resolution - Choose one of 5 different endings based on your choices

**Spiritual Themes**:
- **Gnostic**: Awakening to divine knowledge, transcending material limitations
- **Wiccan**: Triple Goddess cycle (Maiden→Mother→Crone), elemental mastery
- Identity, self-determination, and the divine feminine

## 🎮 Controls

- **Arrow Keys** (↑ ↓ ← →): Move Coin around the world
- **SPACE/ENTER**: Interact with NPCs and objects
- **ESC**: Quit game
- **S**: Save game
- **A**: Attack (in combat)

## 📁 Project Structure

```
COIN-OPERATED-JRPG/
├── coin_operated.py              # Main GUI launcher (NO TERMINAL!)
├── install.py                    # Desktop integration installer
├── COIN-OPERATED-JRPG.desktop   # Linux desktop file
├── python-core/
│   ├── core/
│   │   ├── game_engine.py       # Game loop and state
│   │   └── character.py         # Coin and party members
│   ├── graphics/
│   │   ├── snes_pygame_renderer.py   # 16-bit renderer
│   │   ├── sprite_generator.py        # Procedural Coin sprites
│   │   ├── color_palette.py           # Mystical color schemes
│   │   └── ...
│   ├── systems/                 # Combat, quests, dialogue, etc.
│   └── content/                 # Acts I-IV story content
└── docs/                        # Full documentation
```

## 🔧 Technical Details

### Graphics Architecture

The game uses **procedural generation** for all graphics:
- **No external art assets required** - everything generated in code
- **16-bit authentic style** - matches SNES-era JRPGs
- **256x224 resolution** (scaled 3x for modern displays = 768x672)
- **60 FPS** for smooth animation
- **Mystical color palette** - golds, purples, dark mystical tones

### Why GUI-Only?

This is a complete game, not a development tool:
- ✅ Launches like any desktop game
- ✅ No terminal window clutter
- ✅ Professional game experience
- ✅ Can be distributed as a standalone application
- ✅ Follows modern game design standards

### Character-Matched Graphics

The graphics specifically match the lore:
- **Coin**: Golden circular sprite with magical aura (exactly as described in lore)
- **Mystical environments**: Dark stones with magical sparkles
- **UI theme**: Gold and purple (matching Coin's divine/magical nature)
- **16-bit aesthetic**: Matches the retro JRPG inspiration

## 🚀 Development Status

✅ **Core Engine**: Complete  
✅ **Graphics System**: 16-bit retro renderer working  
✅ **Character System**: Coin + party members implemented  
✅ **Combat System**: Turn-based battles functional  
✅ **Movement**: Tile-based world exploration  
✅ **GUI Launcher**: No terminal required  
✅ **Desktop Integration**: Linux .desktop file  

🚧 **In Progress**:
- Full Act I-IV content integration
- NPC dialogues in graphics mode
- Quest system GUI
- Save/Load GUI
- Sound effects and music

## 📚 Lore Documents

Read more about the game's deep lore:
- [COIN_OPERATED JRPG.md](COIN_OPERATED%20JRPG.md) - Complete game design
- [SPIRITUAL_NARRATIVE.md](SPIRITUAL_NARRATIVE.md) - Gnostic & Wiccan themes
- [DESIGN_LAW.md](DESIGN_LAW.md) - Technical standards
- [README.md](README.md) - Original project documentation

## 🎯 For Players

**This is a complete game you can play right now!**

1. Install it (`python3 install.py`)
2. Launch it from your applications menu
3. Play as Coin and explore the mystical world of Acadmium
4. Make choices that shape your destiny
5. Discover the path from tool to Time Goddess

**No programming knowledge required** - just launch and play!

## 🎨 For Artists/Modders

The procedural graphics system in `python-core/graphics/` can be modified to create different visual styles while maintaining the 16-bit aesthetic and Coin's character design.

## 📞 Support

Having issues? Check:
1. Dependencies installed: `pip install -r requirements.txt`
2. Running from project root directory
3. Python 3.8+ installed
4. Pygame and Pillow libraries available

---

**COIN:OPERATED** - *From coin to goddess, from tool to deity*  
*A Universe Beyond the Universe*

🪙✨🌌
