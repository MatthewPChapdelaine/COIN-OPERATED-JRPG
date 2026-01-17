"""
Type-Safe Interfaces (AAA Standard)

Replaces Dict[str, Any] with proper typed interfaces.
All interfaces use immutable data types for thread safety.

Complexity: O(1) for all interface methods
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, FrozenSet
from .type_definitions import (
    Location, CharacterData, CombatData, QuestData,
    ItemData, Position, CombatAction
)
from .result_types import Result
from .formal_specs import verify_complexity


class GameStateInterface(ABC):
    """
    Read-only interface to game state.
    
    All methods are O(1) for real-time rendering.
    Returns immutable data to prevent state corruption.
    
    Mathematical Property: Pure functions (no side effects)
    Thread Safety: Yes (read-only, immutable returns)
    """
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_player_location(self) -> Location:
        """
        Get current player location with full type safety.
        
        Returns:
            Location object (immutable)
        
        Complexity: O(1)
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_player_position(self) -> Position:
        """
        Get player's current position in location.
        
        Returns:
            Position object (immutable)
        
        Complexity: O(1)
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_player_character(self) -> CharacterData:
        """
        Get player character data.
        
        Returns:
            CharacterData (immutable)
        
        Complexity: O(1)
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_party_members(self) -> Tuple[CharacterData, ...]:
        """
        Get current party members.
        
        Returns:
            Immutable tuple of CharacterData
        
        Complexity: O(1) - returns cached tuple
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_current_encounter(self) -> Optional[CombatData]:
        """
        Get current battle state if in combat.
        
        Returns:
            CombatData if in combat, None otherwise
        
        Complexity: O(1)
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_available_actions(self) -> Tuple[str, ...]:
        """
        Get valid player actions for current context.
        
        Returns:
            Immutable tuple of action names
        
        Complexity: O(1) - pre-computed based on state
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_active_quests(self) -> Tuple[QuestData, ...]:
        """
        Get all active quests.
        
        Returns:
            Immutable tuple of QuestData
        
        Complexity: O(1) - returns cached tuple
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_quest_by_id(self, quest_id: str) -> Result[QuestData, str]:
        """
        Get quest data by ID.
        
        Args:
            quest_id: Quest identifier
        
        Returns:
            Success(QuestData) or Failure(error_message)
        
        Complexity: O(1) - hash table lookup
        Thread Safety: Yes
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get_inventory(self) -> Tuple[ItemData, ...]:
        """
        Get player inventory.
        
        Returns:
            Immutable tuple of ItemData
        
        Complexity: O(1) - returns cached tuple
        Thread Safety: Yes
        """
        pass


class GameCommandInterface(ABC):
    """
    Command interface for game logic modifications.
    
    All commands use Result types for explicit error handling.
    No exceptions thrown across interface boundary.
    
    Mathematical Property: Commands as effect descriptions
    Thread Safety: Requires external synchronization
    """
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def player_move(self, direction: str) -> Result[Position, str]:
        """
        Move player in specified direction.
        
        Args:
            direction: 'up', 'down', 'left', 'right'
        
        Returns:
            Success(new_position) or Failure(error_message)
        
        Complexity: O(1) - position update and collision check
        Thread Safety: No - requires synchronization
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def interact_with_npc(self, npc_id: str) -> Result[str, str]:
        """
        Start dialogue with NPC.
        
        Args:
            npc_id: NPC identifier
        
        Returns:
            Success(dialogue_id) or Failure(error_message)
        
        Complexity: O(1) - hash table lookup
        Thread Safety: No - modifies game state
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def select_dialogue_option(self, option_id: str) -> Result[str, str]:
        """
        Choose dialogue branch.
        
        Args:
            option_id: Dialogue option identifier
        
        Returns:
            Success(next_dialogue_id) or Failure(error_message)
        
        Complexity: O(1)
        Thread Safety: No
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(log n)", space="O(1)", realtime_safe=True)
    def start_combat(self, encounter_id: str) -> Result[CombatData, str]:
        """
        Initiate battle.
        
        Args:
            encounter_id: Combat encounter identifier
        
        Returns:
            Success(CombatData) or Failure(error_message)
        
        Complexity: O(log n) for turn order sorting
        Thread Safety: No
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def execute_combat_action(self, action: CombatAction) -> Result[CombatData, str]:
        """
        Execute combat action.
        
        Args:
            action: CombatAction object
        
        Returns:
            Success(updated_CombatData) or Failure(error_message)
        
        Complexity: O(1) - direct stat manipulation
        Thread Safety: No
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def use_item(self, item_id: str, target_id: str) -> Result[CharacterData, str]:
        """
        Use item from inventory.
        
        Args:
            item_id: Item identifier
            target_id: Target character identifier
        
        Returns:
            Success(updated_CharacterData) or Failure(error_message)
        
        Complexity: O(1)
        Thread Safety: No
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(n)", space="O(n)", realtime_safe=False)
    def save_game(self, slot: int) -> Result[str, str]:
        """
        Save game to slot.
        
        Args:
            slot: Save slot number (1-10)
        
        Returns:
            Success(save_file_path) or Failure(error_message)
        
        Complexity: O(n) where n = save data size (I/O bound)
        Thread Safety: No - file system access
        """
        pass
    
    @abstractmethod
    @verify_complexity(time="O(n)", space="O(n)", realtime_safe=False)
    def load_game(self, slot: int) -> Result[Location, str]:
        """
        Load game from slot.
        
        Args:
            slot: Save slot number (1-10)
        
        Returns:
            Success(starting_location) or Failure(error_message)
        
        Complexity: O(n) where n = save data size (I/O bound)
        Thread Safety: No - modifies entire game state
        """
        pass


class GameEventInterface(ABC):
    """
    Event interface for game logic notifications to graphics layer.
    
    Observer pattern with typed events.
    Graphics layer implements these to receive notifications.
    
    Mathematical Property: Side effects only in graphics layer
    Thread Safety: Implementation dependent
    """
    
    @abstractmethod
    def on_combat_started(self, combat: CombatData) -> None:
        """
        Notification: Combat has begun.
        
        Args:
            combat: Complete combat state
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_combat_ended(self, victory: bool, rewards: Tuple[ItemData, ...]) -> None:
        """
        Notification: Combat has ended.
        
        Args:
            victory: True if player won
            rewards: Items gained from combat
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_dialogue_started(self, npc_id: str, dialogue_text: str) -> None:
        """
        Notification: Dialogue initiated.
        
        Args:
            npc_id: NPC identifier
            dialogue_text: Initial dialogue text
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_quest_updated(self, quest: QuestData) -> None:
        """
        Notification: Quest progress changed.
        
        Args:
            quest: Updated quest data
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_level_up(self, character: CharacterData, new_level: int) -> None:
        """
        Notification: Character leveled up.
        
        Args:
            character: Character who leveled up
            new_level: New level number
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_item_obtained(self, item: ItemData) -> None:
        """
        Notification: Item added to inventory.
        
        Args:
            item: Item obtained
        
        Complexity: Implementation dependent
        """
        pass
    
    @abstractmethod
    def on_location_changed(self, old_location: Location, new_location: Location) -> None:
        """
        Notification: Player moved to new location.
        
        Args:
            old_location: Previous location
            new_location: Current location
        
        Complexity: Implementation dependent
        """
        pass


