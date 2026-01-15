"""
COIN:OPERATED JRPG - Act 3 Content
Temporal Awakening - Time travel and destiny
"""

from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from systems.dialogue import Dialogue, DialogueNode, DialogueChoice, NPC, NPCManager


def create_act3_quests(quest_manager: QuestManager):
    """Create Act 3 quests - Temporal Awakening"""
    
    # Main Quest: Meeting Elder Coin
    quest_elder_coin = Quest(
        quest_id="act3_main_01",
        name="Meeting Your Future",
        description="A mysterious time ship appears, and aboard it is... you, from the future.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=15
    )
    quest_elder_coin.add_objective(QuestObjective(
        "Board the Time Ship",
        "explore",
        "time_ship"
    ))
    quest_elder_coin.add_objective(QuestObjective(
        "Speak with Elder Coin",
        "dialogue",
        "elder_coin_meeting"
    ))
    quest_elder_coin.add_objective(QuestObjective(
        "Learn about your role as Time Goddess",
        "event",
        "time_goddess_revelation"
    ))
    quest_elder_coin.set_rewards(
        exp=1500,
        essence=500,
        items=["Time Fragment"]
    )
    quest_manager.register_quest(quest_elder_coin)
    
    # Main Quest: Time Travel Training
    quest_time_training = Quest(
        quest_id="act3_main_02",
        name="Mastering Time",
        description="Elder Coin teaches you to wield temporal magic and see across timelines.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=16
    )
    quest_time_training.add_objective(QuestObjective(
        "Complete temporal exercises",
        "event",
        "time_exercise",
        required=5
    ))
    quest_time_training.add_objective(QuestObjective(
        "Glimpse alternate timelines",
        "event",
        "timeline_vision"
    ))
    quest_time_training.add_objective(QuestObjective(
        "Unlock Time Goddess abilities",
        "event",
        "time_goddess_unlock"
    ))
    quest_time_training.set_rewards(
        exp=2000,
        essence=750,
        items=["Chrono Amulet"]
    )
    quest_manager.register_quest(quest_time_training)
    
    # Main Quest: Noble Stones
    quest_noble_stones = Quest(
        quest_id="act3_main_03",
        name="The Four Noble Stones",
        description="Learn about the Noble Stones and their role in maintaining Orbspace's stability.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=18
    )
    quest_noble_stones.add_objective(QuestObjective(
        "Visit the Endless Library",
        "explore",
        "endless_library"
    ))
    quest_noble_stones.add_objective(QuestObjective(
        "Research Noble Stones history",
        "event",
        "noble_stones_research"
    ))
    quest_noble_stones.add_objective(QuestObjective(
        "Locate the CircuitStone",
        "event",
        "circuitstone_location"
    ))
    quest_noble_stones.set_rewards(
        exp=2500,
        coins=1500,
        essence=1000
    )
    quest_manager.register_quest(quest_noble_stones)
    
    # Main Quest: Temporal Paradox
    quest_paradox = Quest(
        quest_id="act3_main_04",
        name="Paradox Prevention",
        description="You must travel back in time to set events in motion that led to your own existence.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=20
    )
    quest_paradox.add_objective(QuestObjective(
        "Travel to the past",
        "event",
        "time_travel_past"
    ))
    quest_paradox.add_objective(QuestObjective(
        "Influence key historical events",
        "event",
        "historical_influence",
        required=3
    ))
    quest_paradox.add_objective(QuestObjective(
        "Return to present without destroying timeline",
        "event",
        "stable_return"
    ))
    quest_paradox.set_rewards(
        exp=3000,
        essence=1500
    )
    quest_manager.register_quest(quest_paradox)
    
    # Main Quest: Destiny's Choice
    quest_destiny = Quest(
        quest_id="act3_main_05",
        name="Accept or Reject",
        description="The ultimate question: will you accept your destiny as Time Goddess, or forge your own path?",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=22
    )
    quest_destiny.add_objective(QuestObjective(
        "Witness possible futures",
        "event",
        "future_visions",
        required=5
    ))
    quest_destiny.add_objective(QuestObjective(
        "Make your choice",
        "choice",
        "destiny_decision"
    ))
    quest_destiny.set_rewards(
        exp=4000,
        essence=2000
    )
    quest_manager.register_quest(quest_destiny)
    
    # Side Quest: Time-Displaced Allies
    quest_time_allies = Quest(
        quest_id="act3_side_01",
        name="Echoes from Other Times",
        description="Recruit allies from different timelines who want to help stabilize Orbspace.",
        quest_type=QuestType.SIDE_QUEST,
        quest_giver="Elder Coin",
        level_requirement=17
    )
    quest_time_allies.add_objective(QuestObjective(
        "Locate time-displaced individuals",
        "event",
        "find_displaced",
        required=3
    ))
    quest_time_allies.add_objective(QuestObjective(
        "Help them adjust to current timeline",
        "event",
        "timeline_adjustment"
    ))
    quest_time_allies.set_rewards(
        exp=1500,
        coins=1000,
        equipment=["Temporal Resonator"]
    )
    quest_manager.register_quest(quest_time_allies)


def create_act3_npcs(npc_manager: NPCManager):
    """Create Act 3 NPCs"""
    
    # Elder Coin (future version of protagonist)
    elder_coin = NPC(
        "elder_coin",
        "Elder Coin",
        "Your future self - the fully realized Time Goddess who has mastered temporal magic.",
        "time_ship",
        "independent"
    )
    elder_coin.add_quest("act3_main_01")
    elder_coin.add_quest("act3_main_02")
    elder_coin.default_dialogue = "Elder Coin: I remember this moment. Trust yourself, young one."
    npc_manager.register_npc(elder_coin)
    
    # Librarian of Endless Library
    librarian = NPC(
        "librarian_chronos",
        "Chronos the Librarian",
        "Guardian of the Endless Library, keeper of all Orbspace knowledge across all timelines.",
        "endless_library",
        "independent"
    )
    librarian.default_dialogue = "Chronos: Every book here exists in every timeline. Fascinating, isn't it?"
    npc_manager.register_npc(librarian)
    
    # Time-Displaced Warrior
    warrior = NPC(
        "warrior_displaced",
        "Kiran of Lost Time",
        "A warrior from an alternate timeline where Coin never existed.",
        "time_ship",
        "independent"
    )
    warrior.default_dialogue = "Kiran: In my timeline, Orbspace fell to chaos. You are our hope."
    npc_manager.register_npc(warrior)


def initialize_act3_content(quest_manager, dialogue_system, npc_manager):
    """Initialize all Act 3 content"""
    create_act3_quests(quest_manager)
    create_act3_npcs(npc_manager)
    print("✓ Act 3 content initialized")
