"""
Environment Generator - Procedurally generates environment tiles and backgrounds
"""

from PIL import Image, ImageDraw
import random
import math
from .color_palette import ColorPalette


class EnvironmentGenerator:
    """Generates environment tiles and backgrounds"""
    
    def __init__(self, tile_size: int = 32):
        self.tile_size = tile_size
        self.palette = ColorPalette
    
    def generate_grass_tile(self, variation: int = 0) -> Image:
        """Generate grass tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base grass color
        base_color = self.palette.get('grass')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Add grass blades
        random.seed(variation)
        for _ in range(8):
            x = random.randint(2, self.tile_size - 3)
            y = random.randint(2, self.tile_size - 3)
            blade_color = self.palette.lighten(base_color, random.uniform(0.1, 0.3))
            draw.line([x, y, x, y - 3], fill=blade_color, width=1)
        
        return img
    
    def generate_dirt_tile(self, variation: int = 0) -> Image:
        """Generate dirt tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base dirt color
        base_color = self.palette.get('dirt')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Add texture
        random.seed(variation)
        for _ in range(12):
            x = random.randint(0, self.tile_size)
            y = random.randint(0, self.tile_size)
            size = random.randint(1, 2)
            shade = random.choice([
                self.palette.darken(base_color, 0.2),
                self.palette.lighten(base_color, 0.1)
            ])
            draw.ellipse([x, y, x + size, y + size], fill=shade)
        
        return img
    
    def generate_stone_tile(self, variation: int = 0) -> Image:
        """Generate stone tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base stone color
        base_color = self.palette.get('stone')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Add stone cracks and details
        random.seed(variation)
        crack_color = self.palette.darken(base_color, 0.3)
        for _ in range(3):
            x1 = random.randint(0, self.tile_size)
            y1 = random.randint(0, self.tile_size)
            x2 = x1 + random.randint(-8, 8)
            y2 = y1 + random.randint(-8, 8)
            draw.line([x1, y1, x2, y2], fill=crack_color, width=1)
        
        return img
    
    def generate_water_tile(self, frame: int = 0) -> Image:
        """Generate animated water tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base water color
        base_color = self.palette.get('water')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Animated waves
        for y in range(0, self.tile_size, 4):
            wave_offset = int(math.sin((y + frame) * 0.3) * 2)
            wave_color = self.palette.lighten(base_color, 0.2)
            draw.line([0, y + wave_offset, self.tile_size, y + wave_offset], fill=wave_color, width=1)
        
        return img
    
    def generate_wood_tile(self) -> Image:
        """Generate wood floor tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base wood color
        base_color = self.palette.get('wood')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Wood grain
        grain_color = self.palette.darken(base_color, 0.15)
        for y in range(0, self.tile_size, 3):
            draw.line([0, y, self.tile_size, y], fill=grain_color, width=1)
        
        # Plank separators
        separator_color = self.palette.darken(base_color, 0.3)
        draw.line([0, self.tile_size // 2, self.tile_size, self.tile_size // 2], 
                 fill=separator_color, width=2)
        
        return img
    
    def generate_metal_tile(self) -> Image:
        """Generate metal floor tile"""
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base metal color
        base_color = self.palette.get('metal')
        draw.rectangle([0, 0, self.tile_size, self.tile_size], fill=base_color)
        
        # Metal panel lines
        line_color = self.palette.darken(base_color, 0.3)
        draw.rectangle([0, 0, self.tile_size - 1, self.tile_size - 1], outline=line_color, width=1)
        draw.line([self.tile_size // 2, 0, self.tile_size // 2, self.tile_size], 
                 fill=line_color, width=1)
        
        # Rivets
        rivet_color = self.palette.darken(base_color, 0.2)
        for x, y in [(4, 4), (self.tile_size - 4, 4), (4, self.tile_size - 4), (self.tile_size - 4, self.tile_size - 4)]:
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=rivet_color, outline=line_color)
        
        return img
    
    def generate_wall(self, wall_type: str, width: int = None, height: int = None) -> Image:
        """Generate wall segment"""
        if width is None:
            width = self.tile_size
        if height is None:
            height = self.tile_size * 2
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if wall_type == 'stone':
            base_color = self.palette.get('stone')
            draw.rectangle([0, 0, width - 1, height - 1], fill=base_color, outline=self.palette.darken(base_color, 0.3))
            
            # Stone blocks
            block_color = self.palette.darken(base_color, 0.2)
            for y in range(0, height, self.tile_size):
                draw.line([0, y, width, y], fill=block_color, width=1)
            
        elif wall_type == 'wood':
            base_color = self.palette.get('wood')
            draw.rectangle([0, 0, width - 1, height - 1], fill=base_color)
            
            # Wooden planks
            plank_color = self.palette.darken(base_color, 0.3)
            for x in range(0, width, self.tile_size // 2):
                draw.line([x, 0, x, height], fill=plank_color, width=2)
        
        elif wall_type == 'metal':
            base_color = self.palette.get('metal')
            draw.rectangle([0, 0, width - 1, height - 1], fill=base_color)
            
            # Metal panels
            panel_color = self.palette.darken(base_color, 0.3)
            for y in range(0, height, self.tile_size):
                draw.rectangle([2, y + 2, width - 3, y + self.tile_size - 3], 
                              outline=panel_color, width=1)
        
        return img
    
    def generate_tree(self, size: str = 'medium') -> Image:
        """Generate tree sprite"""
        if size == 'small':
            width, height = 32, 48
            trunk_height = 12
            canopy_radius = 12
        elif size == 'large':
            width, height = 64, 96
            trunk_height = 24
            canopy_radius = 24
        else:  # medium
            width, height = 48, 72
            trunk_height = 18
            canopy_radius = 18
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x = width // 2
        
        # Trunk
        trunk_color = self.palette.get('wood')
        trunk_width = width // 6
        draw.rectangle([center_x - trunk_width, height - trunk_height, 
                       center_x + trunk_width, height],
                      fill=trunk_color, outline=self.palette.darken(trunk_color, 0.3))
        
        # Canopy (multiple layers for depth)
        canopy_color = self.palette.get('grass')
        canopy_y = height - trunk_height - canopy_radius
        
        # Back layer
        draw.ellipse([center_x - canopy_radius, canopy_y - canopy_radius,
                     center_x + canopy_radius, canopy_y + canopy_radius],
                    fill=self.palette.darken(canopy_color, 0.2))
        
        # Middle layer
        draw.ellipse([center_x - canopy_radius * 0.8, canopy_y - canopy_radius * 0.8,
                     center_x + canopy_radius * 0.8, canopy_y + canopy_radius * 0.8],
                    fill=canopy_color)
        
        # Front layer (highlights)
        draw.ellipse([center_x - canopy_radius * 0.5, canopy_y - canopy_radius * 0.5,
                     center_x + canopy_radius * 0.5, canopy_y + canopy_radius * 0.5],
                    fill=self.palette.lighten(canopy_color, 0.2))
        
        return img
    
    def generate_rock(self, size: str = 'medium') -> Image:
        """Generate rock/boulder sprite"""
        if size == 'small':
            width, height = 24, 20
        elif size == 'large':
            width, height = 48, 40
        else:  # medium
            width, height = 32, 28
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rock shape (irregular polygon)
        rock_color = self.palette.get('stone')
        center_x, center_y = width // 2, height // 2
        
        points = []
        num_points = 8
        for i in range(num_points):
            angle = (360 / num_points) * i
            rad = math.radians(angle)
            radius = min(width, height) // 2 * random.uniform(0.7, 1.0)
            x = center_x + int(math.cos(rad) * radius)
            y = center_y + int(math.sin(rad) * radius * 0.8)
            points.append((x, y))
        
        draw.polygon(points, fill=rock_color, outline=self.palette.darken(rock_color, 0.4))
        
        # Shading
        shade_color = self.palette.darken(rock_color, 0.2)
        draw.polygon([(p[0], p[1] + 2) for p in points[:len(points)//2]], fill=shade_color)
        
        return img
    
    def generate_background(self, width: int, height: int, bg_type: str) -> Image:
        """Generate background scene"""
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if bg_type == 'sky':
            # Gradient sky
            for y in range(height):
                ratio = y / height
                color = self.palette.lerp_color(
                    self.palette.get('magic_time'),
                    self.palette.get('white'),
                    ratio
                )
                draw.line([0, y, width, y], fill=color)
        
        elif bg_type == 'night':
            # Night sky
            base_color = (10, 10, 30)
            draw.rectangle([0, 0, width, height], fill=base_color)
            
            # Stars
            random.seed(42)
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height // 2)
                brightness = random.randint(150, 255)
                draw.point([x, y], fill=(brightness, brightness, brightness))
        
        elif bg_type == 'cave':
            # Dark cave
            base_color = (20, 15, 25)
            draw.rectangle([0, 0, width, height], fill=base_color)
            
            # Cave walls (rough edges)
            wall_color = self.palette.get('stone')
            for x in range(0, width, 20):
                offset = random.randint(-10, 10)
                draw.line([x, 0, x + 10, offset + 20], fill=wall_color, width=5)
        
        elif bg_type == 'forest':
            # Forest background
            # Sky
            sky_color = self.palette.lighten(self.palette.get('grass'), 0.5)
            draw.rectangle([0, 0, width, height // 3], fill=sky_color)
            
            # Trees in background (darker, smaller)
            bg_tree_color = self.palette.darken(self.palette.get('grass'), 0.3)
            for x in range(0, width, 40):
                tree_x = x + random.randint(-10, 10)
                tree_height = random.randint(30, 50)
                draw.ellipse([tree_x - 15, height // 3 - tree_height, 
                             tree_x + 15, height // 3],
                            fill=bg_tree_color)
            
            # Ground
            ground_color = self.palette.get('grass')
            draw.rectangle([0, height // 3, width, height], fill=ground_color)
        
        elif bg_type == 'temple':
            # Temple interior
            base_color = (40, 35, 50)
            draw.rectangle([0, 0, width, height], fill=base_color)
            
            # Pillars
            pillar_color = self.palette.get('stone')
            for x in [width // 4, width * 3 // 4]:
                draw.rectangle([x - 20, 0, x + 20, height], 
                              fill=pillar_color,
                              outline=self.palette.darken(pillar_color, 0.3),
                              width=2)
        
        return img
    
    def generate_tileset(self, output_dir: str = "generated_tiles"):
        """Generate complete tileset"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        tiles = {
            'grass': self.generate_grass_tile(),
            'dirt': self.generate_dirt_tile(),
            'stone': self.generate_stone_tile(),
            'water': self.generate_water_tile(),
            'wood': self.generate_wood_tile(),
            'metal': self.generate_metal_tile(),
        }
        
        for name, tile in tiles.items():
            filepath = os.path.join(output_dir, f'{name}_tile.png')
            tile.save(filepath, 'PNG')
        
        # Generate props
        tree = self.generate_tree()
        tree.save(os.path.join(output_dir, 'tree.png'), 'PNG')
        
        rock = self.generate_rock()
        rock.save(os.path.join(output_dir, 'rock.png'), 'PNG')
        
        return output_dir
