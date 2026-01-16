"""
COIN-OPERATED JRPG: Configuration Manager
Handles game settings, preferences, and graphics configuration.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages game configuration and settings."""
    
    DEFAULT_CONFIG = {
        'version': '1.0.0',
        'graphics': {
            'mode': 'retro16',  # 'text', 'graphics', 'retro16'
            'resolution': {
                'width': 768,
                'height': 672
            },
            'scale': 3,  # Retro16 scaling factor
            'fps': 60,
            'fullscreen': False,
            'vsync': True
        },
        'audio': {
            'enabled': True,
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'mute': False
        },
        'gameplay': {
            'difficulty': 'normal',  # 'easy', 'normal', 'hard'
            'auto_save': True,
            'battle_speed': 'normal',  # 'slow', 'normal', 'fast'
            'show_damage_numbers': True
        },
        'controls': {
            'keyboard': {
                'up': 'UP',
                'down': 'DOWN',
                'left': 'LEFT',
                'right': 'RIGHT',
                'confirm': 'SPACE',
                'cancel': 'ESCAPE',
                'menu': 'M',
                'inventory': 'I',
                'save': 'S'
            }
        },
        'debug': {
            'enabled': False,
            'show_fps': False,
            'show_position': False,
            'log_events': False
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to config file. Defaults to ~/.coin-operated-jrpg/config.json
        """
        if config_path is None:
            config_dir = Path.home() / '.coin-operated-jrpg'
            config_dir.mkdir(exist_ok=True)
            config_path = config_dir / 'config.json'
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_config(self.DEFAULT_CONFIG.copy(), loaded_config)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                print("Using default configuration")
        
        return self.DEFAULT_CONFIG.copy()
    
    def _merge_config(self, base: Dict, override: Dict) -> Dict:
        """Recursively merge configurations."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._merge_config(base[key], value)
            else:
                base[key] = value
        return base
    
    def save(self) -> bool:
        """Save current configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get configuration value by path.
        
        Args:
            path: Dot-separated path (e.g., 'graphics.mode')
            default: Default value if path not found
            
        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path: str, value: Any) -> bool:
        """Set configuration value by path.
        
        Args:
            path: Dot-separated path (e.g., 'graphics.mode')
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        keys = path.split('.')
        config = self.config
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set value
        config[keys[-1]] = value
        return True
    
    def reset_to_defaults(self):
        """Reset all configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
    
    def get_graphics_mode(self) -> str:
        """Get current graphics mode."""
        return self.get('graphics.mode', 'snes')
    
    def set_graphics_mode(self, mode: str):
        """Set graphics mode.
        
        Args:
            mode: 'text', 'graphics', or 'retro16'
        """
        if mode in ['text', 'graphics', 'retro16']:
            self.set('graphics.mode', mode)
    
    def get_resolution(self) -> tuple:
        """Get display resolution.
        
        Returns:
            (width, height) tuple
        """
        return (
            self.get('graphics.resolution.width', 768),
            self.get('graphics.resolution.height', 672)
        )
    
    def set_resolution(self, width: int, height: int):
        """Set display resolution."""
        self.set('graphics.resolution.width', width)
        self.set('graphics.resolution.height', height)
    
    def is_fullscreen(self) -> bool:
        """Check if fullscreen is enabled."""
        return self.get('graphics.fullscreen', False)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        current = self.is_fullscreen()
        self.set('graphics.fullscreen', not current)
    
    def get_fps(self) -> int:
        """Get target FPS."""
        return self.get('graphics.fps', 60)
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get('debug.enabled', False)
    
    def export_config(self) -> str:
        """Export configuration as JSON string."""
        return json.dumps(self.config, indent=2)
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(mode={self.get_graphics_mode()}, resolution={self.get_resolution()})"


# Global configuration instance
_config_instance = None


def get_config() -> ConfigManager:
    """Get global configuration instance.
    
    Returns:
        Global ConfigManager instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance


def reset_config():
    """Reset global configuration instance."""
    global _config_instance
    _config_instance = None
