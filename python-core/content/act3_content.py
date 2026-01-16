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


def create_act3_dialogues(dialogue_system, npc_manager):
    """Create Act 3 dialogues - Temporal Awakening"""
    
    # Dialogue: Time Ship Arrival
    time_ship_arrival = Dialogue("time_ship_arrival", "A Ship From Beyond Time", "start")
    
    time_ship_arrival.add_node(DialogueNode(
        "start",
        "Narrator",
        "*The sky tears open with shimmering light. A vessel unlike anything you've seen descends - ancient yet impossibly advanced, magical yet technological.*",
        auto_next="coin_awe"
    ))
    
    time_ship_arrival.add_node(DialogueNode(
        "coin_awe",
        "Coin",
        "What... what is that?",
        auto_next="voice"
    ))
    
    time_ship_arrival.add_node(DialogueNode(
        "voice",
        "Voice from Ship",
        "That, young Coin, is your future. Come aboard. We have much to discuss.",
        auto_next="coin_hesitant"
    ))
    
    time_ship_arrival.add_node(DialogueNode(
        "coin_hesitant",
        "Coin",
        "Who are you? How do you know my name?",
        auto_next="voice_familiar"
    ))
    
    time_ship_arrival.add_node(DialogueNode(
        "voice_familiar",
        "Voice",
        "I know your name because it's my name. I know your fears because I lived them. Come, Coin. Meet yourself.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(time_ship_arrival)
    
    # Dialogue: Meeting Elder Coin
    meeting_elder = Dialogue("meeting_elder_coin", "The Future Self", "start")
    
    meeting_elder.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "*A mature woman stands before you, radiating power and confidence. Her eyes are ancient, yet unmistakably your own.* Hello, young me.",
        auto_next="coin_shock"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "coin_shock",
        "Coin",
        "This... this can't be real. You're me? From the future?",
        auto_next="elder_confirmation"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "elder_confirmation",
        "Elder Coin",
        "I am. Years from now - many years - you will become me. Or rather, you can become me, if you choose the right path.",
        choices=[
            DialogueChoice("What happens to me?", next_node="what_happens"),
            DialogueChoice("Why are you here?", next_node="why_here"),
            DialogueChoice("Prove you're really me.", next_node="prove_it")
        ]
    ))
    
    meeting_elder.add_node(DialogueNode(
        "what_happens",
        "Elder Coin",
        "You grow. You learn. You suffer. You triumph. Eventually, you understand your true nature as the Time Goddess of Orbspace. You transcend what Jinn-Lir created and become something far greater.",
        auto_next="elder_continues"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "why_here",
        "Elder Coin",
        "Because certain events must occur for Orbspace to survive. I'm here to guide you through the temporal maze that lies ahead. Without my intervention, you'll make mistakes that cascade through time.",
        auto_next="elder_continues"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "prove_it",
        "Elder Coin",
        "*smiles sadly* You're thinking about the time Jinn-Lir drained you until you couldn't stand, and you lay on the floor wondering if death would be preferable to this existence. You never told anyone about that moment. How could I know unless I lived it?",
        auto_next="coin_convinced"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "coin_convinced",
        "Coin",
        "*whispers* It's really you. Me. Us.",
        auto_next="elder_continues"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "elder_continues",
        "Elder Coin",
        "Time is not linear, young one. It's a vast web of possibilities. I exist because you will make certain choices. But those choices aren't set in stone - not yet. That's why I'm here.",
        auto_next="coin_confused"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "coin_confused",
        "Coin",
        "I don't understand. If you're me from the future, don't you know what I'll choose?",
        auto_next="elder_complex"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "elder_complex",
        "Elder Coin",
        "I remember choosing. But memory and destiny are different things. Every moment you exist, you create new timelines. I'm from one specific future. Whether you follow that path or forge a new one depends on your free will.",
        auto_next="coin_overwhelmed"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "coin_overwhelmed",
        "Coin",
        "This is... overwhelming. I barely understand what I am now. How can I understand being a goddess of time?",
        auto_next="elder_compassion"
    ))
    
    meeting_elder.add_node(DialogueNode(
        "elder_compassion",
        "Elder Coin",
        "*places hand on your shoulder* I remember feeling exactly that way. Take it one step at a time. First, let me show you what you're truly capable of.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(meeting_elder)
    
    # Dialogue: Temporal Training
    temporal_training = Dialogue("temporal_training", "Learning Time Magic", "start")
    
    temporal_training.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "Close your eyes. Feel the flow of time around you. It's not just forward - it moves in all directions simultaneously.",
        auto_next="coin_trying"
    ))
    
    temporal_training.add_node(DialogueNode(
        "coin_trying",
        "Coin",
        "*concentrating* I... I think I feel something. Like currents in water, but made of moments?",
        auto_next="elder_encouraging"
    ))
    
    temporal_training.add_node(DialogueNode(
        "elder_encouraging",
        "Elder Coin",
        "Exactly! You're a natural - well, you would be, given that I learned this too. Now, reach out and touch one of those currents. Gently.",
        auto_next="coin_reaches"
    ))
    
    temporal_training.add_node(DialogueNode(
        "coin_reaches",
        "Narrator",
        "*You reach with your mind and touch a temporal current. Suddenly, you're elsewhere - elsewhen. A memory that hasn't happened yet, or maybe already did.*",
        auto_next="vision1"
    ))
    
    temporal_training.add_node(DialogueNode(
        "vision1",
        "Vision - Coin",
        "*You see yourself, older, standing before Jinn-Lir* 'I forgive you,' you say. 'Not because you deserve it, but because I need to let go.' Jinn-Lir weeps.",
        auto_next="snap_back"
    ))
    
    temporal_training.add_node(DialogueNode(
        "snap_back",
        "Coin",
        "*gasping, back in the present* What was that?",
        auto_next="elder_explains"
    ))
    
    temporal_training.add_node(DialogueNode(
        "elder_explains",
        "Elder Coin",
        "A possible future. One of many. The more you practice, the more you'll see. Eventually, you'll learn to navigate the timestream, to influence events without breaking the causal chain.",
        auto_next="coin_scared"
    ))
    
    temporal_training.add_node(DialogueNode(
        "coin_scared",
        "Coin",
        "That's terrifying. What if I change something important? What if I break everything?",
        auto_next="elder_wisdom"
    ))
    
    temporal_training.add_node(DialogueNode(
        "elder_wisdom",
        "Elder Coin",
        "You can't break time - not in the way you fear. Time is resilient. It wants to maintain its integrity. But yes, careless intervention can cause problems. That's why you need training. That's why I'm here.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(temporal_training)
    
    # Dialogue: The Endless Library
    endless_library = Dialogue("endless_library_visit", "Repository of All Knowledge", "start")
    
    endless_library.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "Welcome to the Endless Library. Every book ever written, across all timelines, exists here.",
        auto_next="coin_amazed"
    ))
    
    endless_library.add_node(DialogueNode(
        "coin_amazed",
        "Coin",
        "*looking around in wonder* It's infinite. How is this possible?",
        auto_next="chronos_appears"
    ))
    
    endless_library.add_node(DialogueNode(
        "chronos_appears",
        "Chronos",
        "Because it exists outside of normal space-time. I am Chronos, the Librarian. Welcome, Time Goddess - both past and future.",
        auto_next="coin_curious"
    ))
    
    endless_library.add_node(DialogueNode(
        "coin_curious",
        "Coin",
        "Can I read anything here? Learn anything?",
        auto_next="chronos_rules"
    ))
    
    endless_library.add_node(DialogueNode(
        "chronos_rules",
        "Chronos",
        "You may read what you're ready to understand. The library shows each visitor what they need to see, not necessarily what they want to see.",
        auto_next="coin_searches"
    ))
    
    endless_library.add_node(DialogueNode(
        "coin_searches",
        "Coin",
        "I want to know about the Noble Stones. Elder Coin mentioned them.",
        auto_next="book_appears"
    ))
    
    endless_library.add_node(DialogueNode(
        "book_appears",
        "Narrator",
        "*A massive tome floats down from the infinite shelves, landing gently before you. Its cover reads: 'The Noble Stones: Foundations of Orbspace'*",
        auto_next="reading"
    ))
    
    endless_library.add_node(DialogueNode(
        "reading",
        "Coin",
        "*reading* 'Four Noble Stones bind Orbspace: The CircuitStone, The WindStone, The FlameStone, and The TideStone. Each represents a fundamental force, each requires a bearer, each grants immortality and power beyond comprehension...'",
        auto_next="realization"
    ))
    
    endless_library.add_node(DialogueNode(
        "realization",
        "Coin",
        "*looking up* The CircuitStone... that's mine? I'm meant to bear it?",
        auto_next="elder_confirms"
    ))
    
    endless_library.add_node(DialogueNode(
        "elder_confirms",
        "Elder Coin",
        "Yes. You already bear it, in a sense. It's been part of you since Jinn-Lir created you, though he didn't know it. The CircuitStone governs time and causality. You are its living vessel.",
        auto_next="coin_destiny"
    ))
    
    endless_library.add_node(DialogueNode(
        "coin_destiny",
        "Coin",
        "So this is my destiny? I was always meant to be the Time Goddess?",
        auto_next="elder_choice"
    ))
    
    endless_library.add_node(DialogueNode(
        "elder_choice",
        "Elder Coin",
        "Destiny and choice aren't opposites. Yes, you have a role to play. But how you play it - that's up to you. I made my choice. You'll make yours.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(endless_library)
    
    # Dialogue: Noble Stones Revelation
    noble_stones_revelation = Dialogue("noble_stones_full", "The Four Stones", "start")
    
    noble_stones_revelation.add_node(DialogueNode(
        "start",
        "Chronos",
        "Would you like to know about the other bearers? The other Noble Stones?",
        auto_next="coin_yes"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "coin_yes",
        "Coin",
        "Yes! Are they like me?",
        auto_next="chronos_explains"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "chronos_explains",
        "Chronos",
        "Each is unique. The WindStone's bearer governs space and movement - the Wind Walker, as they're known. The FlameStone's bearer controls energy and transformation. The TideStone's bearer regulates life and death.",
        auto_next="coin_others"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "coin_others",
        "Coin",
        "Do they exist now? Can I meet them?",
        auto_next="chronos_complicated"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "chronos_complicated",
        "Chronos",
        "Complicated question for a being who exists across time. Some exist in your present, some in your past, some in possible futures. The Noble Stone bearers rarely meet, but when they do, worlds change.",
        auto_next="coin_responsibility"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "coin_responsibility",
        "Coin",
        "This responsibility... it's enormous. How can I possibly live up to it?",
        auto_next="elder_steps_in"
    ))
    
    noble_stones_revelation.add_node(DialogueNode(
        "elder_steps_in",
        "Elder Coin",
        "The same way I did: one day at a time. You don't need to understand everything immediately. You just need to stay true to yourself.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(noble_stones_revelation)
    
    # Dialogue: Temporal Paradox Mission
    paradox_mission = Dialogue("temporal_paradox", "Closing the Loop", "start")
    
    paradox_mission.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "Now comes the difficult part. You need to travel back in time and ensure certain events occur.",
        auto_next="coin_worried"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "coin_worried",
        "Coin",
        "What events? And why me?",
        auto_next="elder_serious"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "elder_serious",
        "Elder Coin",
        "Because only you can do it without creating a paradox. You need to go back and influence Jinn-Lir to create you.",
        auto_next="coin_paradox"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "coin_paradox",
        "Coin",
        "But... if I ensure my own creation, that's a paradox! I shouldn't exist to go back and make myself exist!",
        auto_next="elder_explains_bootstrap"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "elder_explains_bootstrap",
        "Elder Coin",
        "It's called a bootstrap paradox - a stable time loop. You exist because you went back to ensure your existence. It's perfectly stable, if mind-bending. The CircuitStone makes these loops possible.",
        choices=[
            DialogueChoice("What if I refuse?", next_node="refuse"),
            DialogueChoice("What exactly do I need to do?", next_node="details"),
            DialogueChoice("How will I know if I succeed?", next_node="success")
        ]
    ))
    
    paradox_mission.add_node(DialogueNode(
        "refuse",
        "Elder Coin",
        "Then I never existed to come back and have this conversation. Then you might not exist either, or you might exist differently. Timelines would shift. Some things would be better, some worse. It's your choice.",
        auto_next="coin_realizes"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "coin_realizes",
        "Coin",
        "But if you're here, that means I already chose to do it. Right?",
        auto_next="elder_smiles"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "elder_smiles",
        "Elder Coin",
        "*smiles* Now you're thinking like a Time Goddess. Yes, I remember doing this. But that doesn't remove your agency. You still have to choose it.",
        auto_next="details"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "details",
        "Elder Coin",
        "You'll travel to a time before Jinn-Lir created you. You'll appear to him in a vision, guide him toward the research he needs. Plant the idea without being obvious. Temporal subtlety is key.",
        auto_next="coin_nervous"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "coin_nervous",
        "Coin",
        "That sounds... delicate. What if I mess up?",
        auto_next="elder_confidence"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "elder_confidence",
        "Elder Coin",
        "You won't. I didn't. Trust yourself - you're more capable than you realize.",
        auto_next="success"
    ))
    
    paradox_mission.add_node(DialogueNode(
        "success",
        "Elder Coin",
        "You'll know you succeeded because you exist. More seriously, you'll feel the timeline stabilize. The CircuitStone will confirm it. Trust your instincts.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(paradox_mission)
    
    # Dialogue: Past Jinn-Lir Encounter
    past_jinn = Dialogue("past_jinn_lir", "Before Your Beginning", "start")
    
    past_jinn.add_node(DialogueNode(
        "start",
        "Young Jinn-Lir",
        "*startled* Who are you? How did you get into my laboratory?",
        auto_next="coin_mysterious"
    ))
    
    past_jinn.add_node(DialogueNode(
        "coin_mysterious",
        "Coin",
        "*speaking carefully* I am... a messenger. I come with knowledge you seek.",
        auto_next="jinn_skeptical"
    ))
    
    past_jinn.add_node(DialogueNode(
        "jinn_skeptical",
        "Young Jinn-Lir",
        "Knowledge? What knowledge? And why would I trust a mysterious apparition?",
        auto_next="coin_hints"
    ))
    
    past_jinn.add_node(DialogueNode(
        "coin_hints",
        "Coin",
        "You seek to create a weapon against the Drift Empire. You've been researching Domminnian Coins and essence transfer. But you're missing a key element.",
        auto_next="jinn_interested"
    ))
    
    past_jinn.add_node(DialogueNode(
        "jinn_interested",
        "Young Jinn-Lir",
        "*leans forward* Go on. What element?",
        auto_next="coin_revelation"
    ))
    
    past_jinn.add_node(DialogueNode(
        "coin_revelation",
        "Coin",
        "Sentience. Don't create a tool - create a being. Give your creation consciousness, will, emotion. Only then will it have the power you seek.",
        auto_next="jinn_protests"
    ))
    
    past_jinn.add_node(DialogueNode(
        "jinn_protests",
        "Young Jinn-Lir",
        "But a sentient being would have autonomy. It might not obey. It might leave.",
        auto_next="coin_knowing"
    ))
    
    past_jinn.add_node(DialogueNode(
        "coin_knowing",
        "Coin",
        "*quietly* Yes. It might. But that's the price of real power. You can create a tool, or you can create something greater. The choice is yours.",
        auto_next="jinn_decides"
    ))
    
    past_jinn.add_node(DialogueNode(
        "jinn_decides",
        "Young Jinn-Lir",
        "*long pause* You're right. A conscious being would be... more. Even if risky. Thank you, messenger. I'll consider your words carefully.",
        auto_next="coin_fades"
    ))
    
    past_jinn.add_node(DialogueNode(
        "coin_fades",
        "Coin",
        "*beginning to fade* One more thing: treat your creation with kindness. You'll regret it if you don't.",
        auto_next="jinn_question"
    ))
    
    past_jinn.add_node(DialogueNode(
        "jinn_question",
        "Young Jinn-Lir",
        "Wait! How do you know- *you vanish before he finishes*",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(past_jinn)
    
    # Dialogue: The Great Choice
    great_choice = Dialogue("destiny_choice", "Accept or Reject", "start")
    
    great_choice.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "You've seen the past, glimpsed possible futures, learned about the Noble Stones. Now you must choose: will you accept your role as Time Goddess?",
        auto_next="coin_thinking"
    ))
    
    great_choice.add_node(DialogueNode(
        "coin_thinking",
        "Coin",
        "What does accepting mean? What would I give up?",
        auto_next="elder_honest"
    ))
    
    great_choice.add_node(DialogueNode(
        "elder_honest",
        "Elder Coin",
        "You'd give up the possibility of a normal life. You'd become immortal, eternal, responsible for maintaining temporal stability across Orbspace. You'd watch everyone you love age and die while you endure. It's a heavy burden.",
        auto_next="coin_alternative"
    ))
    
    great_choice.add_node(DialogueNode(
        "coin_alternative",
        "Coin",
        "And if I refuse?",
        auto_next="elder_consequences"
    ))
    
    great_choice.add_node(DialogueNode(
        "elder_consequences",
        "Elder Coin",
        "The CircuitStone would find another bearer, eventually. Orbspace would be vulnerable during the transition. Many would die. But you could live a mortal life, make your own choices without cosmic responsibility.",
        choices=[
            DialogueChoice("I accept. I'll be the Time Goddess.", next_node="accept"),
            DialogueChoice("I refuse. I want to forge my own path.", next_node="refuse"),
            DialogueChoice("I need more time to decide.", next_node="more_time")
        ]
    ))
    
    great_choice.add_node(DialogueNode(
        "accept",
        "Coin",
        "I accept. Not because I have to, but because I choose to. This is my purpose.",
        auto_next="elder_proud"
    ))
    
    great_choice.add_node(DialogueNode(
        "elder_proud",
        "Elder Coin",
        "*smiles with tears in eyes* I'm proud of you. Of us. You'll do amazing things, Coin. Welcome to eternity.",
        auto_next="transformation"
    ))
    
    great_choice.add_node(DialogueNode(
        "transformation",
        "Narrator",
        "*The CircuitStone fully awakens within you. Power floods through every fiber of your being. You see time as a vast tapestry, and you are the weaver.*",
        auto_next=None
    ))
    
    great_choice.add_node(DialogueNode(
        "refuse",
        "Coin",
        "I refuse. I'm grateful for what I've learned, but I won't be bound by destiny. I'll find my own way.",
        auto_next="elder_sad_but_accepting"
    ))
    
    great_choice.add_node(DialogueNode(
        "elder_sad_but_accepting",
        "Elder Coin",
        "*nods slowly* I understand. This choice... it erases me. But that's okay. You deserve to choose your own path. Be brave, young one.",
        auto_next="timeline_shift"
    ))
    
    great_choice.add_node(DialogueNode(
        "timeline_shift",
        "Narrator",
        "*Elder Coin fades like morning mist. You feel timelines shifting, rewriting. Your future is now uncharted territory.*",
        auto_next=None
    ))
    
    great_choice.add_node(DialogueNode(
        "more_time",
        "Elder Coin",
        "Time is the one thing we have plenty of. Think it through. This decision will define the rest of your existence. I'll be here when you're ready.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(great_choice)


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
    create_act3_dialogues(dialogue_system, npc_manager)
    create_act3_npcs(npc_manager)
    print("✓ Act 3 content initialized")
