"""
Sprite Generator - Procedurally generates character and object sprites
"""

from PIL import Image, ImageDraw
import math
from .color_palette import ColorPalette


class SpriteGenerator:
    """Generates pixel art sprites procedurally"""
    
    def __init__(self, pixel_size: int = 32):
        self.pixel_size = pixel_size
        self.palette = ColorPalette
    
    def create_character_sprite(self, character_type: str, facing: str = 'down') -> Image:
        """Generate a character sprite"""
        img = Image.new('RGBA', (self.pixel_size, self.pixel_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        palette = self.palette.character_palette(character_type)
        
        if character_type == 'coin':
            return self._generate_coin_sprite(img, draw, palette, facing)
        elif character_type == 'jinn_lir':
            return self._generate_wizard_sprite(img, draw, palette, facing)
        elif character_type == 'orbius':
            return self._generate_master_sprite(img, draw, palette, facing)
        elif character_type == 'coireena':
            return self._generate_warrior_sprite(img, draw, palette, facing)
        elif character_type == 'selene':
            return self._generate_dark_mage_sprite(img, draw, palette, facing)
        elif character_type == 'typhus':
            return self._generate_creature_sprite(img, draw, palette, facing)
        else:
            return self._generate_generic_sprite(img, draw, palette, facing)
    
    def _generate_coin_sprite(self, img, draw, palette, facing):
        """Generate Coin's sprite - magical being made of coins"""
        size = self.pixel_size
        
        # Body (coin-like circular form)
        center_x, center_y = size // 2, size // 2 + 4
        radius = size // 3
        
        # Draw golden body with coin texture
        draw.ellipse([center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius], 
                    fill=palette['primary'], outline=palette['outline'])
        
        # Coin details (ridges)
        for i in range(4):
            angle = i * (math.pi / 2)
            x1 = center_x + int(math.cos(angle) * radius * 0.7)
            y1 = center_y + int(math.sin(angle) * radius * 0.7)
            x2 = center_x + int(math.cos(angle) * radius * 0.9)
            y2 = center_y + int(math.sin(angle) * radius * 0.9)
            draw.line([x1, y1, x2, y2], fill=palette['secondary'], width=1)
        
        # Head (smaller coin)
        head_y = center_y - radius - 6
        head_radius = radius // 2
        draw.ellipse([center_x - head_radius, head_y - head_radius,
                     center_x + head_radius, head_y + head_radius],
                    fill=palette['primary'], outline=palette['outline'])
        
        # Eyes (based on facing direction)
        eye_y = head_y
        if facing == 'down' or facing == 'front':
            draw.rectangle([center_x - 3, eye_y - 1, center_x - 1, eye_y + 1], fill=palette['accent'])
            draw.rectangle([center_x + 1, eye_y - 1, center_x + 3, eye_y + 1], fill=palette['accent'])
        elif facing == 'up':
            draw.rectangle([center_x - 3, eye_y - 2, center_x - 1, eye_y], fill=palette['accent'])
            draw.rectangle([center_x + 1, eye_y - 2, center_x + 3, eye_y], fill=palette['accent'])
        elif facing == 'left':
            draw.rectangle([center_x - 3, eye_y - 1, center_x - 1, eye_y + 1], fill=palette['accent'])
        elif facing == 'right':
            draw.rectangle([center_x + 1, eye_y - 1, center_x + 3, eye_y + 1], fill=palette['accent'])
        
        # Magical aura
        aura_color = self.palette.with_alpha(palette['accent'], 100)
        draw.ellipse([center_x - radius - 2, center_y - radius - 2,
                     center_x + radius + 2, center_y + radius + 2],
                    outline=aura_color, width=1)
        
        # Arms (small coin extensions)
        arm_y = center_y
        draw.ellipse([center_x - radius - 4, arm_y - 3, center_x - radius, arm_y + 3],
                    fill=palette['secondary'], outline=palette['outline'])
        draw.ellipse([center_x + radius, arm_y - 3, center_x + radius + 4, arm_y + 3],
                    fill=palette['secondary'], outline=palette['outline'])
        
        return img
    
    def _generate_wizard_sprite(self, img, draw, palette, facing):
        """Generate wizard sprite (Jinn-Lir style)"""
        size = self.pixel_size
        center_x = size // 2
        
        # Robe
        robe_top = size // 3
        robe_bottom = size - 4
        robe_width = size // 2
        draw.polygon([
            (center_x, robe_top),
            (center_x - robe_width // 2, robe_bottom),
            (center_x + robe_width // 2, robe_bottom)
        ], fill=palette['primary'], outline=palette['outline'])
        
        # Head
        head_y = robe_top - 6
        head_radius = 5
        draw.ellipse([center_x - head_radius, head_y - head_radius,
                     center_x + head_radius, head_y + head_radius],
                    fill=palette['secondary'], outline=palette['outline'])
        
        # Wizard hat
        hat_points = [
            (center_x, head_y - 12),
            (center_x - 6, head_y - head_radius),
            (center_x + 6, head_y - head_radius)
        ]
        draw.polygon(hat_points, fill=palette['primary'], outline=palette['outline'])
        
        # Staff
        staff_x = center_x + 8
        draw.line([staff_x, robe_top + 5, staff_x, size - 8], fill=self.palette.get('wood'), width=2)
        draw.ellipse([staff_x - 3, robe_top, staff_x + 3, robe_top + 6],
                    fill=palette['accent'], outline=palette['outline'])
        
        return img
    
    def _generate_master_sprite(self, img, draw, palette, facing):
        """Generate Orbius sprite - master wizard"""
        size = self.pixel_size
        center_x = size // 2
        
        # Flowing robe (wider, more elaborate)
        robe_top = size // 3
        robe_bottom = size - 4
        draw.ellipse([center_x - 12, robe_top, center_x + 12, robe_bottom],
                    fill=palette['primary'], outline=palette['outline'])
        
        # Inner robe detail
        draw.ellipse([center_x - 10, robe_top + 2, center_x + 10, robe_bottom - 2],
                    fill=palette['secondary'], outline=None)
        
        # Head
        head_y = robe_top - 6
        head_radius = 6
        draw.ellipse([center_x - head_radius, head_y - head_radius,
                     center_x + head_radius, head_y + head_radius],
                    fill=self.palette.get('skin_light'), outline=palette['outline'])
        
        # Beard
        beard_points = [
            (center_x - 4, head_y + 2),
            (center_x - 5, head_y + 8),
            (center_x, head_y + 10),
            (center_x + 5, head_y + 8),
            (center_x + 4, head_y + 2)
        ]
        draw.polygon(beard_points, fill=self.palette.get('white'), outline=palette['outline'])
        
        # Glowing aura (master level)
        for i in range(3):
            alpha = 50 - i * 15
            aura_color = self.palette.with_alpha(palette['accent'], alpha)
            offset = i * 2
            draw.ellipse([center_x - 12 - offset, robe_top - offset,
                         center_x + 12 + offset, robe_bottom + offset],
                        outline=aura_color, width=1)
        
        return img
    
    def _generate_warrior_sprite(self, img, draw, palette, facing):
        """Generate warrior sprite (Coireena)"""
        size = self.pixel_size
        center_x = size // 2
        
        # Body (armored)
        body_top = size // 3
        body_bottom = size - 4
        body_width = size // 3
        draw.rectangle([center_x - body_width // 2, body_top,
                       center_x + body_width // 2, body_bottom],
                      fill=palette['primary'], outline=palette['outline'])
        
        # Armor plates
        for y in range(body_top + 4, body_bottom, 6):
            draw.line([center_x - body_width // 2 + 2, y,
                      center_x + body_width // 2 - 2, y],
                     fill=palette['secondary'], width=1)
        
        # Head
        head_y = body_top - 6
        head_radius = 5
        draw.ellipse([center_x - head_radius, head_y - head_radius,
                     center_x + head_radius, head_y + head_radius],
                    fill=palette['secondary'], outline=palette['outline'])
        
        # Helmet
        draw.arc([center_x - head_radius - 1, head_y - head_radius - 1,
                 center_x + head_radius + 1, head_y + 2],
                start=180, end=0, fill=palette['primary'], width=2)
        
        # Sword
        sword_x = center_x + 10
        draw.line([sword_x, body_top, sword_x, body_bottom],
                 fill=self.palette.get('metal'), width=2)
        draw.polygon([
            (sword_x - 2, body_top - 6),
            (sword_x, body_top - 10),
            (sword_x + 2, body_top - 6)
        ], fill=self.palette.get('metal'), outline=palette['outline'])
        
        # Magical glow (from Coin's power)
        glow_color = self.palette.with_alpha(palette['accent'], 80)
        draw.ellipse([center_x - body_width // 2 - 2, body_top - 2,
                     center_x + body_width // 2 + 2, body_bottom + 2],
                    outline=glow_color, width=1)
        
        return img
    
    def _generate_dark_mage_sprite(self, img, draw, palette, facing):
        """Generate dark mage sprite (Selene)"""
        size = self.pixel_size
        center_x = size // 2
        
        # Dark flowing robe with tattered edges
        robe_top = size // 3
        robe_bottom = size - 4
        
        # Main robe
        draw.polygon([
            (center_x - 14, robe_top),
            (center_x - 10, robe_bottom - 4),
            (center_x - 12, robe_bottom),
            (center_x, robe_bottom - 2),
            (center_x + 12, robe_bottom),
            (center_x + 10, robe_bottom - 4),
            (center_x + 14, robe_top)
        ], fill=palette['primary'], outline=palette['outline'])
        
        # Inner detail
        draw.ellipse([center_x - 8, robe_top + 4, center_x + 8, robe_top + 16],
                    fill=palette['secondary'], outline=palette['accent'])
        
        # Head
        head_y = robe_top - 6
        head_radius = 5
        draw.ellipse([center_x - head_radius, head_y - head_radius,
                     center_x + head_radius, head_y + head_radius],
                    fill=palette['secondary'], outline=palette['outline'])
        
        # Hood
        hood_points = [
            (center_x - 8, head_y - 4),
            (center_x, head_y - 10),
            (center_x + 8, head_y - 4),
            (center_x + 6, head_y + 4),
            (center_x - 6, head_y + 4)
        ]
        draw.polygon(hood_points, fill=palette['primary'], outline=palette['outline'])
        
        # Chaos energy
        for i in range(4):
            angle = i * math.pi / 2 + math.pi / 4
            x = center_x + int(math.cos(angle) * 10)
            y = robe_top + 10 + int(math.sin(angle) * 8)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2],
                        fill=palette['accent'], outline=None)
        
        return img
    
    def _generate_creature_sprite(self, img, draw, palette, facing):
        """Generate Typhus sprite - shifting creature"""
        size = self.pixel_size
        center_x, center_y = size // 2, size // 2
        
        # Main body (amorphous blob-like)
        points = []
        num_points = 8
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            # Irregular radius for organic look
            radius = 8 + (i % 3) * 2
            x = center_x + int(math.cos(angle) * radius)
            y = center_y + int(math.sin(angle) * radius)
            points.append((x, y))
        
        draw.polygon(points, fill=palette['primary'], outline=palette['outline'])
        
        # Inner swirls
        draw.ellipse([center_x - 4, center_y - 4, center_x + 4, center_y + 4],
                    fill=palette['secondary'], outline=None)
        
        # Multiple eyes (creature feature)
        eye_positions = [(-3, -2), (3, -2), (0, 2)]
        for ex, ey in eye_positions:
            draw.ellipse([center_x + ex - 1, center_y + ey - 1,
                         center_x + ex + 1, center_y + ey + 1],
                        fill=palette['accent'], outline=palette['outline'])
        
        # Temporal distortion effect
        for i in range(3):
            offset = i * 3
            alpha = 60 - i * 20
            aura_color = self.palette.with_alpha(palette['accent'], alpha)
            draw.ellipse([center_x - 10 - offset, center_y - 10 - offset,
                         center_x + 10 + offset, center_y + 10 + offset],
                        outline=aura_color, width=1)
        
        return img
    
    def _generate_generic_sprite(self, img, draw, palette, facing):
        """Generate generic NPC sprite"""
        size = self.pixel_size
        center_x = size // 2
        
        # Simple body
        body_top = size // 3
        body_bottom = size - 4
        draw.rectangle([center_x - 6, body_top, center_x + 6, body_bottom],
                      fill=palette['primary'], outline=palette['outline'])
        
        # Head
        head_y = body_top - 5
        draw.ellipse([center_x - 4, head_y - 4, center_x + 4, head_y + 4],
                    fill=palette['secondary'], outline=palette['outline'])
        
        # Simple eyes
        draw.rectangle([center_x - 2, head_y - 1, center_x - 1, head_y], fill=self.palette.get('black'))
        draw.rectangle([center_x + 1, head_y - 1, center_x + 2, head_y], fill=self.palette.get('black'))
        
        return img
    
    def create_enemy_sprite(self, enemy_type: str) -> Image:
        """Generate enemy sprite"""
        img = Image.new('RGBA', (self.pixel_size, self.pixel_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if enemy_type == 'drift_soldier':
            return self._generate_drift_soldier(img, draw)
        elif enemy_type == 'shadow_beast':
            return self._generate_shadow_beast(img, draw)
        elif enemy_type == 'corrupted_mage':
            return self._generate_corrupted_mage(img, draw)
        else:
            return self._generate_generic_enemy(img, draw)
    
    def _generate_drift_soldier(self, img, draw):
        """Generate Drift Empire soldier"""
        size = self.pixel_size
        center_x = size // 2
        
        # Mechanical body
        body_color = self.palette.get('drift_empire_primary')
        draw.rectangle([center_x - 7, 12, center_x + 7, size - 4],
                      fill=body_color, outline=self.palette.get('black'))
        
        # Tech details
        draw.rectangle([center_x - 5, 16, center_x + 5, 18],
                      fill=self.palette.get('drift_empire_accent'))
        draw.rectangle([center_x - 4, 22, center_x + 4, 24],
                      fill=self.palette.get('drift_empire_accent'))
        
        # Helmet/head
        draw.rectangle([center_x - 6, 4, center_x + 6, 12],
                      fill=body_color, outline=self.palette.get('black'))
        
        # Visor
        draw.rectangle([center_x - 4, 7, center_x + 4, 9],
                      fill=self.palette.get('red'))
        
        return img
    
    def _generate_shadow_beast(self, img, draw):
        """Generate shadow creature"""
        size = self.pixel_size
        center_x, center_y = size // 2, size // 2
        
        # Dark amorphous shape
        points = []
        num_points = 12
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            radius = 10 + math.sin(angle * 3) * 3
            x = center_x + int(math.cos(angle) * radius)
            y = center_y + int(math.sin(angle) * radius)
            points.append((x, y))
        
        draw.polygon(points, fill=(20, 20, 40), outline=(0, 0, 0))
        
        # Glowing eyes
        draw.ellipse([center_x - 5, center_y - 3, center_x - 2, center_y],
                    fill=self.palette.get('red'))
        draw.ellipse([center_x + 2, center_y - 3, center_x + 5, center_y],
                    fill=self.palette.get('red'))
        
        return img
    
    def _generate_corrupted_mage(self, img, draw):
        """Generate corrupted magic user"""
        size = self.pixel_size
        center_x = size // 2
        
        # Twisted robe
        corrupt_color = self.palette.lerp(self.palette.get('dark_cabal_primary'),
                                         self.palette.get('magic_chaos'), 0.5)
        draw.polygon([
            (center_x, 10),
            (center_x - 10, size - 4),
            (center_x + 10, size - 4)
        ], fill=corrupt_color, outline=self.palette.get('black'))
        
        # Distorted head
        draw.ellipse([center_x - 5, 2, center_x + 5, 12],
                    fill=(100, 80, 120), outline=self.palette.get('black'))
        
        # Chaotic energy
        for i in range(3):
            offset = i * 4
            alpha = 80 - i * 25
            energy_color = self.palette.with_alpha(self.palette.get('magic_chaos'), alpha)
            draw.ellipse([center_x - 10 - offset, 10 - offset,
                         center_x + 10 + offset, size - 4 + offset],
                        outline=energy_color, width=1)
        
        return img
    
    def _generate_generic_enemy(self, img, draw):
        """Generate generic enemy"""
        size = self.pixel_size
        center_x, center_y = size // 2, size // 2
        
        # Simple hostile creature
        draw.ellipse([center_x - 8, center_y - 8, center_x + 8, center_y + 8],
                    fill=(150, 50, 50), outline=self.palette.get('black'))
        
        # Angry eyes
        draw.rectangle([center_x - 4, center_y - 2, center_x - 2, center_y],
                      fill=self.palette.get('red'))
        draw.rectangle([center_x + 2, center_y - 2, center_x + 4, center_y],
                      fill=self.palette.get('red'))
        
        return img
    
    def save_sprite(self, sprite: Image, filename: str, directory: str = "generated_sprites"):
        """Save generated sprite to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        sprite.save(filepath, 'PNG')
        return filepath
