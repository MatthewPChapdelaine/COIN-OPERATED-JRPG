#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Asset Generation Automation
Automatically generates placeholder graphics assets for development.
"""

import sys
from pathlib import Path
from typing import Tuple

# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))


def ensure_pil():
    """Ensure PIL/Pillow is available."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        return True
    except ImportError:
        print("❌ Pillow not installed")
        print("   Install: pip install Pillow")
        return False


def create_sprite(size: Tuple[int, int], color: Tuple[int, int, int], 
                 label: str, output_path: Path):
    """Create a simple placeholder sprite."""
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGBA', size, color + (255,))
    draw = ImageDraw.Draw(img)
    
    # Add border
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=(0, 0, 0, 255), width=2)
    
    # Add label
    try:
        # Try to use a better font if available
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    draw.text((text_x, text_y), label, fill=(0, 0, 0, 255), font=font)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    print(f"✅ Created: {output_path}")


def create_character_sprites(assets_dir: Path):
    """Create character sprite placeholders."""
    print("\n📦 Creating Character Sprites...")
    
    characters = [
        ("hero", (100, 200, 255)),  # Blue
        ("mage", (200, 100, 255)),  # Purple
        ("warrior", (255, 100, 100)),  # Red
        ("ranger", (100, 255, 100)),  # Green
        ("cleric", (255, 255, 200)),  # Light yellow
    ]
    
    for name, color in characters:
        create_sprite(
            (32, 32),
            color,
            name[0].upper(),
            assets_dir / 'sprites' / 'characters' / f'{name}.png'
        )


def create_enemy_sprites(assets_dir: Path):
    """Create enemy sprite placeholders."""
    print("\n👾 Creating Enemy Sprites...")
    
    enemies = [
        ("slime", (100, 255, 100)),  # Green
        ("goblin", (150, 100, 50)),  # Brown
        ("skeleton", (200, 200, 200)),  # Gray
        ("dragon", (255, 50, 50)),  # Red
        ("demon", (100, 0, 100)),  # Dark purple
        ("ghost", (150, 150, 255)),  # Light blue
        ("orc", (100, 150, 80)),  # Olive
        ("zombie", (120, 140, 100)),  # Gray-green
    ]
    
    for name, color in enemies:
        create_sprite(
            (48, 48),
            color,
            name[0].upper(),
            assets_dir / 'sprites' / 'enemies' / f'{name}.png'
        )


def create_npc_sprites(assets_dir: Path):
    """Create NPC sprite placeholders."""
    print("\n💬 Creating NPC Sprites...")
    
    npcs = [
        ("merchant", (200, 150, 50)),  # Gold
        ("guard", (100, 100, 150)),  # Blue-gray
        ("villager", (150, 120, 100)),  # Tan
        ("blacksmith", (80, 80, 80)),  # Dark gray
        ("innkeeper", (180, 140, 120)),  # Light brown
    ]
    
    for name, color in npcs:
        create_sprite(
            (32, 32),
            color,
            name[0].upper(),
            assets_dir / 'sprites' / 'npcs' / f'{name}.png'
        )


def create_item_icons(assets_dir: Path):
    """Create item icon placeholders."""
    print("\n🎒 Creating Item Icons...")
    
    items = [
        ("potion", (255, 100, 100)),  # Red
        ("sword", (192, 192, 192)),  # Silver
        ("shield", (100, 150, 200)),  # Blue
        ("armor", (150, 150, 100)),  # Bronze
        ("key", (255, 215, 0)),  # Gold
        ("scroll", (255, 250, 200)),  # Parchment
        ("coin", (255, 215, 0)),  # Gold
        ("gem", (100, 200, 255)),  # Blue
    ]
    
    for name, color in items:
        create_sprite(
            (24, 24),
            color,
            name[0].upper(),
            assets_dir / 'items' / f'{name}.png'
        )


def create_tileset(assets_dir: Path):
    """Create basic tileset placeholders."""
    print("\n🗺️  Creating Tileset...")
    
    tiles = [
        ("grass", (100, 200, 100)),
        ("stone", (150, 150, 150)),
        ("water", (100, 150, 255)),
        ("dirt", (150, 100, 50)),
        ("sand", (230, 220, 170)),
        ("wall", (100, 80, 70)),
        ("floor", (180, 160, 140)),
        ("door", (120, 80, 40)),
    ]
    
    for name, color in tiles:
        create_sprite(
            (32, 32),
            color,
            name[0].upper(),
            assets_dir / 'tilesets' / f'{name}.png'
        )


def create_ui_elements(assets_dir: Path):
    """Create UI element placeholders."""
    print("\n🎨 Creating UI Elements...")
    
    # Button
    create_sprite(
        (120, 40),
        (100, 150, 200),
        "BUTTON",
        assets_dir / 'ui' / 'button.png'
    )
    
    # Panel
    create_sprite(
        (200, 150),
        (50, 50, 50),
        "PANEL",
        assets_dir / 'ui' / 'panel.png'
    )
    
    # Health bar
    create_sprite(
        (100, 10),
        (255, 0, 0),
        "",
        assets_dir / 'ui' / 'health_bar.png'
    )
    
    # Mana bar
    create_sprite(
        (100, 10),
        (0, 100, 255),
        "",
        assets_dir / 'ui' / 'mana_bar.png'
    )
    
    # Dialog box
    create_sprite(
        (400, 100),
        (240, 240, 240),
        "DIALOG",
        assets_dir / 'ui' / 'dialog_box.png'
    )


