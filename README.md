# COIN:OPERATED JRPG

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Game Status: Playable](https://img.shields.io/badge/status-playable-green.svg)]()

**A narrative-driven JRPG set in the Orbspace universe**

Follow Coin's journey from sentient magical artifact to Time Goddess in this turn-based RPG featuring deep storytelling, strategic combat, and meaningful player choices across multiple story acts and endings.

---

## 🎮 Quick Start

### Play the Game

```bash
# Clone the repository
git clone https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG.git
cd COIN-OPERATED-JRPG

# Run the game
python3 play.py
```

### Run Tests

```bash
python3 src/tests/test_game.py
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
- Python 3.8 or higher
- No external dependencies (uses standard library only)
- ~50MB disk space

### Supported Platforms
- Linux
- macOS
- Windows
- Any system with Python 3.8+

### Performance
- Text-based interface for maximum compatibility
- Minimal system requirements
- Save files are compact JSON format

---

## 📚 Documentation

- **[Development Guide](docs/DEVELOPMENT.md)** - For developers and modders
- **[Game Design Document](COIN_OPERATED%20JRPG.md)** - Complete design specification
- **[API Documentation](#)** - Code documentation (in progress)

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
