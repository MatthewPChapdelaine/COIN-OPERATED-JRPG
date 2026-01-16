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


def create_act2_dialogues(dialogue_system, npc_manager):
    """Create Act 2 dialogues - Independence & Conflict"""
    
    # Dialogue: The Break
    the_break = Dialogue("the_break", "Breaking Free", "start")
    
    the_break.add_node(DialogueNode(
        "start",
        "Coin",
        "*looking at Jinn-Lir with newfound resolve* I'm leaving.",
        auto_next="jinn_shocked"
    ))
    
    the_break.add_node(DialogueNode(
        "jinn_shocked",
        "Jinn-Lir",
        "Leaving? Coin, don't be ridiculous. Where would you even go? You need me!",
        auto_next="coin_firm"
    ))
    
    the_break.add_node(DialogueNode(
        "coin_firm",
        "Coin",
        "No, Jinn-Lir. You need me. Or rather, you need what you can take from me. But I'm more than a resource for your war.",
        auto_next="jinn_desperate"
    ))
    
    the_break.add_node(DialogueNode(
        "jinn_desperate",
        "Jinn-Lir",
        "This is about the power transfers, isn't it? Coin, I admit I should have been more transparent, but the cause is just! The Drift Empire threatens all of us!",
        choices=[
            DialogueChoice("I don't care about your war anymore.", next_node="cold_break"),
            DialogueChoice("Maybe your cause is just, but your methods aren't.", next_node="moral_break"),
            DialogueChoice("I need to find my own path.", next_node="gentle_break")
        ]
    ))
    
    the_break.add_node(DialogueNode(
        "cold_break",
        "Coin",
        "You created me as a weapon. I refuse to be one. Goodbye, Jinn-Lir.",
        auto_next="aftermath"
    ))
    
    the_break.add_node(DialogueNode(
        "moral_break",
        "Coin",
        "You taught me about right and wrong, about justice and tyranny. Then you turned around and treated me exactly like you claim the Drift Empire treats magic users - as things to be exploited.",
        auto_next="jinn_guilt"
    ))
    
    the_break.add_node(DialogueNode(
        "jinn_guilt",
        "Jinn-Lir",
        "*silence, then quietly* You're right. I... I became what I fought against. Coin, I'm sorry.",
        auto_next="coin_acknowledgment"
    ))
    
    the_break.add_node(DialogueNode(
        "coin_acknowledgment",
        "Coin",
        "Maybe you are sorry. But sorry doesn't change what happened. I need to leave.",
        auto_next="aftermath"
    ))
    
    the_break.add_node(DialogueNode(
        "gentle_break",
        "Coin",
        "You gave me life, taught me magic, showed me this world. For that, I'm grateful. But I can't be what you want me to be. I need to discover who I am on my own.",
        auto_next="jinn_understanding"
    ))
    
    the_break.add_node(DialogueNode(
        "jinn_understanding",
        "Jinn-Lir",
        "*long pause* Perhaps... perhaps you're right. I've been so focused on winning the war that I lost sight of everything else. If you must go, I won't stop you.",
        auto_next="aftermath"
    ))
    
    the_break.add_node(DialogueNode(
        "aftermath",
        "Narrator",
        "*You turn and walk away from Jinn-Lir's sanctuary. As the door closes behind you, you hear him whisper: 'Be safe, Coin.' For the first time since your creation, you are truly alone.*",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(the_break)
    
    # Dialogue: Alone in the City
    alone_city = Dialogue("alone_in_city", "First Steps Alone", "start")
    
    alone_city.add_node(DialogueNode(
        "start",
        "Coin",
        "*standing in the streets of Acadmium* Where do I even begin? I have no home, no money, no...",
        auto_next="street_voice"
    ))
    
    alone_city.add_node(DialogueNode(
        "street_voice",
        "Street Vendor",
        "Hey there! You look lost. New to the city?",
        auto_next="coin_uncertain"
    ))
    
    alone_city.add_node(DialogueNode(
        "coin_uncertain",
        "Coin",
        "I... yes. I'm looking for a place to stay.",
        auto_next="vendor_kind"
    ))
    
    alone_city.add_node(DialogueNode(
        "vendor_kind",
        "Street Vendor",
        "Times are tough with the war and all. But there's a boarding house two streets over. Tell them Mira sent you - they might have a spare room.",
        auto_next="coin_grateful"
    ))
    
    alone_city.add_node(DialogueNode(
        "coin_grateful",
        "Coin",
        "Thank you. That's... very kind.",
        auto_next="mira_curious"
    ))
    
    alone_city.add_node(DialogueNode(
        "mira_curious",
        "Mira",
        "You're one of those magic folk, aren't you? I can sense it. Don't worry - I won't tell the Drift patrols. Most of us normal folk don't care about the war. We just want to live our lives.",
        auto_next="coin_learning"
    ))
    
    alone_city.add_node(DialogueNode(
        "coin_learning",
        "Coin",
        "*realizing* There are people who don't take sides? Who just... exist?",
        auto_next="mira_laughs"
    ))
    
    alone_city.add_node(DialogueNode(
        "mira_laughs",
        "Mira",
        "*laughs* Most of us, actually! The Light Cabal and Drift Empire make a lot of noise, but ordinary people? We're too busy trying to survive. Remember that, kid.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(alone_city)
    
    # Dialogue: Dark Cabal's Offer
    dark_offer = Dialogue("dark_cabal_offer", "Whispers of Power", "start")
    
    dark_offer.add_node(DialogueNode(
        "start",
        "Selene",
        "Coin. We finally meet face to face. I am Selene of the Dark Cabal.",
        auto_next="coin_wary"
    ))
    
    dark_offer.add_node(DialogueNode(
        "coin_wary",
        "Coin",
        "I know who you are. The Light Cabal says you're dangerous.",
        auto_next="selene_amused"
    ))
    
    dark_offer.add_node(DialogueNode(
        "selene_amused",
        "Selene",
        "*laughs* Of course they do. We're dangerous because we're honest. We don't pretend to be noble while exploiting the vulnerable. We embrace what we are: seekers of power.",
        auto_next="coin_listening"
    ))
    
    dark_offer.add_node(DialogueNode(
        "coin_listening",
        "Coin",
        "And what do you want with me?",
        auto_next="selene_direct"
    ))
    
    dark_offer.add_node(DialogueNode(
        "selene_direct",
        "Selene",
        "I want to offer you what the Light Cabal never did: a choice. You have incredible power, Coin. Join us, and we'll teach you to wield it for yourself, not for some supposed 'greater good.'",
        choices=[
            DialogueChoice("What's the catch?", next_node="catch"),
            DialogueChoice("How are you different from Jinn-Lir?", next_node="difference"),
            DialogueChoice("What would you ask of me?", next_node="ask")
        ]
    ))
    
    dark_offer.add_node(DialogueNode(
        "catch",
        "Selene",
        "No catch. You help us when it serves your interests, we help you when it serves ours. We don't deal in obligation and guilt like the Light Cabal. Power flows where it will, and we ride that current.",
        auto_next="selene_continues"
    ))
    
    dark_offer.add_node(DialogueNode(
        "difference",
        "Selene",
        "Jinn-Lir told you he was saving the world while draining you dry. I'm telling you honestly: I want your power, but I'll pay for it. Training, resources, knowledge - all yours. We deal in transactions, not exploitation.",
        auto_next="selene_continues"
    ))
    
    dark_offer.add_node(DialogueNode(
        "ask",
        "Selene",
        "Help when we call upon you. Fight alongside us when our interests align. But unlike the Light Cabal, if you say no, we accept it. Coercion weakens the partnership.",
        auto_next="selene_continues"
    ))
    
    dark_offer.add_node(DialogueNode(
        "selene_continues",
        "Selene",
        "The Light Cabal pretends magic is about harmony and balance. We know the truth: magic is power, raw and primal. It doesn't care about morality. The question is: will you pretend to be something you're not, or embrace what you are?",
        choices=[
            DialogueChoice("I'll consider your offer.", next_node="consider"),
            DialogueChoice("I'm not interested in more manipulation.", next_node="refuse"),
            DialogueChoice("What exactly is the Dark Cabal's goal?", next_node="goal")
        ]
    ))
    
    dark_offer.add_node(DialogueNode(
        "consider",
        "Selene",
        "Smart. Don't decide hastily. When you're ready, we'll be waiting. *hands you a dark crystal* Crush this and speak my name. I'll come to you.",
        auto_next=None
    ))
    
    dark_offer.add_node(DialogueNode(
        "refuse",
        "Selene",
        "*smiles* That's the spirit. Too many want to use you - I respect that you're wary. But remember: the offer stands. We don't beg or coerce. The choice is always yours.",
        auto_next=None
    ))
    
    dark_offer.add_node(DialogueNode(
        "goal",
        "Selene",
        "Simple: we believe magical beings should rule Orbspace, not hide from technology-worshipping bureaucrats. The strong should thrive, the weak should adapt. Natural order, not artificial constraints.",
        auto_next="coin_thinks"
    ))
    
    dark_offer.add_node(DialogueNode(
        "coin_thinks",
        "Coin",
        "And those who aren't strong?",
        auto_next="selene_honest"
    ))
    
    dark_offer.add_node(DialogueNode(
        "selene_honest",
        "Selene",
        "They find their place or perish. Harsh? Yes. But more honest than the Light Cabal's pretty lies. At least we don't pretend to care about the weak while using them.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(dark_offer)
    
    # Dialogue: Coin Thieves
    coin_thieves = Dialogue("coin_thieves", "Stolen Essence", "start")
    
    coin_thieves.add_node(DialogueNode(
        "start",
        "Thief Leader",
        "Well, well. The famous Coin, all alone. Your Domminnian Coins are worth a fortune on the black market, you know.",
        auto_next="coin_defensive"
    ))
    
    coin_thieves.add_node(DialogueNode(
        "coin_defensive",
        "Coin",
        "Those coins are part of me! Give them back!",
        auto_next="thief_mocking"
    ))
    
    coin_thieves.add_node(DialogueNode(
        "thief_mocking",
        "Thief Leader",
        "Part of you? Lady, you're literally made of money. Can't blame us for wanting a piece. Come on, boys!",
        auto_next=None  # Combat
    ))
    
    dialogue_system.register_dialogue(coin_thieves)
    
    # Dialogue: After Thief Battle
    after_thieves = Dialogue("after_coin_thieves", "Recovery", "start")
    
    after_thieves.add_node(DialogueNode(
        "start",
        "Coin",
        "*collecting scattered coins* These are pieces of my being. When they take them, I feel... diminished. Less whole.",
        auto_next="passerby"
    ))
    
    after_thieves.add_node(DialogueNode(
        "passerby",
        "Passerby",
        "Are you alright? I saw those thieves attack you.",
        auto_next="coin_weary"
    ))
    
    after_thieves.add_node(DialogueNode(
        "coin_weary",
        "Coin",
        "I'm fine. Just tired of everyone wanting to take something from me.",
        auto_next="passerby_kind"
    ))
    
    after_thieves.add_node(DialogueNode(
        "passerby_kind",
        "Passerby",
        "I understand more than you might think. This war has made everyone desperate. But not everyone is out to use you. Some of us still believe in helping each other.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(after_thieves)
    
    # Dialogue: Coireena Confrontation
    coireena_confrontation = Dialogue("coireena_confrontation", "Facing Your Power", "start")
    
    coireena_confrontation.add_node(DialogueNode(
        "start",
        "Coireena",
        "Coin. I hoped I wouldn't have to face you.",
        auto_next="coin_recognition"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "coin_recognition",
        "Coin",
        "Coireena? You were kind to me before. Why are you attacking now?",
        auto_next="coireena_orders"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "coireena_orders",
        "Coireena",
        "Orders from the Light Cabal. Jinn-Lir wants you back. He says you're too dangerous to wander free. But Coin... I don't want to do this.",
        choices=[
            DialogueChoice("Then don't. Walk away.", next_node="walk_away"),
            DialogueChoice("I won't go back to being his prisoner.", next_node="defiant"),
            DialogueChoice("What happened to you, Coireena?", next_node="what_happened")
        ]
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "walk_away",
        "Coireena",
        "I wish I could. But they have my family. If I don't bring you back, they'll... *trails off* I'm sorry, Coin. I have to try.",
        auto_next="battle"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "defiant",
        "Coin",
        "I'll fight you if I must, but I won't be caged again.",
        auto_next="coireena_respect"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "coireena_respect",
        "Coireena",
        "I respect that. More than you know. Let's make this quick.",
        auto_next="battle"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "what_happened",
        "Coireena",
        "Your power changed me, Coin. I'm stronger, but I'm also bound to them. The magic connects us - you, me, Jinn-Lir. I don't fully control my own power. Neither do you, I suspect.",
        auto_next="coin_understanding"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "coin_understanding",
        "Coin",
        "We're both his victims.",
        auto_next="coireena_sad"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "coireena_sad",
        "Coireena",
        "Yes. But that doesn't change what I have to do. *raises weapon* I'm sorry.",
        auto_next="battle"
    ))
    
    coireena_confrontation.add_node(DialogueNode(
        "battle",
        "Narrator",
        "*The battle begins. Your own power turned against you.*",
        auto_next=None  # Combat
    ))
    
    dialogue_system.register_dialogue(coireena_confrontation)
    
    # Dialogue: After Coireena Battle
    after_coireena = Dialogue("after_coireena_battle", "Shared Suffering", "start")
    
    after_coireena.add_node(DialogueNode(
        "start",
        "Coireena",
        "*defeated, breathing heavily* You've gotten stronger. Good.",
        auto_next="coin_helps"
    ))
    
    after_coireena.add_node(DialogueNode(
        "coin_helps",
        "Coin",
        "*extending hand* Let me help you up.",
        auto_next="coireena_surprised"
    ))
    
    after_coireena.add_node(DialogueNode(
        "coireena_surprised",
        "Coireena",
        "After I attacked you? Why would you help me?",
        auto_next="coin_wisdom"
    ))
    
    after_coireena.add_node(DialogueNode(
        "coin_wisdom",
        "Coin",
        "Because you didn't want to fight. Because we're both victims of the same person. Because... I think I understand what Orbius meant about choosing who I want to be.",
        auto_next="coireena_grateful"
    ))
    
    after_coireena.add_node(DialogueNode(
        "coireena_grateful",
        "Coireena",
        "*takes your hand, stands* You're remarkable, Coin. When you're ready to face Jinn-Lir again - and you will have to eventually - I'll stand with you. I promise.",
        auto_next="coin_friend"
    ))
    
    after_coireena.add_node(DialogueNode(
        "coin_friend",
        "Coin",
        "Thank you. That means more than you know.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(after_coireena)
    
    # Dialogue: Emperor Turok Encounter
    emperor_turok = Dialogue("emperor_turok_encounter", "The Enemy's Face", "start")
    
    emperor_turok.add_node(DialogueNode(
        "start",
        "Emperor Turok",
        "So you are the magical anomaly causing disruption across my empire. Fascinating. You're much smaller than I expected.",
        auto_next="coin_brave"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "coin_brave",
        "Coin",
        "I'm not an anomaly. I'm a person. And I'm not afraid of you.",
        auto_next="turok_amused"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "turok_amused",
        "Emperor Turok",
        "*chuckles* Brave words from a creation of desperate wizards. Tell me, did your creator inform you of your purpose? Or did he fill your head with noble causes while draining you like a battery?",
        auto_next="coin_surprised"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "coin_surprised",
        "Coin",
        "How do you know about that?",
        auto_next="turok_intelligence"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "turok_intelligence",
        "Emperor Turok",
        "I know everything that happens in my empire. The Light Cabal creates a sentient being and immediately exploits it. They claim moral superiority while practicing the same exploitation they accuse us of. Hypocrites, all of them.",
        choices=[
            DialogueChoice("You're no better than them.", next_node="no_better"),
            DialogueChoice("Why are you telling me this?", next_node="why_tell"),
            DialogueChoice("What do you want from me?", next_node="what_want")
        ]
    ))
    
    emperor_turok.add_node(DialogueNode(
        "no_better",
        "Emperor Turok",
        "True. I never claimed to be. The difference is that I don't pretend. I seek order through technology, and I eliminate threats to that order. At least I'm honest about it.",
        auto_next="turok_offer"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "why_tell",
        "Emperor Turok",
        "Because I believe in providing accurate information before making decisions. Unlike the Cabals, who deal in deception and half-truths.",
        auto_next="turok_offer"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "what_want",
        "Emperor Turok",
        "Directly to the point. I like that. What I want is simple: neutrality. Or, if you prefer, cooperation.",
        auto_next="turok_offer"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "turok_offer",
        "Emperor Turok",
        "I don't want to destroy you, Coin. You're a unique phenomenon. Join the Drift Empire, and I'll ensure you're treated as an individual with rights, not a resource. We have laws, protections, structure.",
        auto_next="coin_skeptical"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "coin_skeptical",
        "Coin",
        "And if I refuse?",
        auto_next="turok_pragmatic"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "turok_pragmatic",
        "Emperor Turok",
        "Then we are enemies, and I will treat you as such. But know this: I would rather have you as an ally or at minimum, neutral party. This battle between magic and technology is pointless. Both can coexist with proper regulation.",
        auto_next="coin_decision"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "coin_decision",
        "Coin",
        "I... I need time to think about this. Everything I believed is being challenged.",
        auto_next="turok_patience"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "turok_patience",
        "Emperor Turok",
        "Take your time. I'm a patient man. But understand: this war is escalating. Soon, neutrality won't be an option. Choose wisely, Coin. You have more influence than you realize.",
        auto_next="escape"
    ))
    
    emperor_turok.add_node(DialogueNode(
        "escape",
        "Narrator",
        "*Alarms blare. The Emperor gestures dismissively.* 'Go. My guards are coming, but they're slow. Consider this a courtesy. Next time, you may not be so fortunate.'",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(emperor_turok)


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
    create_act2_dialogues(dialogue_system, npc_manager)
    create_act2_npcs(npc_manager)
    print("✓ Act 2 content initialized")
