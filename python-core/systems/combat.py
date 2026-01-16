"""
COIN:OPERATED JRPG - Combat System
Turn-based JRPG combat mechanics
"""

from typing import List, Optional, Tuple
from enum import Enum
import random
from core.character import Character, Ability


class TargetType(Enum):
    """Combat target types"""
    SINGLE_ALLY = "single_ally"
    SINGLE_ENEMY = "single_enemy"
    ALL_ALLIES = "all_allies"
    ALL_ENEMIES = "all_enemies"
    SELF = "self"


class CombatAction:
    """Represents an action in combat"""
    
    def __init__(self, actor: Character, action_type: str, 
                 target: Optional[Character] = None, ability: Optional[Ability] = None):
        self.actor = actor
        self.action_type = action_type  # attack, ability, item, defend, flee
        self.target = target
        self.ability = ability


class CombatSystem:
    """Manages turn-based combat"""
    
    def __init__(self):
        self.player_party: List[Character] = []
        self.enemy_party: List[Character] = []
        self.turn_order: List[Character] = []
        self.current_turn = 0
        self.combat_active = False
        self.combat_log: List[str] = []
        self.escaped = False
    
    def start_combat(self, player_party: List[Character], enemy_party: List[Character]):
        """Initialize combat encounter"""
        self.player_party = [c for c in player_party if c.stats.is_alive()]
        self.enemy_party = enemy_party
        self.combat_active = True
        self.escaped = False
        self.combat_log = []
        self.current_turn = 0
        
        # Determine turn order based on speed stat
        all_combatants = self.player_party + self.enemy_party
        self.turn_order = sorted(all_combatants, key=lambda c: c.stats.speed, reverse=True)
        
        self.log(f"\n{'=' * 60}")
        self.log("COMBAT START!")
        self.log(f"{'=' * 60}")
        self.log(f"\nEnemies: {', '.join([e.name for e in self.enemy_party])}")
        self.log(f"Party: {', '.join([p.name for p in self.player_party])}")
    
    def log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(message)
        print(message)
    
    def display_combat_status(self):
        """Display current combat status"""
        print(f"\n{'-' * 60}")
        print("ENEMIES:")
        for enemy in self.enemy_party:
            if enemy.stats.is_alive():
                print(f"  {enemy.name} - HP: {enemy.stats.current_hp}/{enemy.stats.max_hp}")
            else:
                print(f"  {enemy.name} - DEFEATED")
        
        print(f"\n{'-' * 60}")
        print("YOUR PARTY:")
        for character in self.player_party:
            if character.stats.is_alive():
                print(f"  {character.name} - HP: {character.stats.current_hp}/{enemy.stats.max_hp} | MP: {character.stats.current_mp}/{character.stats.max_mp}")
            else:
                print(f"  {character.name} - FALLEN")
        print(f"{'-' * 60}")
    
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
