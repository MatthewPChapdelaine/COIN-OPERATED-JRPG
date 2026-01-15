# COIN:OPERATED JRPG - Development Guide

## Project Structure

```
COIN-OPERATED-JRPG/
├── src/
│   ├── core/              # Core game engine and character systems
│   │   ├── game_engine.py
│   │   └── character.py
│   ├── systems/           # Game systems (combat, quests, etc.)
│   │   ├── combat.py
│   │   ├── progression.py
│   │   ├── quest.py
│   │   ├── dialogue.py
│   │   └── save_system.py
│   ├── content/           # Game content (quests, NPCs, enemies)
│   │   ├── act1_content.py
│   │   └── enemies.py
│   ├── tests/             # Test suites
│   │   └── test_game.py
│   └── main.py            # Main game entry point
├── assets/                # Game assets
│   ├── audio/
│   ├── graphics/
│   └── data/
├── docs/                  # Documentation
├── saves/                 # Save game files (auto-created)
└── play.py                # Quick start script
```

## Running the Game

### Option 1: Using the quick start script
```bash
python3 play.py
```

### Option 2: Running directly
```bash
python3 src/main.py
```

### Option 3: Running tests
```bash
python3 src/tests/test_game.py
```

## Game Systems Implemented

### ✓ Core Engine
- Game loop and state management
- Main menu system
- Game state transitions
- New Game and New Game+ support

### ✓ Character System
- Character stats and progression
- Ability system with unlocking
- Equipment slots
- Party management
- Multiple playable characters:
  - Coin (protagonist)
  - Jinn-Lir
  - Orbius
  - Typhus
  - Coireena

### ✓ Combat System
- Turn-based JRPG combat
- Turn order based on speed stat
- Physical and magical attacks
- Ability system with MP costs
- Damage calculations
- Boss battles
- Victory rewards (EXP, coins, essence)

### ✓ Progression System
- Character leveling and EXP
- Inventory management
- Equipment system with rarities (Common → Legendary)
- Faction reputation system
- Ability unlocking
- Currency: Domminnian Coins and Magical Essence

### ✓ Quest System
- Multiple quest types (Main Story, Side Quest, Faction Quest)
- Quest objectives with progress tracking
- Quest rewards
- Dynamic quest availability based on level and reputation

### ✓ Dialogue System
- Branching dialogue trees
- Dialogue choices with consequences
- NPC interaction system
- Story-driven conversations

### ✓ Save/Load System
- Multiple save slots (10 slots)
- Auto-save functionality
- Save file metadata
- Save import/export

### ✓ Content - Act 1
- 5 main story quests
- 2 side quests
- 1 faction quest
- 6 NPCs with dialogue
- 3 major dialogue sequences
- Multiple enemy types
- Boss battle (Manifestation of Rage)

## Development Status

### Completed Components
✅ Core game engine
✅ Character system
✅ Combat system
✅ Progression (inventory, equipment, faction)
✅ Quest system
✅ Dialogue system
✅ Save/load system
✅ Act 1 content
✅ Enemy factory and encounters
✅ Basic UI/menu systems

### In Progress
🔄 Act 2-4 content generation
🔄 Time travel mechanics
🔄 Endgame content and superbosses

### Planned
📋 Acts 2-4 complete storylines
📋 All 5 ending paths
📋 Time travel quest chains
📋 Optional superbosses
📋 Complete faction quest lines
📋 Enhanced UI/graphics (optional)
📋 Audio system (optional)

## How to Add New Content

### Adding a New Quest
```python
quest = Quest(
    quest_id="unique_id",
    name="Quest Name",
    description="Quest description",
    quest_type=QuestType.SIDE_QUEST,
    quest_giver="NPC Name",
    level_requirement=5
)

quest.add_objective(QuestObjective(
    "Objective description",
    "objective_type",  # defeat, collect, talk, explore
    "target_name",
    required=3
))

quest.set_rewards(exp=100, coins=50, essence=25)
quest_manager.register_quest(quest)
```

### Adding a New Enemy
```python
def create_new_enemy(level: int = 1) -> Enemy:
    enemy = Enemy(
        name="Enemy Name",
        level=level,
        description="Enemy description",
        faction=CharacterFaction.DRIFT_EMPIRE,
        enemy_type="normal"  # normal, elite, boss
    )
    
    # Customize stats
    enemy.stats.strength += level * 2
    
    # Add abilities
    enemy.add_ability(Ability(
        "Attack Name",
        "Description",
        mp_cost=10,
        power=25,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    return enemy
```

### Adding a New NPC
```python
npc = NPC(
    npc_id="unique_id",
    name="NPC Name",
    description="NPC description",
    location="location_id",
    faction="faction_name"
)

npc.add_dialogue("dialogue_id")
npc.add_quest("quest_id")
npc_manager.register_npc(npc)
```

### Adding Dialogue
```python
dialogue = Dialogue("dialogue_id", "Title", "start_node")

dialogue.add_node(DialogueNode(
    "start_node",
    "Speaker Name",
    "Dialogue text",
    choices=[
        DialogueChoice("Choice 1", next_node="node_1"),
        DialogueChoice("Choice 2", next_node="node_2")
    ]
))

dialogue_system.register_dialogue(dialogue)
```

## Testing

The test suite (`src/tests/test_game.py`) validates:
- Character creation and progression
- Combat mechanics
- Inventory and equipment
- Faction reputation
- Quest objectives
- Enemy generation

Run tests to ensure all systems work correctly after changes.

## Game Balance Guidelines

### Character Progression
- Starting level: 1
- Act 1 end level: ~5-7
- Act 2 end level: ~12-15
- Act 3 end level: ~20-25
- Max level: 50 (Act 4 + endgame)

### Currency
- Domminnian Coins: Primary currency for items/equipment
- Magical Essence: Special currency for ability unlocks
- Act 1 enemy drops: 10-50 coins, 5-25 essence per battle

### Equipment Rarities
- Common: +5-10 stat boost
- Rare: +15-25 stat boost
- Epic: +30-50 stat boost
- Legendary: +60+ stat boost

### Faction Reputation Thresholds
- Hostile: -100 to -50
- Unfriendly: -50 to 0
- Neutral: 0 to 50
- Friendly: 50 to 100
- Honored: 100 to 200
- Revered: 200 to 300
- Exalted: 300+

## Design Philosophy

Following the prompt engineering document:
1. **Narrative-driven**: Story and character development drive gameplay
2. **Player choice matters**: Faction reputation and decisions affect outcomes
3. **Progression is meaningful**: Multiple advancement paths (abilities, equipment, reputation)
4. **Strategic combat**: Turn-based combat requires planning and resource management
5. **Replayability**: Multiple endings and faction paths encourage replays

## Contributing

When adding new content:
1. Follow the existing code structure
2. Use the prompt templates from the design document
3. Maintain character voice consistency
4. Test new content with the test suite
5. Update this documentation

## Known Issues / Future Improvements

- Add graphical UI (currently text-based)
- Implement audio system
- Add more random encounters
- Create Acts 2-4 complete content
- Implement time travel mechanics fully
- Add more equipment variety
- Create all 5 ending paths
- Implement superboss encounters
- Add achievement system
- Implement trading/shop system

## Credits

**Game Design**: Based on comprehensive prompt engineering document
**Universe**: Orbspace - A Universe Beyond the Universe
**Developer**: Loporian Industries / Matt's Lair Brand
**Engine**: Custom Python JRPG Engine
**Inspired by**: Maximum Computer Design Game Template
