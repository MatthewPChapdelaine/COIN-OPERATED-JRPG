#!/usr/bin/env python3
"""
COIN-OPERATED JRPG - Easy Launcher
Simple script to launch the game in graphics mode with all fixes applied
"""

import sys
import os

# Add python-core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

def main():
    """Launch the game in graphics mode"""
    try:
        import pygame
    except ImportError:
        print("=" * 60)
        print("ERROR: Pygame not installed!")
        print("=" * 60)
        print("\nTo install pygame, run:")
        print("  pip install pygame")
        print("\nOr try text mode instead:")
        print("  python3 play.py")
        print("=" * 60)
        sys.exit(1)
    
    print("=" * 60)
    print("         COIN-OPERATED JRPG")
    print("           Graphics Mode")
    print("=" * 60)
    print("\n🎮 Loading game...")
    
    try:
        from core.game_engine import GameEngine, GameState
        from core.character import Character, CharacterRole, CharacterFaction
        from graphics.adapter import GraphicsAdapter
        from graphics.pygame_renderer import PygameRenderer
        from config import get_config
    except ImportError as e:
        print(f"\n⚠️  Import error: {e}")
        print("\nMake sure you're running from the project root directory")
        sys.exit(1)
    
    # Load configuration
    config = get_config()
    
    # Initialize game engine
    print("✓ Initializing game engine...")
    try:
        engine = GameEngine()
        engine.initialize()
    except Exception as e:
        print(f"⚠️  Failed to initialize game engine: {e}")
        sys.exit(1)
    
    # Create player character
    print("✓ Creating player character...")
    player = Character("Coin", CharacterRole.MAGIC_DPS, CharacterFaction.INDEPENDENT)
    player.stats.max_hp = 100
    player.stats.current_hp = 100
    player.stats.max_mp = 50
    player.stats.current_mp = 50
    engine.player = player
    engine.state = GameState.IN_GAME
    
    # Create adapter
    print("✓ Connecting graphics adapter...")
    adapter = GraphicsAdapter(engine)
    
    # Get resolution from config
    width = config.get('graphics.resolution.width', 800)
    height = config.get('graphics.resolution.height', 600)
    
    # Create renderer
    print(f"✓ Initializing pygame renderer ({width}x{height})...")
    try:
        renderer = PygameRenderer(adapter, width=width, height=height)
        adapter.register_event_listener(renderer)
    except Exception as e:
        print(f"⚠️  Failed to initialize renderer: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎮 CONTROLS:")
    print("=" * 60)
    print("  ↑ ↓ ← → : Move around")
    print("  SPACE   : Interact")
    print("  I       : Inventory (coming soon)")
    print("  S       : Save")
    print("  ESC     : Quit")
    print("=" * 60)
    print("\n🎮 Starting game...\n")
    
    try:
        renderer.run()
    except KeyboardInterrupt:
        print("\n\n✋ Game interrupted by user")
    except Exception as e:
        print(f"\n\n⚠️  Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Save config on exit
        config.save()
        print("\n👋 Thanks for playing COIN-OPERATED JRPG!")
        print("=" * 60)


if __name__ == "__main__":
    main()
