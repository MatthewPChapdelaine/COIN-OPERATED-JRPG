"""
UI Generator - Procedurally generates UI elements
"""

from PIL import Image, ImageDraw, ImageFont
import math
from .color_palette import ColorPalette


class UIGenerator:
    """Generates UI elements procedurally"""
    
    def __init__(self):
        self.palette = ColorPalette
    
    def generate_button(self, width: int, height: int, text: str, style: str = 'normal') -> Image:
        """Generate button with text"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Button style colors
        if style == 'primary':
            bg_color = self.palette.get('ui_highlight')
            border_color = self.palette.get('coin_gold')
        elif style == 'danger':
            bg_color = self.palette.get('ui_danger')
            border_color = self.palette.darken(self.palette.get('ui_danger'), 0.3)
        elif style == 'success':
            bg_color = self.palette.get('ui_success')
            border_color = self.palette.darken(self.palette.get('ui_success'), 0.3)
        else:
            bg_color = self.palette.get('ui_background')
            border_color = self.palette.get('ui_border')
        
        # Draw button background
        draw.rectangle([2, 2, width - 2, height - 2], fill=bg_color, outline=border_color, width=2)
        
        # Add gradient effect (lighter at top)
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        gradient_height = height // 2
        for y in range(gradient_height):
            alpha = int(50 * (1 - y / gradient_height))
            color = self.palette.with_alpha(self.palette.get('white'), alpha)
            overlay_draw.line([2, y + 2, width - 2, y + 2], fill=color)
        img = Image.alpha_composite(img, overlay)
        
        # Draw text (centered)
        draw = ImageDraw.Draw(img)
        text_bbox = draw.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        
        # Text shadow
        draw.text((text_x + 1, text_y + 1), text, fill=self.palette.get('black'))
        # Main text
        draw.text((text_x, text_y), text, fill=self.palette.get('ui_text'))
        
        return img
    
    def generate_window(self, width: int, height: int, title: str = "") -> Image:
        """Generate window/dialog box"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Window background
        bg_color = self.palette.with_alpha(self.palette.get('ui_background'), 230)
        border_color = self.palette.get('ui_border')
        
        # Outer border
        draw.rectangle([0, 0, width - 1, height - 1], fill=bg_color, outline=border_color, width=3)
        
        # Inner border
        inner_border = self.palette.lighten(border_color, 0.2)
        draw.rectangle([4, 4, width - 5, height - 5], outline=inner_border, width=1)
        
        # Title bar if title provided
        if title:
            title_height = 24
            title_bg = self.palette.get('ui_highlight')
            draw.rectangle([3, 3, width - 4, title_height], fill=title_bg)
            
            # Title text
            text_bbox = draw.textbbox((0, 0), title)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = 6
            
            draw.text((text_x + 1, text_y + 1), title, fill=self.palette.get('black'))
            draw.text((text_x, text_y), title, fill=self.palette.get('ui_text'))
        
        # Corner decorations
        corner_size = 8
        for x, y in [(6, 6), (width - 6, 6), (6, height - 6), (width - 6, height - 6)]:
            draw.line([x - corner_size, y, x + corner_size, y], fill=border_color, width=1)
            draw.line([x, y - corner_size, x, y + corner_size], fill=border_color, width=1)
        
        return img
    
    def generate_health_bar(self, width: int, height: int, current: float, maximum: float) -> Image:
        """Generate health bar"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background
        draw.rectangle([0, 0, width - 1, height - 1], 
                      fill=(40, 40, 40), 
                      outline=self.palette.get('ui_border'), 
                      width=1)
        
        # Health fill
        if maximum > 0:
            fill_width = int((current / maximum) * (width - 4))
            
            # Color based on health percentage
            health_percent = current / maximum
            if health_percent > 0.5:
                fill_color = self.palette.get('ui_success')
            elif health_percent > 0.25:
                fill_color = self.palette.get('yellow')
            else:
                fill_color = self.palette.get('ui_danger')
            
            if fill_width > 0:
                draw.rectangle([2, 2, fill_width + 2, height - 3], fill=fill_color)
                
                # Gradient overlay
                for x in range(fill_width):
                    alpha = int(50 * (1 - x / max(fill_width, 1)))
                    gradient_color = self.palette.with_alpha(self.palette.get('white'), alpha)
                    draw.line([x + 2, 2, x + 2, height // 2], fill=gradient_color)
        
        return img
    
    def generate_mana_bar(self, width: int, height: int, current: float, maximum: float) -> Image:
        """Generate mana/MP bar"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background
        draw.rectangle([0, 0, width - 1, height - 1],
                      fill=(40, 40, 40),
                      outline=self.palette.get('ui_border'),
                      width=1)
        
        # Mana fill
        if maximum > 0:
            fill_width = int((current / maximum) * (width - 4))
            fill_color = self.palette.get('magic_time')
            
            if fill_width > 0:
                draw.rectangle([2, 2, fill_width + 2, height - 3], fill=fill_color)
                
                # Shimmer effect
                for x in range(0, fill_width, 4):
                    shimmer_color = self.palette.with_alpha(self.palette.get('white'), 100)
                    draw.line([x + 2, 2, x + 2, height - 3], fill=shimmer_color)
        
        return img
    
    def generate_progress_bar(self, width: int, height: int, progress: float) -> Image:
        """Generate generic progress bar (0.0 to 1.0)"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background
        draw.rectangle([0, 0, width - 1, height - 1],
                      fill=(40, 40, 40),
                      outline=self.palette.get('ui_border'),
                      width=1)
        
        # Progress fill
        fill_width = int(progress * (width - 4))
        fill_color = self.palette.get('ui_highlight')
        
        if fill_width > 0:
            draw.rectangle([2, 2, fill_width + 2, height - 3], fill=fill_color)
        
        return img
    
    def generate_icon(self, icon_type: str, size: int = 32) -> Image:
        """Generate icon"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = size // 2, size // 2
        
        if icon_type == 'attack':
            # Sword icon
            color = self.palette.get('red')
            # Blade
            draw.polygon([
                (center_x - 2, size - 4),
                (center_x + 2, size - 4),
                (center_x + 1, 8),
                (center_x - 1, 8)
            ], fill=color, outline=self.palette.get('black'))
            # Point
            draw.polygon([
                (center_x - 3, 8),
                (center_x, 4),
                (center_x + 3, 8)
            ], fill=color, outline=self.palette.get('black'))
            # Hilt
            draw.rectangle([center_x - 5, size - 8, center_x + 5, size - 6],
                          fill=self.palette.get('coin_gold'), outline=self.palette.get('black'))
        
        elif icon_type == 'magic':
            # Sparkle/star icon
            color = self.palette.get('magic_time')
            points = []
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                radius = (size // 3) if i % 2 == 0 else (size // 6)
                x = center_x + int(math.cos(rad) * radius)
                y = center_y + int(math.sin(rad) * radius)
                points.append((x, y))
            draw.polygon(points, fill=color, outline=self.palette.get('black'))
        
        elif icon_type == 'defense':
            # Shield icon
            color = self.palette.get('metal')
            draw.polygon([
                (center_x, 4),
                (center_x + 10, 8),
                (center_x + 10, size - 8),
                (center_x, size - 4),
                (center_x - 10, size - 8),
                (center_x - 10, 8)
            ], fill=color, outline=self.palette.get('black'))
            # Shield emblem
            draw.ellipse([center_x - 4, center_y - 4, center_x + 4, center_y + 4],
                        fill=self.palette.get('coin_gold'), outline=self.palette.get('black'))
        
        elif icon_type == 'item':
            # Potion icon
            color = self.palette.get('magic_healing')
            # Bottle
            draw.polygon([
                (center_x - 4, center_y),
                (center_x - 5, size - 4),
                (center_x + 5, size - 4),
                (center_x + 4, center_y)
            ], fill=color, outline=self.palette.get('black'))
            # Cork
            draw.rectangle([center_x - 3, center_y - 4, center_x + 3, center_y],
                          fill=self.palette.get('wood'), outline=self.palette.get('black'))
        
        elif icon_type == 'coin':
            # Coin icon
            color = self.palette.get('coin_gold')
            draw.ellipse([4, 4, size - 4, size - 4],
                        fill=color, outline=self.palette.get('black'), width=2)
            # Coin detail
            draw.ellipse([8, 8, size - 8, size - 8],
                        fill=self.palette.lighten(color, 0.2), outline=None)
        
        return img
    
    def generate_cursor(self, size: int = 16) -> Image:
        """Generate cursor/pointer"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Arrow cursor
        points = [
            (2, 2),
            (2, size - 4),
            (6, size - 8),
            (size - 4, size - 2)
        ]
        
        # Shadow
        shadow_points = [(p[0] + 1, p[1] + 1) for p in points]
        draw.polygon(shadow_points, fill=self.palette.get('black'))
        
        # Main cursor
        draw.polygon(points, fill=self.palette.get('white'), outline=self.palette.get('black'))
        
        return img
    
    def generate_menu_panel(self, width: int, height: int, style: str = 'normal') -> Image:
        """Generate menu panel background"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Style-specific colors
        if style == 'light_cabal':
            bg_color = self.palette.with_alpha(self.palette.get('light_cabal_primary'), 200)
            accent = self.palette.get('light_cabal_accent')
        elif style == 'dark_cabal':
            bg_color = self.palette.with_alpha(self.palette.get('dark_cabal_primary'), 200)
            accent = self.palette.get('dark_cabal_accent')
        elif style == 'drift':
            bg_color = self.palette.with_alpha(self.palette.get('drift_empire_primary'), 200)
            accent = self.palette.get('drift_empire_accent')
        else:
            bg_color = self.palette.with_alpha(self.palette.get('ui_background'), 220)
            accent = self.palette.get('ui_border')
        
        # Background
        draw.rectangle([0, 0, width - 1, height - 1], fill=bg_color, outline=accent, width=2)
        
        # Decorative corners
        corner_size = 12
        for x, y in [(0, 0), (width, 0), (0, height), (width, height)]:
            if x == 0 and y == 0:  # Top-left
                draw.line([4, 4, corner_size, 4], fill=accent, width=2)
                draw.line([4, 4, 4, corner_size], fill=accent, width=2)
            elif x == width and y == 0:  # Top-right
                draw.line([width - corner_size, 4, width - 4, 4], fill=accent, width=2)
                draw.line([width - 4, 4, width - 4, corner_size], fill=accent, width=2)
            elif x == 0 and y == height:  # Bottom-left
                draw.line([4, height - 4, corner_size, height - 4], fill=accent, width=2)
                draw.line([4, height - corner_size, 4, height - 4], fill=accent, width=2)
            elif x == width and y == height:  # Bottom-right
                draw.line([width - corner_size, height - 4, width - 4, height - 4], fill=accent, width=2)
                draw.line([width - 4, height - corner_size, width - 4, height - 4], fill=accent, width=2)
        
        return img
    
    def generate_dialogue_box(self, width: int, height: int, character_name: str = "") -> Image:
        """Generate dialogue text box"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Box background
        bg_color = self.palette.with_alpha(self.palette.get('ui_background'), 240)
        border_color = self.palette.get('ui_border')
        
        draw.rectangle([0, 0, width - 1, height - 1], fill=bg_color, outline=border_color, width=3)
        
        # Name plate if character name provided
        if character_name:
            name_width = len(character_name) * 8 + 20
            name_height = 20
            name_x = 20
            name_y = -8
            
            # Name plate background
            draw.rectangle([name_x, name_y, name_x + name_width, name_y + name_height],
                          fill=self.palette.get('ui_highlight'), outline=border_color, width=2)
            
            # Name text
            text_x = name_x + 10
            text_y = name_y + 4
            draw.text((text_x + 1, text_y + 1), character_name, fill=self.palette.get('black'))
            draw.text((text_x, text_y), character_name, fill=self.palette.get('ui_text'))
        
        return img
    
    def save_ui_element(self, element: Image, filename: str, directory: str = "generated_ui"):
        """Save UI element to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        element.save(filepath, 'PNG')
        return filepath
