#!/usr/bin/env python3
"""
COIN-OPERATED JRPG - Graphics Mode Launcher
Launch the game with pygame graphics renderer.
"""

import sys
from pathlib import Path

# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))

from core.game_engine import GameEngine, GameState
from core.character import Character
from graphics.adapter import GraphicsAdapter
from graphics.pygame_renderer import PygameRenderer


def main():
    """Launch game in graphics mode."""
    print("🎮 COIN-OPERATED JRPG - Graphics Mode")
    print("=" * 50)
    
    # Initialize game engine
    print("Initializing game engine...")
    engine = GameEngine()
    engine.initialize()
    
    # Create a test player for demonstration
    print("Creating player character...")
    from core.character import Character, CharacterRole, CharacterFaction
    player = Character("Ava", CharacterRole.MAGIC_DPS, CharacterFaction.INDEPENDENT)
    engine.player = player
    engine.state = GameState.IN_GAME
    
    # Create adapter (bridge between graphics and game logic)
    print("Connecting graphics adapter...")
    adapter = GraphicsAdapter(engine)
    
    # Create and configure renderer
    print("Initializing pygame renderer...")
    renderer = PygameRenderer(adapter, width=800, height=600)
    
    # Register renderer as event listener
    adapter.register_event_listener(renderer)
    
    # Start graphics loop
    print("Starting graphics mode...")
    print("\nControls:")
    print("  Arrow Keys - Move")
    print("  Space - Interact")
    print("  I - Inventory")
    print("  S - Save")
    print("  ESC - Quit")
    print("=" * 50)
    
    try:
        renderer.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nThanks for playing!")


if __name__ == "__main__":
    main()
