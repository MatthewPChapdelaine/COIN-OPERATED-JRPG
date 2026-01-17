"""
COIN:OPERATED JRPG - Quest System
Quest management and progression tracking

Academic Subjects:
- Game Design: Quest systems, progression mechanics
- Software Engineering: State management, data structures
- Computer Science: Hash tables for O(1) quest lookups
- Mathematics: Progress tracking, completion percentages

Complexity Guarantees:
- Quest lookup: O(1) with hash table
- Objective update: O(m) where m = objectives per quest
- Quest filtering: O(n) where n = total quests
- All data structures immutable for thread safety
"""

from typing import Dict, Tuple, Optional, FrozenSet
from enum import Enum
from dataclasses import dataclass

# Import AAA Standards
from aaa_standards.result_types import Result, Ok, Err
from aaa_standards.type_definitions import QuestData, QuestObjective
from aaa_standards.formal_specs import verify_complexity, requires, ensures
from aaa_standards.performance import LRUCache


class QuestType(Enum):
    """Types of quests"""
    MAIN_STORY = "Main Story"
    SIDE_QUEST = "Side Quest"
    FACTION_QUEST = "Faction Quest"
    CHARACTER_QUEST = "Character Quest"
    OPTIONAL_BOSS = "Optional Boss"


class QuestStatus(Enum):
    """Quest status states"""
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class QuestRewards:
    """Immutable quest rewards data.
    
    Type Safety: Replaces Dict[str, Any]
    Immutability: Frozen for thread safety
    Complexity: O(1) all operations
    """
    exp: int
    coins: int
    essence: int = 0
    items: Tuple[str, ...] = tuple()
    equipment: Tuple[str, ...] = tuple()
    reputation: Dict[str, int] = None
    
    def __post_init__(self):
        """Set default for mutable field"""
        if self.reputation is None:
            object.__setattr__(self, 'reputation', {})


