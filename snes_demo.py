#!/usr/bin/env python3
"""
SNES JRPG Demo - Showcase the authentic 16-bit JRPG visual system
Generates sample scenes, battles, menus, and maps in SNES style
"""

import sys
import os

# Add python-core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

from graphics import (
    SNESPalette,
    SNESSpriteGenerator,
    SNESMapRenderer,
    SNESBattleScreen,
    SNESUI,
    SNESGameRenderer
)


def main():
    """Generate SNES-style JRPG demo"""
    print("=" * 70)
    print("  COIN:OPERATED JRPG - SNES-Style Visual System Demo")
    print("  Authentic 16-bit JRPG Graphics (256x224 resolution)")
    print("=" * 70)
    print()
    
    # Create output directory
    output_dir = "snes_demo_output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}\n")
    
    try:
        # Initialize renderer
        print("[1/6] Initializing SNES renderer...")
        renderer = SNESGameRenderer()
        
        # Generate character sprites
        print("[2/6] Generating character sprites...")
        sprite_gen = SNESSpriteGenerator(sprite_size=16)
        
        characters = {
            'coin': sprite_gen.generate_coin_sprite(),
            'jinn_lir': sprite_gen.generate_jinn_lir_sprite(),
            'coireena': sprite_gen.generate_warrior_sprite(),
            'orbius': sprite_gen.generate_mage_sprite('white'),
            'selene': sprite_gen.generate_mage_sprite('purple'),
        }
        
        for name, sprite in characters.items():
            sprite_gen.save_sprite(sprite, f'{name}.png', output_dir)
        print(f"  ✓ Saved {len(characters)} character sprites")
        
        # Generate enemy sprites
        print("[3/6] Generating enemy sprites...")
        enemies = ['slime', 'shadow', 'soldier']
        for enemy_type in enemies:
            enemy_sprite = sprite_gen.generate_enemy_sprite(enemy_type)
            sprite_gen.save_sprite(enemy_sprite, f'enemy_{enemy_type}.png', output_dir)
        print(f"  ✓ Saved {len(enemies)} enemy types")
        
        # Generate maps
        print("[4/6] Generating tile-based maps...")
        map_renderer = SNESMapRenderer(tile_size=16)
        
        # Overworld
        overworld = map_renderer.create_simple_overworld(16, 16)
        map_renderer.save_map(overworld, 'overworld_map.png', output_dir)
        
        # Dungeon
        dungeon = map_renderer.create_dungeon_room(12, 10)
        map_renderer.save_map(dungeon, 'dungeon_room.png', output_dir)
        
        print("  ✓ Saved overworld and dungeon maps")
        
        # Generate battle screen
        print("[5/6] Generating battle screen...")
        battle = SNESBattleScreen()
        battle_scene = battle.create_full_battle_scene()
        battle.save_battle_screen(battle_scene, 'battle_scene.png', output_dir)
        print("  ✓ Saved battle screen (256x224)")
        
        # Generate UI elements
        print("[6/6] Generating UI elements...")
        ui = SNESUI()
        
        # Title screen
        title = ui.create_title_screen("COIN:OPERATED")
        ui.save_ui_element(title, 'title_screen.png', output_dir)
        
        # Dialogue box
        dialogue = ui.create_dialogue_box(240, 64, "Coin")
        ui.save_ui_element(dialogue, 'dialogue_box.png', output_dir)
        
        # Main menu
        main_menu = ui.create_main_menu(120, 140)
        ui.save_ui_element(main_menu, 'main_menu.png', output_dir)
        
        # Status window
        status = ui.create_status_window("Coin", 12, 85, 100, 30, 50)
        ui.save_ui_element(status, 'status_window.png', output_dir)
        
        # Save slot
        save_slot = ui.create_save_slot_display(1, "Coin", "Acadmium City", "12:34:56", 12)
        ui.save_ui_element(save_slot, 'save_slot.png', output_dir)
        
        print("  ✓ Saved 5 UI elements")
        
        # Generate complete demo scenes using main renderer
        print("\n[BONUS] Generating complete game scenes...")
        renderer.create_demo_scenes(output_dir)
        
        print("\n" + "=" * 70)
        print("✓ SNES-Style Demo Complete!")
        print("=" * 70)
        print(f"\nGenerated Assets:")
        print(f"  • 5 Character sprites (16x16 pixels)")
        print(f"  • 3 Enemy types")
        print(f"  • 2 Maps (overworld & dungeon)")
        print(f"  • 1 Battle screen (256x224, SNES resolution)")
        print(f"  • 5 UI elements (menus, windows, bars)")
        print(f"  • 4 Complete game scenes")
        print(f"\nAll files saved to: {output_dir}/")
        print(f"\nFeatures:")
        print(f"  • Authentic 16-bit color palette (15-bit RGB)")
        print(f"  • SNES resolution (256x224)")
        print(f"  • Pixel-perfect sprites")
        print(f"  • Tile-based maps")
        print(f"  • Classic JRPG UI")
        print(f"  • Side-view battle system")
        print(f"\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
