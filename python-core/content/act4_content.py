"""
COIN:OPERATED JRPG - Act 4 & Endings Content
Resolution & Consequences - Multiple ending paths
"""

from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from systems.dialogue import Dialogue, DialogueNode, DialogueChoice, NPC, NPCManager


def create_act4_quests(quest_manager: QuestManager):
    """Create Act 4 quests leading to multiple endings"""
    
    # Main Quest: The Final Conflict
    quest_final_conflict = Quest(
        quest_id="act4_main_01",
        name="Convergence of Fates",
        description="All factions converge for the final battle that will determine Orbspace's future.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=25
    )
    quest_final_conflict.add_objective(QuestObjective(
        "Unite your allies",
        "event",
        "ally_gathering"
    ))
    quest_final_conflict.add_objective(QuestObjective(
        "Prepare for final confrontation",
        "event",
        "final_preparations"
    ))
    quest_final_conflict.set_rewards(exp=5000, essence=3000)
    quest_manager.register_quest(quest_final_conflict)
    
    # Ending Path 1: Time Goddess Ending
    quest_goddess_ending = Quest(
        quest_id="act4_ending_01",
        name="Eternal Guardian",
        description="Accept your destiny and become the immortal Time Goddess.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Elder Coin",
        level_requirement=28,
        faction_requirement={}  # No faction requirement
    )
    quest_goddess_ending.add_objective(QuestObjective(
        "Complete the Ascension Ritual",
        "event",
        "ascension_ritual"
    ))
    quest_goddess_ending.add_objective(QuestObjective(
        "Defeat the final boss: Temporal Anomaly",
        "boss",
        "temporal_anomaly"
    ))
    quest_goddess_ending.set_rewards(exp=10000, coins=5000, essence=5000)
    quest_manager.register_quest(quest_goddess_ending)
    
    # Ending Path 2: Rebel Ending
    quest_rebel_ending = Quest(
        quest_id="act4_ending_02",
        name="Forge Your Own Path",
        description="Reject destiny and carve out your own future, despite the consequences.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=30,  # Most difficult path
        faction_requirement={'independent': 100}
    )
    quest_rebel_ending.add_objective(QuestObjective(
        "Break free from temporal chains",
        "event",
        "break_temporal_chains"
    ))
    quest_rebel_ending.add_objective(QuestObjective(
        "Defeat Elder Coin and Time itself",
        "boss",
        "elder_coin_battle"
    ))
    quest_rebel_ending.set_rewards(exp=15000, coins=10000, essence=0)  # No essence - rejected magic
    quest_manager.register_quest(quest_rebel_ending)
    
    # Ending Path 3: Light Cabal Ending
    quest_light_ending = Quest(
        quest_id="act4_ending_03",
        name="Unity of Magic",
        description="Unite all magic users under enlightened leadership and bring peace.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Orbius",
        level_requirement=28,
        faction_requirement={'light_cabal': 200}
    )
    quest_light_ending.add_objective(QuestObjective(
        "Convince Drift Empire to accept magic",
        "event",
        "drift_negotiation"
    ))
    quest_light_ending.add_objective(QuestObjective(
        "Reform the Light Cabal",
        "event",
        "cabal_reform"
    ))
    quest_light_ending.add_objective(QuestObjective(
        "Defeat extremist opposition",
        "boss",
        "extremist_forces"
    ))
    quest_light_ending.set_rewards(exp=12000, essence=6000)
    quest_manager.register_quest(quest_light_ending)
    
    # Ending Path 4: Dark Cabal Ending
    quest_dark_ending = Quest(
        quest_id="act4_ending_04",
        name="Embrace the Chaos",
        description="Embrace chaotic power and reshape Orbspace through strength.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="Selene",
        level_requirement=28,
        faction_requirement={'dark_cabal': 200}
    )
    quest_dark_ending.add_objective(QuestObjective(
        "Overthrow Light Cabal leadership",
        "boss",
        "orbius_dark_path"
    ))
    quest_dark_ending.add_objective(QuestObjective(
        "Conquer Drift Empire",
        "event",
        "empire_conquest"
    ))
    quest_dark_ending.add_objective(QuestObjective(
        "Ascend as Chaos Goddess",
        "event",
        "chaos_ascension"
    ))
    quest_dark_ending.set_rewards(exp=12000, essence=8000)
    quest_manager.register_quest(quest_dark_ending)
    
    # Ending Path 5: Peaceful Ending
    quest_peace_ending = Quest(
        quest_id="act4_ending_05",
        name="Bridge Between Worlds",
        description="Broker true peace between magic users and the Drift Empire.",
        quest_type=QuestType.MAIN_STORY,
        quest_giver="",
        level_requirement=28,
        faction_requirement={
            'light_cabal': 100,
            'drift_empire': 50,
            'independent': 100
        }  # Requires balanced reputation
    )
    quest_peace_ending.add_objective(QuestObjective(
        "Negotiate peace treaty",
        "event",
        "peace_negotiations",
        required=5
    ))
    quest_peace_ending.add_objective(QuestObjective(
        "Defeat warmongering factions",
        "boss",
        "warmongers"
    ))
    quest_peace_ending.add_objective(QuestObjective(
        "Establish Council of Unity",
        "event",
        "unity_council"
    ))
    quest_peace_ending.set_rewards(exp=13000, coins=8000, essence=5000)
    quest_manager.register_quest(quest_peace_ending)
    
    # Optional Superboss Quests
    quest_superboss_1 = Quest(
        quest_id="act4_optional_01",
        name="Alternate Timeline Tyrant",
        description="Face a version of yourself from a timeline where you became a tyrant.",
        quest_type=QuestType.OPTIONAL_BOSS,
        quest_giver="Chronos",
        level_requirement=35
    )
    quest_superboss_1.add_objective(QuestObjective(
        "Defeat Tyrant Coin",
        "boss",
        "tyrant_coin"
    ))
    quest_superboss_1.set_rewards(
        exp=20000,
        equipment=["Tyrant's Crown"],
        essence=10000
    )
    quest_manager.register_quest(quest_superboss_1)
    
    quest_superboss_2 = Quest(
        quest_id="act4_optional_02",
        name="Ancient Guardian of Akashmiran",
        description="Challenge the legendary guardian who created the Noble Stones.",
        quest_type=QuestType.OPTIONAL_BOSS,
        quest_giver="Elder Coin",
        level_requirement=40
    )
    quest_superboss_2.add_objective(QuestObjective(
        "Defeat Ancient Guardian",
        "boss",
        "ancient_guardian"
    ))
    quest_superboss_2.set_rewards(
        exp=30000,
        equipment=["Guardian's Aegis"],
        essence=15000
    )
    quest_manager.register_quest(quest_superboss_2)
    
    quest_superboss_3 = Quest(
        quest_id="act4_optional_03",
        name="Chaos Incarnate",
        description="Face a being of pure chaos from beyond Orbspace.",
        quest_type=QuestType.OPTIONAL_BOSS,
        quest_giver="Orbius",
        level_requirement=45
    )
    quest_superboss_3.add_objective(QuestObjective(
        "Defeat Chaos Incarnate",
        "boss",
        "chaos_incarnate"
    ))
    quest_superboss_3.set_rewards(
        exp=50000,
        equipment=["Chaos Breaker"],
        essence=20000
    )
    quest_manager.register_quest(quest_superboss_3)


