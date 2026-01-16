"""
COIN:OPERATED JRPG - Progression System
Character progression, equipment, and faction reputation
"""

from typing import Dict, List, Optional
from enum import Enum


class EquipmentSlot(Enum):
    """Equipment slot types"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"


class EquipmentRarity(Enum):
    """Equipment quality tiers"""
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class Equipment:
    """Equipment item class"""
    
    def __init__(self, name: str, slot: EquipmentSlot, rarity: EquipmentRarity,
                 description: str = "", stat_bonuses: Optional[Dict[str, int]] = None):
        self.name = name
        self.slot = slot
        self.rarity = rarity
        self.description = description
        self.stat_bonuses = stat_bonuses or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'slot': self.slot.value,
            'rarity': self.rarity.value,
            'description': self.description,
            'stat_bonuses': self.stat_bonuses
        }


class Item:
    """Consumable item class"""
    
    def __init__(self, name: str, description: str, effect: str, power: int, quantity: int = 1):
        self.name = name
        self.description = description
        self.effect = effect  # heal_hp, heal_mp, revive, buff, etc.
        self.power = power
        self.quantity = quantity
    
    def use(self, target):
        """Use item on target"""
        if self.quantity <= 0:
            return False
        
        if self.effect == "heal_hp":
            target.stats.heal(self.power)
            self.quantity -= 1
            return True
        elif self.effect == "heal_mp":
            target.stats.restore_mp(self.power)
            self.quantity -= 1
            return True
        elif self.effect == "revive":
            if not target.stats.is_alive():
                target.stats.current_hp = int(target.stats.max_hp * 0.5)
                self.quantity -= 1
                return True
        
        return False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'effect': self.effect,
            'power': self.power,
            'quantity': self.quantity
        }


class Inventory:
    """Player inventory system"""
    
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self.equipment: List[Equipment] = []
        self.domminnian_coins = 100  # Starting currency
        self.magical_essence = 0
        self.max_items = 99  # Max of each item type
    
    def add_item(self, item: Item, quantity: int = 1):
        """Add item to inventory"""
        if item.name in self.items:
            self.items[item.name].quantity = min(
                self.items[item.name].quantity + quantity,
                self.max_items
            )
        else:
            item.quantity = min(quantity, self.max_items)
            self.items[item.name] = item
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory"""
        if item_name in self.items:
            self.items[item_name].quantity -= quantity
            if self.items[item_name].quantity <= 0:
                del self.items[item_name]
            return True
        return False
    
    def add_equipment(self, equipment: Equipment):
        """Add equipment to inventory"""
        self.equipment.append(equipment)
    
    def remove_equipment(self, equipment_name: str) -> bool:
        """Remove equipment from inventory"""
        for i, equip in enumerate(self.equipment):
            if equip.name == equipment_name:
                self.equipment.pop(i)
                return True
        return False
    
    def add_currency(self, coins: int = 0, essence: int = 0):
        """Add currency"""
        self.domminnian_coins += coins
        self.magical_essence += essence
    
    def spend_currency(self, coins: int = 0, essence: int = 0) -> bool:
        """Spend currency, return False if insufficient funds"""
        if self.domminnian_coins >= coins and self.magical_essence >= essence:
            self.domminnian_coins -= coins
            self.magical_essence -= essence
            return True
        return False
    
    def display(self):
        """Display inventory"""
        print(f"\n{'=' * 60}")
        print(" " * 22 + "INVENTORY")
        print(f"{'=' * 60}")
        print(f"\nCurrency:")
        print(f"  Domminnian Coins: {self.domminnian_coins}")
        print(f"  Magical Essence: {self.magical_essence}")
        
        print(f"\nItems:")
        if not self.items:
            print("  No items")
        else:
            for item in self.items.values():
                print(f"  {item.name} x{item.quantity} - {item.description}")
        
        print(f"\nEquipment:")
        if not self.equipment:
            print("  No equipment")
        else:
            for equip in self.equipment:
                bonuses = ", ".join([f"{k}+{v}" for k, v in equip.stat_bonuses.items()])
                print(f"  [{equip.rarity.value}] {equip.name} - {bonuses}")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'items': {name: item.to_dict() for name, item in self.items.items()},
            'equipment': [e.to_dict() for e in self.equipment],
            'domminnian_coins': self.domminnian_coins,
            'magical_essence': self.magical_essence
        }


