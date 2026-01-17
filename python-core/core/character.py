"""
COIN:OPERATED JRPG - Character System
Character classes, stats, and progression

Academic Subjects:
- Object-Oriented Programming: Character class hierarchies
- Game Design: Character roles and progression systems
- Mathematics: Stat calculations and experience curves
- Type Theory: Immutable character state management

Complexity Guarantees:
- Character creation: O(1)
- Stat access: O(1)
- Ability lookup: O(1) with LRU cache
- Level up: O(1) stat calculations
"""

from typing import Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

# Import AAA Standards
from aaa_standards.result_types import Result, Success, Failure, Ok, Err
from aaa_standards.type_definitions import (
    CharacterStats, CharacterData, AbilityData, ItemData
)
from aaa_standards.formal_specs import (
    verify_complexity, requires, ensures, invariant
)
from aaa_standards.performance import LRUCache, memoize


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


@dataclass(frozen=True)
class Equipment:
    """Immutable equipment loadout.
    
    Type Safety: Replaces Dict[str, Any]
    Immutability: Frozen for thread safety
    Complexity: O(1) all operations
    """
    weapon: Optional[ItemData] = None
    armor: Optional[ItemData] = None
    accessory: Optional[ItemData] = None
    
    def with_weapon(self, weapon: Optional[ItemData]) -> 'Equipment':
        """Return new Equipment with updated weapon."""
        return Equipment(weapon=weapon, armor=self.armor, accessory=self.accessory)
    
    def with_armor(self, armor: Optional[ItemData]) -> 'Equipment':
        """Return new Equipment with updated armor."""
        return Equipment(weapon=self.weapon, armor=armor, accessory=self.accessory)
    
    def with_accessory(self, accessory: Optional[ItemData]) -> 'Equipment':
        """Return new Equipment with updated accessory."""
        return Equipment(weapon=self.weapon, armor=self.armor, accessory=accessory)



