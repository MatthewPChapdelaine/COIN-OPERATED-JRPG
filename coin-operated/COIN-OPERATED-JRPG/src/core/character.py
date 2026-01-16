"""
COIN:OPERATED JRPG - Character System
Character classes, stats, and progression
"""

from typing import Dict, List, Optional
from enum import Enum
import json


class CharacterRole(Enum):
    """Character combat roles"""
    MAGIC_DPS = "Magic DPS"
    PHYSICAL_DPS = "Physical DPS"
    TANK = "Tank"
    HEALER = "Healer"
    SUPPORT = "Support"
    WILD_CARD = "Wild Card"


class CharacterFaction(Enum):
    """Character faction affiliations"""
    LIGHT_CABAL = "Light Cabal"
    DARK_CABAL = "Dark Cabal"
    DRIFT_EMPIRE = "Drift Empire"
    INDEPENDENT = "Independent"
    UNKNOWN = "Unknown"


class Stats:
    """Character statistics"""
    
    def __init__(self, level: int = 1):
        self.level = level
        self.max_hp = 100 + (level * 10)
        self.current_hp = self.max_hp
        self.max_mp = 50 + (level * 5)
        self.current_mp = self.max_mp
        self.strength = 10 + level
        self.magic = 10 + level
        self.defense = 10 + level
        self.magic_defense = 10 + level
        self.speed = 10 + level
        self.luck = 10
    
    def level_up(self):
        """Increase character level and stats"""
        self.level += 1
        self.max_hp += 10
        self.max_mp += 5
        self.strength += 1
        self.magic += 1
        self.defense += 1
        self.magic_defense += 1
        self.speed += 1
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
    
    def heal(self, amount: int):
        """Heal HP"""
        self.current_hp = min(self.current_hp + amount, self.max_hp)
    
    def restore_mp(self, amount: int):
        """Restore MP"""
        self.current_mp = min(self.current_mp + amount, self.max_mp)
    
    def take_damage(self, amount: int) -> int:
        """Take damage and return actual damage dealt"""
        damage = max(1, amount - self.defense)
        self.current_hp = max(0, self.current_hp - damage)
        return damage
    
    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.current_hp > 0
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary"""
        return {
            'level': self.level,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'max_mp': self.max_mp,
            'current_mp': self.current_mp,
            'strength': self.strength,
            'magic': self.magic,
            'defense': self.defense,
            'magic_defense': self.magic_defense,
            'speed': self.speed,
            'luck': self.luck
        }


class Ability:
    """Character ability/skill"""
    
    def __init__(self, name: str, description: str, mp_cost: int, 
                 power: int, ability_type: str, target: str = "single"):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.power = power
        self.ability_type = ability_type  # physical, magic, healing, utility
        self.target = target  # single, multi, all, self
        self.unlocked = False
    
    def can_use(self, character: 'Character') -> bool:
        """Check if character can use this ability"""
        return self.unlocked and character.stats.current_mp >= self.mp_cost
    
    def to_dict(self) -> Dict:
        """Convert ability to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'mp_cost': self.mp_cost,
            'power': self.power,
            'type': self.ability_type,
            'target': self.target,
            'unlocked': self.unlocked
        }