class FactionReputation:
    """Faction reputation system"""
    
    def __init__(self):
        self.reputations = {
            'drift_empire': 0,
            'light_cabal': 0,
            'dark_cabal': 0,
            'independent': 0
        }
        self.reputation_tiers = [
            (-100, "Hostile"),
            (-50, "Unfriendly"),
            (0, "Neutral"),
            (50, "Friendly"),
            (100, "Honored"),
            (200, "Revered"),
            (300, "Exalted")
        ]
    
    def modify_reputation(self, faction: str, amount: int):
        """Modify reputation with a faction"""
        if faction in self.reputations:
            self.reputations[faction] = max(-100, min(300, self.reputations[faction] + amount))
            print(f"\n{'▲' if amount > 0 else '▼'} {faction.replace('_', ' ').title()} reputation: {amount:+d}")
    
    def get_reputation_tier(self, faction: str) -> str:
        """Get reputation tier name"""
        if faction not in self.reputations:
            return "Unknown"
        
        rep = self.reputations[faction]
        for threshold, tier in reversed(self.reputation_tiers):
            if rep >= threshold:
                return tier
        return "Hostile"
    
    def get_primary_faction(self) -> str:
        """Get faction with highest reputation"""
        return max(self.reputations, key=self.reputations.get)
    
    def display(self):
        """Display faction reputations"""
        print(f"\n{'=' * 60}")
        print(" " * 18 + "FACTION REPUTATION")
        print(f"{'=' * 60}")
        
        for faction, rep in self.reputations.items():
            tier = self.get_reputation_tier(faction)
            faction_name = faction.replace('_', ' ').title()
            bar = self.create_reputation_bar(rep)
            print(f"\n{faction_name}:")
            print(f"  {bar} {rep:+d} [{tier}]")
    
    def create_reputation_bar(self, reputation: int, width: int = 30) -> str:
        """Create visual reputation bar"""
        # Normalize to 0-100 range for display
        normalized = int(((reputation + 100) / 400) * width)
        filled = "█" * normalized
        empty = "░" * (width - normalized)
        return f"[{filled}{empty}]"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'reputations': self.reputations.copy(),
            'primary_faction': self.get_primary_faction()
        }


class ProgressionSystem:
    """Manages overall character and game progression"""
    
    def __init__(self):
        self.inventory = Inventory()
        self.faction_reputation = FactionReputation()
        self.unlocked_abilities: Dict[str, List[str]] = {}  # character_name: [ability_names]
        self.discovered_locations: List[str] = []
        self.defeated_bosses: List[str] = []
        self.story_choices: Dict[str, str] = {}
    
    def unlock_ability(self, character_name: str, ability_name: str):
        """Unlock an ability for a character"""
        if character_name not in self.unlocked_abilities:
            self.unlocked_abilities[character_name] = []
        
        if ability_name not in self.unlocked_abilities[character_name]:
            self.unlocked_abilities[character_name].append(ability_name)
            print(f"\n✨ {character_name} learned {ability_name}!")
    
    def discover_location(self, location_name: str):
        """Discover a new location"""
        if location_name not in self.discovered_locations:
            self.discovered_locations.append(location_name)
            print(f"\n📍 Discovered: {location_name}")
    
    def defeat_boss(self, boss_name: str):
        """Record boss defeat"""
        if boss_name not in self.defeated_bosses:
            self.defeated_bosses.append(boss_name)
            print(f"\n🏆 {boss_name} defeated!")
    
    def record_choice(self, choice_id: str, choice: str):
        """Record story choice"""
        self.story_choices[choice_id] = choice
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'inventory': self.inventory.to_dict(),
            'faction_reputation': self.faction_reputation.to_dict(),
            'unlocked_abilities': self.unlocked_abilities,
            'discovered_locations': self.discovered_locations,
            'defeated_bosses': self.defeated_bosses,
            'story_choices': self.story_choices
        }
