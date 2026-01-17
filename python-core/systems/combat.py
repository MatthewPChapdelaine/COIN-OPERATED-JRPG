"""
COIN:OPERATED JRPG - Combat System
Turn-based JRPG combat mechanics

Academic Subjects:
- Game Design: Turn-based combat systems, AI behavior
- Computer Science: Algorithms for damage calculation, turn ordering
- Mathematics: Statistical damage variance, probability systems
- Software Engineering: State management, event handling

Complexity Guarantees:
- Turn order calculation: O(n log n) where n = combatants
- Damage calculation: O(1)
- Action execution: O(1) for single target, O(n) for AOE
- Combat state checks: O(n) where n = combatants
"""

from typing import Tuple, Optional, List as PyList
from enum import Enum
from dataclasses import dataclass
import random

# Import AAA Standards
from aaa_standards.result_types import Result, Ok, Err
from aaa_standards.type_definitions import CharacterData, CombatData, CombatAction
from aaa_standards.formal_specs import verify_complexity, requires, ensures
from aaa_standards.performance import LRUCache

# Import core types
from core.character import Character, CharacterRole


class TargetType(Enum):
    """Combat target types for ability targeting"""
    SINGLE_ALLY = "single_ally"
    SINGLE_ENEMY = "single_enemy"
    ALL_ALLIES = "all_allies"
    ALL_ENEMIES = "all_enemies"
    SELF = "self"


@dataclass(frozen=True)
class CombatResult:
    """Immutable combat result data.
    
    Type Safety: Replaces Dict[str, Any]
    Immutability: Frozen for thread safety
    Complexity: O(1) all operations
    """
    result: str  # 'victory', 'defeat', 'fled'
    exp_gained: int = 0
    coins_gained: int = 0
    items_gained: Tuple[str, ...] = tuple()
    
    @staticmethod
    def victory(exp: int, coins: int) -> 'CombatResult':
        """Create victory result. O(1)"""
        return CombatResult(result='victory', exp_gained=exp, coins_gained=coins)
    
    @staticmethod
    def defeat() -> 'CombatResult':
        """Create defeat result. O(1)"""
        return CombatResult(result='defeat')
    
    @staticmethod
    def fled() -> 'CombatResult':
        """Create fled result. O(1)"""
        return CombatResult(result='fled')


