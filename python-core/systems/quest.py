"""
COIN:OPERATED JRPG - Quest System
Quest management and generation
"""

from typing import Dict, List, Optional
from enum import Enum


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


class QuestObjective:
    """Individual quest objective"""
    
    def __init__(self, description: str, objective_type: str, target: str = "", 
                 required: int = 1, current: int = 0):
        self.description = description
        self.objective_type = objective_type  # defeat, collect, talk, explore, etc.
        self.target = target
        self.required = required
        self.current = current
        self.completed = False
    
    def progress(self, amount: int = 1):
        """Progress objective"""
        self.current = min(self.current + amount, self.required)
        if self.current >= self.required:
            self.completed = True
            return True
        return False
    
    def display(self) -> str:
        """Display objective status"""
        status = "✓" if self.completed else "○"
        return f"  {status} {self.description} ({self.current}/{self.required})"


class Quest:
    """Quest class"""
    
    def __init__(self, quest_id: str, name: str, description: str, quest_type: QuestType,
                 quest_giver: str = "", level_requirement: int = 1, 
                 faction_requirement: Optional[Dict[str, int]] = None):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.quest_type = quest_type
        self.quest_giver = quest_giver
        self.level_requirement = level_requirement
        self.faction_requirement = faction_requirement or {}
        self.status = QuestStatus.NOT_STARTED
        self.objectives: List[QuestObjective] = []
        self.rewards = {
            'exp': 0,
            'coins': 0,
            'essence': 0,
            'items': [],
            'equipment': [],
            'reputation': {}
        }
        self.dialogue_start = []
        self.dialogue_progress = []
        self.dialogue_complete = []
    
    def add_objective(self, objective: QuestObjective):
        """Add objective to quest"""
        self.objectives.append(objective)
    
    def set_rewards(self, exp: int = 0, coins: int = 0, essence: int = 0,
                    items: Optional[List] = None, equipment: Optional[List] = None,
                    reputation: Optional[Dict[str, int]] = None):
        """Set quest rewards"""
        self.rewards['exp'] = exp
        self.rewards['coins'] = coins
        self.rewards['essence'] = essence
        self.rewards['items'] = items or []
        self.rewards['equipment'] = equipment or []
        self.rewards['reputation'] = reputation or {}
    
    def start(self):
        """Start the quest"""
        if self.status == QuestStatus.NOT_STARTED:
            self.status = QuestStatus.ACTIVE
            print(f"\n📜 Quest Started: {self.name}")
            print(f"   {self.description}")
            return True
        return False
    
    def update_objective(self, objective_type: str, target: str, amount: int = 1) -> bool:
        """Update quest objective progress"""
        for objective in self.objectives:
            if objective.objective_type == objective_type and objective.target == target:
                if objective.progress(amount):
                    print(f"✓ Objective completed: {objective.description}")
                    self.check_completion()
                    return True
        return False
    
    def check_completion(self) -> bool:
        """Check if all objectives are completed"""
        if all(obj.completed for obj in self.objectives):
            self.complete()
            return True
        return False
    
    def complete(self):
        """Complete the quest"""
        if self.status == QuestStatus.ACTIVE:
            self.status = QuestStatus.COMPLETED
            print(f"\n🏆 Quest Completed: {self.name}")
            return True
        return False
    
    def fail(self):
        """Fail the quest"""
        self.status = QuestStatus.FAILED
    
    def display(self):
        """Display quest information"""
        print(f"\n{'=' * 60}")
        print(f"[{self.quest_type.value}] {self.name}")
        print(f"{'=' * 60}")
        print(f"\nQuest Giver: {self.quest_giver}")
        print(f"Level Requirement: {self.level_requirement}")
        print(f"Status: {self.status.value.replace('_', ' ').title()}")
        print(f"\n{self.description}")
        
        if self.objectives:
            print(f"\nObjectives:")
            for obj in self.objectives:
                print(obj.display())
        
        if self.status == QuestStatus.COMPLETED:
            print(f"\nRewards:")
            if self.rewards['exp']:
                print(f"  Experience: {self.rewards['exp']}")
            if self.rewards['coins']:
                print(f"  Domminnian Coins: {self.rewards['coins']}")
            if self.rewards['essence']:
                print(f"  Magical Essence: {self.rewards['essence']}")
            if self.rewards['items']:
                print(f"  Items: {', '.join(self.rewards['items'])}")
            if self.rewards['reputation']:
                for faction, rep in self.rewards['reputation'].items():
                    print(f"  {faction.replace('_', ' ').title()}: {rep:+d}")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'quest_id': self.quest_id,
            'name': self.name,
            'description': self.description,
            'quest_type': self.quest_type.value,
            'quest_giver': self.quest_giver,
            'status': self.status.value,
            'objectives': [
                {
                    'description': obj.description,
                    'type': obj.objective_type,
                    'target': obj.target,
                    'current': obj.current,
                    'required': obj.required,
                    'completed': obj.completed
                }
                for obj in self.objectives
            ],
            'rewards': self.rewards
        }


