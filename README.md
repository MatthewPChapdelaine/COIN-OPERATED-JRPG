# COIN:OPERATED JRPG

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Game Status: Playable](https://img.shields.io/badge/status-playable-green.svg)]()
[![Graphics: 16-bit Retro](https://img.shields.io/badge/graphics-16--bit--retro-ff69b4.svg)]()
[![Platform: GUI Desktop](https://img.shields.io/badge/platform-GUI%20Desktop-lightgrey.svg)]()
[![No Terminal Required](https://img.shields.io/badge/launch-GUI%20only-success.svg)]()

**An authentic 16-bit JRPG set in the Orbspace universe - GUI Desktop Game**

Play as **Coin**, a sentient being created from mystical Domminnian coins, on your journey from magical artifact to Time Goddess. Features deep storytelling, strategic turn-based combat, and meaningful player choices in an authentic 16-bit retro style inspired by SNES classics like Final Fantasy VI and Chrono Trigger.

## ✨ NEW: Exclusive GUI Experience

🎮 **No Terminal Required** - Launches as a proper desktop game  
🪙 **Play as Coin** - Unique golden, mystical protagonist  
🎨 **Character-Matched Graphics** - Visuals designed specifically for Coin's magical, coin-based form  
🌌 **Spiritual Narrative** - Themes from Gnostic Christianity and Wicca  
⚔️ **16-bit Combat** - Classic JRPG turn-based battles  

---

## 🎮 Quick Start (GUI Launch)

## 🎮 One-Command Installation

### No Technical Knowledge Required!

**Linux:**
```bash
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG
bash setup.sh
```

**Windows:**
```bash
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG
setup.bat
```
*(Or just double-click `setup.bat`)*

**Any Platform:**
```bash
python3 auto_setup.py
```

### What Happens Automatically

The installer will:
- ✅ Check Python and pip
- ✅ Install all dependencies (pygame, Pillow)
- ✅ Create application menu shortcut
- ✅ Optionally create desktop icon
- ✅ Set up quick launch scripts
- ✅ Offer to launch the game immediately

**Takes 1-2 minutes. Zero configuration needed!**

### After Installation

Launch the game any way you prefer:
- 🔍 Search for "COIN:OPERATED" in your applications menu
- 🖱️ Double-click the desktop icon (if created)
- 🎮 Run `./play.sh` (Linux/macOS) or `play.bat` (Windows)
- 💻 Run `python3 coin_operated.py`

**The game launches as a pure GUI application - no terminal window!**

### What You'll See

1. **Splash Screen**: Golden Coin logo with magical glow
2. **Game World**: 16-bit tile-based exploration
3. **Coin Character**: Golden, mystical sprite with purple eyes and magical aura
4. **UI**: Gold and purple themed (matching Coin's divine nature)
5. **Controls displayed on-screen** - no manual needed!

---

## 🎨 Graphics & Aesthetic

This game's graphics are specifically designed to match the character and setting:

**Coin's Design**:
- Golden circular form (like an enchanted coin)
- Mystical purple eyes
- Glowing magical aura
- Small head coin floating above
- Transforms through the story (Maiden → Mother → Crone / Time Goddess)

**World Aesthetic**:
- Dark mystical stone tiles
- Magical sparkles and effects
- 16-bit SNES-era style (256x224 scaled 3x)
- Purple and gold UI theme
- Authentic retro JRPG look

**Inspired by**: Final Fantasy VI, Chrono Trigger, Secret of Mana

---

## 📖 Story

You are **Coin**, a sentient being created from Domminnian Coins and pure magical essence. Born as a tool for war in the conflict between the magic-focused Light Cabal and the technology-driven Drift Empire, you must discover your own agency and destiny.

**Explore themes of:**
- Identity and self-determination
- Exploitation vs. agency  
- Technology vs. magic
- Predetermined fate vs. free will
- Time travel and temporal paradoxes

**Across 4 acts:**
- **Act I:** Origins & Exploitation
- **Act II:** Independence & Conflict  
- **Act III:** Temporal Awakening
- **Act IV:** Resolution & Consequences (5 unique endings)

---

## ✨ Features

### 🎯 Core Gameplay
- **Turn-Based Combat:** Strategic JRPG-style battles with party management
- **Character Progression:** Level up, unlock abilities, and customize equipment
- **Dual Currency System:** Domminnian Coins and Magical Essence
- **Faction Reputation:** Your choices affect relationships with Light Cabal, Dark Cabal, and Drift Empire

### 📜 Story & Quests
- **30+ Quests:** Main story, side quests, faction quests, and character quests
- **Branching Dialogue:** Choices that matter with consequences
- **Multiple NPCs:** Each with unique personalities and storylines
- **5 Unique Endings:** Based on your choices and faction allegiances

### ⚔️ Combat & Progression
- **Playable Characters:** Coin, Jinn-Lir, Orbius, Typhus, Coireena
- **Enemy Variety:** 10+ enemy types plus bosses and optional superbosses
- **Equipment System:** Common → Rare → Epic → Legendary gear
- **Ability Trees:** Unlock powerful magic and combat abilities

### 🎨 Graphics Systems

#### Retro16-Style System ⭐ NEW!
- **Authentic 16-bit**: True retro 16-bit resolution (256×224) and color depth (15-bit RGB)
- **Pixel-Perfect Sprites**: 16×16 character sprites in classic JRPG style
- **Tile-Based Maps**: Overworld and dungeon exploration with scrolling camera
- **Side-View Battles**: Classic FF4-6 style battle screens
- **Classic UI**: Dark blue windows, yellow cursor, color-coded HP bars
- **Complete Scenes**: Title screen, menus, dialogue boxes, status windows

**Benefits:**
- Authentic golden-age JRPG aesthetic
- Optimized for retro feel
- Instant nostalgia for classic 16-bit RPG fans
- Inspired by FF6, Chrono Trigger, Secret of Mana

See [docs/SNES_GRAPHICS.md](docs/SNES_GRAPHICS.md) for complete documentation (Retro16 system).

#### Modern Procedural System
- **100% Code-Generated:** All graphics created procedurally - no external image files required
- **Character Sprites:** Unique pixel art for all 6+ playable characters (32×32)
- **Enemy Sprites:** Procedurally generated enemy designs
- **Animations:** Walk cycles, attacks, spell casting, and more
- **Visual Effects:** Magic spells, combat effects, particle systems
- **UI Elements:** Buttons, windows, health bars, icons, menus
- **Environment:** Tiles, backgrounds, props, walls - all generated at runtime
- **Dynamic Theming:** Change visual style and colors programmatically

**Benefits:**
- No binary assets in version control
- Tiny file size (graphics system is pure Python code)
- Easy color customization and theming
- Infinite variations possible
- Accessibility-friendly (adjustable for different vision needs)

See [docs/GRAPHICS_SYSTEM.md](docs/GRAPHICS_SYSTEM.md) for modern system documentation.

### 💾 Save System
- **10 Save Slots:** Multiple playthroughs supported
- **Auto-Save:** Never lose progress
- **New Game+:** Replay with bonuses and new dialogue

---

## 🗂️ Project Structure

```
COIN-OPERATED-JRPG/
├── src/
│   ├── core/              # Game engine, character system
│   ├── systems/           # Combat, quests, dialogue, save/load
│   ├── content/           # Story content for all 4 acts
│   ├── tests/             # Automated test suite
│   └── main.py            # Game entry point
├── saves/                 # Save game files (auto-created)
├── docs/                  # Documentation
├── play.py                # Quick launch script
└── COIN_OPERATED JRPG.md  # Complete design document
```

---

## 🎭 Characters

### Coin (Protagonist)
Sentient magical being created for war. Grows from child to adult through the story, eventually awakening as the Time Goddess.

**Role:** Magic DPS  
**Starting Abilities:** Magical Strike, Healing Light  
**Ultimate Power:** Time manipulation and goddess-level magic

### Jinn-Lir
Your creator and flawed mentor. Powerful wizard of the Light Cabal.

**Role:** Magic DPS, Strategic Support  
**Special:** Teleportation, multi-target spells

### Orbius
Master of the Light Cabal with mysterious knowledge of all Orbspace.

**Role:** Healer, Utility  
**Special:** Time-warping assistance, one-use game-changing spells

### Typhus
Mysterious creature that ages with Coin. Non-verbal companion with wild magic.

**Role:** Wild Card  
**Special:** Unpredictable destructive power

### Coireena
Super-soldier empowered by your stolen magic. Former victim, now protector.

**Role:** Tank, Counter-attacks  
**Special:** Defensive magic, damage reflection

---

## 🌍 World of Orbspace

### Main Locations
- **Acadmium City:** Urban hub on Planet Acadmium (Drift system)
- **Lifeblood Temple:** Ancient magical sanctuary
- **Drift Capital:** Technological stronghold of the Empire
- **Light Cabal Headquarters:** Center of magical learning
- **Time Ship:** Vessel of Elder Coin from the future
- **Endless Library:** Dimensional archive of all knowledge

### Factions
- **Light Cabal:** Preserves magical traditions, morally conflicted
- **Dark Cabal:** Embraces chaotic destructive power  
- **Drift Empire:** Technology-focused, views magic as chaos
- **Independent Resistance:** Fights against all forms of oppression

---

## 🎮 Gameplay Guide

### Combat Tips
- Exploit enemy weaknesses (magic vs. physical)
- Manage MP carefully - abilities are powerful but costly
- Use items strategically in tough battles
- Boss battles require pattern recognition

### Progression Tips
- Complete side quests for extra rewards
- Balance faction reputations for best ending options
- Save Magical Essence for important ability unlocks
- Equipment quality matters - seek out rare gear

### Multiple Endings
Your ending is determined by:
- Faction reputation levels
- Key story choices
- Character level
- Specific quest completions

**Available Endings:**
1. **Time Goddess:** Accept immortal destiny
2. **Rebel:** Reject destiny, forge own path (hardest)
3. **Light Cabal:** Unite magic users peacefully
4. **Dark Cabal:** Embrace chaos and power
5. **Peaceful:** Broker peace between all factions

---

## 🛠️ Technical Details

### Requirements
- **Python:** 3.8 or higher
- **PIL/Pillow:** 9.0.0+ (for procedural graphics generation)
- **Disk Space:** ~100MB (includes generated assets)
- **OS:** Linux (primary), macOS, Windows

### Installation

#### Linux (Recommended)
```bash
# Clone repository
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG

# Automated setup
./setup_linux.sh

# Verify installation
./verify.sh

# Play!
python3 play.py
```

#### Other Platforms
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run game
python3 play.py
```

### Steam Deployment

Ready for Steam! See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full instructions.

```bash
# Build for Steam
./build_steam.sh

# Upload using SteamCMD
steamcmd +login YOUR_USERNAME +run_app_build steam_app_build.vdf +quit
```

### Supported Platforms
- ✅ **Linux** (Ubuntu 18.04+, Fedora 30+, etc.)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10+)
- ✅ **Steam** (Ready for distribution)

### Performance
- Text-based interface for maximum compatibility
- Minimal system requirements (512MB RAM)
- Save files are compact JSON format
- Graphics generated on-demand and cached

---

## �️ Developer Tools

### System Diagnostics
Run automated health checks to identify issues:
```bash
python3 diagnose.py
```

Features:
- Python version check
- Dependency verification
- File structure validation
- Import path testing
- Pygame display test
- Configuration check
- Quick functional test

### Performance Profiling
Analyze graphics rendering performance:
```bash
python3 profile_graphics.py
```

Profiles:
- Adapter operations (1000 iterations)
- Configuration system
- Utility functions (10,000 iterations)
- Pygame renderer (100 frames)
- Retro16 renderer (100 frames)
- Bottleneck analysis
- Performance recommendations

### Asset Generation
Create placeholder graphics assets:
```bash
python3 generate_assets.py
```

Generates:
- Character sprites (5 characters)
- Enemy sprites (8 enemies)
- NPC sprites (5 NPCs)
- Item icons (8 items)
- Tileset (8 tiles)
- UI elements (5 elements)
- Effect sprites (7 effects)
- Retro16 palette reference
- Asset manifest (JSON)

### Release Automation
Build and package releases:
```bash
python3 build_release.py
```

Automates:
- Prerequisite checks
- Test suite execution
- Code quality checks
- Build artifact cleaning
- Package creation
- Checksum generation
- Git tag creation

### Testing
Run comprehensive test suite:
```bash
python3 test_graphics_system.py
```

Tests:
- Interface compliance
- Graphics adapter
- Configuration system
- Utility functions
- Validation scripts
- Integration testing
- File structure

---

## �📚 Documentation

### Core Documentation
- **[README](README.md)** - This file (quick start, features overview)
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Linux setup and Steam publishing
- **[Development Guide](docs/DEVELOPMENT.md)** - For developers and modders
- **[Game Design Document](COIN_OPERATED%20JRPG.md)** - Complete design specification

### Graphics System
- **[Retro16 Graphics System](docs/SNES_GRAPHICS.md)** - Authentic 16-bit JRPG visuals
- **[Modern Graphics System](docs/GRAPHICS_SYSTEM.md)** - Procedural graphics documentation
- **[Graphics Integration](GRAPHICS_INTEGRATION.md)** - Integration guide
- **[Architecture Diagram](docs/ARCHITECTURE_DIAGRAM.md)** - System architecture

### Developer Resources
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** ⭐ NEW! - Common issues and solutions
- **[Feature Roadmap](docs/ROADMAP.md)** ⭐ NEW! - Planned features and timeline
- **[Quickstart Guide](QUICKSTART.md)** - Fast setup for developers
- **[Modes Comparison](MODES_COMPARISON.md)** - Text vs Graphics vs Retro16

### Implementation Reports
- **[Complete System Report](COMPLETE_SYSTEM_REPORT.md)** - Full implementation details
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Overview of systems
- **[Content Expansion Summary](CONTENT_EXPANSION_SUMMARY.md)** - Story and content
- **[Procedural Graphics Summary](PROCEDURAL_GRAPHICS_SUMMARY.md)** - Graphics tech


---

## 🎯 Development Roadmap

### ✅ Completed (v1.0)
- Core game engine and systems
- All 4 story acts with 30+ quests
- Turn-based combat system
- 5 playable characters
- 10+ enemy types and bosses
- Save/load system with multiple slots
- Faction reputation system
- Equipment and progression
- All 5 unique endings

### 🚧 In Progress
- Enhanced UI/graphics layer
- Audio system integration
- Additional superboss encounters
- Expanded side quest content

### 📋 Planned Features
- Graphical UI overlay
- Voice acting support
- Additional storylines in other Orbspace empires
- Multiplayer co-op mode (experimental)
- Mod support and tools

---

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional quests and storylines
- Enemy and boss designs
- Equipment and items
- UI improvements
- Bug fixes and optimizations

Please read [DEVELOPMENT.md](docs/DEVELOPMENT.md) before contributing.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Credits

**Universe:** Orbspace - A Universe Beyond the Universe  
**Developer:** Loporian Industries / Matt's Lair Brand  
**Game Design:** Based on comprehensive prompt engineering framework  
**Inspired by:** Maximum Computer Design Game Template

**Special Thanks:**
- All playtesters and contributors
- The JRPG community for inspiration
- Everyone who believed in Coin's story

---

## 📞 Contact

- **GitHub:** [MatthewPChapdelaine](https://github.com/MatthewPChapdelaine)
- **Issues:** [Report bugs or request features](https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG/issues)

---

## 🎮 Enjoy the Game!

```
╔══════════════════════════════════════╗
║     COIN:OPERATED JRPG               ║
║  A Universe Beyond the Universe      ║
╚══════════════════════════════════════╝

Your destiny awaits, Time Goddess...
```

---

*"I am not just coins to be spent. I am Coin, and I choose my own path."*
COIN:OPERATED JRPG