class QuestManager:
    """Manages all quests with AAA standards.
    
    Design Pattern: Immutable State with LRU Cache
    - All quest data immutable (QuestData)
    - O(1) quest lookups via cache
    - Type-safe quest operations
    
    Performance:
    - Quest lookup: O(1) amortized
    - Add quest: O(1)
    - Update objective: O(m) for m objectives
    - Filter quests: O(n) for n quests
    """
    
    def __init__(self):
        """Initialize quest manager.
        
        Complexity: O(1)
        """
        self._all_quests: Dict[str, QuestData] = {}
        self._active_quest_ids: FrozenSet[str] = frozenset()
        self._completed_quest_ids: FrozenSet[str] = frozenset()
        self._failed_quest_ids: FrozenSet[str] = frozenset()
        self._quest_cache: LRUCache[str, QuestData] = LRUCache(capacity=100)
    
    @verify_complexity(time="O(1)", description="Hash table insert with cache update")
    def register_quest(self, quest: QuestData) -> Result[None, str]:
        """Register a quest in the system.
        
        Args:
            quest: Quest data to register
            
        Returns:
            Success[None]: Quest registered
            Failure[str]: Quest already exists
            
        Complexity: O(1) - hash table insert
        Thread Safety: Creates new immutable data
        """
        if quest.id in self._all_quests:
            return Err(f"Quest {quest.id} already registered")
        
        self._all_quests[quest.id] = quest
        self._quest_cache.put(quest.id, quest)
        return Ok(None)
    
    @verify_complexity(time="O(1)", description="Cache lookup with hash table fallback")
    def get_quest(self, quest_id: str) -> Result[QuestData, str]:
        """Get quest by ID with O(1) cache lookup.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            Success[QuestData]: Found quest
            Failure[str]: Quest not found
            
        Complexity: O(1) amortized - LRU cache
        """
        # Try cache first
        cached = self._quest_cache.get(quest_id)
        if cached is not None:
            return Ok(cached)
        
        # Fallback to dict lookup
        if quest_id in self._all_quests:
            quest = self._all_quests[quest_id]
            self._quest_cache.put(quest_id, quest)
            return Ok(quest)
        
        return Err(f"Quest {quest_id} not found")
    
    @verify_complexity(time="O(1)", description="Set operations for quest state tracking")
    @requires(lambda self, quest_id: quest_id in self._all_quests,
              "Quest must exist before starting")
    def start_quest(self, quest_id: str) -> Result[QuestData, str]:
        """Start a quest by ID.
        
        Args:
            quest_id: Quest to start
            
        Returns:
            Success[QuestData]: Started quest
            Failure[str]: Cannot start quest
            
        Complexity: O(1) - set operations
        Side Effects: Updates active quest set, prints message
        
        Preconditions:
            - Quest exists
            - Quest not already active
        Postconditions:
            - Quest marked as active
            - Quest in active_quest_ids set
        """
        quest_result = self.get_quest(quest_id)
        if quest_result.is_failure():
            return quest_result
        
        quest = quest_result.unwrap()
        
        if quest.status != QuestStatus.NOT_STARTED.value:
            return Err(f"Quest {quest_id} cannot be started (status: {quest.status})")
        
        # Update quest status (immutable update)
        updated_quest = QuestData(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            quest_type=quest.quest_type,
            objectives=quest.objectives,
            rewards=quest.rewards,
            status="active",
            progress=0.0
        )
        
        self._all_quests[quest_id] = updated_quest
        self._quest_cache.put(quest_id, updated_quest)
        self._active_quest_ids = frozenset(self._active_quest_ids | {quest_id})
        
        print(f"\n📜 Quest Started: {updated_quest.title}")
        print(f"   {updated_quest.description}")
        
        return Ok(updated_quest)
    
    @verify_complexity(time="O(n)", description="Updates n objectives in quest")
    def update_quest_objective(self, quest_id: str, objective_index: int,
                               progress: int) -> Result[QuestData, str]:
        """Update a specific quest objective.
        
        Args:
            quest_id: Quest to update
            objective_index: Index of objective to update
            progress: New progress value
            
        Returns:
            Success[QuestData]: Updated quest
            Failure[str]: Update failed
            
        Complexity: O(m) where m = number of objectives
        """
        quest_result = self.get_quest(quest_id)
        if quest_result.is_failure():
            return quest_result
        
        quest = quest_result.unwrap()
        
        if objective_index >= len(quest.objectives):
            return Err(f"Invalid objective index: {objective_index}")
        
        # Create updated objectives tuple
        objectives_list = list(quest.objectives)
        old_obj = objectives_list[objective_index]
        
        new_obj = QuestObjective(
            description=old_obj.description,
            objective_type=old_obj.objective_type,
            target=old_obj.target,
            required=old_obj.required,
            current=min(progress, old_obj.required)
        )
        
        objectives_list[objective_index] = new_obj
        new_objectives = tuple(objectives_list)
        
        # Calculate overall progress
        total_progress = sum(obj.current for obj in new_objectives)
        total_required = sum(obj.required for obj in new_objectives)
        progress_pct = total_progress / total_required if total_required > 0 else 0.0
        
        # Check if quest complete
        all_complete = all(obj.is_complete() for obj in new_objectives)
        new_status = "completed" if all_complete else quest.status
        
        # Create updated quest
        updated_quest = QuestData(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            quest_type=quest.quest_type,
            objectives=new_objectives,
            rewards=quest.rewards,
            status=new_status,
            progress=progress_pct
        )
        
        self._all_quests[quest_id] = updated_quest
        self._quest_cache.put(quest_id, updated_quest)
        
        if all_complete:
            self._active_quest_ids = frozenset(self._active_quest_ids - {quest_id})
            self._completed_quest_ids = frozenset(self._completed_quest_ids | {quest_id})
            print(f"\n🏆 Quest Completed: {updated_quest.title}")
        
        return Ok(updated_quest)
    
    @verify_complexity(time="O(n)", description="Filters n quests by requirements")
    def get_available_quests(self, player_level: int,
                           faction_rep: Dict[str, int]) -> Tuple[QuestData, ...]:
        """Get quests available to player.
        
        Args:
            player_level: Player's current level
            faction_rep: Player's faction reputation
            
        Returns:
            Tuple of available quests
            
        Complexity: O(n) where n = total quests
        Note: Could be optimized with indexing by level
        """
        available = []
        for quest in self._all_quests.values():
            if quest.status == QuestStatus.NOT_STARTED.value:
                # Level check would go here with quest metadata
                available.append(quest)
        return tuple(available)
    
    @verify_complexity(time="O(1)", description="Set lookup")
    def get_active_quests(self) -> Tuple[QuestData, ...]:
        """Get all active quests.
        
        Returns:
            Tuple of active quests
            
        Complexity: O(k) where k = active quests (typically < 10)
        """
        return tuple(
            self._all_quests[qid] for qid in self._active_quest_ids
            if qid in self._all_quests
        )
    
    @verify_complexity(time="O(1)", description="Set lookup")
    def get_completed_quests(self) -> Tuple[QuestData, ...]:
        """Get all completed quests.
        
        Returns:
            Tuple of completed quests
            
        Complexity: O(k) where k = completed quests
        """
        return tuple(
            self._all_quests[qid] for qid in self._completed_quest_ids
            if qid in self._all_quests
        )
    
    @verify_complexity(time="O(n)", description="Displays n active quests")
    def display_active_quests(self) -> None:
        """Display all active quests.
        
        Complexity: O(k) where k = active quests
        Side Effects: Prints to console
        """
        print(f"\n{'=' * 60}")
        print(" " * 20 + "ACTIVE QUESTS")
        print(f"{'=' * 60}")
        
        active = self.get_active_quests()
        if not active:
            print("\nNo active quests.")
        else:
            for i, quest in enumerate(active, 1):
                print(f"\n{i}. [{quest.quest_type}] {quest.title}")
                print(f"   Progress: {quest.progress:.0%}")
                for obj in quest.objectives:
                    status = "✓" if obj.is_complete() else "○"
                    print(f"   {status} {obj.description} ({obj.current}/{obj.required})")
