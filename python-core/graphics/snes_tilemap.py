"""
SNES Tilemap System - Tile-based map rendering for overworld and dungeons
Classic JRPG style map system like Final Fantasy and Chrono Trigger
"""

from PIL import Image, ImageDraw
from .snes_palette import SNESPalette
import random


class SNESTileGenerator:
    """Generates individual SNES-style tiles"""
    
    def __init__(self, tile_size: int = 16):
        """
        Initialize tile generator
        SNES used 8x8 or 16x16 tiles
        """
        self.tile_size = tile_size
        self.palette = SNESPalette
    
    def generate_grass_tile(self, variant: int = 0) -> Image:
        """Generate grass tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        grass = self.palette.get('grass')
        grass_dark = self.palette.get('grass_dark')
        grass_light = self.palette.get('grass_light')
        
        # Fill base
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=grass)
        
        # Add grass detail (SNES-style dithering pattern)
        random.seed(variant)
        for y in range(0, self.tile_size, 2):
            for x in range(0, self.tile_size, 2):
                if random.random() < 0.3:
                    draw.point((x, y), fill=grass_dark)
                elif random.random() < 0.2:
                    draw.point((x, y), fill=grass_light)
        
        return img
    
    def generate_water_tile(self, frame: int = 0) -> Image:
        """Generate animated water tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        water = self.palette.get('water')
        water_light = self.palette.get('water_light')
        
        # Fill base
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=water)
        
        # Animated wave pattern (SNES-style)
        offset = frame % 4
        for y in range(0, self.tile_size, 4):
            wave_y = (y + offset) % self.tile_size
            for x in range(0, self.tile_size, 2):
                if (x + offset) % 4 == 0:
                    draw.point((x, wave_y), fill=water_light)
        
        return img
    
    def generate_dirt_tile(self, variant: int = 0) -> Image:
        """Generate dirt/path tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        dirt = self.palette.get('dirt')
        dirt_dark = self.palette.darken(dirt, 0.2)
        dirt_light = self.palette.lighten(dirt, 0.15)
        
        # Fill base
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=dirt)
        
        # Add texture (SNES-style sparse pixels)
        random.seed(variant)
        for i in range(8):
            x = random.randint(0, self.tile_size - 1)
            y = random.randint(0, self.tile_size - 1)
            color = dirt_dark if random.random() < 0.6 else dirt_light
            draw.point((x, y), fill=color)
        
        return img
    
    def generate_stone_tile(self) -> Image:
        """Generate stone floor tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        stone = self.palette.get('stone')
        stone_dark = self.palette.get('stone_dark')
        
        # Tiled stone pattern
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=stone)
        
        # Stone tile lines
        draw.line([0, 0, self.tile_size, 0], fill=stone_dark)
        draw.line([0, 0, 0, self.tile_size], fill=stone_dark)
        draw.line([self.tile_size // 2, 0, self.tile_size // 2, self.tile_size], fill=stone_dark)
        draw.line([0, self.tile_size // 2, self.tile_size, self.tile_size // 2], fill=stone_dark)
        
        return img
    
    def generate_wall_tile(self, wall_type: str = 'stone') -> Image:
        """Generate wall tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if wall_type == 'stone':
            base = self.palette.get('stone')
            dark = self.palette.get('stone_dark')
        else:
            base = self.palette.get('wood')
            dark = self.palette.darken(base, 0.3)
        
        # Fill base
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base)
        
        # Add brick pattern
        mid_y = self.tile_size // 2
        draw.line([0, mid_y, self.tile_size, mid_y], fill=dark)
        draw.line([self.tile_size // 2, 0, self.tile_size // 2, mid_y], fill=dark)
        draw.line([0, mid_y, 0, self.tile_size], fill=dark)
        
        return img
    
    def generate_tree_tile(self) -> Image:
        """Generate tree tile for overworld - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Transparent background (tree sits on grass)
        
        # Tree trunk
        trunk = self.palette.get('wood_dark')
        trunk_x = self.tile_size // 2
        for y in range(self.tile_size // 2, self.tile_size):
            draw.point((trunk_x - 1, y), fill=trunk)
            draw.point((trunk_x, y), fill=trunk)
        
        # Tree leaves (simple cloud shape)
        leaves = self.palette.get('grass_dark')
        leaves_light = self.palette.get('grass')
        
        # Top part
        for y in range(2, self.tile_size // 2 + 2):
            width = 4 - abs(y - 5)
            for x in range(trunk_x - width, trunk_x + width):
                if y < 5:
                    draw.point((x, y), fill=leaves_light)
                else:
                    draw.point((x, y), fill=leaves)
        
        return img
    
    def generate_mountain_tile(self) -> Image:
        """Generate mountain/rock tile - SNES style"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        rock = self.palette.get('stone')
        rock_dark = self.palette.get('stone_dark')
        rock_light = self.palette.lighten(rock, 0.2)
        
        # Mountain shape (triangular)
        for y in range(self.tile_size):
            width = (self.tile_size - y) // 2
            for x in range(self.tile_size // 2 - width, self.tile_size // 2 + width):
                if x < self.tile_size // 2 and y < self.tile_size // 2:
                    draw.point((x, y), fill=rock_light)
                elif x >= self.tile_size // 2 or y >= self.tile_size * 2 // 3:
                    draw.point((x, y), fill=rock_dark)
                else:
                    draw.point((x, y), fill=rock)
        
        return img


class SNESMapRenderer:
    """Renders SNES-style tile-based maps"""
    
    def __init__(self, tile_size: int = 16):
        self.tile_size = tile_size
        self.tile_gen = SNESTileGenerator(tile_size)
        self.tile_cache = {}
    
    def get_tile(self, tile_type: str, variant: int = 0) -> Image:
        """Get cached tile or generate new one"""
        cache_key = f"{tile_type}_{variant}"
        
        if cache_key not in self.tile_cache:
            if tile_type == 'grass':
                self.tile_cache[cache_key] = self.tile_gen.generate_grass_tile(variant)
            elif tile_type == 'water':
                self.tile_cache[cache_key] = self.tile_gen.generate_water_tile(variant)
            elif tile_type == 'dirt':
                self.tile_cache[cache_key] = self.tile_gen.generate_dirt_tile(variant)
            elif tile_type == 'stone':
                self.tile_cache[cache_key] = self.tile_gen.generate_stone_tile()
            elif tile_type == 'wall':
                self.tile_cache[cache_key] = self.tile_gen.generate_wall_tile()
            elif tile_type == 'tree':
                self.tile_cache[cache_key] = self.tile_gen.generate_tree_tile()
            elif tile_type == 'mountain':
                self.tile_cache[cache_key] = self.tile_gen.generate_mountain_tile()
            else:
                # Default grass
                self.tile_cache[cache_key] = self.tile_gen.generate_grass_tile(0)
        
        return self.tile_cache[cache_key]
    
    def render_map(self, map_data: list, width: int, height: int) -> Image:
        """
        Render a complete map from tile data
        
        map_data: 2D array of tile types
        Example: [['grass', 'grass', 'water'], ['dirt', 'stone', 'water'], ...]
        """
        img_width = width * self.tile_size
        img_height = height * self.tile_size
        
        img = Image.new('RGB', (img_width, img_height), (0, 0, 0))
        
        for y in range(height):
            for x in range(width):
                if y < len(map_data) and x < len(map_data[y]):
                    tile_type = map_data[y][x]
                    tile = self.get_tile(tile_type, variant=(x + y) % 3)
                    
                    paste_x = x * self.tile_size
                    paste_y = y * self.tile_size
                    
                    if tile.mode == 'RGBA':
                        img.paste(tile, (paste_x, paste_y), tile)
                    else:
                        img.paste(tile, (paste_x, paste_y))
        
        return img
    
    def create_simple_overworld(self, width: int = 16, height: int = 16) -> Image:
        """Create a simple SNES-style overworld map"""
        # Generate simple map with grass, water, trees
        map_data = []
        
        for y in range(height):
            row = []
            for x in range(width):
                # Create a simple pattern
                if y < 3 or y > height - 3 or x < 3 or x > width - 3:
                    # Border: water
                    row.append('water')
                elif (x + y) % 7 == 0:
                    # Scattered trees
                    row.append('tree')
                elif x == width // 2 and y > 5 and y < height - 5:
                    # Path down the middle
                    row.append('dirt')
                else:
                    # Grass
                    row.append('grass')
            map_data.append(row)
        
        return self.render_map(map_data, width, height)
    
    def create_dungeon_room(self, width: int = 12, height: int = 10) -> Image:
        """Create a simple SNES-style dungeon room"""
        map_data = []
        
        for y in range(height):
            row = []
            for x in range(width):
                # Walls around edges
                if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                    row.append('wall')
                else:
                    row.append('stone')
            map_data.append(row)
        
        # Add door openings
        map_data[height // 2][0] = 'stone'  # Left door
        map_data[height // 2][width - 1] = 'stone'  # Right door
        
        return self.render_map(map_data, width, height)
    
    def save_map(self, map_img: Image, filename: str, directory: str = "snes_maps"):
        """Save map to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        # Scale up 2x for better visibility
        scaled = map_img.resize((map_img.width * 2, map_img.height * 2), Image.NEAREST)
        scaled.save(filepath, 'PNG')
        return filepath
