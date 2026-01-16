"""
COIN:OPERATED JRPG - Act 1 Content
Origins & Exploitation - Story content, quests, and NPCs
"""

from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from systems.dialogue import Dialogue, DialogueNode, DialogueChoice, NPC, NPCManager
from core.character import Coin, JinnLir, Character, CharacterRole, CharacterFaction


def create_act1_quests(quest_manager: QuestManager):
    """Create all Act 1 quests"""
    
    # Main Quest 1: Awakening
    quest_awakening = Quest(
        quest_id="act1_main_01",
        name="Awakening",
        description="You have just been created by Jinn-Lir. Learn about your nature and purpose.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Jinn-Lir",
        level_requirement=1
    )
    quest_awakening.add_objective(QuestObjective(
        "Listen to Jinn-Lir's explanation",
        "dialogue",
        "jinn_lir_awakening"
    ))
    quest_awakening.add_objective(QuestObjective(
        "Learn basic magic abilities",
        "tutorial",
        "magic_training"
    ))
    quest_awakening.set_rewards(exp=50, coins=0, essence=10)
    quest_manager.register_quest(quest_awakening)
    
    # Main Quest 2: First Mission
    quest_first_mission = Quest(
        quest_id="act1_main_02",
        name="The First Mission",
        description="Jinn-Lir sends you to deal with Drift forces threatening the Lifeblood Temple.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Jinn-Lir",
        level_requirement=1
    )
    quest_first_mission.add_objective(QuestObjective(
        "Travel to Lifeblood Temple",
        "explore",
        "lifeblood_temple"
    ))
    quest_first_mission.add_objective(QuestObjective(
        "Defeat Drift soldiers",
        "defeat",
        "drift_soldier",
        required=3
    ))
    quest_first_mission.add_objective(QuestObjective(
        "Report back to Jinn-Lir",
        "talk",
        "jinn_lir"
    ))
    quest_first_mission.set_rewards(
        exp=100,
        coins=50,
        essence=20,
        reputation={'light_cabal': 10}
    )
    quest_manager.register_quest(quest_first_mission)
    
    # Main Quest 3: Meeting Orbius
    quest_meet_orbius = Quest(
        quest_id="act1_main_03",
        name="The Master's Summons",
        description="Jinn-Lir brings you to meet Orbius, the master of the Light Cabal.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Jinn-Lir",
        level_requirement=2
    )
    quest_meet_orbius.add_objective(QuestObjective(
        "Meet Orbius at the Light Cabal headquarters",
        "talk",
        "orbius"
    ))
    quest_meet_orbius.add_objective(QuestObjective(
        "Learn about the conflict between magic and technology",
        "dialogue",
        "orbius_explanation"
    ))
    quest_meet_orbius.set_rewards(
        exp=150,
        essence=30,
        reputation={'light_cabal': 15}
    )
    quest_manager.register_quest(quest_meet_orbius)
    
    # Main Quest 4: The Power Drain
    quest_power_drain = Quest(
        quest_id="act1_main_04",
        name="The Power Drain",
        description="Jinn-Lir forces you to donate your magical essence to create super-soldiers.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Jinn-Lir",
        level_requirement=3
    )
    quest_power_drain.add_objective(QuestObjective(
        "Endure multiple power-draining sessions",
        "event",
        "power_drain",
        required=5
    ))
    quest_power_drain.add_objective(QuestObjective(
        "Meet the first super-soldier: Coireena",
        "talk",
        "coireena"
    ))
    quest_power_drain.set_rewards(exp=200, coins=100, essence=0)  # No essence gained
    quest_manager.register_quest(quest_power_drain)
    
    # Main Quest 5: Breaking Point
    quest_breaking_point = Quest(
        quest_id="act1_main_05",
        name="Breaking Point",
        description="You've had enough of being exploited. Your magical power erupts uncontrollably.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=4
    )
    quest_breaking_point.add_objective(QuestObjective(
        "Confront Jinn-Lir about the exploitation",
        "dialogue",
        "confrontation"
    ))
    quest_breaking_point.add_objective(QuestObjective(
        "Survive the magical outburst (Tutorial Boss Fight)",
        "boss",
        "magical_outburst"
    ))
    quest_breaking_point.add_objective(QuestObjective(
        "Choose: Trust Jinn-Lir or Strike Out Alone",
        "choice",
        "act1_ending_choice"
    ))
    quest_breaking_point.set_rewards(
        exp=500,
        coins=200,
        essence=100,
        reputation={'light_cabal': -20}  # Negative for rebellion
    )
    quest_manager.register_quest(quest_breaking_point)
    
    # Side Quest: Temple Protection
    quest_temple = Quest(
        quest_id="act1_side_01",
        name="Sanctity of the Temple",
        description="Lifeblood priests ask for help protecting sacred artifacts from Drift raiders.",
        quest_type=QuestType.SIDE_QUEST,
        quest_giver="High Priest Maleon",
        level_requirement=2
    )
    quest_temple.add_objective(QuestObjective(
        "Defeat Drift raiders",
        "defeat",
        "drift_raider",
        required=5
    ))
    quest_temple.add_objective(QuestObjective(
        "Recover stolen artifacts",
        "collect",
        "sacred_artifact",
        required=3
    ))
    quest_temple.set_rewards(
        exp=150,
        coins=100,
        essence=25,
        items=["Healing Potion x3"],
        reputation={'light_cabal': 5, 'drift_empire': -5}
    )
    quest_manager.register_quest(quest_temple)
    
    # Side Quest: Lost Citizen
    quest_lost_citizen = Quest(
        quest_id="act1_side_02",
        name="Lost in the Outskirts",
        description="A citizen from Acadmium City is lost in the dangerous outskirts.",
        quest_type=QuestType.SIDE_QUEST,
        quest_giver="Guard Captain Velos",
        level_requirement=1
    )
    quest_lost_citizen.add_objective(QuestObjective(
        "Search the outskirts",
        "explore",
        "acadmium_outskirts"
    ))
    quest_lost_citizen.add_objective(QuestObjective(
        "Rescue the lost citizen",
        "event",
        "rescue_citizen"
    ))
    quest_lost_citizen.add_objective(QuestObjective(
        "Escort citizen back to city",
        "escort",
        "citizen_escort"
    ))
    quest_lost_citizen.set_rewards(
        exp=75,
        coins=50,
        reputation={'independent': 10}
    )
    quest_manager.register_quest(quest_lost_citizen)
    
    # Faction Quest: Light Cabal
    quest_cabal_initiate = Quest(
        quest_id="act1_faction_light_01",
        name="Prove Your Worth",
        description="Orbius wants to test your magical abilities before trusting you fully.",
        quest_type=QuestType.FACTION_QUEST,
        quest_giver="Orbius",
        level_requirement=3,
        faction_requirement={'light_cabal': 25}
    )
    quest_cabal_initiate.add_objective(QuestObjective(
        "Complete magical trials",
        "event",
        "magical_trial",
        required=3
    ))
    quest_cabal_initiate.add_objective(QuestObjective(
        "Defeat summoned magical construct",
        "defeat",
        "magical_construct"
    ))
    quest_cabal_initiate.set_rewards(
        exp=300,
        coins=150,
        essence=75,
        equipment=["Apprentice's Staff"],
        reputation={'light_cabal': 25}
    )
    quest_manager.register_quest(quest_cabal_initiate)


