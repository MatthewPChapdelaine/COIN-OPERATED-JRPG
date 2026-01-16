#!/usr/bin/env python3
"""
COIN-OPERATED JRPG - Unified Graphics Launcher
Supports multiple rendering modes: Standard, Retro16-style, and Text.
"""

import sys
import argparse
from pathlib import Path

# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))


def launch_text_mode():
    """Launch original text-based mode."""
    print("🎮 COIN-OPERATED JRPG - Text Mode")
    print("=" * 50)
    from main import main
    main()


def launch_graphics_mode():
    """Launch standard pygame graphics mode."""
    print("🎮 COIN-OPERATED JRPG - Graphics Mode")
    print("=" * 50)
    
    try:
        from core.game_engine import GameEngine, GameState
        from core.character import Character, CharacterRole, CharacterFaction
        from graphics.adapter import GraphicsAdapter
        from graphics.pygame_renderer import PygameRenderer
        from config import get_config
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("\nMake sure you're running from the project root directory")
        sys.exit(1)
    
    # Load configuration
    config = get_config()
    
    # Initialize game engine
    print("Initializing game engine...")
    try:
        engine = GameEngine()
        engine.initialize()
    except Exception as e:
        print(f"⚠️  Failed to initialize game engine: {e}")
        sys.exit(1)
    
    # Create test player
    print("Creating player character...")
    player = Character("Ava", CharacterRole.MAGIC_DPS, CharacterFaction.INDEPENDENT)
    engine.player = player
    engine.state = GameState.IN_GAME
    
    # Create adapter
    print("Connecting graphics adapter...")
    adapter = GraphicsAdapter(engine)
    
    # Get resolution from config
    width, height = config.get_resolution()
    if config.get('graphics.mode') == 'graphics':
        width = config.get('graphics.resolution.width', 800)
        height = config.get('graphics.resolution.height', 600)
    
    # Create renderer
    print(f"Initializing pygame renderer ({width}x{height})...")
    try:
        renderer = PygameRenderer(adapter, width=width, height=height)
        adapter.register_event_listener(renderer)
    except Exception as e:
        print(f"⚠️  Failed to initialize renderer: {e}")
        sys.exit(1)
    
    print("\n🎮 Controls:")
    print("  Arrow Keys - Move")
    print("  Space - Interact")
    print("  I - Inventory")
    print("  S - Save")
    print("  ESC - Quit")
    print("=" * 50)
    
    try:
        renderer.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Save config on exit
        config.save()
        print("\nThanks for playing!")


def launch_retro16_mode():
    """Launch Retro16-style graphics mode."""
    print("🎮 COIN-OPERATED JRPG - Retro16 Mode")
    print("=" * 50)
    
    try:
        from core.game_engine import GameEngine, GameState
        from core.character import Character, CharacterRole, CharacterFaction
        from graphics.adapter import GraphicsAdapter
        from graphics.snes_pygame_renderer import Retro16PygameRenderer
        from config import get_config
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("\nMake sure you're running from the project root directory")
        sys.exit(1)
    
    # Load configuration
    config = get_config()
    
    # Initialize game engine
    print("Initializing game engine...")
    try:
        engine = GameEngine()
        engine.initialize()
    except Exception as e:
        print(f"⚠️  Failed to initialize game engine: {e}")
        sys.exit(1)
    
    # Create test player
    print("Creating player character...")
    player = Character("Coin", CharacterRole.MAGIC_DPS, CharacterFaction.INDEPENDENT)
    engine.player = player
    engine.state = GameState.IN_GAME
    
    # Create adapter
    print("Connecting graphics adapter...")
    adapter = GraphicsAdapter(engine)
    
    # Get scale from config
    scale = config.get('graphics.scale', 3)
    
    # Create Retro16 renderer
    print(f"Initializing Retro16 renderer (scale: {scale}x)...")
    print(f"📺 Resolution: 256x224 (16-bit standard) scaled to {256*scale}x{224*scale}")
    try:
        renderer = Retro16PygameRenderer(adapter, scale=scale)
        adapter.register_event_listener(renderer)
    except Exception as e:
        print(f"⚠️  Failed to initialize renderer: {e}")
        sys.exit(1)
    
    print("\n🎮 Controls:")
    print("  Arrow Keys - Move")
    print("  Space/Enter - Interact")
    print("  A - Attack (in combat)")
    print("  S - Save")
    print("  ESC - Quit")
    print("\n🎨 Authentic 16-bit retro graphics!")
    print("=" * 50)
    
    try:
        renderer.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Save config on exit
        config.save()
        print("\nThanks for playing!")


def main():
    """Main launcher with mode selection."""
    parser = argparse.ArgumentParser(
        description="COIN-OPERATED JRPG - Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Graphics Modes:
  text      Text-based interactive fiction (original)
  graphics  Standard pygame graphics renderer
  retro16   Authentic 16-bit retro graphics (default)

Examples:
  python3 launch.py                   # Retro16 mode (default)
  python3 launch.py --mode retro16    # Retro16 mode (explicit)
  python3 launch.py --mode graphics   # Standard graphics
  python3 launch.py --mode text       # Text mode
        """
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['text', 'graphics', 'retro16'],
        default='retro16',
        help='Graphics mode to use (default: retro16)'
    )
    
    parser.add_argument(
        '--list-modes', '-l',
        action='store_true',
        help='List all available graphics modes'
    )
    
    args = parser.parse_args()
    
    if args.list_modes:
        print("\n📺 Available Graphics Modes:\n")
        print("  text      - Text-based interactive fiction")
        print("              Original mode, terminal only")
        print("              No graphics dependencies required")
        print("")
        print("  graphics  - Standard pygame renderer")
        print("              800x600 resolution")
        print("              Modern 2D graphics")
        print("              Requires: pygame")
        print("")
        print("  retro16   - 16-bit retro graphics (default)")
        print("              256x224 resolution (scaled 3x)")
        print("              Authentic retro aesthetics")
        print("              Requires: pygame, Pillow")
        print("")
        return
    
    print("\n" + "=" * 50)
    print("COIN-OPERATED JRPG".center(50))
    print("A Time-Travel JRPG Adventure".center(50))
    print("=" * 50 + "\n")
    
    # Check for pygame if graphics mode selected
    if args.mode in ['graphics', 'retro16']:
        try:
            import pygame
        except ImportError:
            print("⚠️  ERROR: pygame not installed")
            print("\nInstall with: pip install pygame")
            print("\nOr run in text mode: python3 launch.py --mode text")
            sys.exit(1)
        
        if args.mode == 'retro16':
            try:
                import PIL
            except ImportError:
                print("⚠️  ERROR: Pillow not installed")
                print("\nInstall with: pip install Pillow")
                print("\nOr use standard graphics: python3 launch.py --mode graphics")
                sys.exit(1)
    
    # Launch selected mode
    if args.mode == 'text':
        launch_text_mode()
    elif args.mode == 'graphics':
        launch_graphics_mode()
    elif args.mode == 'retro16':
        launch_retro16_mode()


if __name__ == "__main__":
    main()