def create_act4_dialogues(dialogue_system, npc_manager):
    """Create Act 4 dialogues - Episodes VI-X and all endings"""
    
    # Dialogue: Return to Present
    return_present = Dialogue("return_to_present", "Back to the War", "start")
    
    return_present.add_node(DialogueNode(
        "start",
        "Narrator",
        "*You return from your temporal journey to find Orbspace on the brink of catastrophe. The war between magic and technology has escalated beyond anyone's expectations.*",
        auto_next="orbius_urgent"
    ))
    
    return_present.add_node(DialogueNode(
        "orbius_urgent",
        "Orbius",
        "Coin! Thank the ancient magic you're here. Everything is falling apart. The Drift Empire and the combined Cabals are preparing for final battle.",
        auto_next="coin_changed"
    ))
    
    return_present.add_node(DialogueNode(
        "coin_changed",
        "Coin",
        "I've learned so much, Orbius. I understand now - this war is meaningless. There's a greater purpose at stake.",
        auto_next="orbius_knows"
    ))
    
    return_present.add_node(DialogueNode(
        "orbius_knows",
        "Orbius",
        "*studies you intently* You've met your future self. You know what you are. The question is: what will you do with that knowledge?",
        choices=[
            DialogueChoice("I'll try to stop the war.", next_node="peace_path"),
            DialogueChoice("I'll embrace my power and take control.", next_node="power_path"),
            DialogueChoice("I'll fulfill my destiny as Time Goddess.", next_node="goddess_path")
        ]
    ))
    
    return_present.add_node(DialogueNode(
        "peace_path",
        "Coin",
        "This war serves no one. Technology and magic can coexist. I'll prove it.",
        auto_next="orbius_peace"
    ))
    
    return_present.add_node(DialogueNode(
        "orbius_peace",
        "Orbius",
        "A noble goal, but perhaps the most difficult path. You'll need to convince both sides to lay down arms. Many will see you as a threat to their power.",
        auto_next=None
    ))
    
    return_present.add_node(DialogueNode(
        "power_path",
        "Coin",
        "I have the power to end this. If neither side will listen to reason, I'll force them to.",
        auto_next="orbius_warning"
    ))
    
    return_present.add_node(DialogueNode(
        "orbius_warning",
        "Orbius",
        "*concerned* Power without wisdom becomes tyranny. But... it is your choice. Just remember who you were.",
        auto_next=None
    ))
    
    return_present.add_node(DialogueNode(
        "goddess_path",
        "Coin",
        "I'll ascend. I'll become what I was meant to be. From that position, I can guide Orbspace properly.",
        auto_next="orbius_accepting"
    ))
    
    return_present.add_node(DialogueNode(
        "orbius_accepting",
        "Orbius",
        "Then you've accepted your destiny. I'm glad. Orbspace needs its Time Goddess, now more than ever.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(return_present)
    
    # Dialogue: Jinn-Lir Reconciliation
    jinn_reconciliation = Dialogue("jinn_lir_reconciliation", "Facing the Creator", "start")
    
    jinn_reconciliation.add_node(DialogueNode(
        "start",
        "Jinn-Lir",
        "*sees you* Coin. I... I didn't expect to see you again. Not after everything I did.",
        auto_next="coin_calm"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "coin_calm",
        "Coin",
        "I've learned a lot since I left, Jinn-Lir. About myself, about time, about what really matters.",
        auto_next="jinn_apologetic"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "jinn_apologetic",
        "Jinn-Lir",
        "I owe you an apology. More than an apology. I created you for selfish reasons and treated you as a resource. You deserved better.",
        choices=[
            DialogueChoice("I forgive you.", next_node="forgive"),
            DialogueChoice("An apology doesn't undo what happened.", next_node="harsh"),
            DialogueChoice("We both made mistakes.", next_node="mutual")
        ]
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "forgive",
        "Coin",
        "I forgive you, Jinn-Lir. Not because you deserve it, but because I need to let go. Holding onto anger would only hurt me.",
        auto_next="jinn_grateful"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "jinn_grateful",
        "Jinn-Lir",
        "*tears flowing* Thank you. I don't deserve your forgiveness, but I'll spend the rest of my life trying to be worthy of it.",
        auto_next="moving_forward"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "harsh",
        "Coin",
        "You're right, it doesn't. You exploited me, drained me, treated me as a thing. I've moved past it, but I haven't forgotten.",
        auto_next="jinn_accepts"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "jinn_accepts",
        "Jinn-Lir",
        "*nods solemnly* I understand. I can't change the past. But if there's ever anything I can do to help you, I will. No strings attached.",
        auto_next="moving_forward"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "mutual",
        "Coin",
        "You created me for the wrong reasons, but you also gave me life. You taught me magic, showed me this world. It's complicated.",
        auto_next="jinn_understands"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "jinn_understands",
        "Jinn-Lir",
        "Complicated. Yes. That's accurate. For what it's worth, seeing what you've become - the person you are now - I'm proud of you.",
        auto_next="moving_forward"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "moving_forward",
        "Coin",
        "The war is coming to a head. I need to know: will you stand with me?",
        auto_next="jinn_commits"
    ))
    
    jinn_reconciliation.add_node(DialogueNode(
        "jinn_commits",
        "Jinn-Lir",
        "Always. Whatever you need, I'm with you. This time, as equals.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(jinn_reconciliation)
    
    # Dialogue: Coireena Joins
    coireena_ally = Dialogue("coireena_joins", "The Super Soldier's Choice", "start")
    
    coireena_ally.add_node(DialogueNode(
        "start",
        "Coireena",
        "Coin! I heard you were back. I kept my promise - I'm ready to stand with you.",
        auto_next="coin_grateful"
    ))
    
    coireena_ally.add_node(DialogueNode(
        "coin_grateful",
        "Coin",
        "Coireena. I'm glad to see you. How are the others - the super soldiers?",
        auto_next="coireena_report"
    ))
    
    coireena_ally.add_node(DialogueNode(
        "coireena_report",
        "Coireena",
        "Split. Some still serve the Light Cabal, others have gone independent. A few joined the Dark Cabal. Your power changed all of us, but how we use it varies.",
        auto_next="coin_responsibility"
    ))
    
    coireena_ally.add_node(DialogueNode(
        "coin_responsibility",
        "Coin",
        "I feel responsible for what happened to you all.",
        auto_next="coireena_reassures"
    ))
    
    coireena_ally.add_node(DialogueNode(
        "coireena_reassures",
        "Coireena",
        "Don't. You were a victim too. What matters is what we do now. I've made my choice - I fight for you, because you're the only one who's ever treated me like a person, not a weapon.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(coireena_ally)
    
    # Dialogue: Typhus Revelation
    typhus_reveal = Dialogue("typhus_revelation", "The Mysterious Companion", "start")
    
    typhus_reveal.add_node(DialogueNode(
        "start",
        "Narrator",
        "*A creature approaches - small, shifting, somehow familiar. It's Typhus, the being who has appeared throughout your journey.*",
        auto_next="typhus_communication"
    ))
    
    typhus_reveal.add_node(DialogueNode(
        "typhus_communication",
        "Typhus",
        "*communicates through emotions and images rather than words: friendship, protection, shared destiny*",
        auto_next="coin_understanding"
    ))
    
    typhus_reveal.add_node(DialogueNode(
        "coin_understanding",
        "Coin",
        "You've been with me since the beginning. You're... connected to me somehow, aren't you?",
        auto_next="elder_explains"
    ))
    
    typhus_reveal.add_node(DialogueNode(
        "elder_explains",
        "Elder Coin",
        "*appears briefly* Typhus is your temporal shadow - a manifestation of your power that exists slightly outside of time. As you grow, so does Typhus.",
        auto_next="coin_companion"
    ))
    
    typhus_reveal.add_node(DialogueNode(
        "coin_companion",
        "Coin",
        "Then you're part of me. We grow together. *to Typhus* I'm glad you're here.",
        auto_next="typhus_response"
    ))
    
    typhus_reveal.add_node(DialogueNode(
        "typhus_response",
        "Typhus",
        "*radiates warmth and determination: always together*",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(typhus_reveal)
    
    # ENDING PATH 1: Time Goddess Ending
    goddess_ending = Dialogue("goddess_ending_sequence", "Eternal Guardian", "start")
    
    goddess_ending.add_node(DialogueNode(
        "start",
        "Elder Coin",
        "It's time. The Ascension Ritual will complete your transformation. Are you ready?",
        auto_next="coin_ready"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "coin_ready",
        "Coin",
        "I am. I've seen what needs to be done. I accept this responsibility.",
        auto_next="ritual_begins"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "ritual_begins",
        "Narrator",
        "*The CircuitStone fully awakens. Power beyond mortal comprehension flows through you. Past, present, and future become one.*",
        auto_next="ascension"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "ascension",
        "Coin",
        "*voice echoing across time* I am Coin, Time Goddess of Orbspace. Guardian of causality. Protector of the temporal stream. I accept this burden willingly.",
        auto_next="temporal_anomaly"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "temporal_anomaly",
        "Narrator",
        "*A massive distortion appears - the Temporal Anomaly, a being of chaotic time attempting to destabilize Orbspace.*",
        auto_next="final_battle_goddess"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "final_battle_goddess",
        "Coin",
        "This is what I was meant to stop. This is why the Time Goddess exists. *power radiating* Let's end this.",
        auto_next=None  # Epic boss battle
    ))
    
    goddess_ending.add_node(DialogueNode(
        "goddess_victory",
        "Narrator",
        "*The Temporal Anomaly is sealed. Time stabilizes. You stand eternal, watching over Orbspace from outside of linear time.*",
        auto_next="goddess_epilogue"
    ))
    
    goddess_ending.add_node(DialogueNode(
        "goddess_epilogue",
        "Coin",
        "*looking out over Orbspace across all timelines* I am alone, but I am content. I've saved countless lives across infinite moments. This is my purpose. This is who I choose to be.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(goddess_ending)
    
    # ENDING PATH 2: Rebel Ending
    rebel_ending = Dialogue("rebel_ending_sequence", "Forge Your Own Path", "start")
    
    rebel_ending.add_node(DialogueNode(
        "start",
        "Coin",
        "*to Elder Coin* I reject this. I won't be bound by destiny or duty. I'll forge my own path.",
        auto_next="elder_fades"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "elder_fades",
        "Elder Coin",
        "*smiling sadly* I understand. Goodbye, young one. Be brave. *fades from existence*",
        auto_next="circuitstone_reaction"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "circuitstone_reaction",
        "Narrator",
        "*The CircuitStone reacts violently to your rejection. Time itself seems to fight you.*",
        auto_next="coin_determination"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "coin_determination",
        "Coin",
        "I don't care if I'm meant to be your vessel! I choose my own fate!",
        auto_next="breaking_chains"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "breaking_chains",
        "Narrator",
        "*You channel all your power into breaking the temporal chains that bind you to destiny. The strain is immense.*",
        auto_next="reality_battle"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "reality_battle",
        "Coin",
        "*fighting against time itself* I... will... be... FREE!",
        auto_next=None  # Hardest boss battle
    ))
    
    rebel_ending.add_node(DialogueNode(
        "rebel_victory",
        "Narrator",
        "*The chains shatter. The CircuitStone releases you. You are mortal again, but free. Time will find another bearer.*",
        auto_next="rebel_epilogue"
    ))
    
    rebel_ending.add_node(DialogueNode(
        "rebel_epilogue",
        "Coin",
        "*exhausted but smiling* I did it. I'm free. My life is my own now. Whatever comes next, I'll face it as myself, not as what others need me to be.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(rebel_ending)
    
    # ENDING PATH 3: Light Cabal Unity Ending
    light_ending = Dialogue("light_cabal_ending", "Unity of Magic", "start")
    
    light_ending.add_node(DialogueNode(
        "start",
        "Orbius",
        "You've chosen to unite the magic users. A noble goal, but it requires reforming the Light Cabal from within.",
        auto_next="coin_resolve"
    ))
    
    light_ending.add_node(DialogueNode(
        "coin_resolve",
        "Coin",
        "The Light Cabal has good ideals corrupted by bad practices. I'll change it. Make it what it claims to be.",
        auto_next="orbius_support"
    ))
    
    light_ending.add_node(DialogueNode(
        "orbius_support",
        "Orbius",
        "Then you have my full support. Together, we'll create a Cabal that truly protects and respects all magic users.",
        auto_next="drift_negotiation"
    ))
    
    light_ending.add_node(DialogueNode(
        "drift_negotiation",
        "Narrator",
        "*You arrange a meeting with Emperor Turok, proposing a new relationship between magic and technology.*",
        auto_next="turok_skeptical"
    ))
    
    light_ending.add_node(DialogueNode(
        "turok_skeptical",
        "Emperor Turok",
        "You expect me to trust magic users after years of conflict?",
        auto_next="coin_proposal"
    ))
    
    light_ending.add_node(DialogueNode(
        "coin_proposal",
        "Coin",
        "I expect you to be pragmatic. Magic and technology are stronger together than divided. I'll prove it.",
        auto_next="demonstration"
    ))
    
    light_ending.add_node(DialogueNode(
        "demonstration",
        "Narrator",
        "*You demonstrate how magical enhancement of technology creates unprecedented power. Turok is impressed.*",
        auto_next="uneasy_peace"
    ))
    
    light_ending.add_node(DialogueNode(
        "uneasy_peace",
        "Emperor Turok",
        "Very well. An alliance. But know that I'll be watching carefully.",
        auto_next="extremist_opposition"
    ))
    
    light_ending.add_node(DialogueNode(
        "extremist_opposition",
        "Narrator",
        "*Not everyone accepts the new order. Extremists from both sides unite against you.*",
        auto_next="final_battle_light"
    ))
    
    light_ending.add_node(DialogueNode(
        "final_battle_light",
        "Coin",
        "I won't let fear and hatred destroy what we've built. Stand with me!",
        auto_next=None  # Boss battle against combined extremists
    ))
    
    light_ending.add_node(DialogueNode(
        "light_victory",
        "Narrator",
        "*The extremists are defeated. A new era begins with the Reformed Light Cabal leading magical advancement alongside technological progress.*",
        auto_next="light_epilogue"
    ))
    
    light_ending.add_node(DialogueNode(
        "light_epilogue",
        "Coin",
        "*addressing a gathering* Magic and technology are not enemies. Today, we prove that cooperation is stronger than conflict. This is the beginning of true peace.",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(light_ending)
    
    # ENDING PATH 4: Dark Cabal Chaos Ending
    dark_ending = Dialogue("dark_cabal_ending", "Embrace the Chaos", "start")
    
    dark_ending.add_node(DialogueNode(
        "start",
        "Selene",
        "You've chosen power. Good. The weak have ruled for too long. Time for the strong to take their rightful place.",
        auto_next="coin_powerful"
    ))
    
    dark_ending.add_node(DialogueNode(
        "coin_powerful",
        "Coin",
        "I'm done pretending to be gentle. I have the power to reshape Orbspace. Why shouldn't I use it?",
        auto_next="selene_pleased"
    ))
    
    dark_ending.add_node(DialogueNode(
        "selene_pleased",
        "Selene",
        "Exactly! The Light Cabal's weakness led to this war. Under our rule, there will be order through strength.",
        auto_next="orbius_confrontation"
    ))
    
    dark_ending.add_node(DialogueNode(
        "orbius_confrontation",
        "Orbius",
        "*appears* Coin, this isn't who you are. Power without compassion becomes tyranny.",
        auto_next="coin_cold"
    ))
    
    dark_ending.add_node(DialogueNode(
        "coin_cold",
        "Coin",
        "You taught me about choice, Orbius. This is my choice. Stand aside or stand against me.",
        auto_next="orbius_battle"
    ))
    
    dark_ending.add_node(DialogueNode(
        "orbius_battle",
        "Orbius",
        "*sadly* Then I must stop you. Forgive me, Coin.",
        auto_next=None  # Boss battle against Orbius
    ))
    
    dark_ending.add_node(DialogueNode(
        "dark_victory_orbius",
        "Coin",
        "*standing over defeated Orbius* I'm sorry it came to this. But nothing will stop me now.",
        auto_next="empire_conquest"
    ))
    
    dark_ending.add_node(DialogueNode(
        "empire_conquest",
        "Narrator",
        "*You systematically conquer the Drift Empire, absorbing its technology into Dark Cabal power structures.*",
        auto_next="chaos_ascension"
    ))
    
    dark_ending.add_node(DialogueNode(
        "chaos_ascension",
        "Coin",
        "*channeling immense power* I ascend not as Time Goddess, but as Chaos Goddess! Orbspace will know true strength!",
        auto_next="dark_epilogue"
    ))
    
    dark_ending.add_node(DialogueNode(
        "dark_epilogue",
        "Narrator",
        "*You rule Orbspace with absolute power. Order through strength. Many prosper. Many suffer. You've become what you once feared.*",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(dark_ending)
    
    # ENDING PATH 5: Peaceful Unity Ending
    peace_ending = Dialogue("peaceful_ending", "Bridge Between Worlds", "start")
    
    peace_ending.add_node(DialogueNode(
        "start",
        "Coin",
        "*addressing leaders from all factions* This war has cost us too much. Magic users and technology adherents can coexist. I'll prove it.",
        auto_next="skeptical_leaders"
    ))
    
    peace_ending.add_node(DialogueNode(
        "skeptical_leaders",
        "Various Leaders",
        "*murmuring* How can we trust each other after everything?",
        auto_next="coin_demonstration"
    ))
    
    peace_ending.add_node(DialogueNode(
        "coin_demonstration",
        "Coin",
        "Because I embody both. I was created by magic, empowered by it, yet I've learned from technology. I exist between your worlds. If I can do it, so can Orbspace.",
        auto_next="emperor_speaks"
    ))
    
    peace_ending.add_node(DialogueNode(
        "emperor_speaks",
        "Emperor Turok",
        "Your words are appealing, but words aren't enough. We need guarantees.",
        auto_next="coin_proposal"
    ))
    
    peace_ending.add_node(DialogueNode(
        "coin_proposal",
        "Coin",
        "Then I propose the Council of Unity. Representatives from all factions, equal voting power, with me as neutral mediator. No faction dominates. All voices heard.",
        auto_next="orbius_supports"
    ))
    
    peace_ending.add_node(DialogueNode(
        "orbius_supports",
        "Orbius",
        "The Light Cabal supports this proposal. It's time we lived up to our ideals.",
        auto_next="selene_objects"
    ))
    
    peace_ending.add_node(DialogueNode(
        "selene_objects",
        "Selene",
        "The Dark Cabal does not. Peace means weakness!",
        auto_next="coin_challenge"
    ))
    
    peace_ending.add_node(DialogueNode(
        "coin_challenge",
        "Coin",
        "Then you oppose not just me, but the will of Orbspace. I'm sorry, Selene.",
        auto_next="warmonger_battle"
    ))
    
    peace_ending.add_node(DialogueNode(
        "warmonger_battle",
        "Narrator",
        "*Those who refuse peace unite against you. It's a desperate, final battle for Orbspace's future.*",
        auto_next=None  # Boss battle
    ))
    
    peace_ending.add_node(DialogueNode(
        "peace_victory",
        "Narrator",
        "*The warmongering factions are defeated. Those willing to negotiate remain. Peace becomes possible.*",
        auto_next="council_formation"
    ))
    
    peace_ending.add_node(DialogueNode(
        "council_formation",
        "Coin",
        "*presiding over the first Council of Unity* Today, we choose cooperation over conflict. This is the hardest path, but the most rewarding. Welcome to a new era.",
        auto_next="peace_epilogue"
    ))
    
    peace_ending.add_node(DialogueNode(
        "peace_epilogue",
        "Narrator",
        "*Years later, Orbspace thrives. Magic and technology advance together. You remain as mediator, respected by all sides. You've created lasting peace.*",
        auto_next=None
    ))
    
    dialogue_system.register_dialogue(peace_ending)


def create_ending_requirements() -> dict:
    """Define requirements for each ending"""
    return {
        'time_goddess': {
            'description': 'Become the eternal Time Goddess',
            'requirements': {
                'quest': 'act4_ending_01',
                'level': 28,
                'story_flags': {'accepted_destiny': True}
            }
        },
        'rebel': {
            'description': 'Forge your own path, rejecting destiny',
            'requirements': {
                'quest': 'act4_ending_02',
                'level': 30,
                'faction': {'independent': 100},
                'story_flags': {'rejected_destiny': True}
            }
        },
        'light_cabal': {
            'description': 'Unite magic users under enlightened leadership',
            'requirements': {
                'quest': 'act4_ending_03',
                'level': 28,
                'faction': {'light_cabal': 200}
            }
        },
        'dark_cabal': {
            'description': 'Embrace chaos and reshape through power',
            'requirements': {
                'quest': 'act4_ending_04',
                'level': 28,
                'faction': {'dark_cabal': 200}
            }
        },
        'peaceful': {
            'description': 'Broker peace between all factions',
            'requirements': {
                'quest': 'act4_ending_05',
                'level': 28,
                'faction': {
                    'light_cabal': 100,
                    'drift_empire': 50,
                    'independent': 100
                }
            }
        }
    }


def initialize_act4_content(quest_manager, dialogue_system, npc_manager):
    """Initialize all Act 4 content"""
    create_act4_quests(quest_manager)
    create_act4_dialogues(dialogue_system, npc_manager)
    print("✓ Act 4 content initialized")
    print("✓ 5 ending paths with full narrative created")
    print("✓ 3 optional superboss encounters created")
    print("✓ Episodes VI-X fully represented")


def get_available_endings(player_level: int, faction_rep: dict, story_flags: dict) -> list:
    """Determine which endings are available to player"""
    endings = create_ending_requirements()
    available = []
    
    for ending_id, ending_data in endings.items():
        requirements = ending_data['requirements']
        
        # Check level
        if player_level < requirements.get('level', 0):
            continue
        
        # Check faction requirements
        if 'faction' in requirements:
            meets_faction = True
            for faction, required_rep in requirements['faction'].items():
                if faction_rep.get(faction, 0) < required_rep:
                    meets_faction = False
                    break
            if not meets_faction:
                continue
        
        # Check story flags
        if 'story_flags' in requirements:
            meets_flags = True
            for flag, required_value in requirements['story_flags'].items():
                if story_flags.get(flag) != required_value:
                    meets_flags = False
                    break
            if not meets_flags:
                continue
        
        available.append(ending_id)
    
    return available
