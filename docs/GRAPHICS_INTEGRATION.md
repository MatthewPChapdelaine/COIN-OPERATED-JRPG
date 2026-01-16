# Graphics System Implementation Guide

## Overview

The COIN-OPERATED JRPG now supports **dual-mode gameplay**:
- **Text Mode** (original) - Terminal-based interactive fiction
- **Graphics Mode** (new) - Pygame-based visual renderer

Both modes use **identical game logic** with zero data duplication.

## Architecture

### Key Principle: Interface-Based Separation

```
┌─────────────────────────────────────────────────────────┐
│                    Graphics Layer                        │
│  (python-core/graphics/)                                │
│  - pygame_renderer.py   - Main renderer                 │
│  - adapter.py           - Interface implementation       │
│  - asset_manager.py     - Asset loading                 │
│  - SNES renderers       - Retro graphics                │
└────────────────┬────────────────────────────────────────┘
                 │ Uses ONLY interfaces
                 ↓
┌─────────────────────────────────────────────────────────┐
│              Interfaces (interfaces.py)                  │
│  - GameStateInterface   - Read game state               │
│  - GameCommandInterface - Send commands                 │
│  - GameEventInterface   - Receive events                │
└────────────────┬────────────────────────────────────────┘
                 │ Implemented by adapter
                 ↓
┌─────────────────────────────────────────────────────────┐
│                    Game Logic                           │
│  (python-core/core/, systems/, content/)                │
│  - Game engine, combat, quests, dialogue               │
│  - Character stats, progression                         │
│  - All game data and rules                             │
└─────────────────────────────────────────────────────────┘
```

## File Structure

```
python-core/
├── interfaces.py              # Interface definitions (bridge layer)
├── graphics/
│   ├── adapter.py            # Implements interfaces
│   ├── pygame_renderer.py    # Main pygame renderer
│   ├── asset_manager.py      # Asset loading by ID
│   └── [SNES renderers]      # Retro graphics system
├── core/
│   ├── game_engine.py        # Core game loop
│   └── character.py          # Character system
├── systems/
│   ├── combat.py             # Battle system
│   ├── dialogue.py           # Dialogue system
│   └── quest.py              # Quest system
└── content/
    ├── act1_content.py       # Story content
    └── enemies.py            # Enemy definitions
```

## How It Works

### 1. Interface Layer (interfaces.py)

Three interfaces define ALL communication:

**GameStateInterface** - Graphics reads game state (read-only)
```python
def get_party_members() -> List[Dict[str, Any]]
def get_current_encounter() -> Optional[Dict[str, Any]]
def get_player_location() -> Dict[str, Any]
```

**GameCommandInterface** - Graphics sends commands
```python
def player_move(direction: str) -> None
def execute_combat_action(action_id: str, target_id: str) -> None
def interact_with_npc(npc_id: str) -> None
```

**GameEventInterface** - Graphics receives events
```python
def on_combat_started(encounter_data: Dict) -> None
def on_damage_dealt(amount: int, target_id: str) -> None
def on_quest_completed(quest_id: str) -> None
```

### 2. Adapter (graphics/adapter.py)

**GraphicsAdapter** implements both GameStateInterface and GameCommandInterface.

- **Wraps game engine** - `self.engine = game_engine`
- **Converts objects to dicts** - Graphics never sees game objects directly
- **Routes commands** - Calls appropriate game systems
- **Manages events** - Notifies registered listeners

Example:
```python
def get_party_members(self) -> List[Dict[str, Any]]:
    # Read from game engine, convert to dict
    party_data = []
    if self.engine.player:
        party_data.append(self._character_to_dict(self.engine.player))
    return party_data

def player_move(self, direction: str) -> None:
    # Send command to game engine
    if hasattr(self.engine, 'handle_movement'):
        self.engine.handle_movement(direction)
```

### 3. Pygame Renderer (graphics/pygame_renderer.py)

**PygameRenderer** implements GameEventInterface.

- **Receives adapter** - Constructor takes `adapter: GameStateInterface`
- **Reads state** - Calls adapter methods to get game state
- **Renders visuals** - Converts state to pygame graphics
- **Handles input** - Converts pygame events to commands via adapter
- **Receives events** - Implements event callbacks

