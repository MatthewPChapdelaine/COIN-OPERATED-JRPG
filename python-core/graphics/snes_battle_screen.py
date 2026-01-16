"""
SNES Battle Screen - Classic JRPG battle screen renderer
Side-view battle system like Final Fantasy IV-VI
"""

from PIL import Image, ImageDraw, ImageFont
from .snes_palette import SNESPalette
from .snes_sprite_generator import SNESSpriteGenerator


class SNESBattleScreen:
    """Renders SNES-style battle screen"""
    
    # Standard SNES resolutions
    SNES_WIDTH = 256
    SNES_HEIGHT = 224
    
    def __init__(self):
        self.palette = SNESPalette
        self.sprite_gen = SNESSpriteGenerator(sprite_size=24)  # Slightly larger for battle
    
    def generate_battle_background(self, bg_type: str = 'grassland') -> Image:
        """Generate battle background - SNES style"""
        img = Image.new('RGB', (self.SNES_WIDTH, self.SNES_HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if bg_type == 'grassland':
            # Sky gradient
            sky_top = self.palette.get('sky')
            sky_bottom = self.palette.get('sky_dark')
            
            for y in range(self.SNES_HEIGHT // 2):
                ratio = y / (self.SNES_HEIGHT // 2)
                color = (
                    int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio),
                    int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio),
                    int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)
                )
                draw.line([0, y, self.SNES_WIDTH, y], fill=color)
            
            # Ground
            grass = self.palette.get('grass')
            grass_dark = self.palette.get('grass_dark')
            
            for y in range(self.SNES_HEIGHT // 2, self.SNES_HEIGHT):
                # Simple grass texture
                for x in range(0, self.SNES_WIDTH, 4):
                    color = grass_dark if (x + y) % 8 == 0 else grass
                    draw.point((x, y), fill=color)
                    draw.point((x + 1, y), fill=color)
        
        elif bg_type == 'cave':
            # Dark cave background
            bg_top = (20, 15, 25)
            bg_bottom = (10, 8, 15)
            
            for y in range(self.SNES_HEIGHT):
                ratio = y / self.SNES_HEIGHT
                color = (
                    int(bg_top[0] + (bg_bottom[0] - bg_top[0]) * ratio),
                    int(bg_top[1] + (bg_bottom[1] - bg_top[1]) * ratio),
                    int(bg_top[2] + (bg_bottom[2] - bg_top[2]) * ratio)
                )
                draw.line([0, y, self.SNES_WIDTH, y], fill=color)
            
            # Rock formations
            stone = self.palette.get('stone_dark')
            for x in range(0, self.SNES_WIDTH, 32):
                for y_offset in range(3):
                    y = self.SNES_HEIGHT - 20 + y_offset * 4
                    width = 16 - y_offset * 4
                    draw.rectangle([x, y, x + width, y + 4], fill=stone)
        
        elif bg_type == 'castle':
            # Castle interior
            bg_color = (40, 35, 50)
            draw.rectangle([0, 0, self.SNES_WIDTH, self.SNES_HEIGHT], fill=bg_color)
            
            # Stone pillars
            pillar_color = self.palette.get('stone')
            for x in [32, self.SNES_WIDTH - 48]:
                draw.rectangle([x, 0, x + 16, self.SNES_HEIGHT], fill=pillar_color)
        
        return img
    
    def render_battle_screen(self,
                            party_sprites: list,
                            enemy_sprites: list,
                            background_type: str = 'grassland') -> Image:
        """
        Render complete battle screen with party and enemies
        
        party_sprites: List of (sprite_image, name) tuples for party members
        enemy_sprites: List of (sprite_image, name) tuples for enemies
        """
        # Create base screen with background
        screen = self.generate_battle_background(background_type)
        
        # Position party members (bottom left, stacked)
        party_x_start = 32
        party_y_start = self.SNES_HEIGHT - 80
        party_spacing = 32
        
        for i, (sprite, name) in enumerate(party_sprites):
            x = party_x_start + (i * 20)
            y = party_y_start + (i * party_spacing)
            
            if sprite.mode == 'RGBA':
                # Scale sprite for battle (2x)
                scaled_sprite = sprite.resize((sprite.width * 2, sprite.height * 2), Image.NEAREST)
                screen.paste(scaled_sprite, (x, y), scaled_sprite)
            else:
                scaled_sprite = sprite.resize((sprite.width * 2, sprite.height * 2), Image.NEAREST)
                screen.paste(scaled_sprite, (x, y))
        
        # Position enemies (right side, stacked)
        enemy_x_start = self.SNES_WIDTH - 80
        enemy_y_start = 60
        enemy_spacing = 40
        
        for i, (sprite, name) in enumerate(enemy_sprites):
            x = enemy_x_start - (i * 10)
            y = enemy_y_start + (i * enemy_spacing)
            
            if sprite.mode == 'RGBA':
                scaled_sprite = sprite.resize((sprite.width * 2, sprite.height * 2), Image.NEAREST)
                screen.paste(scaled_sprite, (x, y), scaled_sprite)
            else:
                scaled_sprite = sprite.resize((sprite.width * 2, sprite.height * 2), Image.NEAREST)
                screen.paste(scaled_sprite, (x, y))
        
        return screen
    
    def create_battle_menu_window(self, width: int, height: int) -> Image:
        """Create SNES-style battle menu window"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Window background (classic JRPG dark blue)
        window_bg = self.palette.get('ui_window')
        border_color = self.palette.get('ui_border')
        
        # Semi-transparent window
        for y in range(height):
            for x in range(width):
                if x < 2 or x >= width - 2 or y < 2 or y >= height - 2:
                    # Border
                    draw.point((x, y), fill=border_color)
                else:
                    # Interior
                    draw.point((x, y), fill=window_bg)
        
        return img
    
    def render_battle_command_menu(self, commands: list, selected: int = 0) -> Image:
        """
        Render battle command menu (Attack, Magic, Item, etc.)
        
        commands: List of command strings
        selected: Index of currently selected command
        """
        menu_width = 80
        menu_height = 16 + (len(commands) * 12)
        
        img = self.create_battle_menu_window(menu_width, menu_height)
        draw = ImageDraw.Draw(img)
        
        # Text color
        text_color = self.palette.get('ui_text')
        cursor_color = self.palette.get('ui_cursor')
        
        # Draw commands
        for i, command in enumerate(commands):
            y = 8 + (i * 12)
            x = 16
            
            # Draw cursor for selected item
            if i == selected:
                # Simple arrow cursor
                draw.point((8, y + 2), fill=cursor_color)
                draw.point((9, y + 2), fill=cursor_color)
                draw.point((10, y + 2), fill=cursor_color)
                draw.point((9, y + 3), fill=cursor_color)
            
            # Draw command text (simplified - just show as white pixels)
            # In a real implementation, you'd use a pixel font
            for char_offset, char in enumerate(command[:8]):
                char_x = x + (char_offset * 6)
                # Simple 3x5 pixel representation
                draw.rectangle([char_x, y, char_x + 4, y + 6], fill=text_color)
        
        return img
    
    def render_hp_bar(self, current_hp: int, max_hp: int, width: int = 40) -> Image:
        """Render SNES-style HP bar"""
        height = 6
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background
        draw.rectangle([0, 0, width - 1, height - 1], fill=(0, 0, 0, 255))
        draw.rectangle([1, 1, width - 2, height - 2], outline=self.palette.get('ui_border'))
        
        # HP fill
        if max_hp > 0:
            hp_ratio = current_hp / max_hp
            fill_width = int((width - 4) * hp_ratio)
            
            # Color based on HP percentage
            if hp_ratio > 0.5:
                hp_color = self.palette.get('ui_hp_green')
            elif hp_ratio > 0.25:
                hp_color = self.palette.get('ui_hp_yellow')
            else:
                hp_color = self.palette.get('ui_hp_red')
            
            if fill_width > 0:
                draw.rectangle([2, 2, 2 + fill_width, height - 3], fill=hp_color)
        
        return img
    
    def render_character_status(self, name: str, hp: int, max_hp: int, mp: int, max_mp: int) -> Image:
        """Render character status box for battle"""
        width = 80
        height = 32
        
        img = self.create_battle_menu_window(width, height)
        draw = ImageDraw.Draw(img)
        
        text_color = self.palette.get('ui_text')
        
        # Character name (simplified)
        name_y = 4
        for i, char in enumerate(name[:8]):
            char_x = 8 + (i * 6)
            draw.rectangle([char_x, name_y, char_x + 4, name_y + 6], fill=text_color)
        
        # HP bar
        hp_bar = self.render_hp_bar(hp, max_hp, 60)
        img.paste(hp_bar, (10, 14), hp_bar)
        
        # MP bar
        mp_bar_img = Image.new('RGBA', (60, 6), (0, 0, 0, 0))
        mp_draw = ImageDraw.Draw(mp_bar_img)
        mp_draw.rectangle([0, 0, 59, 5], fill=(0, 0, 0, 255))
        mp_draw.rectangle([1, 1, 58, 4], outline=self.palette.get('ui_border'))
        
        if max_mp > 0:
            mp_fill = int(58 * (mp / max_mp))
            if mp_fill > 0:
                mp_draw.rectangle([2, 2, 2 + mp_fill, 3], fill=self.palette.get('ui_mp_blue'))
        
        img.paste(mp_bar_img, (10, 22), mp_bar_img)
        
        return img
    
    def create_full_battle_scene(self) -> Image:
        """Create a complete sample battle scene"""
        # Generate sprites
        coin = self.sprite_gen.generate_coin_sprite()
        jinn_lir = self.sprite_gen.generate_jinn_lir_sprite()
        
        enemy1 = self.sprite_gen.generate_enemy_sprite('shadow')
        enemy2 = self.sprite_gen.generate_enemy_sprite('slime')
        
        party = [(coin, "Coin"), (jinn_lir, "Jinn-Lir")]
        enemies = [(enemy1, "Shadow"), (enemy2, "Slime")]
        
        # Render battle screen
        battle = self.render_battle_screen(party, enemies, 'grassland')
        
        # Add battle menu (bottom of screen)
        commands = ["Attack", "Magic", "Item", "Defend"]
        menu = self.render_battle_command_menu(commands, selected=0)
        
        # Paste menu at bottom left
        battle.paste(menu, (16, self.SNES_HEIGHT - menu.height - 8), menu)
        
        # Add character status boxes (bottom right)
        coin_status = self.render_character_status("Coin", 85, 100, 30, 50)
        jinn_status = self.render_character_status("Jinn-Lir", 120, 150, 45, 80)
        
        battle.paste(coin_status, (self.SNES_WIDTH - coin_status.width - 16, self.SNES_HEIGHT - 72), coin_status)
        battle.paste(jinn_status, (self.SNES_WIDTH - jinn_status.width - 16, self.SNES_HEIGHT - 36), jinn_status)
        
        return battle
    
    def save_battle_screen(self, screen: Image, filename: str, directory: str = "snes_battles"):
        """Save battle screen to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        # Scale up 2x for better visibility
        scaled = screen.resize((screen.width * 2, screen.height * 2), Image.NEAREST)
        scaled.save(filepath, 'PNG')
        return filepath
