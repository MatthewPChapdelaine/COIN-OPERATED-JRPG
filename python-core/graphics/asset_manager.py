"""Asset Manager: Loads and caches sprites/assets by name from game logic."""

from pathlib import Path
from typing import Dict, Any

class AssetManager:
    """Load assets using IDs from game logic only."""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.cache = {}
    
    def get_sprite(self, asset_id: str):
        """Get sprite by ID (from game logic, never hardcoded)."""
        if asset_id in self.cache:
            return self.cache[asset_id]
        # Load from file using ID
        return None