Example:
```python
def _render(self):
    # Get state via interface
    encounter = self.adapter.get_current_encounter()
    
    if encounter:
        self._render_combat(encounter)
    else:
        self._render_overworld()

def _handle_keypress(self, key: int):
    # Send command via interface
    if key == pygame.K_UP:
        self.adapter.player_move('up')
```

## Running the Game

### Text Mode (Original)
```bash
python3 play.py
```

### Graphics Mode (New)
```bash
python3 play_graphics.py
```

### Controls (Graphics Mode)
- **Arrow Keys** - Move character
- **Space** - Interact with NPCs
- **I** - Open inventory
- **S** - Save game
- **ESC** - Quit

## Development Guidelines

### ✅ DO

1. **Graphics reads via interface**
   ```python
   party = self.adapter.get_party_members()
   location = self.adapter.get_player_location()
   ```

2. **Graphics sends commands via interface**
   ```python
   self.adapter.player_move('up')
   self.adapter.execute_combat_action('attack', enemy_id)
   ```

3. **Load assets by ID from game logic**
   ```python
   sprite = asset_manager.get_sprite(character['name'])
   ```

### ❌ DON'T

1. **Never import game logic in graphics**
   ```python
   # ❌ FORBIDDEN
   from core.game_engine import GameEngine
   from systems.combat import CombatSystem
   from content.enemies import ENEMIES
   ```

2. **Never hardcode game data in graphics**
   ```python
   # ❌ FORBIDDEN
   ENEMIES = {'goblin': {...}}  # In graphics layer
   ```

3. **Never access game objects directly**
   ```python
   # ❌ FORBIDDEN
   hp = self.engine.player.stats.current_hp
   
   # ✅ CORRECT
   party = self.adapter.get_party_members()
   hp = party[0]['current_hp']
   ```

## Validation

### Automated Checks

Run validation scripts:
```bash
python3 automation/validate_interfaces.py
python3 automation/validate_no_redundancy.py
```

### CI/CD Integration

GitHub Actions automatically validates:
- Interface compliance (no forbidden imports)
- No data duplication
- Save file compatibility
- Feature parity between modes

## Adding New Features

### Example: Add New Combat Action

1. **Define in game logic** (systems/combat.py)
   ```python
   def special_attack(self, target):
       # Implementation
   ```

2. **Expose via interface** (adapter.py)
   ```python
   def execute_combat_action(self, action_id: str, target_id: str):
       if action_id == 'special_attack':
           self.engine.combat_system.special_attack(target_id)
   ```

3. **Render in graphics** (pygame_renderer.py)
   ```python
   def _render_combat_menu(self):
       actions = self.adapter.get_available_actions()
       if 'special_attack' in actions:
           # Show in menu
   ```

## Benefits

### ✅ Zero Data Duplication
- Game data lives in ONE place (content/)
- Graphics reads via interface
- Save files work in both modes

### ✅ Easy Testing
- Test game logic without graphics
- Test graphics with mock adapter
- CI/CD catches violations automatically

### ✅ Flexible Rendering
- Swap renderers easily (pygame → others)
- Multiple graphics modes (2D, SNES-style, 3D)
- Text mode always available as fallback

### ✅ Clean Architecture
- Clear separation of concerns
- No circular dependencies
- Easy to understand and maintain

## Troubleshooting

### Graphics won't start
```bash
# Install pygame
pip install pygame

# Check for errors
python3 play_graphics.py
```

### Interface violations
```bash
# Run validator
python3 automation/validate_interfaces.py

# Check for forbidden imports in graphics/
grep -r "from core import" python-core/graphics/
grep -r "from systems import" python-core/graphics/
```

### Asset loading issues
- Ensure assets are in `assets/` directory
- Use IDs from game logic, not hardcoded paths
- Check asset_manager.py cache

## Next Steps

1. **Enhance graphics**
   - Add sprite animations
   - Improve battle screen
   - Create map system

2. **Add more events**
   - Status effects
   - Cutscenes
   - Particle effects

3. **Optimize rendering**
   - Sprite caching
   - Dirty rect updates
   - Background loading

## References

- [interfaces.py](python-core/interfaces.py) - Interface definitions
- [adapter.py](python-core/graphics/adapter.py) - Implementation
- [pygame_renderer.py](python-core/graphics/pygame_renderer.py) - Renderer
- [AUDIT_REPORT.md](../AUDIT_REPORT.md) - Validation results