class Character:
    """Base character class for player characters and NPCs"""
    
    def __init__(self, name: str, role: CharacterRole, faction: CharacterFaction,
                 level: int = 1, description: str = ""):
        self.name = name
        self.role = role
        self.faction = faction
        self.description = description
        self.stats = Stats(level)
        self.abilities: List[Ability] = []
        self.equipment = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        self.exp = 0
        self.exp_to_next_level = 100
        self.is_playable = False
    
    def add_ability(self, ability: Ability, unlocked: bool = False):
        """Add an ability to character"""
        ability.unlocked = unlocked
        self.abilities.append(ability)
    
    def unlock_ability(self, ability_name: str) -> bool:
        """Unlock an ability by name"""
        for ability in self.abilities:
            if ability.name == ability_name:
                ability.unlocked = True
                return True
        return False
    
    def gain_exp(self, amount: int) -> bool:
        """Gain experience points, return True if leveled up"""
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Level up character"""
        self.exp -= self.exp_to_next_level
        self.stats.level_up()
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        print(f"\n✨ {self.name} reached level {self.stats.level}!")
    
    def equip_item(self, item, slot: str):
        """Equip an item"""
        if slot in self.equipment:
            self.equipment[slot] = item
    
    def get_available_abilities(self) -> List[Ability]:
        """Get list of usable abilities"""
        return [a for a in self.abilities if a.can_use(self)]
    
    def display_status(self):
        """Display character status"""
        print(f"\n{'=' * 60}")
        print(f"{self.name} - {self.role.value} ({self.faction.value})")
        print(f"{'=' * 60}")
        print(f"Level: {self.stats.level}")
        print(f"HP: {self.stats.current_hp}/{self.stats.max_hp}")
        print(f"MP: {self.stats.current_mp}/{self.stats.max_mp}")
        print(f"EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"\nStats:")
        print(f"  STR: {self.stats.strength}  MAG: {self.stats.magic}")
        print(f"  DEF: {self.stats.defense}  MDF: {self.stats.magic_defense}")
        print(f"  SPD: {self.stats.speed}  LUK: {self.stats.luck}")
        
        print(f"\nAbilities:")
        for ability in self.abilities:
            status = "✓" if ability.unlocked else "✗"
            print(f"  {status} {ability.name} (MP: {ability.mp_cost})")
        
        print(f"\nEquipment:")
        for slot, item in self.equipment.items():
            item_name = item.name if item else "None"
            print(f"  {slot.capitalize()}: {item_name}")
    
    def to_dict(self) -> Dict:
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'role': self.role.value,
            'faction': self.faction.value,
            'description': self.description,
            'stats': self.stats.to_dict(),
            'abilities': [a.to_dict() for a in self.abilities],
            'equipment': {k: v.to_dict() if v else None for k, v in self.equipment.items()},
            'exp': self.exp,
            'exp_to_next_level': self.exp_to_next_level,
            'is_playable': self.is_playable
        }


class Coin(Character):
    """Coin - The protagonist who grows throughout the story"""
    
    def __init__(self, age_state: str = "young"):
        super().__init__(
            name="Coin",
            role=CharacterRole.MAGIC_DPS,
            faction=CharacterFaction.INDEPENDENT,
            level=1,
            description="A sentient magical artifact created for war, discovering her own agency and destiny."
        )
        self.age_state = age_state  # young, teen, adult, elder
        self.is_playable = True
        self.magical_essence = 0
        self.time_goddess_awakened = False
        
        # Add starting abilities
        self.add_ability(Ability(
            "Magical Strike",
            "Basic magical attack",
            mp_cost=5,
            power=20,
            ability_type="magic",
            target="single"
        ), unlocked=True)
        
        self.add_ability(Ability(
            "Healing Light",
            "Restore HP to one ally",
            mp_cost=10,
            power=30,
            ability_type="healing",
            target="single"
        ), unlocked=True)
        
        # Locked abilities to be unlocked through progression
        self.add_ability(Ability(
            "Time Glimpse",
            "See future attack patterns",
            mp_cost=20,
            power=0,
            ability_type="utility",
            target="self"
        ), unlocked=False)
        
        self.add_ability(Ability(
            "Transmutation",
            "Transform magical energy into matter",
            mp_cost=30,
            power=50,
            ability_type="magic",
            target="single"
        ), unlocked=False)
    
    def age_up(self):
        """Progress to next age state"""
        age_progression = ["young", "teen", "adult", "elder"]
        current_index = age_progression.index(self.age_state)
        if current_index < len(age_progression) - 1:
            self.age_state = age_progression[current_index + 1]
            # Stat boost when aging up
            self.stats.max_hp += 20
            self.stats.max_mp += 15
            self.stats.current_hp = self.stats.max_hp
            self.stats.current_mp = self.stats.max_mp
            print(f"\n✨ Coin has grown! Age state: {self.age_state}")
    
    def awaken_time_goddess(self):
        """Unlock Time Goddess abilities"""
        if not self.time_goddess_awakened:
            self.time_goddess_awakened = True
            self.unlock_ability("Time Glimpse")
            print("\n✨ Coin has awakened as the Time Goddess!")
            print("New abilities unlocked!")


class JinnLir(Character):
    """Jinn-Lir - Coin's creator and flawed mentor"""
    
    def __init__(self):
        super().__init__(
            name="Jinn-Lir",
            role=CharacterRole.MAGIC_DPS,
            faction=CharacterFaction.LIGHT_CABAL,
            level=15,
            description="Powerful wizard of the Light Cabal. Coin's creator and former manipulator."
        )
        self.is_playable = False  # Becomes playable after reconciliation
        
        self.add_ability(Ability(
            "Teleportation",
            "Instantly move across battlefield",
            mp_cost=25,
            power=0,
            ability_type="utility",
            target="self"
        ), unlocked=True)
        
        self.add_ability(Ability(
            "Multi-Cast",
            "Cast spell on all enemies",
            mp_cost=40,
            power=35,
            ability_type="magic",
            target="all"
        ), unlocked=True)


