"""
COIN:OPERATED JRPG - Enemy System
Enemy characters and boss battles
"""

from typing import Dict, List
from core.character import Character, CharacterRole, CharacterFaction, Ability, Stats


class Enemy(Character):
    """Enemy character class"""
    
    def __init__(self, name: str, level: int, description: str,
                 faction: CharacterFaction, enemy_type: str = "normal"):
        super().__init__(
            name=name,
            role=CharacterRole.PHYSICAL_DPS,  # Default, can be customized
            faction=faction,
            level=level,
            description=description
        )
        self.enemy_type = enemy_type  # normal, elite, boss
        self.loot_coins = level * 10
        self.loot_essence = level * 5
    
    def set_loot(self, coins: int, essence: int):
        """Set custom loot amounts"""
        self.loot_coins = coins
        self.loot_essence = essence


def create_drift_soldier(level: int = 1) -> Enemy:
    """Create Drift Empire soldier enemy"""
    enemy = Enemy(
        name="Drift Soldier",
        level=level,
        description="A soldier of the technology-focused Drift Empire, armed with advanced weaponry.",
        faction=CharacterFaction.DRIFT_EMPIRE,
        enemy_type="normal"
    )
    enemy.role = CharacterRole.PHYSICAL_DPS
    
    # Boost stats for physical combat
    enemy.stats.strength += level * 2
    enemy.stats.defense += level
    enemy.stats.magic_defense = int(enemy.stats.magic_defense * 0.7)  # Weak to magic
    
    enemy.add_ability(Ability(
        "Energy Blast",
        "Fires technological energy weapon",
        mp_cost=10,
        power=25,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    return enemy


def create_drift_raider(level: int = 2) -> Enemy:
    """Create Drift raider enemy"""
    enemy = Enemy(
        name="Drift Raider",
        level=level,
        description="Elite Drift forces specialized in raids and theft.",
        faction=CharacterFaction.DRIFT_EMPIRE,
        enemy_type="elite"
    )
    enemy.role = CharacterRole.PHYSICAL_DPS
    
    enemy.stats.strength += level * 3
    enemy.stats.speed += level * 2
    enemy.stats.defense += level * 2
    
    enemy.add_ability(Ability(
        "Rapid Fire",
        "Multiple quick attacks",
        mp_cost=15,
        power=20,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    enemy.set_loot(coins=level * 15, essence=level * 7)
    
    return enemy


def create_dark_cabal_mage(level: int = 3) -> Enemy:
    """Create Dark Cabal mage enemy"""
    enemy = Enemy(
        name="Dark Cabal Mage",
        level=level,
        description="A mage who practices chaotic and destructive magic.",
        faction=CharacterFaction.DARK_CABAL,
        enemy_type="normal"
    )
    enemy.role = CharacterRole.MAGIC_DPS
    
    enemy.stats.magic += level * 3
    enemy.stats.magic_defense += level * 2
    enemy.stats.defense = int(enemy.stats.defense * 0.6)  # Weak to physical
    
    enemy.add_ability(Ability(
        "Chaos Bolt",
        "Destructive magical attack",
        mp_cost=20,
        power=35,
        ability_type="magic",
        target="single"
    ), unlocked=True)
    
    enemy.add_ability(Ability(
        "Dark Barrier",
        "Temporarily boost defense",
        mp_cost=15,
        power=0,
        ability_type="utility",
        target="self"
    ), unlocked=True)
    
    return enemy


def create_wild_beast(level: int = 1) -> Enemy:
    """Create wild beast enemy"""
    enemy = Enemy(
        name="Wild Beast",
        level=level,
        description="A creature corrupted by wild magic from the outskirts.",
        faction=CharacterFaction.INDEPENDENT,
        enemy_type="normal"
    )
    enemy.role = CharacterRole.PHYSICAL_DPS
    
    enemy.stats.strength += level * 2
    enemy.stats.speed += level * 3
    enemy.stats.max_hp += level * 5
    enemy.stats.current_hp = enemy.stats.max_hp
    
    enemy.add_ability(Ability(
        "Savage Bite",
        "Powerful physical attack",
        mp_cost=0,
        power=30,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    return enemy


def create_magical_construct(level: int = 5) -> Enemy:
    """Create magical construct enemy for trials"""
    enemy = Enemy(
        name="Magical Construct",
        level=level,
        description="A being of pure magical energy summoned for testing purposes.",
        faction=CharacterFaction.LIGHT_CABAL,
        enemy_type="elite"
    )
    enemy.role = CharacterRole.MAGIC_DPS
    
    enemy.stats.magic += level * 4
    enemy.stats.magic_defense += level * 3
    enemy.stats.defense += level * 2
    enemy.stats.max_hp += level * 10
    enemy.stats.current_hp = enemy.stats.max_hp
    
    enemy.add_ability(Ability(
        "Arcane Missile",
        "Multiple magical projectiles",
        mp_cost=25,
        power=30,
        ability_type="magic",
        target="single"
    ), unlocked=True)
    
    enemy.add_ability(Ability(
        "Magic Barrier",
        "Reduce incoming damage",
        mp_cost=20,
        power=0,
        ability_type="utility",
        target="self"
    ), unlocked=True)
    
    enemy.set_loot(coins=level * 20, essence=level * 15)
    
    return enemy


def create_super_soldier(level: int = 4) -> Enemy:
    """Create super-soldier empowered by Coin's magic"""
    enemy = Enemy(
        name="Super Soldier",
        level=level,
        description="A Drift soldier enhanced with stolen magical power from Coin.",
        faction=CharacterFaction.DRIFT_EMPIRE,
        enemy_type="elite"
    )
    enemy.role = CharacterRole.TANK
    
    # Hybrid stats - both tech and magic
    enemy.stats.strength += level * 3
    enemy.stats.magic += level * 2
    enemy.stats.defense += level * 4
    enemy.stats.magic_defense += level * 3
    enemy.stats.max_hp += level * 15
    enemy.stats.current_hp = enemy.stats.max_hp
    
    enemy.add_ability(Ability(
        "Enhanced Strike",
        "Magically-enhanced physical attack",
        mp_cost=15,
        power=40,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    enemy.add_ability(Ability(
        "Stolen Magic",
        "Use Coin's magic against her",
        mp_cost=25,
        power=35,
        ability_type="magic",
        target="single"
    ), unlocked=True)
    
    enemy.set_loot(coins=level * 25, essence=level * 20)
    
    return enemy


# BOSS: Magical Outburst (Act 1 Tutorial Boss)
def create_boss_magical_outburst() -> Enemy:
    """Create Act 1 boss - manifestation of Coin's uncontrolled power"""
    boss = Enemy(
        name="Manifestation of Rage",
        level=5,
        description="Your own magical power given physical form - violent, chaotic, and barely contained.",
        faction=CharacterFaction.INDEPENDENT,
        enemy_type="boss"
    )
    boss.role = CharacterRole.MAGIC_DPS
    
    # Boss stats
    boss.stats.level = 5
    boss.stats.max_hp = 500
    boss.stats.current_hp = 500
    boss.stats.max_mp = 200
    boss.stats.current_mp = 200
    boss.stats.magic = 40
    boss.stats.magic_defense = 30
    boss.stats.defense = 25
    boss.stats.speed = 25
    
    # Boss abilities
    boss.add_ability(Ability(
        "Uncontrolled Blast",
        "Wild magical explosion hitting all enemies",
        mp_cost=30,
        power=45,
        ability_type="magic",
        target="all"
    ), unlocked=True)
    
    boss.add_ability(Ability(
        "Emotional Surge",
        "Channel raw emotion into devastating single-target magic",
        mp_cost=40,
        power=70,
        ability_type="magic",
        target="single"
    ), unlocked=True)
    
    boss.add_ability(Ability(
        "Desperate Recovery",
        "Heal when health drops below 50%",
        mp_cost=50,
        power=150,
        ability_type="healing",
        target="self"
    ), unlocked=True)
    
    boss.set_loot(coins=500, essence=250)
    
    return boss


# BOSS: Emperor Turok (Act 2 - mentioned for future implementation)
def create_boss_emperor_turok() -> Enemy:
    """Create Emperor Turok boss (non-lethal encounter)"""
    boss = Enemy(
        name="Emperor Turok",
        level=15,
        description="Leader of the Drift Empire. A master strategist and formidable opponent.",
        faction=CharacterFaction.DRIFT_EMPIRE,
        enemy_type="boss"
    )
    boss.role = CharacterRole.TANK
    
    # Boss stats
    boss.stats.level = 15
    boss.stats.max_hp = 2000
    boss.stats.current_hp = 2000
    boss.stats.max_mp = 300
    boss.stats.current_mp = 300
    boss.stats.strength = 60
    boss.stats.defense = 70
    boss.stats.magic_defense = 50
    boss.stats.speed = 40
    
    boss.add_ability(Ability(
        "Imperial Command",
        "Summon reinforcements",
        mp_cost=50,
        power=0,
        ability_type="utility",
        target="self"
    ), unlocked=True)
    
    boss.add_ability(Ability(
        "Technology Suppression Field",
        "Reduce magical effectiveness",
        mp_cost=40,
        power=0,
        ability_type="utility",
        target="all"
    ), unlocked=True)
    
    boss.add_ability(Ability(
        "Plasma Cannon",
        "Devastating energy weapon",
        mp_cost=60,
        power=90,
        ability_type="physical",
        target="single"
    ), unlocked=True)
    
    boss.set_loot(coins=2000, essence=1000)
    
    return boss


class EnemyFactory:
    """Factory for creating enemies"""
    
    @staticmethod
    def create_enemy(enemy_type: str, level: int = 1) -> Enemy:
        """Create an enemy by type"""
        enemy_creators = {
            'drift_soldier': create_drift_soldier,
            'drift_raider': create_drift_raider,
            'dark_cabal_mage': create_dark_cabal_mage,
            'wild_beast': create_wild_beast,
            'magical_construct': create_magical_construct,
            'super_soldier': create_super_soldier,
            'boss_magical_outburst': lambda l=None: create_boss_magical_outburst(),
            'boss_emperor_turok': lambda l=None: create_boss_emperor_turok()
        }
        
        if enemy_type in enemy_creators:
            return enemy_creators[enemy_type](level)
        else:
            # Default to drift soldier
            return create_drift_soldier(level)
    
    @staticmethod
    def create_encounter(encounter_name: str, player_level: int = 1) -> List[Enemy]:
        """Create a pre-defined enemy encounter"""
        encounters = {
            'tutorial_combat': [
                create_drift_soldier(1),
                create_wild_beast(1)
            ],
            'temple_defense': [
                create_drift_soldier(2),
                create_drift_soldier(2),
                create_drift_raider(2)
            ],
            'dark_cabal_ambush': [
                create_dark_cabal_mage(3),
                create_dark_cabal_mage(3)
            ],
            'super_soldier_squad': [
                create_super_soldier(4),
                create_drift_soldier(4),
                create_drift_soldier(4)
            ],
            'magical_trial': [
                create_magical_construct(5)
            ],
            'act1_boss': [
                create_boss_magical_outburst()
            ],
            'random_encounter_easy': [
                create_wild_beast(max(1, player_level - 1)),
                create_wild_beast(max(1, player_level - 1))
            ],
            'random_encounter_medium': [
                create_drift_soldier(player_level),
                create_drift_soldier(player_level),
                create_wild_beast(player_level)
            ],
            'random_encounter_hard': [
                create_drift_raider(player_level + 1),
                create_dark_cabal_mage(player_level + 1)
            ]
        }
        
        return encounters.get(encounter_name, [create_drift_soldier(player_level)])