class QuestManager:
    """Manages all quests in the game"""
    
    def __init__(self):
        self.all_quests: Dict[str, Quest] = {}
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        self.failed_quests: List[Quest] = []
    
    def register_quest(self, quest: Quest):
        """Register a quest in the system"""
        self.all_quests[quest.quest_id] = quest
    
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest by ID"""
        if quest_id in self.all_quests:
            quest = self.all_quests[quest_id]
            if quest.start():
                self.active_quests.append(quest)
                return True
        return False
    
    def update_quest_objective(self, objective_type: str, target: str, amount: int = 1):
        """Update objectives across all active quests"""
        for quest in self.active_quests:
            quest.update_objective(objective_type, target, amount)
    
    def complete_quest(self, quest_id: str) -> Optional[Dict]:
        """Complete a quest and return rewards"""
        if quest_id in self.all_quests:
            quest = self.all_quests[quest_id]
            if quest.complete():
                if quest in self.active_quests:
                    self.active_quests.remove(quest)
                self.completed_quests.append(quest)
                return quest.rewards
        return None
    
    def get_available_quests(self, level: int, faction_rep: Dict[str, int]) -> List[Quest]:
        """Get quests available to player"""
        available = []
        for quest in self.all_quests.values():
            if quest.status == QuestStatus.NOT_STARTED:
                if level >= quest.level_requirement:
                    # Check faction requirements
                    meets_faction_req = True
                    for faction, req_rep in quest.faction_requirement.items():
                        if faction_rep.get(faction, 0) < req_rep:
                            meets_faction_req = False
                            break
                    if meets_faction_req:
                        available.append(quest)
        return available
    
    def display_active_quests(self):
        """Display all active quests"""
        print(f"\n{'=' * 60}")
        print(" " * 20 + "ACTIVE QUESTS")
        print(f"{'=' * 60}")
        
        if not self.active_quests:
            print("\nNo active quests.")
        else:
            for i, quest in enumerate(self.active_quests, 1):
                print(f"\n{i}. [{quest.quest_type.value}] {quest.name}")
                for obj in quest.objectives:
                    print(obj.display())
    
    def display_completed_quests(self):
        """Display completed quests"""
        print(f"\n{'=' * 60}")
        print(" " * 18 + "COMPLETED QUESTS")
        print(f"{'=' * 60}")
        
        if not self.completed_quests:
            print("\nNo completed quests yet.")
        else:
            for quest in self.completed_quests:
                print(f"\n✓ [{quest.quest_type.value}] {quest.name}")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'active_quests': [q.to_dict() for q in self.active_quests],
            'completed_quests': [q.to_dict() for q in self.completed_quests],
            'failed_quests': [q.to_dict() for q in self.failed_quests]
        }
