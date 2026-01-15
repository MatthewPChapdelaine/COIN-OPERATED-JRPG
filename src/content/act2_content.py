"""
COIN:OPERATED JRPG - Act 2 Content
Independence & Conflict - Coin's journey alone
"""

from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from systems.dialogue import Dialogue, DialogueNode, DialogueChoice, NPC, NPCManager


def create_act2_quests(quest_manager: QuestManager):
    """Create Act 2 quests - Independence & Conflict"""
    
    # Main Quest: The Separation
    quest_separation = Quest(
        quest_id="act2_main_01",
        name="Breaking Free",
        description="After your confrontation, you must decide whether to trust Jinn-Lir or strike out alone.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=5
    )
    quest_separation.add_objective(QuestObjective(
        "Leave Jinn-Lir's sanctuary",
        "explore",
        "drift_capital"
    ))
    quest_separation.add_objective(QuestObjective(
        "Find safe haven in the city",
        "event",
        "safe_haven"
    ))
    quest_separation.set_rewards(exp=300, coins=200, essence=50)
    quest_manager.register_quest(quest_separation)
    
    # Main Quest: Retrieving the Coins
    quest_coins = Quest(
        quest_id="act2_main_02",
        name="Coin Collection",
        description="Retrieve your Domminnian Coins that were scattered across the city.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=6
    )
    quest_coins.add_objective(QuestObjective(
        "Locate scattered Domminnian Coins",
        "collect",
        "domminnian_coin",
        required=10
    ))
    quest_coins.add_objective(QuestObjective(
        "Defeat thieves who stole coins",
        "defeat",
        "coin_thief",
        required=5
    ))
    quest_coins.set_rewards(
        exp=400,
        coins=500,
        essence=100,
        items=["Coin Fragment Amulet"]
    )
    quest_manager.register_quest(quest_coins)
    
    # Main Quest: Dark Cabal Manipulation
    quest_dark_cabal = Quest(
        quest_id="act2_main_03",
        name="Whispers in the Dark",
        description="The Dark Cabal approaches you with promises of power and freedom.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Selene (Dark Cabal)",
        level_requirement=8
    )
    quest_dark_cabal.add_objective(QuestObjective(
        "Meet with Dark Cabal representatives",
        "talk",
        "selene"
    ))
    quest_dark_cabal.add_objective(QuestObjective(
        "Witness Dark Cabal methods",
        "event",
        "dark_demonstration"
    ))
    quest_dark_cabal.add_objective(QuestObjective(
        "Choose: Join Dark Cabal, Refuse, or Negotiate",
        "choice",
        "dark_cabal_choice"
    ))
    quest_dark_cabal.set_rewards(
        exp=600,
        essence=150,
        reputation={'dark_cabal': 25}  # Or negative if refused
    )
    quest_manager.register_quest(quest_dark_cabal)
    
    # Main Quest: Super Soldier Encounters
    quest_super_soldiers = Quest(
        quest_id="act2_main_04",
        name="Facing Your Power",
        description="Encounter super-soldiers empowered by your own stolen magic.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=10
    )
    quest_super_soldiers.add_objective(QuestObjective(
        "Defeat corrupted super-soldiers",
        "defeat",
        "super_soldier",
        required=3
    ))
    quest_super_soldiers.add_objective(QuestObjective(
        "Confront Coireena",
        "boss",
        "coireena_encounter"
    ))
    quest_super_soldiers.set_rewards(
        exp=800,
        coins=600,
        essence=200
    )
    quest_manager.register_quest(quest_super_soldiers)
    
    # Main Quest: Emperor Turok Encounter
    quest_turok = Quest(
        quest_id="act2_main_05",
        name="The Emperor's Gambit",
        description="A confrontation with Emperor Turok himself - but this isn't meant to be won.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=12
    )
    quest_turok.add_objective(QuestObjective(
        "Infiltrate Drift Palace",
        "explore",
        "drift_palace"
    ))
    quest_turok.add_objective(QuestObjective(
        "Face Emperor Turok (non-lethal)",
        "boss",
        "emperor_turok"
    ))
    quest_turok.add_objective(QuestObjective(
        "Escape from Drift Palace",
        "event",
        "palace_escape"
    ))
    quest_turok.set_rewards(
        exp=1200,
        coins=1000,
        essence=300,
        reputation={'drift_empire': -50}
    )
    quest_manager.register_quest(quest_turok)
    
    # Side Quest: Underground Resistance
    quest_resistance = Quest(
        quest_id="act2_side_01",
        name="Voices of Dissent",
        description="An underground resistance movement seeks your help against the Drift Empire.",
        quest_type=QuestType.SIDE_QUEST,
        quest_giver="Resistance Leader Kael",
        level_requirement=7
    )
    quest_resistance.add_objective(QuestObjective(
        "Disrupt Drift supply lines",
        "event",
        "supply_disruption",
        required=3
    ))
    quest_resistance.add_objective(QuestObjective(
        "Rescue imprisoned resistance members",
        "event",
        "rescue_prisoners"
    ))
    quest_resistance.set_rewards(
        exp=500,
        coins=300,
        equipment=["Resistance Band"],
        reputation={'independent': 30, 'drift_empire': -20}
    )
    quest_manager.register_quest(quest_resistance)


def create_act2_npcs(npc_manager: NPCManager):
    """Create Act 2 NPCs"""
    
    # Selene - Dark Cabal Representative
    selene = NPC(
        "selene",
        "Selene",
        "A charismatic Dark Cabal mage who offers power without pretense of goodness.",
        "dark_cabal_hideout",
        "dark_cabal"
    )
    selene.add_quest("act2_main_03")
    selene.default_dialogue = "Selene: Power recognizes power, Coin. Join us and be free of their chains."
    npc_manager.register_npc(selene)
    
    # Resistance Leader Kael
    kael = NPC(
        "kael",
        "Kael",
        "Leader of the underground resistance against the Drift Empire.",
        "resistance_hideout",
        "independent"
    )
    kael.add_quest("act2_side_01")
    kael.default_dialogue = "Kael: We fight for freedom from both magic tyranny and technological oppression."
    npc_manager.register_npc(kael)
    
    # Informant
    informant = NPC(
        "informant_shadows",
        "Mysterious Informant",
        "A hooded figure who seems to know more than they should.",
        "drift_capital",
        "unknown"
    )
    informant.default_dialogue = "Informant: The Emperor knows about you. Be careful, Time Goddess..."
    npc_manager.register_npc(informant)


def initialize_act2_content(quest_manager, dialogue_system, npc_manager):
    """Initialize all Act 2 content"""
    create_act2_quests(quest_manager)
    create_act2_npcs(npc_manager)
    print("✓ Act 2 content initialized")