# Example implementation stub
class ExampleGameState(GameStateInterface):
    """Example implementation showing proper typing"""
    
    def __init__(self):
        self._player_loc = Location(
            id="test", name="Test", description="Test location",
            position=Position(0, 0), region="test"
        )
        self._player_pos = Position(5, 5)
    
    def get_player_location(self) -> Location:
        return self._player_loc
    
    def get_player_position(self) -> Position:
        return self._player_pos
    
    def get_player_character(self) -> CharacterData:
        from .type_definitions import CharacterStats
        stats = CharacterStats(
            level=1, max_hp=100, current_hp=100,
            max_mp=50, current_mp=50,
            strength=10, magic=10, defense=10,
            magic_defense=10, speed=10, luck=10
        )
        return CharacterData(
            name="Hero", role="hero",
            faction="independent",
            description="Player character",
            stats=stats,
            abilities=tuple(),
            equipment={},
            exp=0,
            exp_to_next_level=100
        )
    
    def get_party_members(self) -> Tuple[CharacterData, ...]:
        return ()
    
    def get_current_encounter(self) -> Optional[CombatData]:
        return None
    
    def get_available_actions(self) -> Tuple[str, ...]:
        return ("move", "interact", "menu")
    
    def get_active_quests(self) -> Tuple[QuestData, ...]:
        return ()
    
    def get_quest_by_id(self, quest_id: str) -> Result[QuestData, str]:
        from .result_types import Err
        return Err(f"Quest {quest_id} not found")
    
    def get_inventory(self) -> Tuple[ItemData, ...]:
        return ()


if __name__ == "__main__":
    # Test interface implementation
    state = ExampleGameState()
    
    loc = state.get_player_location()
    assert isinstance(loc, Location)
    assert loc.name == "Test"
    
    pos = state.get_player_position()
    assert isinstance(pos, Position)
    assert pos.x == 5 and pos.y == 5
    
    char = state.get_player_character()
    assert isinstance(char, CharacterData)
    assert char.stats.is_alive()
    
    print("✓ All type-safe interface tests passed")