def create_effects(assets_dir: Path):
    """Create effect sprite placeholders."""
    print("\n✨ Creating Effect Sprites...")
    
    effects = [
        ("explosion", (255, 150, 0)),
        ("magic", (200, 100, 255)),
        ("heal", (100, 255, 100)),
        ("poison", (150, 255, 100)),
        ("fire", (255, 100, 0)),
        ("ice", (100, 200, 255)),
        ("lightning", (255, 255, 100)),
    ]
    
    for name, color in effects:
        create_sprite(
            (64, 64),
            color,
            name[0].upper(),
            assets_dir / 'effects' / f'{name}.png'
        )


def create_snes_palette_reference(assets_dir: Path):
    """Create SNES palette reference image."""
    from PIL import Image, ImageDraw
    
    print("\n🎮 Creating SNES Palette Reference...")
    
    # Import SNES palette
    try:
        from graphics.snes_palette import SNESPalette
        palette = SNESPalette()
        
        # Create palette grid
        colors_per_row = 8
        swatch_size = 40
        
        all_colors = []
        for category in ['background', 'ui', 'character', 'enemy', 'effect']:
            colors = palette.get_palette(category)
            all_colors.extend(colors)
        
        rows = (len(all_colors) + colors_per_row - 1) // colors_per_row
        
        img = Image.new('RGB', 
                       (colors_per_row * swatch_size, rows * swatch_size),
                       (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        for i, color in enumerate(all_colors):
            row = i // colors_per_row
            col = i % colors_per_row
            x = col * swatch_size
            y = row * swatch_size
            
            draw.rectangle(
                [x, y, x + swatch_size - 1, y + swatch_size - 1],
                fill=color,
                outline=(0, 0, 0)
            )
        
        output_path = assets_dir / 'palettes' / 'snes_palette.png'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print(f"✅ Created: {output_path}")
        
    except Exception as e:
        print(f"⚠️  Could not create SNES palette: {e}")


def generate_asset_manifest(assets_dir: Path):
    """Generate a manifest of all created assets."""
    import json
    
    print("\n📋 Generating Asset Manifest...")
    
    manifest = {
        "version": "1.0",
        "generated": True,
        "assets": {
            "characters": [],
            "enemies": [],
            "npcs": [],
            "items": [],
            "tiles": [],
            "ui": [],
            "effects": []
        }
    }
    
    # Scan directories
    for category in manifest["assets"]:
        if category == "tiles":
            search_dir = assets_dir / 'tilesets'
        else:
            search_dir = assets_dir / category if category != 'items' else assets_dir / 'items'
        
        if search_dir.exists():
            for asset_file in search_dir.glob('*.png'):
                manifest["assets"][category].append({
                    "name": asset_file.stem,
                    "path": str(asset_file.relative_to(assets_dir)),
                    "size": asset_file.stat().st_size
                })
    
    manifest_path = assets_dir / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Created: {manifest_path}")


def print_summary(assets_dir: Path):
    """Print summary of generated assets."""
    print("\n" + "=" * 60)
    print("Asset Generation Summary".center(60))
    print("=" * 60)
    
    total_files = 0
    total_size = 0
    
    for asset_file in assets_dir.rglob('*.png'):
        total_files += 1
        total_size += asset_file.stat().st_size
    
    print(f"\nTotal Assets: {total_files}")
    print(f"Total Size: {total_size / 1024:.2f} KB")
    print(f"\nAssets Location: {assets_dir}")
    
    print("\n📁 Directory Structure:")
    for directory in sorted(assets_dir.rglob('*')):
        if directory.is_dir():
            level = len(directory.relative_to(assets_dir).parts)
            indent = "  " * level
            count = len(list(directory.glob('*.png')))
            if count > 0:
                print(f"{indent}📂 {directory.name}/ ({count} files)")
    
    print("\n" + "=" * 60)


def main():
    """Run asset generation."""
    print("\n" + "=" * 60)
    print("COIN-OPERATED JRPG - Asset Generation".center(60))
    print("=" * 60)
    
    if not ensure_pil():
        return 1
    
    # Get project root and assets directory
    project_root = Path(__file__).parent
    assets_dir = project_root / 'assets'
    
    print(f"\nGenerating assets in: {assets_dir}")
    
    # Create all asset types
    try:
        create_character_sprites(assets_dir)
        create_enemy_sprites(assets_dir)
        create_npc_sprites(assets_dir)
        create_item_icons(assets_dir)
        create_tileset(assets_dir)
        create_ui_elements(assets_dir)
        create_effects(assets_dir)
        create_snes_palette_reference(assets_dir)
        generate_asset_manifest(assets_dir)
        
        print_summary(assets_dir)
        
        print("\n✅ Asset generation complete!")
        print("\nNext steps:")
        print("  1. Review generated assets in assets/ directory")
        print("  2. Replace placeholders with actual artwork")
        print("  3. Run: python3 demo_graphics.py to see them in action")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during asset generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
