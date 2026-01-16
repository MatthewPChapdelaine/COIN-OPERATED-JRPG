"""
SNES Sprite Generator - 16-bit era character sprites
Creates authentic SNES-style sprites with proper pixel art and limited palettes
"""

from PIL import Image, ImageDraw
from .snes_palette import SNESPalette


class SNESSpriteGenerator:
    """Generates SNES-style 16-bit character sprites"""
    
    def __init__(self, sprite_size: int = 16):
        """
        Initialize SNES sprite generator
        SNES typically used 16x16 or 24x24 sprites for characters
        """
        self.sprite_size = sprite_size
        self.palette = SNESPalette
    
    def generate_coin_sprite(self) -> Image:
        """Generate Coin character (golden protagonist) - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        pal = self.palette.get_palette_for_character('coin')
        gold = pal['primary']
        gold_dark = pal['secondary']
        highlight = pal['highlight']
        shadow = pal['shadow']
        
        center = self.sprite_size // 2
        
        # Coin body (circular, pixel-perfect)
        # Outer circle - shadow
        for y in range(4, 12):
            for x in range(4, 12):
                dx, dy = x - center, y - center
                if 3.5 <= (dx*dx + dy*dy)**0.5 <= 5.5:
                    draw.point((x, y), fill=shadow)
        
        # Main body
        for y in range(4, 12):
            for x in range(4, 12):
                dx, dy = x - center, y - center
                dist = (dx*dx + dy*dy)**0.5
                if dist <= 3.5:
                    if x < center and y < center:
                        draw.point((x, y), fill=highlight)  # Top-left highlight
                    elif x >= center or y >= center:
                        draw.point((x, y), fill=gold_dark)  # Bottom-right shadow
                    else:
                        draw.point((x, y), fill=gold)
        
        # Eyes (simple SNES style)
        draw.point((center - 2, center - 1), fill=self.palette.get('black'))
        draw.point((center + 1, center - 1), fill=self.palette.get('black'))
        
        # Mouth (simple pixel)
        draw.point((center - 1, center + 1), fill=shadow)
        draw.point((center, center + 1), fill=shadow)
        
        # Magical aura (4 pixels around)
        aura = self.palette.get('magic_yellow')
        draw.point((center, center - 6), fill=aura)
        draw.point((center - 5, center), fill=aura)
        draw.point((center + 4, center), fill=aura)
        draw.point((center, center + 5), fill=aura)
        
        return img
    
    def generate_jinn_lir_sprite(self) -> Image:
        """Generate Jinn-Lir (blue wizard) - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        pal = self.palette.get_palette_for_character('jinn_lir')
        
        center = self.sprite_size // 2
        
        # Robe (blue, flowing)
        robe = pal['robe']
        robe_light = pal['robe_light']
        
        # Body shape (SNES-style simplified humanoid)
        for y in range(8, 15):
            width = 3 if y < 12 else 5
            for x in range(center - width, center + width):
                if x < center:
                    draw.point((x, y), fill=robe)
                else:
                    draw.point((x, y), fill=robe_light)
        
        # Head (skin tone, small)
        skin = pal['skin']
        for y in range(4, 8):
            for x in range(center - 2, center + 2):
                draw.point((x, y), fill=skin)
        
        # Hat (pointed wizard hat)
        for y in range(1, 4):
            width = 4 - y
            for x in range(center - width, center + width):
                draw.point((x, y), fill=robe)
        
        # Eyes
        draw.point((center - 1, 5), fill=self.palette.get('black'))
        draw.point((center + 1, 5), fill=self.palette.get('black'))
        
        # Staff (simple vertical line)
        staff = pal['staff']
        for y in range(7, 14):
            draw.point((center - 4, y), fill=staff)
        
        # Staff orb (magic)
        draw.point((center - 4, 6), fill=pal['magic'])
        draw.point((center - 4, 5), fill=pal['magic'])
        
        return img
    
    def generate_warrior_sprite(self) -> Image:
        """Generate generic warrior (for Coireena) - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        pal = self.palette.get_palette_for_character('coireena')
        
        center = self.sprite_size // 2
        
        # Armored body
        armor = pal['armor']
        armor_light = pal['armor_light']
        
        # Torso (armor)
        for y in range(7, 14):
            width = 3 if y < 10 else 4
            for x in range(center - width, center + width):
                if x < center:
                    draw.point((x, y), fill=armor)
                else:
                    draw.point((x, y), fill=armor_light)
        
        # Head (helmet visible)
        skin = pal['skin']
        for y in range(4, 7):
            for x in range(center - 2, center + 2):
                if y == 4:
                    draw.point((x, y), fill=armor)  # Helmet
                else:
                    draw.point((x, y), fill=skin)
        
        # Hair
        hair = pal['hair']
        draw.point((center - 2, 5), fill=hair)
        draw.point((center + 1, 5), fill=hair)
        
        # Eyes
        draw.point((center - 1, 5), fill=self.palette.get('black'))
        draw.point((center + 1, 5), fill=self.palette.get('black'))
        
        # Shield (left side)
        for y in range(8, 12):
            draw.point((center - 4, y), fill=armor_light)
            draw.point((center - 5, y), fill=armor)
        
        # Sword (right side)
        sword = pal['sword']
        for y in range(6, 13):
            draw.point((center + 4, y), fill=sword)
        
        return img
    
    def generate_mage_sprite(self, color_scheme: str = 'purple') -> Image:
        """Generate generic mage sprite - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = self.sprite_size // 2
        
        # Determine colors
        if color_scheme == 'purple':
            pal = self.palette.get_palette_for_character('selene')
            robe = pal['robe']
            robe_light = pal['robe_light']
        else:
            pal = self.palette.get_palette_for_character('orbius')
            robe = pal['robe']
            robe_light = pal['robe_light']
        
        # Flowing robe
        for y in range(8, 15):
            width = 3 if y < 11 else 5
            for x in range(center - width, center + width):
                if (x + y) % 2 == 0:
                    draw.point((x, y), fill=robe)
                else:
                    draw.point((x, y), fill=robe_light)
        
        # Head
        skin = self.palette.get('skin_light')
        for y in range(4, 8):
            for x in range(center - 2, center + 2):
                draw.point((x, y), fill=skin)
        
        # Hair
        hair = self.palette.get('hair_black') if color_scheme == 'purple' else self.palette.get('hair_white')
        for y in range(3, 6):
            for x in range(center - 2, center + 2):
                if y == 3 or x == center - 2 or x == center + 1:
                    draw.point((x, y), fill=hair)
        
        # Eyes
        draw.point((center - 1, 5), fill=self.palette.get('black'))
        draw.point((center + 1, 5), fill=self.palette.get('black'))
        
        # Magic aura hands
        magic_color = pal.get('magic', self.palette.get('magic_purple'))
        draw.point((center - 4, 10), fill=magic_color)
        draw.point((center + 3, 10), fill=magic_color)
        
        return img
    
    def generate_enemy_sprite(self, enemy_type: str) -> Image:
        """Generate enemy sprite - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = self.sprite_size // 2
        
        if enemy_type == 'slime':
            # Classic SNES slime enemy
            body = self.palette.get('enemy_green')
            body_dark = self.palette.darken(body, 0.3)
            highlight = self.palette.lighten(body, 0.3)
            
            # Blob shape
            for y in range(8, 14):
                width = 4 - abs(y - 11)
                for x in range(center - width, center + width):
                    if y < 10 and x < center:
                        draw.point((x, y), fill=highlight)
                    elif y >= 12:
                        draw.point((x, y), fill=body_dark)
                    else:
                        draw.point((x, y), fill=body)
            
            # Eyes
            draw.point((center - 1, 9), fill=self.palette.get('black'))
            draw.point((center + 1, 9), fill=self.palette.get('black'))
            draw.point((center - 1, 10), fill=self.palette.get('white'))
            draw.point((center + 1, 10), fill=self.palette.get('white'))
        
        elif enemy_type == 'shadow':
            # Shadow creature (dark, wispy)
            body = self.palette.get('enemy_dark')
            shadow = self.palette.get('shadow_purple')
            
            # Amorphous shadow form
            for y in range(6, 14):
                width = 3 + (y % 2)
                for x in range(center - width, center + width):
                    if (x + y) % 3 == 0:
                        draw.point((x, y), fill=shadow)
                    else:
                        draw.point((x, y), fill=body)
            
            # Glowing eyes
            draw.point((center - 2, 8), fill=self.palette.get('fire_red'))
            draw.point((center + 1, 8), fill=self.palette.get('fire_red'))
        
        elif enemy_type == 'soldier':
            # Enemy soldier
            armor = self.palette.get('enemy_red')
            armor_dark = self.palette.darken(armor, 0.2)
            
            # Body
            for y in range(7, 14):
                for x in range(center - 3, center + 3):
                    if x < center:
                        draw.point((x, y), fill=armor)
                    else:
                        draw.point((x, y), fill=armor_dark)
            
            # Helmet
            for y in range(4, 7):
                for x in range(center - 2, center + 2):
                    draw.point((x, y), fill=armor_dark)
            
            # Visor
            draw.point((center - 1, 5), fill=self.palette.get('black'))
            draw.point((center, 5), fill=self.palette.get('black'))
            draw.point((center + 1, 5), fill=self.palette.get('black'))
            
            # Weapon
            weapon = self.palette.get('metal')
            for y in range(5, 12):
                draw.point((center + 4, y), fill=weapon)
        
        else:
            # Default monster
            body = self.palette.get('enemy_purple')
            # Simple monster shape
            for y in range(6, 13):
                width = 3
                for x in range(center - width, center + width):
                    draw.point((x, y), fill=body)
            
            # Eyes
            draw.point((center - 1, 8), fill=self.palette.get('fire_red'))
            draw.point((center + 1, 8), fill=self.palette.get('fire_red'))
        
        return img
    
    def generate_npc_sprite(self, npc_type: str = 'citizen') -> Image:
        """Generate NPC sprite - SNES style"""
        img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = self.sprite_size // 2
        
        # Clothing color based on type
        if npc_type == 'merchant':
            clothes = self.palette.get('fire_orange')
        elif npc_type == 'priest':
            clothes = self.palette.get('white')
        else:
            clothes = self.palette.get('hero_blue')
        
        clothes_dark = self.palette.darken(clothes, 0.2)
        
        # Body
        for y in range(8, 15):
            width = 2 if y < 11 else 3
            for x in range(center - width, center + width):
                if x < center:
                    draw.point((x, y), fill=clothes)
                else:
                    draw.point((x, y), fill=clothes_dark)
        
        # Head
        skin = self.palette.get('skin_medium')
        for y in range(4, 8):
            for x in range(center - 2, center + 2):
                draw.point((x, y), fill=skin)
        
        # Hair
        hair = self.palette.get('hair_brown')
        for y in range(3, 5):
            for x in range(center - 2, center + 2):
                draw.point((x, y), fill=hair)
        
        # Eyes
        draw.point((center - 1, 5), fill=self.palette.get('black'))
        draw.point((center + 1, 5), fill=self.palette.get('black'))
        
        return img
    
    def save_sprite(self, sprite: Image, filename: str, directory: str = "snes_sprites"):
        """Save sprite to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        # Scale up for visibility (3x or 4x for display)
        scaled = sprite.resize((sprite.width * 3, sprite.height * 3), Image.NEAREST)
        scaled.save(filepath, 'PNG')
        return filepath
