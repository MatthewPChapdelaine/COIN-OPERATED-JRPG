#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Graphics Demo Mode
Demonstrates all graphics features with automated showcase.
"""

import sys
import time
from pathlib import Path

# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))


class DemoGameEngine:
    """Mock game engine for demonstration purposes."""
    
    def __init__(self):
        self.state = 'in_game'
        self.current_location = MockLocation()
        self.player = MockCharacter("Coin", 100, 100, 50, 50)
        self.party = [
            MockCharacter("Jinn Lir", 120, 120, 40, 40),
            MockCharacter("Coireena", 150, 150, 30, 30)
        ]
        self.combat_system = None
        self.message_log = []
        self.demo_phase = 0
        self.frame_count = 0
    
    def update_demo(self):
        """Update demo state for showcase."""
        self.frame_count += 1
        
        # Cycle through different demo phases
        if self.frame_count % 300 == 0:  # Every 5 seconds
            self.demo_phase = (self.demo_phase + 1) % 4
            
            if self.demo_phase == 0:
                # Overworld exploration
                self.state = 'in_game'
                self.combat_system = None
                self.message_log = ["Exploring the world..."]
                
            elif self.demo_phase == 1:
                # Show party stats
                self.message_log = ["Party Status: All members healthy"]
                
            elif self.demo_phase == 2:
                # Enter combat
                self.state = 'combat'
                self.combat_system = MockCombat()
                self.message_log = ["Battle started!"]
                
            elif self.demo_phase == 3:
                # Combat actions
                if self.combat_system:
                    self.combat_system.enemies[0].current_hp -= 20
                    self.message_log = ["20 damage dealt!"]


class MockLocation:
    """Mock location for demo."""
    name = "Demo Area"
    description = "A showcase of the graphics system"
    npcs = []
    x = 0
    y = 0


class MockCharacter:
    """Mock character for demo."""
    def __init__(self, name, max_hp, current_hp, max_mp, current_mp):
        self.name = name
        self.stats = MockStats(max_hp, current_hp, max_mp, current_mp)
        self.level = 10
        self.role = "Hero"
        self.faction = "Independent"


class MockStats:
    """Mock stats for demo."""
    def __init__(self, max_hp, current_hp, max_mp, current_mp):
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.max_mp = max_mp
        self.current_mp = current_mp


class MockCombat:
    """Mock combat for demo."""
    def __init__(self):
        self.turn = 0
        self.phase = 'player_turn'
        self.enemies = [
            MockEnemy("Shadow Beast", 80, 100),
            MockEnemy("Dark Mage", 60, 80)
        ]


class MockEnemy:
    """Mock enemy for demo."""
    def __init__(self, name, current_hp, max_hp):
        self.name = name
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.enemy_id = name.lower().replace(' ', '_')
        self.level = 8


def run_graphics_demo(mode='retro16'):
    """Run graphics demonstration.
    
    Args:
        mode: 'graphics' or 'retro16'
    """
    print("🎮 COIN-OPERATED JRPG - Graphics Demo")
    print("=" * 60)
    print(f"Mode: {mode.upper()}")
    print("\nThis demo showcases:")
    print("  • Overworld rendering")
    print("  • Party member display")
    print("  • Combat screen")
    print("  • HP/MP bars")
    print("  • Message system")
    print("  • Automatic transitions")
    print("\nPress ESC to exit")
    print("=" * 60)
    
    # Create demo engine
    from core.game_engine import GameState
    engine = DemoGameEngine()
    
    # Create adapter
    from graphics.adapter import GraphicsAdapter
    adapter = GraphicsAdapter(engine)
    
    # Create appropriate renderer
    if mode == 'retro16':
        print("\n📺 Initializing Retro16 renderer...")
        from graphics.snes_pygame_renderer import Retro16PygameRenderer
        renderer = Retro16PygameRenderer(adapter, scale=3)
    else:
        print("\n🖼️ Initializing graphics renderer...")
        from graphics.pygame_renderer import PygameRenderer
        renderer = PygameRenderer(adapter, width=800, height=600)
    
    adapter.register_event_listener(renderer)
    
    print("✅ Demo ready! Watch the automatic showcase...")
    print("\nThe demo will cycle through different game states:")
    print("  Phase 1: Overworld exploration")
    print("  Phase 2: Party status")
    print("  Phase 3: Combat initiated")
    print("  Phase 4: Combat actions")
    time.sleep(2)
    
    # Wrap renderer run to update demo state
    original_render = renderer._render
    
    def demo_render():
        engine.update_demo()
        original_render()
    
    renderer._render = demo_render
    
    try:
        renderer.run()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted")
    except Exception as e:
        print(f"\n\nDemo error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nDemo complete!")


def main():
    """Main demo entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="COIN-OPERATED JRPG Graphics Demo"
    )
    parser.add_argument(
        '--mode', '-m',
        choices=['graphics', 'retro16'],
        default='retro16',
        help='Graphics mode to demo (default: retro16)'
    )
    
    args = parser.parse_args()
    
    # Check for pygame
    try:
        import pygame
    except ImportError:
        print("⚠️  ERROR: pygame not installed")
        print("\nInstall with: pip install pygame")
        sys.exit(1)
    
    # Check for PIL if Retro16 mode
    if args.mode == 'retro16':
        try:
            import PIL
        except ImportError:
            print("⚠️  ERROR: Pillow not installed")
            print("\nInstall with: pip install Pillow")
            print("Or use: python3 demo_graphics.py --mode graphics")
            sys.exit(1)
    
    run_graphics_demo(args.mode)


if __name__ == "__main__":
    main()
