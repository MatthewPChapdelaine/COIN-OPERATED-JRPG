"""
COIN:OPERATED JRPG - Integrated Game
Complete playable game bringing all systems together

Academic Subjects:
- Software Engineering: System integration, state management
- Game Design: Game loop, player interaction, progression
- Computer Science: Error handling, type safety, modularity

Complexity Guarantees:
- Game loop: O(1) per iteration
- Save/Load: O(n) for state size
- Combat: O(t*a) for t turns and a actors
- Quest updates: O(m) for m objectives
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Dict, Optional
from dataclasses import dataclass
import random

# AAA Standards
from aaa_standards.result_types import Result, Ok, Err
from aaa_standards.formal_specs import verify_complexity

# Core Systems
from core.game_engine import GameEngine, GameState
from core.character import create_coin, create_jinn_lir, create_orbius, create_typhus, create_coireena
from systems.combat import CombatSystem
from systems.progression import ProgressionSystem, Inventory, Equipment, EquipmentSlot, EquipmentRarity, Item
from systems.quest import QuestManager
from systems.dialogue import DialogueSystem, NPCManager
from systems.save_system import SaveSystem
from content.act1_content import initialize_act1_content
from content.enemies import EnemyFactory


@dataclass(frozen=True)
class GameConfig:
    """Immutable game configuration.
    
    Type Safety: Replaces scattered config values
    Immutability: Prevents accidental modification
    """
    max_party_size: int = 4
    max_save_slots: int = 10
    starting_location: str = "jinn_lir_sanctuary"
    starting_coins: int = 0
    starting_essence: int = 0
    newgame_plus_bonus_level: int = 5
    newgame_plus_bonus_coins: int = 500
    newgame_plus_bonus_essence: int = 100


class CoinOperatedJRPG(GameEngine):
    """Complete integrated COIN:OPERATED JRPG game with AAA standards.
    
    Design Pattern: Result-based Error Handling
    - All critical operations return Result types
    - Type-safe state management
    - Immutable configuration
    
    Performance:
    - Game loop: O(1) per iteration
    - Save: O(n) for state size
    - Load: O(n) for parsing
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize game with type-safe configuration.
        
        Args:
            config: Game configuration (uses defaults if None)
            
        Complexity: O(1) - system initialization
        Side Effects: Creates save directory
        """
        super().__init__()
        
        self._config = config or GameConfig()
        
        # Core systems
        self.combat_system = CombatSystem()
        self.progression = ProgressionSystem()
        self.quest_manager = QuestManager()
        self.dialogue_system = DialogueSystem()
        self.npc_manager = NPCManager()
        self.save_system = SaveSystem()
        
        # Game state
        self.coin: Optional[Coin] = None
        self.party_members: Dict[str, any] = {}
        self.active_party: List[any] = []
        self.current_location: str = self._config.starting_location
        self.locations_visited: List[str] = []
        self.playtime: int = 0
    
    @verify_complexity(time="O(1)", description="Initializes fixed number of systems")
    def initialize(self) -> Result[None, str]:
        """Initialize game with all systems.
        
        Returns:
            Success[None]: All systems initialized
            Failure[str]: Initialization failed
            
        Complexity: O(1) - fixed initialization steps
        Side Effects: Loads content, prints messages
        
        Postconditions:
            - All systems ready
            - Content loaded
            - Starter items created
        """
        if not super().initialize():
            return Err("Failed to initialize game engine")
        
        try:
            # Initialize content
            initialize_act1_content(self.quest_manager, self.dialogue_system, self.npc_manager)
            
            # Create starter equipment
            result = self._initialize_starter_items()
            if result.is_failure():
                return Err(f"Failed to create starter items: {result.unwrap_failure()}")
            
            print("✓ All systems initialized")
            print("✓ Act 1 content loaded")
            return Ok(None)
            
        except Exception as e:
            return Err(f"Initialization exception: {e}")
    
    @verify_complexity(time="O(1)", description="Creates fixed starter items")
    def _initialize_starter_items(self) -> Result[None, str]:
        """Initialize starter items and equipment.
        
        Returns:
            Success[None]: Items created
            Failure[str]: Creation failed
            
        Complexity: O(1) - creates fixed number of items
        Side Effects: Adds items to inventory
        """
        try:
            # Add starter healing items
            self.progression.inventory.add_item(
                Item("Healing Potion", "Restores 50 HP", "heal_hp", 50, quantity=3)
            )
            self.progression.inventory.add_item(
                Item("Magic Tonic", "Restores 30 MP", "heal_mp", 30, quantity=2)
            )
            
            # Add starter equipment
            starter_weapon = Equipment(
                "Wooden Staff",
                EquipmentSlot.WEAPON,
                EquipmentRarity.COMMON,
                "A basic wooden staff for casting magic",
                {'magic': 5, 'mp': 10}
            )
            self.progression.inventory.add_equipment(starter_weapon)
            
            return Ok(None)
            
        except Exception as e:
            return Err(f"Exception creating starter items: {e}")
    
    @verify_complexity(time="O(1)", description="Creates fixed party members")
    def new_game(self) -> Result[None, str]:
        """Start a new game with type-safe initialization.
        
        Returns:
            Success[None]: New game started
            Failure[str]: Failed to start
            
        Complexity: O(1) - creates fixed characters
        Side Effects: Prints intro, starts quest/dialogue
        
        Postconditions:
            - Coin created and in active_party
            - Starting location set
            - First quest started
        """
        super().new_game()
        
        try:
            # Create Coin (protagonist)
            self.coin = create_coin(age_state="young")
            self.player = self.coin
            self.active_party = [self.coin]
            
            # Create other party members (not yet recruited)
            self.party_members = {
                'jinn_lir': create_jinn_lir(),
                'orbius': create_orbius(),
                'typhus': create_typhus(),
                'coireena': create_coireena()
            }
            
            # Set starting location
            self.current_location = self._config.starting_location
            self.progression.discover_location(self.current_location)
            
            # Show opening
            print("\n" + "=" * 60)
            print(" " * 15 + "ACT I: ORIGINS & EXPLOITATION")
            print(" " * 18 + "City of Acadmium")
            print("=" * 60)
            
            input("\nPress Enter to begin your journey...")
            
            # Start first quest and dialogue
            self.quest_manager.start_quest("act1_main_01")
            self.dialogue_system.start_dialogue(
                "jinn_lir_awakening",
                self._get_game_state()
            )
            
            return Ok(None)
            
        except Exception as e:
            return Err(f"Failed to start new game: {e}")
    
    def new_game_plus(self):
        """Start New Game+ with retained abilities"""
        super().new_game_plus()
        self.new_game()
        
        # Bonus starting resources for NG+
        self.progression.inventory.add_currency(coins=500, essence=100)
        self.coin.stats.level = 5
        self.coin.stats.max_hp += 50
        self.coin.stats.max_mp += 30
        self.coin.stats.current_hp = self.coin.stats.max_hp
        self.coin.stats.current_mp = self.coin.stats.max_mp
        
        print("\n✨ New Game+ bonuses applied!")
        print("  Starting Level: 5")
        print("  Bonus Currency: 500 coins, 100 essence")
    
    def game_loop(self):
        """Enhanced main game loop"""
        print(f"\n{'=' * 60}")
        print(f"Location: {self.current_location.replace('_', ' ').title()}")
        print(f"Act {self.game_progress['act']}")
        print(f"{'=' * 60}")
        
        # Show active quests
        if self.quest_manager.active_quests:
            print(f"\n[Active Quest: {self.quest_manager.active_quests[0].name}]")
        
        print(f"\n{self.coin.name} - HP: {self.coin.stats.current_hp}/{self.coin.stats.max_hp} | MP: {self.coin.stats.current_mp}/{self.coin.stats.max_mp}")
        print(f"Level {self.coin.stats.level} | Coins: {self.progression.inventory.domminnian_coins} | Essence: {self.progression.inventory.magical_essence}")
        
        print("\n1. Explore Area")
        print("2. Quest Log")
        print("3. Party Status")
        print("4. Inventory")
        print("5. Faction Reputation")
        print("6. Rest (Restore HP/MP)")
        print("7. Save Game")
        print("8. Main Menu")
        
        choice = input("\nWhat will you do? ").strip()
        
        if choice == "1":
            self.explore_area()
        elif choice == "2":
            self.show_quest_log()
        elif choice == "3":
            self.show_party_status()
        elif choice == "4":
            self.progression.inventory.display()
            input("\nPress Enter to continue...")
        elif choice == "5":
            self.progression.faction_reputation.display()
            input("\nPress Enter to continue...")
        elif choice == "6":
            self.rest()
        elif choice == "7":
            self.save_game_menu()
        elif choice == "8":
            self.state = GameState.MAIN_MENU
        else:
            print("Invalid choice.")
    
    def explore_area(self):
        """Explore current area"""
        print(f"\n{'=' * 60}")
        print(f"Exploring: {self.current_location.replace('_', ' ').title()}")
        print(f"{'=' * 60}")
        
        # Get NPCs in area
        npcs = self.npc_manager.get_npcs_at_location(self.current_location)
        
        if npcs:
            print(f"\nPeople here:")
            for i, npc in enumerate(npcs, 1):
                print(f"  {i}. {npc.name} - {npc.description}")
        
        print(f"\nOptions:")
        print("1. Talk to someone")
        print("2. Look for enemies (Battle)")
        print("3. Search for items")
        print("4. Travel to different location")
        print("5. Return")
        
        choice = input("\nChoose action: ").strip()
        
        if choice == "1" and npcs:
            self.talk_to_npc(npcs)
        elif choice == "2":
            self.random_encounter()
        elif choice == "3":
            self.search_for_items()
        elif choice == "4":
            self.travel()
        elif choice == "5":
            return
        else:
            print("Invalid choice or no NPCs here.")
            input("\nPress Enter to continue...")
    
    def talk_to_npc(self, npcs):
        """Talk to an NPC"""
        print("\nWho do you want to talk to?")
        for i, npc in enumerate(npcs, 1):
            print(f"{i}. {npc.name}")
        print(f"{len(npcs) + 1}. Cancel")
        
        try:
            choice = int(input("\nChoice: ").strip())
            if 1 <= choice <= len(npcs):
                npc = npcs[choice - 1]
                print(f"\n{npc.interact()}")
                
                # Check for available dialogues
                dialogues = npc.get_available_dialogue(self._get_game_state())
                if dialogues:
                    print(f"\n[Dialogue available]")
                    self.dialogue_system.start_dialogue(dialogues[0], self._get_game_state())
                
                # Check for quests
                if npc.quest_ids:
                    available_quests = [
                        q for q in self.quest_manager.all_quests.values()
                        if q.quest_id in npc.quest_ids and q.status.value == "not_started"
                    ]
                    if available_quests:
                        print(f"\n[Quest available: {available_quests[0].name}]")
                        accept = input("Accept quest? (y/n): ").strip().lower()
                        if accept == 'y':
                            self.quest_manager.start_quest(available_quests[0].quest_id)
                
                input("\nPress Enter to continue...")
        except ValueError:
            pass
    
    def random_encounter(self):
        """Trigger a random combat encounter"""
        print("\nSearching for enemies...")
        
        # Determine encounter difficulty based on quest progress
        encounter_types = ['random_encounter_easy', 'random_encounter_medium']
        if self.coin.stats.level >= 3:
            encounter_types.append('random_encounter_hard')
        
        encounter = random.choice(encounter_types)
        enemies = EnemyFactory.create_encounter(encounter, self.coin.stats.level)
        
        print(f"\n⚔️ Encountered: {', '.join([e.name for e in enemies])}!")
        input("Press Enter to begin combat...")
        
        # Start combat
        result = self.combat_system.run_combat(self.active_party, enemies)
        
        # Process results
        if result['result'] == 'victory':
            self.progression.inventory.add_currency(
                coins=result.get('coins', 0),
                essence=result.get('exp', 0) // 10  # Convert some exp to essence
            )
            # Update quest objectives
            for enemy in enemies:
                self.quest_manager.update_quest_objective('defeat', enemy.name.lower().replace(' ', '_'), 1)
        
        input("\nPress Enter to continue...")
    
    def search_for_items(self):
        """Search area for items"""
        print("\nSearching the area...")
        
        # Random chance to find items
        if random.random() < 0.5:
            # Found something!
            items = [
                Item("Healing Potion", "Restores 50 HP", "heal_hp", 50),
                Item("Magic Tonic", "Restores 30 MP", "heal_mp", 30),
            ]
            found_item = random.choice(items)
            self.progression.inventory.add_item(found_item)
            print(f"\n✨ Found: {found_item.name}!")
        else:
            coins_found = random.randint(10, 50)
            self.progression.inventory.add_currency(coins=coins_found)
            print(f"\n✨ Found {coins_found} Domminnian Coins!")
        
        input("\nPress Enter to continue...")
    
    def travel(self):
        """Travel to a different location"""
        locations = {
            '1': ('acadmium_city_center', 'Acadmium City Center'),
            '2': ('jinn_lir_sanctuary', "Jinn-Lir's Sanctuary"),
            '3': ('lifeblood_temple', 'Lifeblood Temple'),
            '4': ('acadmium_outskirts', 'Acadmium Outskirts'),
            '5': ('light_cabal_headquarters', 'Light Cabal Headquarters')
        }
        
        print("\nTravel to:")
        for key, (loc_id, loc_name) in locations.items():
            marker = "✓" if loc_id in self.locations_visited else "?"
            print(f"{key}. {loc_name} {marker}")
        print("6. Cancel")
        
        choice = input("\nWhere to? ").strip()
        
        if choice in locations:
            loc_id, loc_name = locations[choice]
            self.current_location = loc_id
            if loc_id not in self.locations_visited:
                self.progression.discover_location(loc_name)
                self.locations_visited.append(loc_id)
            print(f"\nTraveled to {loc_name}")
            input("Press Enter to continue...")
    
    def show_quest_log(self):
        """Show quest log"""
        self.quest_manager.display_active_quests()
        print("\n" + "-" * 60)
        self.quest_manager.display_completed_quests()
        input("\nPress Enter to continue...")
    
    def show_party_status(self):
        """Show party member status"""
        print(f"\n{'=' * 60}")
        print(" " * 20 + "PARTY STATUS")
        print(f"{'=' * 60}")
        
        for i, member in enumerate(self.active_party, 1):
            print(f"\n{i}. {member.name} - Level {member.stats.level} {member.role.value}")
            print(f"   HP: {member.stats.current_hp}/{member.stats.max_hp} | MP: {member.stats.current_mp}/{member.stats.max_mp}")
            print(f"   EXP: {member.exp}/{member.exp_to_next_level}")
        
        print("\n1. View detailed status")
        print("2. Return")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            try:
                member_num = int(input("Which party member? ")) - 1
                if 0 <= member_num < len(self.active_party):
                    self.active_party[member_num].display_status()
            except:
                pass
        
        input("\nPress Enter to continue...")
    
    def rest(self):
        """Rest to restore HP/MP"""
        print("\nResting...")
        for member in self.active_party:
            member.stats.current_hp = member.stats.max_hp
            member.stats.current_mp = member.stats.max_mp
        print("✨ Party fully restored!")
        
        # Auto-save after resting
        self.save_system.auto_save(self._serialize_game_state())
        
        input("\nPress Enter to continue...")
    
    def save_game_menu(self):
        """Save game menu"""
        self.save_system.display_saves()
        
        print("\nSave to which slot? (1-10, or 0 to cancel)")
        try:
            slot = int(input("Slot: ").strip())
            if slot == 0:
                return
            
            if self.save_system.save_game(slot, self._serialize_game_state()):
                print("Game saved successfully!")
        except ValueError:
            print("Invalid slot number.")
        
        input("\nPress Enter to continue...")
    
    def _get_game_state(self) -> dict:
        """Get current game state for dialogues and choices"""
        return {
            'faction_reputation': self.progression.faction_reputation.reputations,
            'story_flags': self.game_progress['story_flags'],
            'inventory': [item.name for item in self.progression.inventory.items.values()],
            'level': self.coin.stats.level if self.coin else 1
        }
    
    def _serialize_game_state(self) -> dict:
        """Serialize complete game state for saving"""
        return {
            'playtime': self.playtime,
            'game_progress': self.game_progress,
            'current_location': self.current_location,
            'locations_visited': self.locations_visited,
            'player': self.coin.to_dict() if self.coin else None,
            'active_party': [m.to_dict() for m in self.active_party],
            'party_members': {k: v.to_dict() for k, v in self.party_members.items()},
            'progression': self.progression.to_dict(),
            'quest_manager': self.quest_manager.to_dict()
        }


def main():
    """Entry point"""
    game = CoinOperatedJRPG()
    game.run()


if __name__ == "__main__":
    main()
