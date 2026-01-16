"""
SNES Color Palette - Authentic 16-bit era color palette
Based on SNES hardware capabilities (32,768 colors, 15-bit RGB)
"""


class SNESPalette:
    """
    SNES-era color palette with authentic 16-bit limitations
    SNES used 15-bit RGB (5 bits per channel = 32 levels per channel)
    """
    
    # SNES hardware constraint: 5 bits per channel (0-31)
    # We convert to 8-bit (0-255) by multiplying by 8.225 (255/31)
    
    @staticmethod
    def snes_rgb(r5: int, g5: int, b5: int) -> tuple:
        """Convert 5-bit SNES RGB to 8-bit RGB"""
        r8 = int((r5 / 31.0) * 255)
        g8 = int((g5 / 31.0) * 255)
        b8 = int((b5 / 31.0) * 255)
        return (r8, g8, b8, 255)
    
    # SNES System Colors (authentic palette)
    COLORS = {
        # Basic colors (high saturation, SNES-era style)
        'black': snes_rgb.__func__(0, 0, 0),
        'white': snes_rgb.__func__(31, 31, 31),
        'dark_gray': snes_rgb.__func__(10, 10, 10),
        'gray': snes_rgb.__func__(16, 16, 16),
        'light_gray': snes_rgb.__func__(24, 24, 24),
        
        # Primary colors (vibrant SNES style)
        'red': snes_rgb.__func__(31, 0, 0),
        'green': snes_rgb.__func__(0, 31, 0),
        'blue': snes_rgb.__func__(0, 0, 31),
        'yellow': snes_rgb.__func__(31, 31, 0),
        'cyan': snes_rgb.__func__(0, 31, 31),
        'magenta': snes_rgb.__func__(31, 0, 31),
        
        # Character colors (inspired by FF6, Chrono Trigger)
        'hero_gold': snes_rgb.__func__(31, 24, 0),      # Golden protagonist
        'hero_gold_dark': snes_rgb.__func__(20, 15, 0),
        'hero_blue': snes_rgb.__func__(8, 16, 31),      # Blue mage robes
        'hero_blue_light': snes_rgb.__func__(16, 24, 31),
        'hero_purple': snes_rgb.__func__(20, 8, 28),    # Purple magic
        'hero_purple_light': snes_rgb.__func__(28, 16, 31),
        
        # Skin tones (SNES style)
        'skin_light': snes_rgb.__func__(31, 24, 20),
        'skin_medium': snes_rgb.__func__(28, 20, 16),
        'skin_dark': snes_rgb.__func__(20, 14, 10),
        'skin_shadow': snes_rgb.__func__(16, 10, 8),
        
        # Hair colors
        'hair_blonde': snes_rgb.__func__(31, 28, 12),
        'hair_brown': snes_rgb.__func__(18, 12, 8),
        'hair_black': snes_rgb.__func__(4, 4, 6),
        'hair_white': snes_rgb.__func__(28, 28, 30),
        'hair_blue': snes_rgb.__func__(12, 16, 28),
        
        # Environment colors
        'grass': snes_rgb.__func__(8, 24, 8),
        'grass_dark': snes_rgb.__func__(4, 16, 4),
        'grass_light': snes_rgb.__func__(12, 28, 12),
        'dirt': snes_rgb.__func__(20, 14, 8),
        'stone': snes_rgb.__func__(18, 18, 20),
        'stone_dark': snes_rgb.__func__(12, 12, 14),
        'water': snes_rgb.__func__(4, 12, 28),
        'water_light': snes_rgb.__func__(8, 20, 31),
        'sky': snes_rgb.__func__(8, 20, 31),
        'sky_dark': snes_rgb.__func__(4, 12, 24),
        
        # Wood/Brown
        'wood': snes_rgb.__func__(20, 12, 4),
        'wood_light': snes_rgb.__func__(24, 16, 8),
        'wood_dark': snes_rgb.__func__(14, 8, 2),
        
        # Metal (silver/gray)
        'metal': snes_rgb.__func__(20, 20, 24),
        'metal_light': snes_rgb.__func__(26, 26, 28),
        'metal_dark': snes_rgb.__func__(12, 12, 16),
        
        # Magic effects (vibrant SNES style)
        'magic_blue': snes_rgb.__func__(8, 16, 31),
        'magic_cyan': snes_rgb.__func__(0, 28, 31),
        'magic_purple': snes_rgb.__func__(24, 8, 31),
        'magic_pink': snes_rgb.__func__(31, 16, 28),
        'magic_yellow': snes_rgb.__func__(31, 28, 8),
        'magic_white': snes_rgb.__func__(31, 31, 31),
        
        # Fire/Heat
        'fire_yellow': snes_rgb.__func__(31, 28, 4),
        'fire_orange': snes_rgb.__func__(31, 16, 0),
        'fire_red': snes_rgb.__func__(31, 8, 0),
        'fire_dark': snes_rgb.__func__(20, 4, 0),
        
        # Ice/Cold
        'ice_white': snes_rgb.__func__(28, 31, 31),
        'ice_cyan': snes_rgb.__func__(16, 28, 31),
        'ice_blue': snes_rgb.__func__(12, 20, 28),
        
        # Lightning
        'lightning_white': snes_rgb.__func__(31, 31, 28),
        'lightning_yellow': snes_rgb.__func__(31, 31, 16),
        'lightning_blue': snes_rgb.__func__(20, 24, 31),
        
        # Dark/Shadow
        'shadow': snes_rgb.__func__(4, 0, 8),
        'shadow_purple': snes_rgb.__func__(12, 4, 16),
        'shadow_blue': snes_rgb.__func__(4, 4, 12),
        
        # UI colors (classic JRPG)
        'ui_window': snes_rgb.__func__(0, 4, 20),       # Dark blue window
        'ui_border': snes_rgb.__func__(24, 24, 28),     # Light border
        'ui_text': snes_rgb.__func__(31, 31, 31),       # White text
        'ui_cursor': snes_rgb.__func__(31, 28, 8),      # Yellow cursor
        'ui_hp_green': snes_rgb.__func__(8, 28, 8),     # HP bar green
        'ui_hp_yellow': snes_rgb.__func__(31, 28, 0),   # HP bar yellow
        'ui_hp_red': snes_rgb.__func__(31, 8, 0),       # HP bar red
        'ui_mp_blue': snes_rgb.__func__(8, 16, 31),     # MP bar blue
        
        # Enemy colors
        'enemy_red': snes_rgb.__func__(28, 8, 8),
        'enemy_purple': snes_rgb.__func__(20, 8, 24),
        'enemy_green': snes_rgb.__func__(12, 24, 8),
        'enemy_dark': snes_rgb.__func__(8, 4, 10),
    }
    
    @classmethod
    def get(cls, color_name: str) -> tuple:
        """Get color by name"""
        return cls.COLORS.get(color_name, cls.COLORS['white'])
    
    @classmethod
    def get_palette_for_character(cls, character_name: str) -> dict:
        """Get color palette for specific character (SNES style)"""
        palettes = {
            'coin': {
                'primary': cls.get('hero_gold'),
                'secondary': cls.get('hero_gold_dark'),
                'highlight': cls.get('magic_yellow'),
                'shadow': cls.get('wood_dark'),
                'eye': cls.get('black'),
            },
            'jinn_lir': {
                'robe': cls.get('hero_blue'),
                'robe_light': cls.get('hero_blue_light'),
                'staff': cls.get('wood'),
                'magic': cls.get('magic_purple'),
                'skin': cls.get('skin_light'),
            },
            'orbius': {
                'robe': cls.get('hero_purple'),
                'robe_light': cls.get('hero_purple_light'),
                'beard': cls.get('hair_white'),
                'skin': cls.get('skin_medium'),
                'magic': cls.get('magic_white'),
            },
            'coireena': {
                'armor': cls.get('metal'),
                'armor_light': cls.get('metal_light'),
                'hair': cls.get('hair_brown'),
                'skin': cls.get('skin_medium'),
                'sword': cls.get('metal_light'),
            },
            'selene': {
                'robe': cls.get('shadow_purple'),
                'robe_light': cls.get('hero_purple'),
                'hair': cls.get('hair_black'),
                'skin': cls.get('skin_light'),
                'magic': cls.get('magic_purple'),
            },
            'typhus': {
                'body': cls.get('enemy_purple'),
                'body_dark': cls.get('enemy_dark'),
                'eye': cls.get('fire_red'),
                'claw': cls.get('stone_dark'),
            },
        }
        return palettes.get(character_name, {})
    
    @classmethod
    def get_gradient(cls, color1_name: str, color2_name: str, steps: int) -> list:
        """Generate gradient between two SNES colors"""
        c1 = cls.get(color1_name)
        c2 = cls.get(color2_name)
        
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            gradient.append((r, g, b, 255))
        
        return gradient
    
    @classmethod
    def darken(cls, color: tuple, amount: float = 0.3) -> tuple:
        """Darken a color (SNES style - reduces brightness)"""
        factor = 1.0 - amount
        return (
            int(color[0] * factor),
            int(color[1] * factor),
            int(color[2] * factor),
            color[3] if len(color) > 3 else 255
        )
    
    @classmethod
    def lighten(cls, color: tuple, amount: float = 0.3) -> tuple:
        """Lighten a color (SNES style)"""
        factor = 1.0 + amount
        return (
            min(255, int(color[0] * factor)),
            min(255, int(color[1] * factor)),
            min(255, int(color[2] * factor)),
            color[3] if len(color) > 3 else 255
        )
