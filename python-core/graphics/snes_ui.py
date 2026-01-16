"""
SNES UI System - Classic JRPG menus and interface
Inspired by Final Fantasy, Chrono Trigger, and other SNES RPGs
"""

from PIL import Image, ImageDraw
from .snes_palette import SNESPalette


class SNESUI:
    """SNES-style UI generator for classic JRPG interfaces"""
    
    def __init__(self):
        self.palette = SNESPalette
    
    def create_text_window(self, width: int, height: int, border_style: str = 'classic') -> Image:
        """
        Create SNES-style text/menu window
        
        border_style: 'classic' (FF-style), 'fancy' (ornate), 'simple'
        """
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Window colors
        window_bg = self.palette.get('ui_window')
        border_outer = self.palette.get('ui_border')
        border_inner = self.palette.darken(border_outer, 0.3)
        
        if border_style == 'classic':
            # Classic FF-style window
            # Outer border (light)
            draw.rectangle([0, 0, width - 1, height - 1], outline=border_outer, width=2)
            # Inner border (dark)
            draw.rectangle([2, 2, width - 3, height - 3], outline=border_inner, width=1)
            # Fill
            draw.rectangle([3, 3, width - 4, height - 4], fill=window_bg)
            
            # Corner decorations (small L-shapes)
            for x, y in [(1, 1), (width - 2, 1), (1, height - 2), (width - 2, height - 2)]:
                draw.point((x, y), fill=border_outer)
        
        elif border_style == 'fancy':
            # Ornate border with corners
            draw.rectangle([0, 0, width - 1, height - 1], outline=border_outer, width=2)
            draw.rectangle([3, 3, width - 4, height - 4], fill=window_bg)
            
            # Decorative corners (larger)
            corner_size = 6
            for corner_x, corner_y in [(0, 0), (width - corner_size, 0), 
                                       (0, height - corner_size), (width - corner_size, height - corner_size)]:
                draw.rectangle([corner_x, corner_y, corner_x + corner_size, corner_y + corner_size],
                              outline=self.palette.get('ui_cursor'), width=1)
        
        else:  # simple
            # Simple single border
            draw.rectangle([0, 0, width - 1, height - 1], outline=border_outer, width=1)
            draw.rectangle([1, 1, width - 2, height - 2], fill=window_bg)
        
        return img
    
    def create_dialogue_box(self, width: int = 240, height: int = 64, speaker_name: str = "") -> Image:
        """Create SNES-style dialogue box (typically bottom of screen)"""
        img = self.create_text_window(width, height, 'classic')
        draw = ImageDraw.Draw(img)
        
        if speaker_name:
            # Name plate (small window above main box)
            name_width = len(speaker_name) * 6 + 16
            name_height = 16
            name_plate = self.create_text_window(name_width, name_height, 'simple')
            
            # Position name plate at top-left of dialogue box
            img.paste(name_plate, (8, -8), name_plate)
            
            # Draw name (simplified - each char as white block)
            text_color = self.palette.get('ui_text')
            for i, char in enumerate(speaker_name):
                char_x = 16 + (i * 6)
                char_y = -2
                draw.rectangle([char_x, char_y, char_x + 4, char_y + 6], fill=text_color)
        
        # Arrow indicator (for "press A to continue")
        arrow_color = self.palette.get('ui_cursor')
        arrow_x = width - 16
        arrow_y = height - 12
        # Simple down arrow
        draw.polygon([(arrow_x, arrow_y), (arrow_x + 6, arrow_y), (arrow_x + 3, arrow_y + 4)],
                    fill=arrow_color)
        
        return img
    
    def create_menu_cursor(self, size: int = 12) -> Image:
        """Create SNES-style menu cursor (hand pointing or arrow)"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        cursor_color = self.palette.get('ui_cursor')
        
        # Simple right-pointing arrow
        mid = size // 2
        draw.polygon([
            (2, mid),
            (size - 4, mid - 3),
            (size - 4, mid + 3)
        ], fill=cursor_color)
        
        # Add glowing effect (lighter pixel at tip)
        draw.point((size - 4, mid), fill=self.palette.lighten(cursor_color, 0.3))
        
        return img
    
    def create_main_menu(self, width: int = 120, height: int = 140) -> Image:
        """Create SNES-style main menu window"""
        img = self.create_text_window(width, height, 'classic')
        draw = ImageDraw.Draw(img)
        
        # Menu options
        options = ["Item", "Magic", "Equip", "Status", "Config", "Save"]
        text_color = self.palette.get('ui_text')
        
        y_start = 12
        y_spacing = 20
        x_start = 24
        
        for i, option in enumerate(options):
            y = y_start + (i * y_spacing)
            
            # Draw option text (simplified)
            for char_i, char in enumerate(option):
                char_x = x_start + (char_i * 6)
                draw.rectangle([char_x, y, char_x + 4, y + 6], fill=text_color)
        
        # Draw cursor at first option
        cursor = self.create_menu_cursor(10)
        img.paste(cursor, (12, y_start - 2), cursor)
        
        return img
    
    def create_status_window(self, char_name: str, level: int, hp: int, max_hp: int,
                            mp: int, max_mp: int) -> Image:
        """Create character status window for menu"""
        width = 200
        height = 60
        
        img = self.create_text_window(width, height, 'classic')
        draw = ImageDraw.Draw(img)
        
        text_color = self.palette.get('ui_text')
        
        # Character name
        name_x = 12
        name_y = 8
        for i, char in enumerate(char_name[:12]):
            char_x = name_x + (i * 6)
            draw.rectangle([char_x, name_y, char_x + 4, name_y + 6], fill=text_color)
        
        # Level (LV ##)
        level_x = name_x + 80
        level_y = name_y
        # "LV" text
        draw.rectangle([level_x, level_y, level_x + 8, level_y + 6], fill=text_color)
        # Level number (simplified)
        draw.rectangle([level_x + 12, level_y, level_x + 24, level_y + 6], fill=text_color)
        
        # HP bar
        hp_label_x = 12
        hp_label_y = 24
        # "HP" label
        draw.rectangle([hp_label_x, hp_label_y, hp_label_x + 10, hp_label_y + 6], fill=text_color)
        
        # HP bar
        bar_width = 80
        bar_height = 8
        bar_x = hp_label_x + 24
        bar_y = hp_label_y
        
        # Background
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                      fill=(0, 0, 0, 255), outline=self.palette.get('ui_border'))
        
        # HP fill
        if max_hp > 0:
            hp_ratio = hp / max_hp
            fill_width = int(bar_width * hp_ratio)
            
            if hp_ratio > 0.5:
                hp_color = self.palette.get('ui_hp_green')
            elif hp_ratio > 0.25:
                hp_color = self.palette.get('ui_hp_yellow')
            else:
                hp_color = self.palette.get('ui_hp_red')
            
            if fill_width > 0:
                draw.rectangle([bar_x + 2, bar_y + 2, bar_x + fill_width - 2, bar_y + bar_height - 2],
                              fill=hp_color)
        
        # HP numbers (simplified)
        num_x = bar_x + bar_width + 8
        draw.rectangle([num_x, bar_y, num_x + 30, bar_y + 6], fill=text_color)
        
        # MP bar
        mp_label_y = 40
        draw.rectangle([hp_label_x, mp_label_y, hp_label_x + 10, mp_label_y + 6], fill=text_color)
        
        # MP bar
        draw.rectangle([bar_x, mp_label_y, bar_x + bar_width, mp_label_y + bar_height],
                      fill=(0, 0, 0, 255), outline=self.palette.get('ui_border'))
        
        if max_mp > 0:
            mp_fill = int(bar_width * (mp / max_mp))
            if mp_fill > 0:
                draw.rectangle([bar_x + 2, mp_label_y + 2, bar_x + mp_fill - 2, mp_label_y + bar_height - 2],
                              fill=self.palette.get('ui_mp_blue'))
        
        # MP numbers
        draw.rectangle([num_x, mp_label_y, num_x + 30, mp_label_y + 6], fill=text_color)
        
        return img
    
    def create_item_menu(self, items: list, selected: int = 0) -> Image:
        """Create SNES-style item menu"""
        width = 180
        max_visible = 8
        height = 24 + (max_visible * 16)
        
        img = self.create_text_window(width, height, 'classic')
        draw = ImageDraw.Draw(img)
        
        text_color = self.palette.get('ui_text')
        cursor_color = self.palette.get('ui_cursor')
        
        # Title
        title = "ITEMS"
        title_y = 8
        for i, char in enumerate(title):
            char_x = 12 + (i * 6)
            draw.rectangle([char_x, title_y, char_x + 4, title_y + 6], fill=text_color)
        
        # Item list
        list_y_start = 24
        for i, item in enumerate(items[:max_visible]):
            y = list_y_start + (i * 16)
            x = 24
            
            # Cursor for selected
            if i == selected:
                draw.polygon([(12, y + 3), (18, y), (18, y + 6)], fill=cursor_color)
            
            # Item name
            for char_i, char in enumerate(item[:16]):
                char_x = x + (char_i * 6)
                draw.rectangle([char_x, y, char_x + 4, char_y + 6], fill=text_color)
            
            # Item quantity (x##)
            qty_x = width - 40
            draw.rectangle([qty_x, y, qty_x + 20, y + 6], fill=text_color)
        
        return img
    
    def create_save_slot_display(self, slot_num: int, character_name: str,
                                 location: str, playtime: str, level: int) -> Image:
        """Create save slot display for save/load menu"""
        width = 240
        height = 48
        
        img = self.create_text_window(width, height, 'classic')
        draw = ImageDraw.Draw(img)
        
        text_color = self.palette.get('ui_text')
        
        # Slot number
        slot_x = 12
        slot_y = 8
        slot_text = f"SLOT {slot_num}"
        for i, char in enumerate(slot_text):
            char_x = slot_x + (i * 6)
            draw.rectangle([char_x, slot_y, char_x + 4, slot_y + 6], fill=text_color)
        
        # Character name
        char_x = 12
        char_y = 22
        for i, char in enumerate(character_name[:12]):
            cx = char_x + (i * 6)
            draw.rectangle([cx, char_y, cx + 4, char_y + 6], fill=text_color)
        
        # Level
        level_x = 90
        for i, char in enumerate(f"LV{level}"):
            cx = level_x + (i * 6)
            draw.rectangle([cx, char_y, cx + 4, char_y + 6], fill=text_color)
        
        # Location
        loc_y = 34
        for i, char in enumerate(location[:20]):
            cx = char_x + (i * 6)
            draw.rectangle([cx, loc_y, cx + 4, loc_y + 6], fill=text_color)
        
        # Playtime
        time_x = width - 60
        for i, char in enumerate(playtime[:8]):
            cx = time_x + (i * 6)
            draw.rectangle([cx, loc_y, cx + 4, loc_y + 6], fill=text_color)
        
        return img
    
    def create_title_screen(self, game_title: str = "COIN:OPERATED") -> Image:
        """Create SNES-style title screen"""
        width = 256
        height = 224
        
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Gradient background
        sky_top = self.palette.get('shadow_purple')
        sky_bottom = self.palette.get('shadow_blue')
        
        for y in range(height):
            ratio = y / height
            color = (
                int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio),
                int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio),
                int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)
            )
            draw.line([0, y, width, y], fill=color)
        
        # Title (large text, centered)
        title_color = self.palette.get('ui_cursor')
        title_y = height // 3
        title_x = (width - len(game_title) * 8) // 2
        
        # Large pixel font (2x2 pixels per character pixel)
        for i, char in enumerate(game_title):
            char_x = title_x + (i * 12)
            draw.rectangle([char_x, title_y, char_x + 10, title_y + 14], fill=title_color)
        
        # "Press Start" text (blinking)
        start_text = "PRESS START"
        start_y = height * 2 // 3
        start_x = (width - len(start_text) * 6) // 2
        
        start_color = self.palette.get('ui_text')
        for i, char in enumerate(start_text):
            char_x = start_x + (i * 6)
            draw.rectangle([char_x, start_y, char_x + 4, start_y + 6], fill=start_color)
        
        # Copyright text
        copyright = "1995 LOPORIAN INDUSTRIES"
        copy_y = height - 20
        copy_x = (width - len(copyright) * 4) // 2
        
        copy_color = self.palette.get('gray')
        for i, char in enumerate(copyright):
            char_x = copy_x + (i * 4)
            draw.rectangle([char_x, copy_y, char_x + 3, copy_y + 5], fill=copy_color)
        
        return img
    
    def save_ui_element(self, element: Image, filename: str, directory: str = "snes_ui"):
        """Save UI element to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        # Scale up 2x for better visibility
        scaled = element.resize((element.width * 2, element.height * 2), Image.NEAREST)
        scaled.save(filepath, 'PNG')
        return filepath
