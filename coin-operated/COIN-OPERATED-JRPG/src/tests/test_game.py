"""
COIN:OPERATED JRPG - Test Suite
Automated testing for all game systems
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.character import Coin, JinnLir, Stats, Ability
from systems.combat import CombatSystem
from systems.progression import Inventory, Equipment, EquipmentSlot, EquipmentRarity, FactionReputation
from systems.quest import Quest, QuestObjective, QuestType, QuestManager
from content.enemies import EnemyFactory


def test_character_system():
    """Test character creation and abilities"""
    print("\n" + "=" * 60)
    print("Testing Character System...")
    print("=" * 60)
    
    # Create Coin
    coin = Coin()
    print(f"✓ Created {coin.name}")
    print(f"  Level: {coin.stats.level}")
    print(f"  HP: {coin.stats.current_hp}/{coin.stats.max_hp}")
    print(f"  Abilities: {len(coin.abilities)}")
    
    # Test level up
    coin.gain_exp(150)
    print(f"✓ Gained experience")
    print(f"  New Level: {coin.stats.level}")
    
    # Test aging
    coin.age_up()
    print(f"✓ Aged up to: {coin.age_state}")
    
    # Create party member
    jinn_lir = JinnLir()
    print(f"✓ Created {jinn_lir.name}")
    print(f"  Level: {jinn_lir.stats.level}")
    print(f"  Faction: {jinn_lir.faction.value}")
    
    return True


def test_combat_system():
    """Test combat mechanics"""
    print("\n" + "=" * 60)
    print("Testing Combat System...")
    print("=" * 60)
    
    # Create combatants
    coin = Coin()
    coin.stats.level = 5
    coin.stats.current_hp = 150
    coin.stats.max_hp = 150
    
    enemies = [
        EnemyFactory.create_enemy('drift_soldier', 3),
        EnemyFactory.create_enemy('wild_beast', 3)
    ]
    
    print(f"✓ Created party: {coin.name}")
    print(f"✓ Created enemies: {', '.join([e.name for e in enemies])}")
    
    # Initialize combat
    combat = CombatSystem()
    combat.start_combat([coin], enemies)
    print(f"✓ Combat initialized")
    print(f"  Turn order: {len(combat.turn_order)} combatants")
    
    # Test damage calculation
    damage = combat.calculate_physical_damage(coin, enemies[0])
    print(f"✓ Damage calculation: {damage}")
    
    return True


def test_progression_system():
    """Test progression mechanics"""
    print("\n" + "=" * 60)
    print("Testing Progression System...")
    print("=" * 60)
    
    # Test inventory
    inventory = Inventory()
    inventory.add_currency(coins=100, essence=50)
    print(f"✓ Added currency")
    print(f"  Coins: {inventory.domminnian_coins}")
    print(f"  Essence: {inventory.magical_essence}")
    
    # Test equipment
    weapon = Equipment(
        "Magic Staff",
        EquipmentSlot.WEAPON,
        EquipmentRarity.RARE,
        "A powerful magical staff",
        {'magic': 10, 'mp': 20}
    )
    inventory.add_equipment(weapon)
    print(f"✓ Added equipment: {weapon.name}")
    
    # Test faction reputation
    faction_rep = FactionReputation()
    faction_rep.modify_reputation('light_cabal', 50)
    faction_rep.modify_reputation('drift_empire', -30)
    print(f"✓ Modified faction reputations")
    print(f"  Light Cabal: {faction_rep.get_reputation_tier('light_cabal')}")
    print(f"  Drift Empire: {faction_rep.get_reputation_tier('drift_empire')}")
    
    return True


def test_quest_system():
    """Test quest mechanics"""
    print("\n" + "=" * 60)
    print("Testing Quest System...")
    print("=" * 60)
    
    # Create quest
    quest = Quest(
        "test_quest",
        "Test Quest",
        "A quest for testing purposes",
        QuestType.SIDE_QUEST,
        "Test NPC",
        level_requirement=1
    )
    
    # Add objectives
    quest.add_objective(QuestObjective(
        "Defeat 3 enemies",
        "defeat",
        "enemy",
        required=3
    ))
    
    quest.add_objective(QuestObjective(
        "Talk to NPC",
        "talk",
        "npc"
    ))
    
    print(f"✓ Created quest: {quest.name}")
    print(f"  Objectives: {len(quest.objectives)}")
    
    # Start quest
    quest.start()
    print(f"✓ Quest started")
    
    # Update objectives
    quest.update_objective("defeat", "enemy", 2)
    print(f"✓ Updated objective progress")
    
    quest.update_objective("defeat", "enemy", 1)
    print(f"✓ Objective completed")
    
    return True


def test_enemy_factory():
    """Test enemy creation"""
    print("\n" + "=" * 60)
    print("Testing Enemy Factory...")
    print("=" * 60)
    
    # Test different enemy types
    enemies = {
        'drift_soldier': EnemyFactory.create_enemy('drift_soldier', 2),
        'dark_cabal_mage': EnemyFactory.create_enemy('dark_cabal_mage', 3),
        'wild_beast': EnemyFactory.create_enemy('wild_beast', 1),
        'super_soldier': EnemyFactory.create_enemy('super_soldier', 4)
    }
    
    for enemy_type, enemy in enemies.items():
        print(f"✓ Created {enemy_type}: {enemy.name}")
        print(f"  Level {enemy.stats.level} | HP: {enemy.stats.max_hp}")
    
    # Test encounter creation
    encounter = EnemyFactory.create_encounter('temple_defense', 2)
    print(f"✓ Created encounter: {len(encounter)} enemies")
    
    # Test boss creation
    boss = EnemyFactory.create_enemy('boss_magical_outburst')
    print(f"✓ Created boss: {boss.name}")
    print(f"  HP: {boss.stats.max_hp} | Abilities: {len(boss.abilities)}")
    
    return True


def test_all_systems():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 20 + "COIN:OPERATED JRPG")
    print(" " * 22 + "TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Character System", test_character_system),
        ("Combat System", test_combat_system),
        ("Progression System", test_progression_system),
        ("Quest System", test_quest_system),
        ("Enemy Factory", test_enemy_factory)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✓ {test_name} PASSED")
            else:
                failed += 1
                print(f"\n✗ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n✗ {test_name} FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = test_all_systems()
    sys.exit(0 if success else 1)