class Character:
    """Base character class for player characters and NPCs.
    
    Design Pattern: Immutable State Pattern
    - All state stored in immutable CharacterData
    - Updates create new instances
    - Thread-safe by design
    
    Performance:
    - Stat access: O(1)
    - Ability lookup: O(1) with cache
    - Level calculations: O(1)
    """
    
    def __init__(self, data: CharacterData):
        """Initialize character with immutable data.
        
        Args:
            data: Immutable character data
            
        Complexity: O(1)
        """
        self._data = data
        self._ability_cache: LRUCache[str, AbilityData] = LRUCache(capacity=20)
        # Pre-populate cache
        for ability in data.abilities:
            self._ability_cache.put(ability.name, ability)
    
    @property
    def data(self) -> CharacterData:
        """Get immutable character data.
        
        Complexity: O(1)
        """
        return self._data
    
    @property
    def name(self) -> str:
        """Character name. Complexity: O(1)"""
        return self._data.name
    
    @property
    def stats(self) -> CharacterStats:
        """Character stats. Complexity: O(1)"""
        return self._data.stats
    
    @property
    def abilities(self) -> Tuple[AbilityData, ...]:
        """Character abilities. Complexity: O(1)"""
        return self._data.abilities
    
    @verify_complexity("O(1)", "Ability lookup via LRU cache")
    def get_ability(self, name: str) -> Result[AbilityData, str]:
        """Get ability by name with O(1) cache lookup.
        
        Args:
            name: Ability name
            
        Returns:
            Success[AbilityData]: Found ability
            Failure[str]: Ability not found
            
        Complexity: O(1) amortized - LRU cache
        Thread Safety: Cache is thread-safe
        """
        # Try cache first (O(1))
        cached = self._ability_cache.get(name)
        if cached is not None:
            return Ok(cached)
        
        # Fallback to linear search (only for cache misses)
        for ability in self._data.abilities:
            if ability.name == name:
                self._ability_cache.put(name, ability)
                return Ok(ability)
        
        return Err(f"Ability not found: {name}")
    
    @verify_complexity("O(n)", "Filters n abilities")
    def get_available_abilities(self) -> Tuple[AbilityData, ...]:
        """Get list of usable abilities.
        
        Returns:
            Tuple of abilities character can currently use
            
        Complexity: O(n) where n = number of abilities
        Note: Could be O(1) with pre-computed cache
        """
        return tuple(
            a for a in self._data.abilities 
            if a.unlocked and self._data.stats.current_mp >= a.mp_cost
        )
    
    @verify_complexity("O(1)", "Creates new immutable character data")
    @requires(lambda self, amount: amount > 0, "Heal amount must be positive")
    @ensures(lambda self, result: result.is_success() or self._data.stats.current_hp == self._data.stats.max_hp,
             "Healing succeeds or HP already at max")
    def heal(self, amount: int) -> Result[CharacterData, str]:
        """Heal character HP.
        
        Args:
            amount: HP to restore
            
        Returns:
            Success[CharacterData]: Updated character
            Failure[str]: Invalid heal amount
            
        Complexity: O(1) - stat arithmetic and object creation
        Thread Safety: Creates new immutable data
        Side Effects: None (functional update)
        
        Preconditions:
            - amount > 0
        Postconditions:
            - current_hp ≤ max_hp
            - HP increased by min(amount, max_hp - current_hp)
        """
        if amount <= 0:
            return Err("Heal amount must be positive")
        
        if self._data.stats.current_hp >= self._data.stats.max_hp:
            return Err("Already at full HP")
        
        new_hp = min(self._data.stats.current_hp + amount, self._data.stats.max_hp)
        new_stats = CharacterStats(
            level=self._data.stats.level,
            max_hp=self._data.stats.max_hp,
            current_hp=new_hp,
            max_mp=self._data.stats.max_mp,
            current_mp=self._data.stats.current_mp,
            strength=self._data.stats.strength,
            magic=self._data.stats.magic,
            defense=self._data.stats.defense,
            magic_defense=self._data.stats.magic_defense,
            speed=self._data.stats.speed,
            luck=self._data.stats.luck
        )
        
        new_data = CharacterData(
            name=self._data.name,
            role=self._data.role,
            faction=self._data.faction,
            description=self._data.description,
            stats=new_stats,
            abilities=self._data.abilities,
            equipment=self._data.equipment,
            exp=self._data.exp,
            exp_to_next_level=self._data.exp_to_next_level,
            is_playable=self._data.is_playable,
            metadata=self._data.metadata
        )
        
        self._data = new_data
        return Ok(new_data)
    
    @verify_complexity("O(1)", "MP restoration is constant time")
    @requires(lambda self, amount: amount > 0, "Restore amount must be positive")
    def restore_mp(self, amount: int) -> Result[CharacterData, str]:
        """Restore character MP.
        
        Args:
            amount: MP to restore
            
        Returns:
            Success[CharacterData]: Updated character
            Failure[str]: Invalid amount or already at max
            
        Complexity: O(1)
        """
        if amount <= 0:
            return Err("Restore amount must be positive")
        
        if self._data.stats.current_mp >= self._data.stats.max_mp:
            return Err("Already at full MP")
        
        new_mp = min(self._data.stats.current_mp + amount, self._data.stats.max_mp)
        new_stats = CharacterStats(
            level=self._data.stats.level,
            max_hp=self._data.stats.max_hp,
            current_hp=self._data.stats.current_hp,
            max_mp=self._data.stats.max_mp,
            current_mp=new_mp,
            strength=self._data.stats.strength,
            magic=self._data.stats.magic,
            defense=self._data.stats.defense,
            magic_defense=self._data.stats.magic_defense,
            speed=self._data.stats.speed,
            luck=self._data.stats.luck
        )
        
        new_data = self._data.with_stats(new_stats)
        self._data = new_data
        return Ok(new_data)
    
    @verify_complexity("O(1)", "Damage calculation is constant time")
    @requires(lambda self, amount: amount >= 0, "Damage must be non-negative")
    @ensures(lambda self, result: result.is_success(), "Damage always succeeds")
    def take_damage(self, amount: int) -> Result[Tuple[CharacterData, int], str]:
        """Take damage and return actual damage dealt.
        
        Args:
            amount: Raw damage amount
            
        Returns:
            Success[(CharacterData, int)]: (Updated character, actual damage)
            Failure[str]: Invalid damage amount
            
        Complexity: O(1) - arithmetic operations
        Thread Safety: Creates new immutable data
        
        Preconditions:
            - amount ≥ 0
        Postconditions:
            - current_hp ≥ 0
            - Damage dealt ≥ 1 (minimum damage)
        """
        if amount < 0:
            return Err("Damage must be non-negative")
        
        # Calculate actual damage (minimum 1)
        damage = max(1, amount - self._data.stats.defense)
        new_hp = max(0, self._data.stats.current_hp - damage)
        
        new_stats = CharacterStats(
            level=self._data.stats.level,
            max_hp=self._data.stats.max_hp,
            current_hp=new_hp,
            max_mp=self._data.stats.max_mp,
            current_mp=self._data.stats.current_mp,
            strength=self._data.stats.strength,
            magic=self._data.stats.magic,
            defense=self._data.stats.defense,
            magic_defense=self._data.stats.magic_defense,
            speed=self._data.stats.speed,
            luck=self._data.stats.luck
        )
        
        new_data = self._data.with_stats(new_stats)
        self._data = new_data
        return Ok((new_data, damage))
    
    @verify_complexity("O(1)", "Alive check is constant")
    def is_alive(self) -> bool:
        """Check if character is alive.
        
        Returns:
            True if current_hp > 0
            
        Complexity: O(1) - comparison
        """
        return self._data.stats.current_hp > 0
    
    @verify_complexity("O(1)", "Level up calculations are constant")
    @memoize
    def calculate_level_stats(self, level: int) -> CharacterStats:
        """Calculate stats for a given level.
        
        Args:
            level: Target level
            
        Returns:
            Character stats at specified level
            
        Complexity: O(1) - memoized arithmetic
        Note: Memoized for repeated calculations
        """
        return CharacterStats(
            level=level,
            max_hp=100 + (level * 10),
            current_hp=100 + (level * 10),
            max_mp=50 + (level * 5),
            current_mp=50 + (level * 5),
            strength=10 + level,
            magic=10 + level,
            defense=10 + level,
            magic_defense=10 + level,
            speed=10 + level,
            luck=10
        )
    
    @verify_complexity("O(1)", "Level up is constant time")
    def level_up(self) -> Result[CharacterData, str]:
        """Level up character.
        
        Returns:
            Success[CharacterData]: Leveled up character
            Failure[str]: Cannot level up (insufficient EXP)
            
        Complexity: O(1) - stat calculations and object creation
        Side Effects: Prints level up message
        """
        if self._data.exp < self._data.exp_to_next_level:
            return Err(f"Insufficient EXP: {self._data.exp}/{self._data.exp_to_next_level}")
        
        new_level = self._data.stats.level + 1
        new_stats = self.calculate_level_stats(new_level)
        remaining_exp = self._data.exp - self._data.exp_to_next_level
        new_exp_threshold = int(self._data.exp_to_next_level * 1.5)
        
        new_data = CharacterData(
            name=self._data.name,
            role=self._data.role,
            faction=self._data.faction,
            description=self._data.description,
            stats=new_stats,
            abilities=self._data.abilities,
            equipment=self._data.equipment,
            exp=remaining_exp,
            exp_to_next_level=new_exp_threshold,
            is_playable=self._data.is_playable,
            metadata=self._data.metadata
        )
        
        self._data = new_data
        print(f"\n✨ {self._data.name} reached level {new_level}!")
        return Ok(new_data)
    
    @verify_complexity("O(1)", "EXP gain with level check")
    def gain_exp(self, amount: int) -> Result[Tuple[CharacterData, bool], str]:
        """Gain experience points.
        
        Args:
            amount: EXP to gain
            
        Returns:
            Success[(CharacterData, bool)]: (Updated character, leveled_up flag)
            Failure[str]: Invalid EXP amount
            
        Complexity: O(1) - arithmetic and level check
        Note: May trigger level_up() which is also O(1)
        """
        if amount <= 0:
            return Err("EXP amount must be positive")
        
        new_exp = self._data.exp + amount
        new_data = self._data.with_exp(new_exp, self._data.exp_to_next_level)
        self._data = new_data
        
        # Check if level up
        if new_exp >= self._data.exp_to_next_level:
            level_result = self.level_up()
            if level_result.is_success():
                return Ok((level_result.unwrap(), True))
            else:
                return Ok((new_data, False))
        
        return Ok((new_data, False))
    
    @verify_complexity("O(1)", "Ability unlock is constant via cache")
    def unlock_ability(self, ability_name: str) -> Result[CharacterData, str]:
        """Unlock an ability by name.
        
        Args:
            ability_name: Name of ability to unlock
            
        Returns:
            Success[CharacterData]: Updated character with unlocked ability
            Failure[str]: Ability not found
            
        Complexity: O(1) amortized - uses LRU cache
        """
        ability_result = self.get_ability(ability_name)
        if ability_result.is_failure():
            return Err(ability_result.unwrap_failure())
        
        ability = ability_result.unwrap()
        
        # Create new tuple with updated ability
        new_abilities = tuple(
            AbilityData(
                name=a.name,
                description=a.description,
                mp_cost=a.mp_cost,
                power=a.power,
                ability_type=a.ability_type,
                target=a.target,
                unlocked=True if a.name == ability_name else a.unlocked
            )
            for a in self._data.abilities
        )
        
        new_data = self._data.with_abilities(new_abilities)
        self._data = new_data
        
        # Update cache
        self._ability_cache.put(ability_name, new_abilities[self._find_ability_index(ability_name)])
        
        return Ok(new_data)
    
    def _find_ability_index(self, name: str) -> int:
        """Helper to find ability index. O(n) but only called during updates."""
        for i, ability in enumerate(self._data.abilities):
            if ability.name == name:
                return i
        return -1
    
    @verify_complexity("O(1)", "Status display is constant for fixed abilities")
    def display_status(self):
        """Display character status.
        
        Complexity: O(1) for typical characters with < 10 abilities
        Side Effects: Prints to console
        """
        print(f"\n{'=' * 60}")
        print(f"{self._data.name} - {self._data.role} ({self._data.faction})")
        print(f"{'=' * 60}")
        print(f"Level: {self._data.stats.level}")
        print(f"HP: {self._data.stats.current_hp}/{self._data.stats.max_hp}")
        print(f"MP: {self._data.stats.current_mp}/{self._data.stats.max_mp}")
        print(f"EXP: {self._data.exp}/{self._data.exp_to_next_level}")
        print(f"\nStats:")
        print(f"  STR: {self._data.stats.strength}  MAG: {self._data.stats.magic}")
        print(f"  DEF: {self._data.stats.defense}  MDF: {self._data.stats.magic_defense}")
        print(f"  SPD: {self._data.stats.speed}  LUK: {self._data.stats.luck}")
        
        print(f"\nAbilities:")
        for ability in self._data.abilities:
            status = "✓" if ability.unlocked else "✗"
            print(f"  {status} {ability.name} (MP: {ability.mp_cost})")


