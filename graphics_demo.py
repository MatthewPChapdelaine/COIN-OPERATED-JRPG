#!/usr/bin/env python3
"""
Graphics Demo - Showcases the procedural graphics generation system
Generates sample sprites, animations, effects, UI elements, and environments
"""

import os
import sys

# Add python-core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

from graphics import (
    SpriteGenerator,
    AnimationGenerator,
    UIGenerator,
    EffectGenerator,
    EnvironmentGenerator,
    ColorPalette
)


def create_output_directory(base_dir: str = "generated_graphics"):
    """Create output directory structure"""
    dirs = [
        base_dir,
        f"{base_dir}/sprites",
        f"{base_dir}/animations",
        f"{base_dir}/effects",
        f"{base_dir}/ui",
        f"{base_dir}/environment",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return base_dir


def demo_sprites(output_dir: str):
    """Generate character and enemy sprites"""
    print("Generating character sprites...")
    
    sprite_gen = SpriteGenerator()
    
    # Main characters
    characters = {
        'coin': sprite_gen.generate_coin_sprite(),
        'jinn_lir': sprite_gen.generate_jinn_lir_sprite(),
        'orbius': sprite_gen.generate_orbius_sprite(),
        'coireena': sprite_gen.generate_coireena_sprite(),
        'selene': sprite_gen.generate_selene_sprite(),
        'typhus': sprite_gen.generate_typhus_sprite(),
    }
    
    for name, sprite in characters.items():
        filepath = os.path.join(output_dir, 'sprites', f'{name}.png')
        sprite.save(filepath, 'PNG')
        print(f"  ✓ Saved {name}.png")
    
    # Enemies
    print("\nGenerating enemy sprites...")
    enemies = {
        'shadow_creature': sprite_gen.generate_enemy_sprite('shadow_creature'),
        'corrupted_coin': sprite_gen.generate_enemy_sprite('corrupted_coin'),
        'time_wraith': sprite_gen.generate_enemy_sprite('time_wraith'),
        'cabal_soldier': sprite_gen.generate_enemy_sprite('cabal_soldier'),
    }
    
    for name, sprite in enemies.items():
        filepath = os.path.join(output_dir, 'sprites', f'enemy_{name}.png')
        sprite.save(filepath, 'PNG')
        print(f"  ✓ Saved enemy_{name}.png")


def demo_animations(output_dir: str):
    """Generate character animations"""
    print("\nGenerating animations...")
    
    anim_gen = AnimationGenerator()
    sprite_gen = SpriteGenerator()
    
    # Generate animation for Coin
    coin_sprite = sprite_gen.generate_coin_sprite()
    
    animations = {
        'walk': anim_gen.generate_walk_animation(coin_sprite),
        'attack': anim_gen.generate_attack_animation(coin_sprite),
        'cast': anim_gen.generate_cast_animation(coin_sprite),
        'damage': anim_gen.generate_damage_animation(coin_sprite),
        'idle': anim_gen.generate_idle_animation(coin_sprite),
        'victory': anim_gen.generate_victory_animation(coin_sprite),
    }
    
    for anim_name, frames in animations.items():
        # Save individual frames
        for i, frame in enumerate(frames):
            filepath = os.path.join(output_dir, 'animations', f'coin_{anim_name}_frame_{i}.png')
            frame.save(filepath, 'PNG')
        
        # Create spritesheet
        spritesheet = anim_gen.create_spritesheet(frames, 4)
        filepath = os.path.join(output_dir, 'animations', f'coin_{anim_name}_spritesheet.png')
        spritesheet.save(filepath, 'PNG')
        print(f"  ✓ Saved coin_{anim_name} animation ({len(frames)} frames)")


def demo_effects(output_dir: str):
    """Generate magic and combat effects"""
    print("\nGenerating visual effects...")
    
    effect_gen = EffectGenerator()
    
    # Magic effects
    magic_types = ['time', 'fire', 'ice', 'lightning', 'healing', 'dark']
    
    for magic_type in magic_types:
        frames = effect_gen.generate_magic_effect(magic_type)
        
        # Save individual frames
        for i, frame in enumerate(frames):
            filepath = os.path.join(output_dir, 'effects', f'magic_{magic_type}_frame_{i}.png')
            frame.save(filepath, 'PNG')
        
        # Create spritesheet
        anim_gen = AnimationGenerator()
        spritesheet = anim_gen.create_spritesheet(frames, 4)
        filepath = os.path.join(output_dir, 'effects', f'magic_{magic_type}_spritesheet.png')
        spritesheet.save(filepath, 'PNG')
        print(f"  ✓ Saved {magic_type} magic effect ({len(frames)} frames)")
    
    # Combat effects
    print("\nGenerating combat effects...")
    slash = effect_gen.generate_slash_effect()
    filepath = os.path.join(output_dir, 'effects', 'slash_effect.png')
    slash.save(filepath, 'PNG')
    print(f"  ✓ Saved slash effect")
    
    impact = effect_gen.generate_impact_effect()
    filepath = os.path.join(output_dir, 'effects', 'impact_effect.png')
    impact.save(filepath, 'PNG')
    print(f"  ✓ Saved impact effect")


def demo_ui(output_dir: str):
    """Generate UI elements"""
    print("\nGenerating UI elements...")
    
    ui_gen = UIGenerator()
    
    # Buttons
    buttons = {
        'normal': ui_gen.generate_button(120, 40, "Normal", 'normal'),
        'primary': ui_gen.generate_button(120, 40, "Primary", 'primary'),
        'danger': ui_gen.generate_button(120, 40, "Danger", 'danger'),
        'success': ui_gen.generate_button(120, 40, "Success", 'success'),
    }
    
    for name, button in buttons.items():
        filepath = os.path.join(output_dir, 'ui', f'button_{name}.png')
        button.save(filepath, 'PNG')
    print(f"  ✓ Saved 4 button styles")
    
    # Windows
    window = ui_gen.generate_window(320, 200, "Game Menu")
    filepath = os.path.join(output_dir, 'ui', 'window.png')
    window.save(filepath, 'PNG')
    print(f"  ✓ Saved window")
    
    # Bars
    health_bar = ui_gen.generate_health_bar(200, 20, 75, 100)
    filepath = os.path.join(output_dir, 'ui', 'health_bar.png')
    health_bar.save(filepath, 'PNG')
    
    mana_bar = ui_gen.generate_mana_bar(200, 20, 50, 100)
    filepath = os.path.join(output_dir, 'ui', 'mana_bar.png')
    mana_bar.save(filepath, 'PNG')
    print(f"  ✓ Saved health and mana bars")
    
    # Icons
    icons = ['attack', 'magic', 'defense', 'item', 'coin']
    for icon_type in icons:
        icon = ui_gen.generate_icon(icon_type, 32)
        filepath = os.path.join(output_dir, 'ui', f'icon_{icon_type}.png')
        icon.save(filepath, 'PNG')
    print(f"  ✓ Saved {len(icons)} icons")
    
    # Menu panels
    panels = {
        'normal': ui_gen.generate_menu_panel(300, 200, 'normal'),
        'light_cabal': ui_gen.generate_menu_panel(300, 200, 'light_cabal'),
        'dark_cabal': ui_gen.generate_menu_panel(300, 200, 'dark_cabal'),
        'drift': ui_gen.generate_menu_panel(300, 200, 'drift'),
    }
    
    for name, panel in panels.items():
        filepath = os.path.join(output_dir, 'ui', f'panel_{name}.png')
        panel.save(filepath, 'PNG')
    print(f"  ✓ Saved 4 menu panel styles")
    
    # Dialogue box
    dialogue = ui_gen.generate_dialogue_box(600, 120, "Coin")
    filepath = os.path.join(output_dir, 'ui', 'dialogue_box.png')
    dialogue.save(filepath, 'PNG')
    print(f"  ✓ Saved dialogue box")


def demo_environment(output_dir: str):
    """Generate environment tiles and backgrounds"""
    print("\nGenerating environment tiles...")
    
    env_gen = EnvironmentGenerator(tile_size=32)
    
    # Ground tiles
    tiles = {
        'grass': env_gen.generate_grass_tile(),
        'dirt': env_gen.generate_dirt_tile(),
        'stone': env_gen.generate_stone_tile(),
        'water': env_gen.generate_water_tile(),
        'wood': env_gen.generate_wood_tile(),
        'metal': env_gen.generate_metal_tile(),
    }
    
    for name, tile in tiles.items():
        filepath = os.path.join(output_dir, 'environment', f'tile_{name}.png')
        tile.save(filepath, 'PNG')
    print(f"  ✓ Saved {len(tiles)} tile types")
    
    # Walls
    print("\nGenerating wall segments...")
    walls = {
        'stone': env_gen.generate_wall('stone', 64, 96),
        'wood': env_gen.generate_wall('wood', 64, 96),
        'metal': env_gen.generate_wall('metal', 64, 96),
    }
    
    for name, wall in walls.items():
        filepath = os.path.join(output_dir, 'environment', f'wall_{name}.png')
        wall.save(filepath, 'PNG')
    print(f"  ✓ Saved {len(walls)} wall types")
    
    # Props
    print("\nGenerating environment props...")
    tree_small = env_gen.generate_tree('small')
    tree_small.save(os.path.join(output_dir, 'environment', 'tree_small.png'), 'PNG')
    
    tree_medium = env_gen.generate_tree('medium')
    tree_medium.save(os.path.join(output_dir, 'environment', 'tree_medium.png'), 'PNG')
    
    tree_large = env_gen.generate_tree('large')
    tree_large.save(os.path.join(output_dir, 'environment', 'tree_large.png'), 'PNG')
    
    rock_small = env_gen.generate_rock('small')
    rock_small.save(os.path.join(output_dir, 'environment', 'rock_small.png'), 'PNG')
    
    rock_medium = env_gen.generate_rock('medium')
    rock_medium.save(os.path.join(output_dir, 'environment', 'rock_medium.png'), 'PNG')
    
    rock_large = env_gen.generate_rock('large')
    rock_large.save(os.path.join(output_dir, 'environment', 'rock_large.png'), 'PNG')
    
    print(f"  ✓ Saved trees and rocks (3 sizes each)")
    
    # Backgrounds
    print("\nGenerating background scenes...")
    backgrounds = ['sky', 'night', 'cave', 'forest', 'temple']
    
    for bg_type in backgrounds:
        bg = env_gen.generate_background(640, 480, bg_type)
        filepath = os.path.join(output_dir, 'environment', f'bg_{bg_type}.png')
        bg.save(filepath, 'PNG')
    print(f"  ✓ Saved {len(backgrounds)} background scenes")


def demo_color_palette(output_dir: str):
    """Generate color palette reference"""
    print("\nGenerating color palette reference...")
    
    from PIL import Image, ImageDraw
    
    palette = ColorPalette
    
    # Create palette image
    swatch_size = 40
    swatches_per_row = 8
    
    # Get all colors
    all_colors = {
        # Basic colors
        'white': palette.get('white'),
        'black': palette.get('black'),
        'red': palette.get('red'),
        'blue': palette.get('blue'),
        'green': palette.get('green'),
        'yellow': palette.get('yellow'),
        'purple': palette.get('purple'),
        'orange': palette.get('orange'),
        
        # Material colors
        'grass': palette.get('grass'),
        'dirt': palette.get('dirt'),
        'stone': palette.get('stone'),
        'water': palette.get('water'),
        'wood': palette.get('wood'),
        'metal': palette.get('metal'),
        
        # Magic colors
        'magic_time': palette.get('magic_time'),
        'magic_fire': palette.get('magic_fire'),
        'magic_ice': palette.get('magic_ice'),
        'magic_lightning': palette.get('magic_lightning'),
        'magic_healing': palette.get('magic_healing'),
        'magic_dark': palette.get('magic_dark'),
        
        # Character colors
        'coin_gold': palette.get('coin_gold'),
        'coin_silver': palette.get('coin_silver'),
        
        # UI colors
        'ui_background': palette.get('ui_background'),
        'ui_border': palette.get('ui_border'),
        'ui_text': palette.get('ui_text'),
        'ui_highlight': palette.get('ui_highlight'),
        'ui_danger': palette.get('ui_danger'),
        'ui_success': palette.get('ui_success'),
    }
    
    num_colors = len(all_colors)
    num_rows = (num_colors + swatches_per_row - 1) // swatches_per_row
    
    img_width = swatches_per_row * swatch_size
    img_height = num_rows * swatch_size
    
    img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    for i, (name, color) in enumerate(all_colors.items()):
        row = i // swatches_per_row
        col = i % swatches_per_row
        
        x = col * swatch_size
        y = row * swatch_size
        
        # Draw color swatch
        draw.rectangle([x, y, x + swatch_size - 2, y + swatch_size - 2], fill=color[:3], outline=(0, 0, 0))
    
    filepath = os.path.join(output_dir, 'color_palette.png')
    img.save(filepath, 'PNG')
    print(f"  ✓ Saved color palette reference ({num_colors} colors)")


def main():
    """Main demo function"""
    print("=" * 60)
    print("COIN:OPERATED JRPG - Procedural Graphics Demo")
    print("=" * 60)
    print("\nGenerating all graphics procedurally...")
    print()
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"Output directory: {output_dir}\n")
    
    # Generate all graphics
    try:
        demo_color_palette(output_dir)
        demo_sprites(output_dir)
        demo_animations(output_dir)
        demo_effects(output_dir)
        demo_ui(output_dir)
        demo_environment(output_dir)
        
        print("\n" + "=" * 60)
        print("✓ Graphics generation complete!")
        print("=" * 60)
        print(f"\nAll generated graphics saved to: {output_dir}")
        print("\nGenerated assets:")
        print("  • Character sprites (6 main characters)")
        print("  • Enemy sprites (4 types)")
        print("  • Character animations (6 types)")
        print("  • Magic effects (6 elements)")
        print("  • Combat effects (slash, impact)")
        print("  • UI elements (buttons, windows, bars, icons, panels)")
        print("  • Environment tiles (6 types)")
        print("  • Environment props (trees, rocks)")
        print("  • Background scenes (5 types)")
        print("  • Color palette reference")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