class Orbius(Character):
    """Orbius - Master wizard with knowledge of all Orbspace"""
    
    def __init__(self):
        super().__init__(
            name="Orbius",
            role=CharacterRole.HEALER,
            faction=CharacterFaction.LIGHT_CABAL,
            level=50,
            description="Cryptic master of the Light Cabal with deep knowledge of Orbspace's history."
        )
        self.is_playable = False  # Recruitable mid-game
        
        self.add_ability(Ability(
            "Greater Heal",
            "Restore large amount of HP to all allies",
            mp_cost=50,
            power=80,
            ability_type="healing",
            target="all"
        ), unlocked=True)
        
        self.add_ability(Ability(
            "Reality Warp",
            "One-use game-changing spell",
            mp_cost=100,
            power=500,
            ability_type="magic",
            target="all"
        ), unlocked=True)


class Typhus(Character):
    """Typhus - Mysterious creature with wild magic"""
    
    def __init__(self):
        super().__init__(
            name="Typhus",
            role=CharacterRole.WILD_CARD,
            faction=CharacterFaction.DARK_CABAL,
            level=1,
            description="Mysterious creature that ages with Coin. Non-verbal companion."
        )
        self.is_playable = False  # Optional recruitment
        
        self.add_ability(Ability(
            "Wild Strike",
            "Powerful but unpredictable physical attack",
            mp_cost=0,
            power=50,
            ability_type="physical",
            target="single"
        ), unlocked=True)
        
        self.add_ability(Ability(
            "Chaos Magic",
            "Random magical effect",
            mp_cost=20,
            power=40,
            ability_type="magic",
            target="single"
        ), unlocked=True)


class Coireena(Character):
    """Coireena - Super-soldier empowered by Coin's magic"""
    
    def __init__(self):
        super().__init__(
            name="Coireena",
            role=CharacterRole.TANK,
            faction=CharacterFaction.DRIFT_EMPIRE,
            level=10,
            description="Soldier who received Coin's magic. Former victim, now protector."
        )
        self.is_playable = False  # Recruitable after civil war arc
        
        self.add_ability(Ability(
            "Shield Wall",
            "Protect all allies from next attack",
            mp_cost=30,
            power=0,
            ability_type="utility",
            target="all"
        ), unlocked=True)
        
        self.add_ability(Ability(
            "Counter Strike",
            "Reflect damage back to attacker",
            mp_cost=20,
            power=30,
            ability_type="physical",
            target="self"
        ), unlocked=True)