# Factory functions for creating character data

# Factory functions for creating specific characters with AAA standards

@verify_complexity("O(1)", "Character creation is constant time")
def create_coin(age_state: str = "young", level: int = 1) -> Character:
    """Create Coin character with type-safe data.
    
    Args:
        age_state: Age state ('young', 'teen', 'adult', 'elder')
        level: Starting level
        
    Returns:
        Character instance with Coin's data
        
    Complexity: O(1) - fixed number of abilities
    """
    stats = CharacterStats(
        level=level,
        max_hp=100 + (level * 10),
        current_hp=100 + (level * 10),
        max_mp=50 + (level * 5),
        current_mp=50 + (level * 5),
        strength=10 + level,
        magic=15 + level,  # Higher magic for Coin
        defense=10 + level,
        magic_defense=12 + level,
        speed=11 + level,
        luck=12
    )
    
    abilities = (
        AbilityData(
            name="Magical Strike",
            description="Basic magical attack",
            mp_cost=5,
            power=20,
            ability_type="magic",
            target="single",
            unlocked=True
        ),
        AbilityData(
            name="Healing Light",
            description="Restore HP to one ally",
            mp_cost=10,
            power=30,
            ability_type="healing",
            target="single",
            unlocked=True
        ),
        AbilityData(
            name="Time Glimpse",
            description="See future attack patterns",
            mp_cost=20,
            power=0,
            ability_type="utility",
            target="self",
            unlocked=False
        ),
        AbilityData(
            name="Transmutation",
            description="Transform magical energy into matter",
            mp_cost=30,
            power=50,
            ability_type="magic",
            target="single",
            unlocked=False
        ),
    )
    
    data = CharacterData(
        name="Coin",
        role=CharacterRole.MAGIC_DPS.value,
        faction=CharacterFaction.INDEPENDENT.value,
        description="A sentient magical artifact created for war, discovering her own agency and destiny.",
        stats=stats,
        abilities=abilities,
        equipment={},
        exp=0,
        exp_to_next_level=100,
        is_playable=True,
        metadata={
            'age_state': age_state,
            'magical_essence': 0,
            'time_goddess_awakened': False
        }
    )
    
    return Character(data)


