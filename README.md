# COIN:OPERATED JRPG

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Game Status: Playable](https://img.shields.io/badge/status-playable-green.svg)]()
[![Graphics: SNES-Style](https://img.shields.io/badge/graphics-SNES--style-ff69b4.svg)]()
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()
[![Steam: Ready](https://img.shields.io/badge/Steam-ready-blue.svg)]()

**An authentic SNES-style JRPG set in the Orbspace universe**

Follow Coin's journey from sentient magical artifact to Time Goddess in this turn-based RPG featuring deep storytelling, strategic combat, and meaningful player choices. Features **authentic 16-bit graphics** generated procedurally to recreate the golden age of SNES JRPGs.

---

## 🎮 Quick Start

### Linux Users (Recommended)

```bash
# Clone the repository
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG

# Run automated setup (installs dependencies)
chmod +x setup_linux.sh
./setup_linux.sh

# Verify installation
./verify.sh

# Run the game
python3 play.py
```

### Manual Setup (All Platforms)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the game
python3 play.py
```

### Test Procedural Graphics

```bash
# Generate SNES-style graphics samples ⭐
python3 snes_demo.py

# Generate game icons
python3 generate_icon.py

# Test graphics system
python3 test_graphics.py
```

### Build for Steam

```bash
# Build Steam-ready package
chmod +x build_steam.sh
./build_steam.sh

# Output will be in steam_build/
```

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

#### SNES-Style System ⭐ NEW!
- **Authentic 16-bit**: True SNES resolution (256×224) and color depth (15-bit RGB)
- **Pixel-Perfect Sprites**: 16×16 character sprites in classic JRPG style
- **Tile-Based Maps**: Overworld and dungeon exploration with scrolling camera
- **Side-View Battles**: Classic FF4-6 style battle screens
- **Classic UI**: Dark blue windows, yellow cursor, color-coded HP bars
- **Complete Scenes**: Title screen, menus, dialogue boxes, status windows

**Benefits:**
- Authentic golden-age JRPG aesthetic
- Optimized for retro feel
- Instant nostalgia for SNES RPG fans
- Inspired by FF6, Chrono Trigger, Secret of Mana

See [docs/SNES_GRAPHICS.md](docs/SNES_GRAPHICS.md) for complete documentation.

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

## 📚 Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** ⭐ NEW! - Linux setup and Steam publishing
- **[SNES Graphics System](docs/SNES_GRAPHICS.md)** - Authentic 16-bit JRPG visuals
- **[Modern Graphics System](docs/GRAPHICS_SYSTEM.md)** - Complete procedural graphics documentation
- **[Development Guide](docs/DEVELOPMENT.md)** - For developers and modders
- **[Game Design Document](COIN_OPERATED%20JRPG.md)** - Complete design specification


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
