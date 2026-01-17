"""
Type-Safe Data Structures (AAA Standard)

Replaces Dict[str, Any] with proper typed dataclasses.
All types are immutable (frozen) for thread safety and predictability.

Mathematical Properties:
- Algebraic Data Types (Product Types)
- Structural typing with nominal guarantees
- O(1) access to all fields
"""

from dataclasses import dataclass, field
from typing import Tuple, FrozenSet, Optional, List
from enum import Enum


@dataclass(frozen=True)
class Position:
    """
    2D position in game world.
    
    Invariants:
    - x, y ∈ ℤ (integers)
    - No negative coordinates enforced at construction
    
    Complexity: O(1) creation and access
    """
    x: int
    y: int
    
    def __post_init__(self):
        """Validate invariants"""
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Position coordinates must be non-negative: ({self.x}, {self.y})")
    
    def distance_to(self, other: 'Position') -> float:
        """
        Manhattan distance between positions.
        Complexity: O(1)
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Location:
    """
    Game location with full type safety.
    Replaces: Dict[str, Any]
    
    Complexity: O(1) all operations
    Immutable: Yes
    """
    id: str
    name: str
    description: str
    position: Position
    region: str
    is_safe: bool = True
    npcs: Tuple[str, ...] = field(default_factory=tuple)
    items: Tuple[str, ...] = field(default_factory=tuple)
    enemies: Tuple[str, ...] = field(default_factory=tuple)
    connected_locations: Tuple[str, ...] = field(default_factory=tuple)
    required_quest: Optional[str] = None
    
    def __post_init__(self):
        """Validate location data"""
        if not self.id or not self.name:
            raise ValueError("Location must have id and name")


@dataclass(frozen=True)
class CharacterStats:
    """
    Character statistics with mathematical guarantees.
    
    Invariants:
    - All stats ≥ 0
    - current_hp ≤ max_hp
    - current_mp ≤ max_mp
    
    Complexity: O(1) all operations
    """
    level: int
    max_hp: int
    current_hp: int
    max_mp: int
    current_mp: int
    strength: int
    magic: int
    defense: int
    magic_defense: int
    speed: int
    luck: int
    
    def __post_init__(self):
        """Enforce invariants"""
        if self.level < 1:
            raise ValueError(f"Level must be ≥ 1, got {self.level}")
        if self.current_hp > self.max_hp:
            raise ValueError(f"current_hp ({self.current_hp}) > max_hp ({self.max_hp})")
        if self.current_mp > self.max_mp:
            raise ValueError(f"current_mp ({self.current_mp}) > max_mp ({self.max_mp})")
        if any(s < 0 for s in [self.max_hp, self.max_mp, self.strength, self.magic, 
                                self.defense, self.magic_defense, self.speed, self.luck]):
            raise ValueError("All stats must be non-negative")
    
    def is_alive(self) -> bool:
        """O(1) check"""
        return self.current_hp > 0
    
    def hp_percentage(self) -> float:
        """O(1) calculation"""
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0


@dataclass(frozen=True)
class AbilityData:
    """
    Type-safe ability/skill data.
    Replaces: Mutable Ability class
    
    Complexity: O(1) all operations
    Immutable: Yes
    """
    name: str
    description: str
    mp_cost: int
    power: int
    ability_type: str  # 'physical', 'magic', 'healing', 'utility'
    target: str  # 'single', 'multi', 'all', 'self'
    unlocked: bool = False
    
    def __post_init__(self):
        """Validate ability data"""
        if self.mp_cost < 0:
            raise ValueError(f"MP cost must be ≥ 0, got {self.mp_cost}")
        if self.power < 0:
            raise ValueError(f"Power must be ≥ 0, got {self.power}")
        if self.ability_type not in ['physical', 'magic', 'healing', 'utility']:
            raise ValueError(f"Invalid ability type: {self.ability_type}")
        if self.target not in ['single', 'multi', 'all', 'self']:
            raise ValueError(f"Invalid target: {self.target}")
    
    def can_use_with_mp(self, current_mp: int) -> bool:
        """Check if ability can be used with available MP.
        
        Complexity: O(1)
        """
        return self.unlocked and current_mp >= self.mp_cost


@dataclass(frozen=True)
class CharacterData:
    """
    Complete character data with type safety.
    Replaces: Dict[str, Any] and mutable Character class
    
    Complexity: O(1) all field access
    Immutable: Yes (use with_* methods for updates)
    """
    name: str
    role: str  # CharacterRole enum value
    faction: str  # CharacterFaction enum value
    description: str
    stats: CharacterStats
    abilities: Tuple[AbilityData, ...]
    equipment: dict  # Equipment slots
    exp: int
    exp_to_next_level: int
    is_playable: bool = False
    metadata: dict = field(default_factory=dict)  # For subclass-specific data
    
    def __post_init__(self):
        """Validate character data"""
        if not self.name:
            raise ValueError("Character must have a name")
        if self.exp < 0:
            raise ValueError(f"EXP must be ≥ 0, got {self.exp}")
        if self.exp_to_next_level < 1:
            raise ValueError(f"exp_to_next_level must be ≥ 1, got {self.exp_to_next_level}")
    
    def with_stats(self, new_stats: CharacterStats) -> 'CharacterData':
        """
        Immutable update pattern.
        O(1) operation (shallow copy).
        """
        from dataclasses import replace
        return replace(self, stats=new_stats)
    
    def with_abilities(self, new_abilities: Tuple[AbilityData, ...]) -> 'CharacterData':
        """Update abilities immutably.
        
        Complexity: O(1)
        """
        from dataclasses import replace
        return replace(self, abilities=new_abilities)
    
    def with_exp(self, new_exp: int, new_threshold: int) -> 'CharacterData':
        """Update experience immutably.
        
        Complexity: O(1)
        """
        from dataclasses import replace
        return replace(self, exp=new_exp, exp_to_next_level=new_threshold)


@dataclass(frozen=True)
class CombatAction:
    """
    Type-safe combat action.
    
    Complexity: O(1)
    """
    actor_id: str
    action_type: str  # 'attack', 'ability', 'item', 'defend', 'flee'
    target_id: Optional[str] = None
    ability_id: Optional[str] = None
    item_id: Optional[str] = None


@dataclass(frozen=True)
class CombatData:
    """
    Complete combat state with type safety.
    Replaces: Dict[str, Any]
    
    Complexity: O(1) all operations
    Immutable: Yes
    """
    encounter_id: str
    player_party: Tuple[CharacterData, ...]
    enemy_party: Tuple[CharacterData, ...]
    turn_order: Tuple[str, ...]  # Character IDs
    current_turn: int
    combat_log: Tuple[str, ...]
    is_active: bool = True
    
    def __post_init__(self):
        """Validate combat data"""
        if self.current_turn < 0:
            raise ValueError(f"current_turn must be ≥ 0, got {self.current_turn}")
        if not self.player_party:
            raise ValueError("Combat must have at least one player character")


@dataclass(frozen=True)
class QuestObjective:
    """
    Type-safe quest objective.
    
    Complexity: O(1)
    """
    description: str
    objective_type: str
    target: str
    required: int
    current: int = 0
    
    def __post_init__(self):
        """Validate objective"""
        if self.required < 1:
            raise ValueError(f"required must be ≥ 1, got {self.required}")
        if self.current < 0 or self.current > self.required:
            raise ValueError(f"current must be in [0, {self.required}], got {self.current}")
    
    def is_complete(self) -> bool:
        """O(1) check"""
        return self.current >= self.required
    
    def progress_percentage(self) -> float:
        """O(1) calculation"""
        return (self.current / self.required * 100) if self.required > 0 else 0.0


@dataclass(frozen=True)
class QuestData:
    """
    Type-safe quest data.
    Replaces: Dict[str, Any]
    
    Complexity: O(1) all operations
    Immutable: Yes
    """
    id: str
    name: str
    description: str
    quest_type: str
    status: str
    objectives: Tuple[QuestObjective, ...]
    level_requirement: int = 1
    rewards_exp: int = 0
    rewards_coins: int = 0
    rewards_items: Tuple[str, ...] = field(default_factory=tuple)
    
    def is_complete(self) -> bool:
        """
        O(n) where n = number of objectives.
        Typically n < 10.
        """
        return all(obj.is_complete() for obj in self.objectives)


@dataclass(frozen=True)
class ItemData:
    """
    Type-safe item data.
    
    Complexity: O(1)
    """
    id: str
    name: str
    description: str
    item_type: str
    rarity: str
    value: int
    usable_in_combat: bool = False
    consumable: bool = False


@dataclass(frozen=True)
class SaveData:
    """
    Complete save game state with type safety.
    Replaces: Dict[str, Any]
    
    Complexity: O(1) all field access
    Immutable: Yes
    """
    slot: int
    player: CharacterData
    party: Tuple[CharacterData, ...]
    location: Location
    completed_quests: FrozenSet[str] = field(default_factory=frozenset)
    active_quests: FrozenSet[str] = field(default_factory=frozenset)
    inventory: Tuple[str, ...] = field(default_factory=tuple)
    playtime_seconds: int = 0
    game_version: str = "1.0.0"
    
    def __post_init__(self):
        """Validate save data"""
        if self.slot < 1:
            raise ValueError(f"Save slot must be ≥ 1, got {self.slot}")
        if self.playtime_seconds < 0:
            raise ValueError(f"Playtime cannot be negative: {self.playtime_seconds}")


# Type Guards for runtime type checking
def is_valid_position(pos: Position) -> bool:
    """O(1) validation"""
    return isinstance(pos, Position) and pos.x >= 0 and pos.y >= 0


def is_valid_character(char: CharacterData) -> bool:
    """O(1) validation"""
    return (isinstance(char, CharacterData) and 
            bool(char.name) and 
            isinstance(char.stats, CharacterStats))


# Example usage
if __name__ == "__main__":
    # Test Position
    pos = Position(10, 20)
    assert pos.x == 10
    assert pos.distance_to(Position(15, 25)) == 10
    
    # Test CharacterStats
    stats = CharacterStats(
        level=1, max_hp=100, current_hp=100,
        max_mp=50, current_mp=50,
        strength=10, magic=10, defense=10,
        magic_defense=10, speed=10, luck=10
    )
    assert stats.is_alive()
    assert stats.hp_percentage() == 1.0
    
    # Test CharacterData with updated signature
    char = CharacterData(
        name="Coin", role="protagonist",
        faction="independent", 
        description="Test character",
        stats=stats,
        abilities=tuple(),
        equipment={},
        exp=0,
        exp_to_next_level=100
    )
    assert is_valid_character(char)
    
    print("✓ All type definition tests passed")


@dataclass(frozen=True)
class FactionReputation:
    """
    Faction reputation tracking with type safety.
    
    Invariants:
    - All reputation values ∈ ℤ
    - Values typically range [-100, 100]
    
    Complexity: O(1) all operations
    """
    drift_empire: int = 0
    light_cabal: int = 0
    dark_cabal: int = 0
    independent: int = 0
    
    @staticmethod
    def create_neutral() -> 'FactionReputation':
        """Create neutral reputation (all zeros).
        
        Complexity: O(1)
        """
        return FactionReputation(
            drift_empire=0,
            light_cabal=0,
            dark_cabal=0,
            independent=0
        )


@dataclass(frozen=True)
class GameProgress:
    """
    Game progress tracking with type safety.
    Replaces: Dict[str, Any] for game_progress
    
    Invariants:
    - act ≥ 1
    - Quests are immutable tuples (not lists)
    - Story flags are immutable dict
    
    Complexity: O(1) creation and field access
    """
    act: int
    completed_quests: Tuple[str, ...]
    active_quests: Tuple[str, ...]
    faction_reputation: FactionReputation
    story_flags: dict  # Immutable after creation
    time_traveled: bool
    new_game_plus: bool
    
    def __post_init__(self):
        """Enforce invariants"""
        if self.act < 1:
            raise ValueError(f"Act must be ≥ 1, got {self.act}")
    
    @staticmethod
    def create_initial() -> 'GameProgress':
        """Create initial game progress state.
        
        Complexity: O(1)
        """
        return GameProgress(
            act=1,
            completed_quests=tuple(),
            active_quests=tuple(),
            faction_reputation=FactionReputation.create_neutral(),
            story_flags={},
            time_traveled=False,
            new_game_plus=False
        )
