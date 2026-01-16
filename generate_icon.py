#!/usr/bin/env python3
"""
Generate game icon for Steam and desktop launchers.
Creates a simple but appealing icon for the Coin-Operated JRPG.
"""

from PIL import Image, ImageDraw
import os

def create_game_icon():
    """Create game icon in multiple sizes for different platforms."""
    
    # Create output directory
    os.makedirs("assets/icons", exist_ok=True)
    
    # Define icon sizes needed
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    for size in sizes:
        # Create image with transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # SNES-style color palette
        gold = (255, 215, 0, 255)  # Coin color
        dark_gold = (218, 165, 32, 255)  # Shadow
        blue = (41, 128, 185, 255)  # Background accent
        white = (255, 255, 255, 255)
        
        # Draw background circle (blue)
        padding = size // 8
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill=blue,
            outline=dark_gold,
            width=max(1, size // 32)
        )
        
        # Draw coin (centered circle)
        coin_padding = size // 4
        draw.ellipse(
            [coin_padding, coin_padding, size - coin_padding, size - coin_padding],
            fill=gold,
            outline=dark_gold,
            width=max(1, size // 16)
        )
        
        # Draw coin detail (inner circle)
        detail_padding = size // 3
        draw.ellipse(
            [detail_padding, detail_padding, size - detail_padding, size - detail_padding],
            fill=None,
            outline=dark_gold,
            width=max(1, size // 24)
        )
        
        # Draw cross/star pattern in center
        center = size // 2
        star_size = size // 8
        # Horizontal line
        draw.line(
            [center - star_size, center, center + star_size, center],
            fill=dark_gold,
            width=max(1, size // 32)
        )
        # Vertical line
        draw.line(
            [center, center - star_size, center, center + star_size],
            fill=dark_gold,
            width=max(1, size // 32)
        )
        
        # Save icon
        img.save(f"assets/icons/icon_{size}.png", 'PNG')
        print(f"Created icon: icon_{size}.png")
    
    # Create combined ICO file for Windows
    images = [Image.open(f"assets/icons/icon_{s}.png") for s in [16, 32, 48, 256]]
    images[0].save(
        "assets/icons/game.ico",
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (256, 256)]
    )
    print("Created Windows ICO file: game.ico")
    
    # Use 512 size as the main icon for Steam
    Image.open("assets/icons/icon_512.png").save("assets/icons/steam_icon.png")
    print("Created Steam icon: steam_icon.png")
    
    print("\n✓ All icons generated successfully!")
    print("Icons are available in: assets/icons/")

if __name__ == "__main__":
    create_game_icon()