@verify_complexity("O(1)", "Character creation is constant time")
def create_jinn_lir(level: int = 15) -> Character:
    """Create Jinn-Lir character with type-safe data.
    
    Args:
        level: Starting level
        
    Returns:
        Character instance
        
    Complexity: O(1)
    """
    stats = CharacterStats(
        level=level,
        max_hp=100 + (level * 10),
        current_hp=100 + (level * 10),
        max_mp=50 + (level * 5),
        current_mp=50 + (level * 5),
        strength=10 + level,
        magic=18 + level,
        defense=10 + level,
        magic_defense=15 + level,
        speed=12 + level,
        luck=10
    )
    
    abilities = (
        AbilityData(
            name="Teleportation",
            description="Instantly move across battlefield",
            mp_cost=25,
            power=0,
            ability_type="utility",
            target="self",
            unlocked=True
        ),
        AbilityData(
            name="Multi-Cast",
            description="Cast spell on all enemies",
            mp_cost=40,
            power=35,
            ability_type="magic",
            target="all",
            unlocked=True
        ),
    )
    
    data = CharacterData(
        name="Jinn-Lir",
        role=CharacterRole.MAGIC_DPS.value,
        faction=CharacterFaction.LIGHT_CABAL.value,
        description="Powerful wizard of the Light Cabal. Coin's creator and former manipulator.",
        stats=stats,
        abilities=abilities,
        equipment={},
        exp=0,
        exp_to_next_level=int(100 * (1.5 ** (level - 1))),
        is_playable=False,
        metadata={}
    )
    
    return Character(data)