def create_act1_dialogues(dialogue_system, npc_manager):
    """Create Act 1 dialogues"""
    
    # Dialogue: Coin's Awakening
    awakening_dialogue = Dialogue("jinn_lir_awakening", "Awakening", "start")
    
    awakening_dialogue.add_node(DialogueNode(
        "start",
        "Jinn-Lir",
        "Open your eyes, my creation. Yes... yes! It worked! You are awake, and you are perfect.",
        auto_next="coin_responds"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "coin_responds",
        "Coin",
        "Where... where am I? What am I?",
        auto_next="explanation"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "explanation",
        "Jinn-Lir",
        "You are in my sanctuary, deep within Acadmium. As for what you are... you are Coin, a being I have created from Domminnian Coins and pure magical essence. You are sentient, powerful, and essential to our cause.",
        auto_next="purpose"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "purpose",
        "Jinn-Lir",
        "The Drift Empire threatens all magic users with their technology. The Light Cabal needs power to fight back, and you, my dear Coin, can provide that power. Will you help us?",
        choices=[
            DialogueChoice("I want to help.", next_node="accept"),
            DialogueChoice("What choice do I have?", next_node="reluctant"),
            DialogueChoice("Tell me more about this conflict.", next_node="learn_more")
        ]
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "accept",
        "Coin",
        "If I was created to help, then I will do my best.",
        auto_next="training"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "reluctant",
        "Coin",
        "I don't understand any of this, but I suppose I have no choice...",
        auto_next="training"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "learn_more",
        "Jinn-Lir",
        "The Drift Empire believes technology should rule all of Orbspace. They hunt magic users, imprison them, force them to serve their technological empire. We of the Light Cabal preserve the ancient magical traditions. This is a war for the soul of our universe.",
        auto_next="training"
    ))
    
    awakening_dialogue.add_node(DialogueNode(
        "training",
        "Jinn-Lir",
        "Good. Now, let me teach you to harness your innate magical abilities. Focus your energy, and feel the magic flow through you...",
        auto_next=None  # End dialogue
    ))
    
    dialogue_system.register_dialogue(awakening_dialogue)
    
    # Dialogue: Meeting Orbius
    orbius_dialogue = Dialogue("orbius_introduction", "The Master", "start")
    
    orbius_dialogue.add_node(DialogueNode(
        "start",
        "Orbius",
        "So this is the creation Jinn-Lir spoke of. Fascinating. You possess remarkable magical energy, young one.",
        auto_next="coin_nervous"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "coin_nervous",
        "Coin",
        "Thank you, Master Orbius. Jinn-Lir has told me about you. You know everything about Orbspace.",
        auto_next="orbius_knowing"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "orbius_knowing",
        "Orbius",
        "*smiles mysteriously* Not everything, dear Coin. But I know enough. I know, for instance, that your role in this conflict is far greater than even Jinn-Lir realizes. Tell me, do you understand what you truly are?",
        choices=[
            DialogueChoice("I'm a magical being created to help the Light Cabal.", next_node="surface_truth"),
            DialogueChoice("I... I'm not sure. What do you mean?", next_node="deeper_truth"),
            DialogueChoice("Does it matter? I am what I am.", next_node="philosophical")
        ]
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "surface_truth",
        "Orbius",
        "Yes, that is what you are told. But identity is more than origin, young Coin. In time, you will discover truths even I cannot fully reveal to you yet.",
        auto_next="warning"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "deeper_truth",
        "Coin",
        "You speak in riddles. If you know something about me, please tell me!",
        auto_next="patience"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "patience",
        "Orbius",
        "Patience, dear one. Some truths must be discovered, not told. Your journey has only just begun. Trust in your own power, not just in what others tell you.",
        auto_next="warning"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "philosophical",
        "Orbius",
        "*chuckles* Wise words from one so young. Yes, you are what you choose to be. Remember that in the difficult times ahead.",
        auto_next="warning"
    ))
    
    orbius_dialogue.add_node(DialogueNode(
        "warning",
        "Orbius",
        "Jinn-Lir is brilliant but... complicated. He will ask much of you. Remember that you have agency, Coin. You always have a choice.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(orbius_dialogue)
    
    # Dialogue: The Confrontation
    confrontation_dialogue = Dialogue("confrontation", "Breaking Point", "start")
    
    confrontation_dialogue.add_node(DialogueNode(
        "start",
        "Coin",
        "No more, Jinn-Lir! I won't let you drain me again!",
        auto_next="jinn_surprised"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "jinn_surprised",
        "Jinn-Lir",
        "Coin! Calm yourself. You don't understand what's at stake. These soldiers need your power to-",
        auto_next="coin_anger"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "coin_anger",
        "Coin",
        "To fight YOUR war! I am not a tool! I am not just coins to be spent! I... I don't know what I am, but I know I won't be used like this anymore!",
        auto_next="jinn_pleading"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "jinn_pleading",
        "Jinn-Lir",
        "Coin, please, you must understand- the Drift Empire will destroy us all if we don't fight back. I created you to save us!",
        choices=[
            DialogueChoice("You created me for yourself, not for me!", next_node="reject"),
            DialogueChoice("Maybe you did, but this is wrong. There must be another way.", next_node="compromise"),
            DialogueChoice("*magical energy surges uncontrollably*", next_node="eruption")
        ]
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "reject",
        "Coin",
        "I am done being your weapon. If you won't let me go, I'll make you!",
        auto_next="eruption"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "compromise",
        "Coin",
        "I'll help fight the Drift Empire, but as a person, not a resource to be drained. Treat me with respect, or lose me forever.",
        auto_next="jinn_considers"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "jinn_considers",
        "Jinn-Lir",
        "*long pause* You're right. I... I have treated you poorly. Forgive me, Coin. I was so focused on the war that I forgot you are not merely a tool, but a sentient being. Can we start anew?",
        auto_next="eruption"
    ))
    
    confrontation_dialogue.add_node(DialogueNode(
        "eruption",
        "Narrator",
        "*Your magical power erupts in a brilliant explosion of light and energy! The room shakes as your emotions manifest as raw magical force!*",
        auto_next=None  # Leads to boss fight
    ))
    
    dialogue_system.register_dialogue(confrontation_dialogue)


def create_act1_npcs(npc_manager: NPCManager):
    """Create Act 1 NPCs"""
    
    # Jinn-Lir (already exists as playable character, but also NPC)
    jinn_lir_npc = NPC(
        "jinn_lir",
        "Jinn-Lir",
        "A powerful wizard of the Light Cabal. Your creator and mentor, though his methods are questionable.",
        "jinn_lir_sanctuary",
        "light_cabal"
    )
    jinn_lir_npc.add_dialogue("jinn_lir_awakening")
    jinn_lir_npc.add_quest("act1_main_01")
    jinn_lir_npc.add_quest("act1_main_02")
    jinn_lir_npc.default_dialogue = "Jinn-Lir: Coin, we have much work to do."
    npc_manager.register_npc(jinn_lir_npc)
    
    # Orbius
    orbius_npc = NPC(
        "orbius",
        "Orbius",
        "Master of the Light Cabal. Cryptic and all-knowing, he seems to understand your true nature better than anyone.",
        "light_cabal_headquarters",
        "light_cabal"
    )
    orbius_npc.add_dialogue("orbius_introduction")
    orbius_npc.add_quest("act1_main_03")
    orbius_npc.add_quest("act1_faction_light_01")
    orbius_npc.default_dialogue = "Orbius: Time reveals all truths, young Coin."
    npc_manager.register_npc(orbius_npc)
    
    # High Priest Maleon
    maleon = NPC(
        "maleon",
        "High Priest Maleon",
        "Leader of the Lifeblood priests. Devoted to protecting ancient magical traditions.",
        "lifeblood_temple",
        "light_cabal"
    )
    maleon.add_quest("act1_side_01")
    maleon.default_dialogue = "High Priest Maleon: May the ancient magic protect you, child."
    npc_manager.register_npc(maleon)
    
    # Guard Captain Velos
    velos = NPC(
        "velos",
        "Guard Captain Velos",
        "Captain of the Acadmium city guard. Tries to remain neutral in the conflict.",
        "acadmium_city_center",
        "independent"
    )
    velos.add_quest("act1_side_02")
    velos.default_dialogue = "Guard Captain Velos: Stay safe out there. These are dangerous times."
    npc_manager.register_npc(velos)
    
    # Coireena (early encounter, not yet recruitable)
    coireena = NPC(
        "coireena",
        "Coireena",
        "The first super-soldier empowered by your stolen magic. She seems conflicted.",
        "jinn_lir_sanctuary",
        "drift_empire"
    )
    coireena.default_dialogue = "Coireena: This power... it feels wrong. I'm sorry."
    npc_manager.register_npc(coireena)
    
    # Merchant
    merchant = NPC(
        "merchant_thorn",
        "Merchant Thorn",
        "A traveling merchant selling supplies and equipment.",
        "acadmium_city_center",
        "independent"
    )
    merchant.default_dialogue = "Merchant Thorn: Welcome! Looking for supplies? I have the finest goods in Acadmium!"
    npc_manager.register_npc(merchant)


def initialize_act1_content(quest_manager, dialogue_system, npc_manager):
    """Initialize all Act 1 content"""
    create_act1_quests(quest_manager)
    create_act1_dialogues(dialogue_system, npc_manager)
    create_act1_npcs(npc_manager)
    print("✓ Act 1 content initialized")
