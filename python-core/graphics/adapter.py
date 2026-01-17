"""Graphics-Logic Adapter: Implements interfaces to prevent direct coupling."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from interfaces import GameStateInterface, GameCommandInterface, GameEventInterface
from typing import Dict, List, Any, Optional


class GraphicsAdapter(GameStateInterface, GameCommandInterface):
    """Adapter between graphics and game logic.
    
    This adapter is the ONLY connection between graphics and game logic.
    Graphics layer never imports from core/systems/content directly.
    """
    
    def __init__(self, game_engine):
        """Initialize adapter with game engine.
        
        Args:
            game_engine: The core GameEngine instance
        """
        self.engine = game_engine
        self.event_listeners = []
    
    def register_event_listener(self, listener: GameEventInterface):
        """Register for game events.
        
        Args:
            listener: Object implementing GameEventInterface
        """
        self.event_listeners.append(listener)
    
    def _notify_listeners(self, event_name: str, *args, **kwargs):
        """Notify all registered listeners of an event."""
        for listener in self.event_listeners:
            if hasattr(listener, event_name):
                getattr(listener, event_name)(*args, **kwargs)
    
    # GameStateInterface implementation - READ ONLY access to game state
    
    def get_player_location(self) -> Dict[str, Any]:
        """Get current player location data."""
        # Get player coordinates
        x = getattr(self.engine, 'player_x', 5)
        y = getattr(self.engine, 'player_y', 5)
        
        location_name = self.engine.current_location if self.engine.current_location else 'Acadmium City'
        
        return {
            'name': location_name if isinstance(location_name, str) else getattr(location_name, 'name', 'Unknown'),
            'description': 'Explore the city and seek adventures',
            'nearby_npcs': [],
            'x': x,
            'y': y
        }
    
    def get_party_members(self) -> List[Dict[str, Any]]:
        """Get current party with stats, equipment, abilities."""
        party_data = []
        
        # Include player
        if self.engine.player:
            party_data.append(self._character_to_dict(self.engine.player))
        
        # Include party members
        for member in self.engine.party:
            party_data.append(self._character_to_dict(member))
        
        return party_data
    
    def _character_to_dict(self, character) -> Dict[str, Any]:
        """Convert character object to dictionary."""
        return {
            'name': getattr(character, 'name', 'Unknown'),
            'level': getattr(character, 'level', 1),
            'current_hp': getattr(getattr(character, 'stats', None), 'current_hp', 100),
            'max_hp': getattr(getattr(character, 'stats', None), 'max_hp', 100),
            'current_mp': getattr(getattr(character, 'stats', None), 'current_mp', 50),
            'max_mp': getattr(getattr(character, 'stats', None), 'max_mp', 50),
            'role': getattr(character, 'role', 'Unknown'),
            'faction': getattr(character, 'faction', 'Unknown')
        }
    
    def get_current_encounter(self) -> Optional[Dict[str, Any]]:
        """Get current battle state if in combat."""
        from core.game_engine import GameState
        
        if self.engine.state != GameState.COMBAT:
            return None
        
        # Get combat system data
        if not hasattr(self.engine, 'combat_system') or not self.engine.combat_system:
            return None
        
        combat = self.engine.combat_system
        
        return {
            'turn': getattr(combat, 'turn', 0),
            'phase': getattr(combat, 'phase', 'player_turn'),
            'enemies': [self._enemy_to_dict(e) for e in getattr(combat, 'enemies', [])],
            'active_character': getattr(combat, 'active_character', None)
        }
    
    def _enemy_to_dict(self, enemy) -> Dict[str, Any]:
        """Convert enemy object to dictionary."""
        return {
            'id': getattr(enemy, 'enemy_id', 'unknown'),
            'name': getattr(enemy, 'name', 'Enemy'),
            'current_hp': getattr(enemy, 'current_hp', 100),
            'max_hp': getattr(enemy, 'max_hp', 100),
            'level': getattr(enemy, 'level', 1)
        }
    
    def get_available_actions(self) -> List[str]:
        """Get valid player actions for current context."""
        from core.game_engine import GameState
        
        actions = []
        
        if self.engine.state == GameState.IN_GAME:
            actions.extend(['move_up', 'move_down', 'move_left', 'move_right'])
            actions.append('interact')
            actions.append('inventory')
            actions.append('save')
        elif self.engine.state == GameState.COMBAT:
            actions.extend(['attack', 'skill', 'item', 'defend'])
        elif self.engine.state == GameState.DIALOGUE:
            actions.append('advance_dialogue')
        elif self.engine.state == GameState.MAIN_MENU:
            actions.extend(['new_game', 'load_game', 'quit'])
        
        return actions
    
    def get_ui_elements(self) -> Dict[str, Any]:
        """Get current menu/UI state."""
        return {
            'messages': getattr(self.engine, 'message_log', []),
            'current_menu': getattr(self.engine, 'current_menu', None),
            'game_state': self.engine.state.value if hasattr(self.engine.state, 'value') else str(self.engine.state)
        }
    
    def get_asset_requirements(self) -> Dict[str, List[str]]:
        """Get assets needed for current state."""
        assets = {
            'sprites': [],
            'tilesets': [],
            'ui': []
        }
        
        # Player sprite
        if self.engine.player:
            assets['sprites'].append(f"character_{self.engine.player.name.lower()}")
        
        # Party sprites
        for member in self.engine.party:
            assets['sprites'].append(f"character_{member.name.lower()}")
        
        # Enemy sprites in combat
        from core.game_engine import GameState
        if self.engine.state == GameState.COMBAT:
            if hasattr(self.engine, 'combat_system') and self.engine.combat_system:
                for enemy in getattr(self.engine.combat_system, 'enemies', []):
                    assets['sprites'].append(f"enemy_{getattr(enemy, 'enemy_id', 'unknown')}")
        
        return assets
    
    def get_quest(self, quest_id: str) -> Dict[str, Any]:
        """Get quest data by ID (read-only)."""
        # Access quest from systems
        if hasattr(self.engine, 'quest_system') and self.engine.quest_system:
            quest = self.engine.quest_system.get_quest(quest_id)
            if quest:
                return {
                    'id': quest_id,
                    'title': getattr(quest, 'title', 'Unknown Quest'),
                    'description': getattr(quest, 'description', ''),
                    'status': getattr(quest, 'status', 'active')
                }
        
        return {'id': quest_id, 'title': 'Unknown Quest', 'description': '', 'status': 'unknown'}
    
    def get_enemy(self, enemy_id: str) -> Dict[str, Any]:
        """Get enemy data by ID (read-only)."""
        # This would access enemy definitions from content
        return {
            'id': enemy_id,
            'name': enemy_id.replace('_', ' ').title(),
            'description': ''
        }
    
    # GameCommandInterface implementation - Commands TO game logic
    
    def player_move(self, direction: str) -> None:
        """Move player in specified direction.
        
        Args:
            direction: 'up', 'down', 'left', or 'right'
        """
        # Delegate to game engine's movement system
        if hasattr(self.engine, 'handle_movement'):
            self.engine.handle_movement(direction)
    
    def interact_with_npc(self, npc_id: str) -> None:
        """Start dialogue with NPC.
        
        Args:
            npc_id: ID of NPC to interact with
        """
        if hasattr(self.engine, 'dialogue_system'):
            self.engine.dialogue_system.start_dialogue(npc_id)
            self._notify_listeners('on_dialogue_displayed', f"Talking to {npc_id}")
    
    def select_dialogue_option(self, option_id: str) -> None:
        """Choose dialogue branch.
        
        Args:
            option_id: ID of dialogue option
        """
        if hasattr(self.engine, 'dialogue_system'):
            self.engine.dialogue_system.select_option(option_id)
    
    def start_combat(self, encounter_id: str) -> None:
        """Initiate battle.
        
        Args:
            encounter_id: ID of encounter to start
        """
        if hasattr(self.engine, 'combat_system'):
            self.engine.combat_system.start_encounter(encounter_id)
            encounter_data = {'encounter_id': encounter_id}
            self._notify_listeners('on_combat_started', encounter_data)
    
    def execute_combat_action(self, action_id: str, target_id: str) -> None:
        """Execute combat action.
        
        Args:
            action_id: ID of action to perform
            target_id: ID of target
        """
        if hasattr(self.engine, 'combat_system'):
            result = self.engine.combat_system.execute_action(action_id, target_id)
            
            # Notify listeners of results
            if result and 'damage' in result:
                self._notify_listeners('on_damage_dealt', result['damage'], target_id)
            if result and 'enemy_defeated' in result:
                self._notify_listeners('on_enemy_defeated', target_id)
    
    def use_item(self, item_id: str, target_id: str) -> None:
        """Use item from inventory.
        
        Args:
            item_id: ID of item to use
            target_id: ID of target character
        """
        if hasattr(self.engine, 'inventory_system'):
            self.engine.inventory_system.use_item(item_id, target_id)
            self._notify_listeners('on_inventory_changed', self.engine.inventory_system.get_inventory())
    
    def save_game(self, slot: int) -> None:
        """Save game to slot.
        
        Args:
            slot: Save slot number
        """
        if hasattr(self.engine, 'save_system'):
            self.engine.save_system.save_game(slot)
    
    def load_game(self, slot: int) -> None:
        """Load game from slot.
        
        Args:
            slot: Save slot number
        """
        if hasattr(self.engine, 'save_system'):
            self.engine.save_system.load_game(slot)