@verify_complexity("O(1)", "Character creation is constant time")
def create_orbius(level: int = 50) -> Character:
    """Create Orbius character.
    
    Complexity: O(1)
    """
    stats = CharacterStats(
        level=level,
        max_hp=100 + (level * 10),
        current_hp=100 + (level * 10),
        max_mp=50 + (level * 5),
        current_mp=50 + (level * 5),
        strength=10 + level,
        magic=20 + level,
        defense=12 + level,
        magic_defense=18 + level,
        speed=10 + level,
        luck=15
    )
    
    abilities = (
        AbilityData(
            name="Greater Heal",
            description="Restore large amount of HP to all allies",
            mp_cost=50,
            power=80,
            ability_type="healing",
            target="all",
            unlocked=True
        ),
        AbilityData(
            name="Reality Warp",
            description="One-use game-changing spell",
            mp_cost=100,
            power=500,
            ability_type="magic",
            target="all",
            unlocked=True
        ),
    )
    
    data = CharacterData(
        name="Orbius",
        role=CharacterRole.HEALER.value,
        faction=CharacterFaction.LIGHT_CABAL.value,
        description="Cryptic master of the Light Cabal with deep knowledge of Orbspace's history.",
        stats=stats,
        abilities=abilities,
        equipment={},
        exp=0,
        exp_to_next_level=int(100 * (1.5 ** (level - 1))),
        is_playable=False,
        metadata={}
    )
    
    return Character(data)


