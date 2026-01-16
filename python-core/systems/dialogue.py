"""
COIN:OPERATED JRPG - Dialogue System
Manages NPC interactions and story dialogue
"""

from typing import Dict, List, Optional, Callable
from enum import Enum


class DialogueChoice:
    """A dialogue choice option"""
    
    def __init__(self, text: str, next_node: Optional[str] = None, 
                 requirement: Optional[Dict] = None, consequence: Optional[Callable] = None):
        self.text = text
        self.next_node = next_node
        self.requirement = requirement or {}  # faction_rep, items, etc.
        self.consequence = consequence  # Function to execute if chosen
    
    def is_available(self, game_state: Dict) -> bool:
        """Check if choice is available based on requirements"""
        # Check faction reputation requirements
        if 'faction_rep' in self.requirement:
            for faction, required_rep in self.requirement['faction_rep'].items():
                if game_state.get('faction_reputation', {}).get(faction, 0) < required_rep:
                    return False
        
        # Check item requirements
        if 'items' in self.requirement:
            for item in self.requirement['items']:
                if item not in game_state.get('inventory', []):
                    return False
        
        # Check story flags
        if 'flags' in self.requirement:
            for flag, required_value in self.requirement['flags'].items():
                if game_state.get('story_flags', {}).get(flag) != required_value:
                    return False
        
        return True


class DialogueNode:
    """A node in a dialogue tree"""
    
    def __init__(self, node_id: str, speaker: str, text: str, 
                 choices: Optional[List[DialogueChoice]] = None,
                 auto_next: Optional[str] = None):
        self.node_id = node_id
        self.speaker = speaker
        self.text = text
        self.choices = choices or []
        self.auto_next = auto_next  # Automatically advance to next node


class Dialogue:
    """Complete dialogue interaction"""
    
    def __init__(self, dialogue_id: str, title: str, start_node: str):
        self.dialogue_id = dialogue_id
        self.title = title
        self.start_node = start_node
        self.nodes: Dict[str, DialogueNode] = {}
        self.current_node: Optional[DialogueNode] = None
    
    def add_node(self, node: DialogueNode):
        """Add a node to the dialogue"""
        self.nodes[node.node_id] = node
    
    def start(self) -> Optional[DialogueNode]:
        """Start the dialogue"""
        if self.start_node in self.nodes:
            self.current_node = self.nodes[self.start_node]
            return self.current_node
        return None
    
    def advance(self, choice_index: int = 0) -> Optional[DialogueNode]:
        """Advance to next node based on choice"""
        if not self.current_node:
            return None
        
        # Auto-advance if no choices
        if self.current_node.auto_next:
            next_node_id = self.current_node.auto_next
        elif self.current_node.choices and choice_index < len(self.current_node.choices):
            choice = self.current_node.choices[choice_index]
            next_node_id = choice.next_node
            
            # Execute consequence
            if choice.consequence:
                choice.consequence()
        else:
            return None  # End of dialogue
        
        if next_node_id and next_node_id in self.nodes:
            self.current_node = self.nodes[next_node_id]
            return self.current_node
        else:
            self.current_node = None
            return None


class DialogueSystem:
    """Manages all dialogues in the game"""
    
    def __init__(self):
        self.dialogues: Dict[str, Dialogue] = {}
        self.active_dialogue: Optional[Dialogue] = None
        self.game_state: Dict = {}
    
    def register_dialogue(self, dialogue: Dialogue):
        """Register a dialogue"""
        self.dialogues[dialogue.dialogue_id] = dialogue
    
    def start_dialogue(self, dialogue_id: str, game_state: Dict) -> bool:
        """Start a dialogue"""
        if dialogue_id in self.dialogues:
            self.active_dialogue = self.dialogues[dialogue_id]
            self.game_state = game_state
            node = self.active_dialogue.start()
            if node:
                self.display_node(node)
                return True
        return False
    
    def display_node(self, node: DialogueNode):
        """Display a dialogue node"""
        print(f"\n{'=' * 60}")
        print(f"{node.speaker}:")
        print(f"{'=' * 60}")
        print(f"\n{node.text}\n")
        
        if node.choices:
            available_choices = [
                (i, choice) for i, choice in enumerate(node.choices)
                if choice.is_available(self.game_state)
            ]
            
            if available_choices:
                for i, (original_index, choice) in enumerate(available_choices, 1):
                    print(f"{i}. {choice.text}")
                
                while True:
                    try:
                        choice_num = int(input("\nYour choice: ").strip())
                        if 1 <= choice_num <= len(available_choices):
                            original_index = available_choices[choice_num - 1][0]
                            self.advance_dialogue(original_index)
                            break
                        else:
                            print("Invalid choice number.")
                    except ValueError:
                        print("Please enter a number.")
            else:
                print("[No available choices - dialogue ends]")
                self.active_dialogue = None
        elif node.auto_next:
            input("\nPress Enter to continue...")
            self.advance_dialogue()
        else:
            # End of dialogue
            input("\nPress Enter to continue...")
            self.active_dialogue = None
    
    def advance_dialogue(self, choice_index: int = 0):
        """Advance the active dialogue"""
        if self.active_dialogue:
            next_node = self.active_dialogue.advance(choice_index)
            if next_node:
                self.display_node(next_node)
            else:
                print("\n[End of conversation]")
                self.active_dialogue = None
    
    def is_dialogue_active(self) -> bool:
        """Check if dialogue is currently active"""
        return self.active_dialogue is not None


class NPC:
    """Non-playable character"""
    
    def __init__(self, npc_id: str, name: str, description: str, 
                 location: str, faction: str = "independent"):
        self.npc_id = npc_id
        self.name = name
        self.description = description
        self.location = location
        self.faction = faction
        self.dialogue_ids: List[str] = []
        self.quest_ids: List[str] = []
        self.default_dialogue = f"{name}: Hello, traveler."
    
    def add_dialogue(self, dialogue_id: str):
        """Add a dialogue option for this NPC"""
        self.dialogue_ids.append(dialogue_id)
    
    def add_quest(self, quest_id: str):
        """Add a quest this NPC offers"""
        self.quest_ids.append(quest_id)
    
    def get_available_dialogue(self, game_state: Dict) -> List[str]:
        """Get available dialogues based on game state"""
        # Simple implementation - return all dialogues
        # Could be enhanced to check story flags, reputation, etc.
        return self.dialogue_ids
    
    def interact(self) -> str:
        """Get default interaction text"""
        return self.default_dialogue


class NPCManager:
    """Manages all NPCs in the game"""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.location_npcs: Dict[str, List[NPC]] = {}
    
    def register_npc(self, npc: NPC):
        """Register an NPC"""
        self.npcs[npc.npc_id] = npc
        
        # Add to location index
        if npc.location not in self.location_npcs:
            self.location_npcs[npc.location] = []
        self.location_npcs[npc.location].append(npc)
    
    def get_npcs_at_location(self, location: str) -> List[NPC]:
        """Get all NPCs at a location"""
        return self.location_npcs.get(location, [])
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """Get NPC by ID"""
        return self.npcs.get(npc_id)
