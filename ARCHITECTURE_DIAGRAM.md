# Graphics System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COIN-OPERATED JRPG                               │
│                     Graphics System Architecture                         │
└─────────────────────────────────────────────────────────────────────────┘

                        ┌────────────────────────┐
                        │   User Launches Game   │
                        │  python3 launch_game.py│
                        └───────────┬────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
         ┌──────────▼──────┐  ┌────▼─────┐  ┌─────▼────────┐
         │   Text Mode     │  │ Graphics │  │  SNES Mode   │
         │   (Terminal)    │  │   Mode   │  │  (Retro)     │
         │                 │  │ (Modern) │  │              │
         │ No graphics     │  │ 800x600  │  │ 256x224 (3x) │
         │ dependencies    │  │          │  │              │
         └──────────┬──────┘  └────┬─────┘  └─────┬────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
┌───────────────────────────────────▼──────────────────────────────────────┐
│                        INTERFACE LAYER                                    │
│  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────────────┐ │
│  │ GameStateInterface│  │GameCommandInterface│  │ GameEventInterface   │ │
│  │                   │  │                    │  │                      │ │
│  │ get_party_members │  │ player_move()      │  │ on_combat_started()  │ │
│  │ get_location()    │  │ interact_npc()     │  │ on_damage_dealt()    │ │
│  │ get_encounter()   │  │ save_game()        │  │ on_quest_completed() │ │
│  └──────────────────┘  └───────────────────┘  └──────────────────────┘ │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │ Implemented by
┌───────────────────────────────────▼──────────────────────────────────────┐
│                        GRAPHICS ADAPTER                                   │
│                                                                           │
│  • Implements GameStateInterface (reads game state)                      │
│  • Implements GameCommandInterface (sends commands)                      │
│  • Manages GameEventInterface listeners (notifies events)                │
│  • Converts game objects ↔ dictionaries                                  │
│  • Routes all commands to appropriate systems                            │
│  • Single bridge between graphics and game logic                         │
│                                                                           │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │ Accesses
┌───────────────────────────────────▼──────────────────────────────────────┐
│                          GAME ENGINE                                      │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                        Core Game Logic                              │ │
│  │  • GameEngine - Main loop and state                                │ │
│  │  • Character - Stats, abilities, progression                       │ │
│  │  • Combat - Battle system                                          │ │
│  │  • Dialogue - NPC conversations                                    │ │
│  │  • Quest - Quest tracking                                          │ │
│  │  • Save - Save/load system                                         │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                        Game Content                                 │ │
│  │  • act1_content.py - Act 1 quests & story                         │ │
│  │  • act2_content.py - Act 2 quests & story                         │ │
│  │  • act3_content.py - Act 3 quests & story                         │ │
│  │  • act4_content.py - Act 4 endings                                │ │
│  │  • enemies.py - All enemy definitions                             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                       KEY ARCHITECTURE RULES                              │
│                                                                           │
│  ✅ DO:                                   ❌ DON'T:                       │
│  • Graphics imports from interfaces.py   • Graphics import from core/    │
│  • Adapter accesses game engine          • Graphics import from systems/ │
│  • Use interface methods only            • Graphics import from content/ │
│  • Load assets by ID from game logic     • Hardcode game data           │
│  • Convert objects to dicts              • Access objects directly       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW EXAMPLE                                 │
│                                                                           │
│  Player Presses Arrow Key:                                               │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 1. Pygame captures key event                                     │   │
│  │ 2. Renderer calls adapter.player_move('up')                      │   │
│  │ 3. Adapter routes to engine.handle_movement('up')                │   │
│  │ 4. Engine updates player position                                │   │
│  │ 5. Renderer calls adapter.get_player_location()                  │   │
│  │ 6. Adapter returns location as dictionary                        │   │
│  │ 7. Renderer displays new position                                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  Combat Damage Event:                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 1. Engine executes attack                                        │   │
│  │ 2. Adapter calls listener.on_damage_dealt(50, 'enemy_1')         │   │
│  │ 3. Renderer receives event notification                          │   │
│  │ 4. Renderer displays "50 damage!" message                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                      SAVE FILE COMPATIBILITY                              │
│                                                                           │
│            ┌──────────┐                                                  │
│            │ Save File│                                                  │
│            │ (JSON)   │                                                  │
│            └────┬─────┘                                                  │
│                 │                                                         │
│       ┌─────────┼─────────┐                                             │
│       │         │         │                                             │
│   ┌───▼───┐ ┌──▼───┐ ┌──▼────┐                                        │
│   │ Text  │ │Graph-│ │ SNES  │                                        │
│   │ Mode  │ │ ics  │ │ Mode  │                                        │
│   └───────┘ └──────┘ └───────┘                                        │
│                                                                           │
│  Same save format works in all modes!                                    │
│  Save in one mode, load in another.                                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                       AUTOMATED VALIDATION                                │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ Every Git Push:                                                  │   │
│  │                                                                   │   │
│  │  1. GitHub Actions triggers                                      │   │
│  │  2. Run validate_interfaces.py                                   │   │
│  │     → Check: Graphics only imports from interfaces               │   │
│  │  3. Run validate_no_redundancy.py                                │   │
│  │     → Check: No duplicate game data                              │   │
│  │  4. Run validate_save_files.py                                   │   │
│  │     → Check: Save format compatibility                           │   │
│  │  5. Run validate_feature_parity.py                               │   │
│  │     → Check: All modes have same features                        │   │
│  │                                                                   │   │
│  │  ✅ All pass → Merge allowed                                     │   │
│  │  ❌ Any fail → Block merge, show violation                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         FILE ORGANIZATION                                 │
│                                                                           │
│  python-core/                                                            │
│  ├── interfaces.py          ← Interface definitions                     │
│  ├── main.py                ← Text mode entry point                     │
│  ├── core/                  ← Game engine & systems                     │
│  │   ├── game_engine.py                                                 │
│  │   └── character.py                                                   │
│  ├── systems/               ← Game mechanics                            │
│  │   ├── combat.py                                                      │
│  │   ├── dialogue.py                                                    │
│  │   └── quest.py                                                       │
│  ├── content/               ← All game data                             │
│  │   ├── act1_content.py                                                │
│  │   ├── act2_content.py                                                │
│  │   ├── act3_content.py                                                │
│  │   ├── act4_content.py                                                │
│  │   └── enemies.py                                                     │
│  └── graphics/              ← Graphics renderers                        │
│      ├── adapter.py         ← Interface implementation                  │
│      ├── pygame_renderer.py ← Modern graphics                           │
│      ├── snes_pygame_renderer.py ← Retro graphics                       │
│      ├── snes_renderer.py   ← SNES graphics generator                   │
│      └── [other SNES files]                                             │
│                                                                           │
│  Root level:                                                             │
│  ├── launch_game.py         ← Unified launcher (all modes)              │
│  ├── play.py                ← Direct text mode launcher                 │
│  ├── play_graphics.py       ← Direct graphics launcher                  │
│  ├── automation/            ← Validation scripts                        │
│  └── docs/                  ← Documentation                             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

```