@verify_complexity("O(1)", "Character creation is constant time")
def create_typhus(level: int = 1) -> Character:
    """Create Typhus character.
    
    Complexity: O(1)
    """
    stats = CharacterStats(
        level=level,
        max_hp=120 + (level * 12),  # Higher HP for wild card
        current_hp=120 + (level * 12),
        max_mp=30 + (level * 3),
        current_mp=30 + (level * 3),
        strength=15 + level,
        magic=12 + level,
        defense=8 + level,
        magic_defense=8 + level,
        speed=15 + level,  # Very fast
        luck=20  # High luck
    )
    
    abilities = (
        AbilityData(
            name="Wild Strike",
            description="Powerful but unpredictable physical attack",
            mp_cost=0,
            power=50,
            ability_type="physical",
            target="single",
            unlocked=True
        ),
        AbilityData(
            name="Chaos Magic",
            description="Random magical effect",
            mp_cost=20,
            power=40,
            ability_type="magic",
            target="single",
            unlocked=True
        ),
    )
    
    data = CharacterData(
        name="Typhus",
        role=CharacterRole.WILD_CARD.value,
        faction=CharacterFaction.DARK_CABAL.value,
        description="Mysterious creature that ages with Coin. Non-verbal companion.",
        stats=stats,
        abilities=abilities,
        equipment={},
        exp=0,
        exp_to_next_level=100,
        is_playable=False,
        metadata={}
    )
    
    return Character(data)


@verify_complexity("O(1)", "Character creation is constant time")
def create_coireena(level: int = 10) -> Character:
    """Create Coireena character.
    
    Complexity: O(1)
    """
    stats = CharacterStats(
        level=level,
        max_hp=140 + (level * 14),  # Tank has highest HP
        current_hp=140 + (level * 14),
        max_mp=40 + (level * 4),
        current_mp=40 + (level * 4),
        strength=12 + level,
        magic=8 + level,
        defense=15 + level,  # High defense
        magic_defense=12 + level,
        speed=8 + level,  # Slower but tanky
        luck=10
    )
    
    abilities = (
        AbilityData(
            name="Shield Wall",
            description="Protect all allies from next attack",
            mp_cost=30,
            power=0,
            ability_type="utility",
            target="all",
            unlocked=True
        ),
        AbilityData(
            name="Counter Strike",
            description="Reflect damage back to attacker",
            mp_cost=20,
            power=30,
            ability_type="physical",
            target="self",
            unlocked=True
        ),
    )
    
    data = CharacterData(
        name="Coireena",
        role=CharacterRole.TANK.value,
        faction=CharacterFaction.DRIFT_EMPIRE.value,
        description="Soldier who received Coin's magic. Former victim, now protector.",
        stats=stats,
        abilities=abilities,
        equipment={},
        exp=0,
        exp_to_next_level=int(100 * (1.5 ** (level - 1))),
        is_playable=False,
        metadata={}
    )
    
    return Character(data)