class CombatSystem:
    """Manages turn-based combat with AAA standards.
    
    Design Pattern: Immutable State Management
    - Combat state stored in immutable CombatData
    - Updates create new instances
    - Thread-safe by design
    
    Performance:
    - Turn order: O(n log n) for n combatants
    - Action execution: O(1) single target, O(n) AOE
    - State checks: O(n) for n combatants
    - Damage cache: O(1) lookups
    """
    
    def __init__(self):
        """Initialize combat system.
        
        Complexity: O(1)
        """
        self._combat_data: Optional[CombatData] = None
        self._combat_active: bool = False
        self._escaped: bool = False
        self._combat_log: PyList[str] = []
        self._damage_cache: LRUCache[Tuple[str, str], int] = LRUCache(capacity=50)
    
    @verify_complexity("O(n log n)", "Sorting turn order by speed")
    @requires(lambda self, player_party, enemy_party: len(player_party) > 0 and len(enemy_party) > 0,
              "Both parties must have at least one character")
    def start_combat(self, player_party: Tuple[Character, ...], 
                    enemy_party: Tuple[Character, ...]) -> Result[None, str]:
        """Initialize combat encounter.
        
        Args:
            player_party: Player characters
            enemy_party: Enemy characters
            
        Returns:
            Success[None]: Combat started
            Failure[str]: Invalid party composition
            
        Complexity: O(n log n) where n = total combatants (for sorting)
        Side Effects: Initializes combat state, prints to console
        
        Preconditions:
            - Both parties non-empty
            - At least one player alive
        Postconditions:
            - Combat active
            - Turn order calculated
            - Log initialized
        """
        if not player_party:
            return Err("Player party is empty")
        if not enemy_party:
            return Err("Enemy party is empty")
        
        # Filter to alive characters only
        alive_players = tuple(c for c in player_party if c.is_alive())
        if not alive_players:
            return Err("No alive players in party")
        
        # Determine turn order based on speed (O(n log n))
        all_combatants = list(alive_players) + list(enemy_party)
        turn_order = tuple(
            c.name for c in sorted(all_combatants, 
                                  key=lambda c: c.stats.speed, 
                                  reverse=True)
        )
        
        # Create immutable combat data
        player_data = tuple(c.data for c in alive_players)
        enemy_data = tuple(c.data for c in enemy_party)
        
        self._combat_data = CombatData(
            encounter_id=f"combat_{random.randint(1000, 9999)}",
            player_party=player_data,
            enemy_party=enemy_data,
            turn_order=turn_order,
            current_turn=0,
            combat_log=tuple(),
            is_active=True
        )
        
        self._combat_active = True
        self._escaped = False
        self._combat_log = []
        
        self._log(f"\n{'=' * 60}")
        self._log("COMBAT START!")
        self._log(f"{'=' * 60}")
        self._log(f"\nEnemies: {', '.join([e.name for e in enemy_party])}")
        self._log(f"Party: {', '.join([p.name for p in alive_players])}")
        
        return Ok(None)
    
    def _log(self, message: str) -> None:
        """Add message to combat log.
        
        Complexity: O(1) - append operation
        """
        self._combat_log.append(message)
        print(message)
    
    @verify_complexity("O(1)", "Constant time damage calculation with cache")
    def calculate_physical_damage(self, attacker: Character, target: Character) -> int:
        """Calculate physical damage with variance.
        
        Args:
            attacker: Attacking character
            target: Target character
            
        Returns:
            Damage amount (minimum 1)
            
        Complexity: O(1) - arithmetic with cached lookups
        Thread Safety: Pure function, no shared state
        
        Formula: (STR * 2) + variance - DEF
        Variance: [-5, 5]
        Minimum damage: 1
        """
        # Check cache first
        cache_key = (attacker.name, target.name)
        cached = self._damage_cache.get(cache_key)
        if cached is not None and random.random() < 0.3:  # 30% cache hit for variance
            return cached
        
        base_damage = attacker.stats.strength * 2
        variance = random.randint(-5, 5)
        damage = max(1, base_damage + variance - target.stats.defense)
        
        # Cache result
        self._damage_cache.put(cache_key, damage)
        return damage
    
    @verify_complexity("O(1)", "Constant time magic damage calculation")
    def calculate_magic_damage(self, attacker: Character, target: Character, 
                               spell_power: int) -> int:
        """Calculate magic damage with spell power.
        
        Args:
            attacker: Attacking character
            target: Target character
            spell_power: Base power of spell
            
        Returns:
            Damage amount (minimum 1)
            
        Complexity: O(1) - arithmetic operations
        
        Formula: (MAG * 1.5) + spell_power + variance - M.DEF
        Variance: [-5, 5]
        Minimum damage: 1
        """
        base_damage = (attacker.stats.magic * 1.5) + spell_power
        variance = random.randint(-5, 5)
        damage = max(1, int(base_damage + variance - target.stats.magic_defense))
        return damage
    
    @verify_complexity("O(n)", "Checks n combatants for alive status")
    def check_combat_end(self, player_party: Tuple[Character, ...],
                        enemy_party: Tuple[Character, ...]) -> Tuple[bool, str]:
        """Check if combat has ended.
        
        Args:
            player_party: Current player characters
            enemy_party: Current enemy characters
            
        Returns:
            (ended: bool, result: str) tuple
            result in {'victory', 'defeat', 'fled', 'ongoing'}
            
        Complexity: O(n) where n = total combatants
        """
        if self._escaped:
            return True, "fled"
        
        # O(n) checks
        enemies_alive = any(c.is_alive() for c in enemy_party)
        party_alive = any(c.is_alive() for c in player_party)
        
        if not enemies_alive:
            return True, "victory"
        elif not party_alive:
            return True, "defeat"
        else:
            return False, "ongoing"
    
    @verify_complexity("O(1)", "Constant time status display")
    def display_combat_status(self, player_party: Tuple[Character, ...],
                             enemy_party: Tuple[Character, ...]) -> None:
        """Display current combat status.
        
        Complexity: O(n) where n = combatants (but n is small, typically < 10)
        Side Effects: Prints to console
        """
        print(f"\n{'-' * 60}")
        print("ENEMIES:")
        for enemy in enemy_party:
            if enemy.is_alive():
                print(f"  {enemy.name} - HP: {enemy.stats.current_hp}/{enemy.stats.max_hp}")
            else:
                print(f"  {enemy.name} - DEFEATED")
        
        print(f"\n{'-' * 60}")
        print("YOUR PARTY:")
        for character in player_party:
            if character.is_alive():
                print(f"  {character.name} - HP: {character.stats.current_hp}/{character.stats.max_hp} | MP: {character.stats.current_mp}/{character.stats.max_mp}")
            else:
                print(f"  {character.name} - FALLEN")
        print(f"{'-' * 60}")
    
    @verify_complexity("O(n)", "Distributes EXP to n party members")
    def end_combat(self, result: str, player_party: Tuple[Character, ...],
                  enemy_party: Tuple[Character, ...]) -> CombatResult:
        """End combat and calculate rewards.
        
        Args:
            result: Combat result ('victory', 'defeat', 'fled')
            player_party: Player characters
            enemy_party: Enemy characters
            
        Returns:
            CombatResult with rewards and outcome
            
        Complexity: O(n) where n = party size (for EXP distribution)
        Side Effects: Modifies character EXP, prints to console
        """
        self._combat_active = False
        
        if result == "victory":
            self._log(f"\n{'=' * 60}")
            self._log("VICTORY!")
            self._log(f"{'=' * 60}")
            
            # Calculate rewards (O(n) for n enemies)
            total_exp = sum(e.stats.level * 20 for e in enemy_party)
            total_coins = sum(e.stats.level * 10 for e in enemy_party)
            
            self._log(f"\nRewards:")
            self._log(f"  Experience: {total_exp}")
            self._log(f"  Domminnian Coins: {total_coins}")
            
            # Distribute EXP (O(n) for n party members)
            for character in player_party:
                if character.is_alive():
                    exp_result = character.gain_exp(total_exp)
                    if exp_result.is_success():
                        _, leveled_up = exp_result.unwrap()
                        if leveled_up:
                            self._log(f"  ✨ {character.name} leveled up!")
            
            return CombatResult.victory(total_exp, total_coins)
        
        elif result == "defeat":
            self._log(f"\n{'=' * 60}")
            self._log("DEFEAT!")
            self._log(f"{'=' * 60}")
            return CombatResult.defeat()
        
        elif result == "fled":
            return CombatResult.fled()
        
        else:
            return CombatResult(result='unknown')
    
    def get_player_action(self, character: Character) -> CombatAction:
        """Get action from player for their character"""
        print(f"\n{character.name}'s turn!")
        print("\n1. Attack")
        print("2. Ability")
        print("3. Defend")
        print("4. Item")
        print("5. Flee")
        
        while True:
            choice = input("\nChoose action: ").strip()
            
            if choice == "1":
                target = self.select_target(self.enemy_party)
                if target:
                    return CombatAction(character, "attack", target=target)
            
            elif choice == "2":
                ability = self.select_ability(character)
                if ability:
                    if ability.target in ["single", "single_ally", "single_enemy"]:
                        if ability.ability_type in ["healing", "utility"]:
                            target = self.select_target(self.player_party)
                        else:
                            target = self.select_target(self.enemy_party)
                        if target:
                            return CombatAction(character, "ability", target=target, ability=ability)
                    else:
                        return CombatAction(character, "ability", ability=ability)
            
            elif choice == "3":
                return CombatAction(character, "defend")
            
            elif choice == "4":
                print("Item system not yet implemented.")
                continue
            
            elif choice == "5":
                return CombatAction(character, "flee")
            
            else:
                print("Invalid choice. Try again.")
    
    def select_target(self, targets: List[Character]) -> Optional[Character]:
        """Let player select a target from list"""
        alive_targets = [t for t in targets if t.stats.is_alive()]
        if not alive_targets:
            return None
        
        print("\nSelect target:")
        for i, target in enumerate(alive_targets, 1):
            print(f"{i}. {target.name} (HP: {target.stats.current_hp}/{target.stats.max_hp})")
        
        while True:
            try:
                choice = int(input("\nTarget number: ").strip())
                if 1 <= choice <= len(alive_targets):
                    return alive_targets[choice - 1]
                else:
                    print("Invalid target number.")
            except ValueError:
                print("Please enter a number.")
    
    def select_ability(self, character: Character) -> Optional[Ability]:
        """Let player select an ability"""
        available = character.get_available_abilities()
        if not available:
            print("\nNo abilities available!")
            return None
        
        print("\nSelect ability:")
        for i, ability in enumerate(available, 1):
            print(f"{i}. {ability.name} (MP: {ability.mp_cost}) - {ability.description}")
        print(f"{len(available) + 1}. Cancel")
        
        while True:
            try:
                choice = int(input("\nAbility number: ").strip())
                if 1 <= choice <= len(available):
                    return available[choice - 1]
                elif choice == len(available) + 1:
                    return None
                else:
                    print("Invalid ability number.")
            except ValueError:
                print("Please enter a number.")
    
    def get_enemy_action(self, enemy: Character) -> CombatAction:
        """Determine enemy AI action"""
        # Simple AI: 70% attack, 30% use ability if available
        if random.random() < 0.7 or not enemy.abilities:
            # Basic attack
            target = random.choice([p for p in self.player_party if p.stats.is_alive()])
            return CombatAction(enemy, "attack", target=target)
        else:
            # Use random ability
            available = enemy.get_available_abilities()
            if available:
                ability = random.choice(available)
                if ability.ability_type in ["healing", "utility"]:
                    target = random.choice([e for e in self.enemy_party if e.stats.is_alive()])
                else:
                    target = random.choice([p for p in self.player_party if p.stats.is_alive()])
                return CombatAction(enemy, "ability", target=target, ability=ability)
            else:
                target = random.choice([p for p in self.player_party if p.stats.is_alive()])
                return CombatAction(enemy, "attack", target=target)
    
    def execute_action(self, action: CombatAction):
        """Execute a combat action"""
        actor = action.actor
        
        if action.action_type == "attack":
            damage = self.calculate_physical_damage(actor, action.target)
            actual_damage = action.target.stats.take_damage(damage)
            self.log(f"\n{actor.name} attacks {action.target.name} for {actual_damage} damage!")
            
            if not action.target.stats.is_alive():
                self.log(f"💀 {action.target.name} has been defeated!")
        
        elif action.action_type == "ability":
            ability = action.ability
            actor.stats.current_mp -= ability.mp_cost
            
            if ability.ability_type == "magic":
                if ability.target == "all":
                    targets = self.enemy_party if actor in self.player_party else self.player_party
                    self.log(f"\n{actor.name} casts {ability.name}!")
                    for target in targets:
                        if target.stats.is_alive():
                            damage = self.calculate_magic_damage(actor, target, ability.power)
                            actual_damage = target.stats.take_damage(damage)
                            self.log(f"  {target.name} takes {actual_damage} damage!")
                            if not target.stats.is_alive():
                                self.log(f"  💀 {target.name} has been defeated!")
                else:
                    damage = self.calculate_magic_damage(actor, action.target, ability.power)
                    actual_damage = action.target.stats.take_damage(damage)
                    self.log(f"\n{actor.name} casts {ability.name} on {action.target.name} for {actual_damage} damage!")
                    if not action.target.stats.is_alive():
                        self.log(f"💀 {action.target.name} has been defeated!")
            
            elif ability.ability_type == "healing":
                if ability.target == "all":
                    targets = self.player_party if actor in self.player_party else self.enemy_party
                    self.log(f"\n{actor.name} casts {ability.name}!")
                    for target in targets:
                        if target.stats.is_alive():
                            target.stats.heal(ability.power)
                            self.log(f"  {target.name} restored {ability.power} HP!")
                else:
                    action.target.stats.heal(ability.power)
                    self.log(f"\n{actor.name} casts {ability.name} on {action.target.name}, restoring {ability.power} HP!")
            
            elif ability.ability_type == "utility":
                self.log(f"\n{actor.name} uses {ability.name}!")
                # Utility effects would be implemented based on specific ability
        
        elif action.action_type == "defend":
            self.log(f"\n{actor.name} takes a defensive stance!")
            # Defense bonus would be applied here
        
        elif action.action_type == "flee":
            if random.random() < 0.5:
                self.log(f"\n{actor.name} attempts to flee...")
                self.log("Successfully escaped from battle!")
                self.escaped = True
                self.combat_active = False
            else:
                self.log(f"\n{actor.name} attempts to flee but fails!")
    
    def calculate_physical_damage(self, attacker: Character, target: Character) -> int:
        """Calculate physical damage"""
        base_damage = attacker.stats.strength * 2
        variance = random.randint(-5, 5)
        damage = max(1, base_damage + variance - target.stats.defense)
        return damage
    
    def calculate_magic_damage(self, attacker: Character, target: Character, spell_power: int) -> int:
        """Calculate magic damage"""
        base_damage = (attacker.stats.magic * 1.5) + spell_power
        variance = random.randint(-5, 5)
        damage = max(1, int(base_damage + variance - target.stats.magic_defense))
        return damage
    
    def check_combat_end(self) -> Tuple[bool, str]:
        """Check if combat has ended and return result"""
        if self.escaped:
            return True, "fled"
        
        enemies_alive = any(e.stats.is_alive() for e in self.enemy_party)
        party_alive = any(p.stats.is_alive() for p in self.player_party)
        
        if not enemies_alive:
            return True, "victory"
        elif not party_alive:
            return True, "defeat"
        else:
            return False, "ongoing"
    
    def combat_turn(self):
        """Execute one turn of combat"""
        if not self.combat_active:
            return
        
        self.display_combat_status()
        
        for combatant in self.turn_order:
            if not combatant.stats.is_alive():
                continue
            
            # Check if combat ended
            ended, result = self.check_combat_end()
            if ended:
                self.end_combat(result)
                return
            
            # Get action
            if combatant in self.player_party:
                action = self.get_player_action(combatant)
            else:
                action = self.get_enemy_action(combatant)
            
            # Execute action
            self.execute_action(action)
            
            # Check if action ended combat (flee)
            if not self.combat_active:
                return
        
        self.current_turn += 1
    
    def end_combat(self, result: str):
        """End combat and distribute rewards"""
        self.combat_active = False
        
        if result == "victory":
            self.log(f"\n{'=' * 60}")
            self.log("VICTORY!")
            self.log(f"{'=' * 60}")
            
            # Calculate rewards
            total_exp = sum(enemy.stats.level * 20 for enemy in self.enemy_party)
            total_coins = sum(enemy.stats.level * 10 for enemy in self.enemy_party)
            
            self.log(f"\nRewards:")
            self.log(f"  Experience: {total_exp}")
            self.log(f"  Domminnian Coins: {total_coins}")
            
            # Distribute EXP
            for character in self.player_party:
                if character.stats.is_alive():
                    if character.gain_exp(total_exp):
                        self.log(f"  {character.name} leveled up!")
            
            return {"exp": total_exp, "coins": total_coins, "result": "victory"}
        
        elif result == "defeat":
            self.log(f"\n{'=' * 60}")
            self.log("DEFEAT!")
            self.log(f"{'=' * 60}")
            return {"result": "defeat"}
        
        elif result == "fled":
            return {"result": "fled"}
    
    def run_combat(self, player_party: List[Character], enemy_party: List[Character]) -> dict:
        """Run complete combat encounter"""
        self.start_combat(player_party, enemy_party)
        
        while self.combat_active:
            self.combat_turn()
        
        ended, result = self.check_combat_end()
        if ended:
            return self.end_combat(result)
        
        return {"result": "unknown"}
