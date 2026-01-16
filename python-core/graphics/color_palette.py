"""
Color Palette System - Procedurally defined color schemes
"""

class ColorPalette:
    """Manages color palettes for procedural graphics"""
    
    # Base color definitions
    COLORS = {
        # Character colors
        'coin_gold': (255, 215, 0),
        'coin_silver': (192, 192, 192),
        'coin_bronze': (205, 127, 50),
        'skin_light': (255, 220, 177),
        'skin_medium': (198, 134, 66),
        'skin_dark': (141, 85, 36),
        
        # Magic colors
        'magic_light': (255, 255, 200),
        'magic_time': (138, 43, 226),
        'magic_chaos': (220, 20, 60),
        'magic_healing': (50, 205, 50),
        'magic_lightning': (255, 255, 0),
        'magic_fire': (255, 69, 0),
        'magic_ice': (135, 206, 250),
        'magic_earth': (139, 69, 19),
        
        # Faction colors
        'light_cabal_primary': (240, 230, 140),
        'light_cabal_accent': (255, 215, 0),
        'dark_cabal_primary': (75, 0, 130),
        'dark_cabal_accent': (148, 0, 211),
        'drift_empire_primary': (70, 130, 180),
        'drift_empire_accent': (0, 191, 255),
        
        # UI colors
        'ui_background': (40, 40, 50),
        'ui_border': (200, 200, 220),
        'ui_text': (255, 255, 255),
        'ui_highlight': (255, 215, 0),
        'ui_danger': (220, 20, 60),
        'ui_success': (50, 205, 50),
        
        # Environment colors
        'grass': (34, 139, 34),
        'stone': (128, 128, 128),
        'water': (65, 105, 225),
        'sand': (244, 164, 96),
        'wood': (139, 69, 19),
        'metal': (192, 192, 192),
        
        # Standard colors
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'orange': (255, 165, 0),
        'transparent': (0, 0, 0, 0)
    }
    
    @classmethod
    def get(cls, color_name: str) -> tuple:
        """Get color by name"""
        return cls.COLORS.get(color_name, cls.COLORS['white'])
    
    @classmethod
    def lerp(cls, color1: tuple, color2: tuple, t: float) -> tuple:
        """Linear interpolation between two colors"""
        t = max(0.0, min(1.0, t))
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (r, g, b)
    
    @classmethod
    def darken(cls, color: tuple, factor: float) -> tuple:
        """Darken a color by factor (0-1)"""
        return tuple(int(c * (1 - factor)) for c in color[:3])
    
    @classmethod
    def lighten(cls, color: tuple, factor: float) -> tuple:
        """Lighten a color by factor (0-1)"""
        return tuple(int(c + (255 - c) * factor) for c in color[:3])
    
    @classmethod
    def with_alpha(cls, color: tuple, alpha: int) -> tuple:
        """Add alpha channel to color"""
        return color[:3] + (alpha,)
    
    @classmethod
    def character_palette(cls, character_type: str) -> dict:
        """Get character-specific color palette"""
        palettes = {
            'coin': {
                'primary': cls.COLORS['coin_gold'],
                'secondary': cls.COLORS['coin_silver'],
                'accent': cls.COLORS['magic_time'],
                'outline': cls.COLORS['black']
            },
            'jinn_lir': {
                'primary': cls.COLORS['light_cabal_primary'],
                'secondary': cls.COLORS['skin_light'],
                'accent': cls.COLORS['light_cabal_accent'],
                'outline': cls.COLORS['black']
            },
            'orbius': {
                'primary': cls.COLORS['white'],
                'secondary': cls.COLORS['light_cabal_accent'],
                'accent': cls.COLORS['magic_light'],
                'outline': cls.COLORS['black']
            },
            'coireena': {
                'primary': cls.COLORS['drift_empire_primary'],
                'secondary': cls.COLORS['skin_medium'],
                'accent': cls.COLORS['coin_gold'],
                'outline': cls.COLORS['black']
            },
            'selene': {
                'primary': cls.COLORS['dark_cabal_primary'],
                'secondary': cls.COLORS['skin_dark'],
                'accent': cls.COLORS['dark_cabal_accent'],
                'outline': cls.COLORS['black']
            },
            'typhus': {
                'primary': cls.COLORS['magic_chaos'],
                'secondary': cls.COLORS['purple'],
                'accent': cls.COLORS['magic_time'],
                'outline': cls.COLORS['black']
            }
        }
        return palettes.get(character_type, palettes['coin'])
