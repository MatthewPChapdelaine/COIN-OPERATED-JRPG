"""
COIN:OPERATED JRPG - Act 4 & Endings Content
Resolution & Consequences - Multiple ending paths
"""

from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from systems.dialogue import NPC, NPCManager


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
    print("✓ Act 4 content initialized")
    print("✓ 5 ending paths created")
    print("✓ 3 optional superboss encounters created")


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
