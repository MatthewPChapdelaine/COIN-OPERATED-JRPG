"""
COIN-OPERATED JRPG: Graphics-Logic Interface
Single source of truth for all data exchange between game logic and graphics layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class GameStateInterface(ABC):
    """Read-only access to game state."""
    
    @abstractmethod
    def get_player_location(self) -> Dict[str, Any]:
        """Current player location data."""
        pass
    
    @abstractmethod
    def get_party_members(self) -> List[Dict[str, Any]]:
        """Current party with stats, equipment, abilities."""
        pass
    
    @abstractmethod
    def get_current_encounter(self) -> Optional[Dict[str, Any]]:
        """Current battle state if in combat."""
        pass
    
    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """Valid player actions for current context."""
        pass
    
    @abstractmethod
    def get_ui_elements(self) -> Dict[str, Any]:
        """Current menu/UI state."""
        pass
    
    @abstractmethod
    def get_asset_requirements(self) -> Dict[str, List[str]]:
        """Assets needed for current state."""
        pass
    
    @abstractmethod
    def get_quest(self, quest_id: str) -> Dict[str, Any]:
        """Quest data by ID (read-only)."""
        pass
    
    @abstractmethod
    def get_enemy(self, enemy_id: str) -> Dict[str, Any]:
        """Enemy data by ID (read-only)."""
        pass

class GameCommandInterface(ABC):
    """Commands graphics layer sends to game logic."""
    
    @abstractmethod
    def player_move(self, direction: str) -> None:
        """Move player (up/down/left/right)."""
        pass
    
    @abstractmethod
    def interact_with_npc(self, npc_id: str) -> None:
        """Start dialogue with NPC."""
        pass
    
    @abstractmethod
    def select_dialogue_option(self, option_id: str) -> None:
        """Choose dialogue branch."""
        pass
    
    @abstractmethod
    def start_combat(self, encounter_id: str) -> None:
        """Initiate battle."""
        pass
    
    @abstractmethod
    def execute_combat_action(self, action_id: str, target_id: str) -> None:
        """Execute combat action."""
        pass
    
    @abstractmethod
    def use_item(self, item_id: str, target_id: str) -> None:
        """Use item from inventory."""
        pass
    
    @abstractmethod
    def save_game(self, slot: int) -> None:
        """Save to slot."""
        pass
    
    @abstractmethod
    def load_game(self, slot: int) -> None:
        """Load from slot."""
        pass

class GameEventInterface(ABC):
    """Events game logic raises for graphics."""
    
    @abstractmethod
    def on_combat_started(self, encounter_data: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def on_enemy_defeated(self, enemy_id: str) -> None:
        pass
    
    @abstractmethod
    def on_damage_dealt(self, amount: int, target_id: str) -> None:
        pass
    
    @abstractmethod
    def on_dialogue_displayed(self, dialogue_text: str) -> None:
        pass
    
    @abstractmethod
    def on_inventory_changed(self, inventory: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def on_level_up(self, character_id: str) -> None:
        pass
    
    @abstractmethod
    def on_quest_completed(self, quest_id: str) -> None:
        pass
    
    @abstractmethod
    def on_ending_triggered(self, ending_id: str) -> None:
        pass
