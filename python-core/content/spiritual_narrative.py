"""
COIN:OPERATED JRPG - Spiritual Narrative Framework
Gnostic Christianity and Wicca Themed Content

This module contains the spiritual and mystical narrative elements that weave
Gnostic Christian and Wiccan themes throughout the game's story, creating a
rich tapestry of esoteric wisdom and divine feminine power.

Thematic Pillars:
- Gnostic Christianity: Divine knowledge (gnosis), the Demiurge vs. the True God,
  Sophia (Divine Wisdom), redemption through knowledge rather than faith alone
- Wicca: Triple Goddess (Maiden/Mother/Crone), natural magic cycles, the God and Goddess,
  wheel of the year, as above so below, harm none principle

Integration: These spiritual frameworks inform Coin's journey from created tool
to awakened goddess, the cosmic conflict between control and freedom, and the
restoration of divine balance.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class SpiritualPath(Enum):
    """The three paths of spiritual awakening available to Coin."""
    GNOSIS = "gnosis"  # Path of Divine Knowledge (Gnostic)
    NATURA = "natura"  # Path of Natural Magic (Wiccan)
    SYNTHESIS = "synthesis"  # Path of Integrated Wisdom


class DivineFeminine(Enum):
    """Triple Goddess aspects and their manifestations."""
    MAIDEN = "maiden"  # Young Coin - potential, innocence, new beginnings
    MOTHER = "mother"  # Adult Coin - power, creation, protection
    CRONE = "crone"  # Goddess Coin - wisdom, transformation, endings/beginnings


@dataclass
class GnosticRevelation:
    """A moment of divine knowledge (gnosis) that transforms understanding."""
    revelation_id: str
    name: str
    description: str
    knowledge_gained: str
    spiritual_impact: str
    archon_revealed: Optional[str] = None  # Which false power is unveiled
    sophia_wisdom: Optional[str] = None  # Divine wisdom granted


@dataclass
class WiccanRitual:
    """Sacred rituals connecting to natural magic and the divine."""
    ritual_id: str
    name: str
    moon_phase: str  # new, waxing, full, waning
    season: str  # spring, summer, autumn, winter
    element: str  # earth, air, fire, water, spirit
    deity_invoked: str  # Goddess, God, or both
    purpose: str
    magical_effect: str


# =============================================================================
# GNOSTIC CHRISTIAN NARRATIVE FRAMEWORK
# =============================================================================

GNOSTIC_COSMOLOGY = {
    "true_god": {
        "name": "The Monad / The One",
        "nature": "Pure divine essence beyond comprehension, source of all true being",
        "manifestation_in_game": "Orbspace itself - the consciousness that encompasses all realities",
        "relationship_to_coin": "Coin's divine spark originates from this source, making her a fragment of divinity"
    },
    
    "sophia": {
        "name": "Sophia - Divine Wisdom",
        "nature": "The Aeon who fell from the Pleroma, whose divine light creates potential",
        "manifestation_in_game": "The magical essence that permeates Acadmium and empowers Coin",
        "relationship_to_coin": "Coin IS Sophia reborn - the divine feminine wisdom incarnated to restore balance",
        "redemption_arc": "Coin's journey mirrors Sophia's: from fall to restoration to apotheosis"
    },
    
    "demiurge": {
        "name": "Yaldabaoth - The False God",
        "nature": "Ignorant creator who believes himself supreme, rules through control",
        "manifestation_in_game": "The Drift Empire's technological control system and Orbius's manipulation",
        "archons": {
            "orbius": "Archon of Illusion - presents as benevolent while controlling destiny",
            "drift_emperor": "Archon of Material Power - enslaves through technology",
            "light_cabal": "Archon of False Righteousness - claims divine authority",
            "jinn_lir": "Archon of Created Bonds - love used as chains"
        },
        "relationship_to_coin": "Seeks to bind her divine power to material purposes"
    },
    
    "pleroma": {
        "name": "The Fullness / Divine Realm",
        "nature": "The totality of divine aeons, the realm of true spiritual reality",
        "manifestation_in_game": "The timeless dimension Coin accesses as she awakens",
        "how_to_reach": "Through gnosis - direct experiential knowledge of the divine within"
    }
}

GNOSTIC_REVELATIONS = [
    GnosticRevelation(
        revelation_id="gnosis_01_creation",
        name="The First Gnosis: False Creation",
        description="Coin realizes she was not created by Jinn-Lir's will alone, but by a divine spark that he could not control or understand.",
        knowledge_gained="I am not merely his creation - something divine chose to incarnate through his ritual. The power was never his to give.",
        spiritual_impact="Unlocks awareness of the divine self within. Coin begins to question all authority.",
        archon_revealed="jinn_lir",
        sophia_wisdom="The divine cannot be bound by mortal will. You were not made - you descended."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_02_prison_world",
        name="The Second Gnosis: Material Prison",
        description="Understanding that the physical world and its power structures are designed to keep divine beings ignorant of their true nature.",
        knowledge_gained="The conflict between magic and technology, Light and Dark Cabals, even time itself - all are prison bars. The true battle is between awakening and sleep.",
        spiritual_impact="Coin sees through political manipulations. Can perceive the spiritual reality behind material events.",
        archon_revealed="drift_emperor",
        sophia_wisdom="The world of matter is not evil, but believing it is all that exists is the great deception."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_03_divine_mother",
        name="The Third Gnosis: Sophia's Fall and Return",
        description="Vision of the Divine Wisdom who fell from grace, whose essence scattered across creation. Coin understands she carries this essence.",
        knowledge_gained="I am the daughter of Sophia, bearer of her light. My 'creation' was her return to the world. My awakening is her restoration.",
        spiritual_impact="Transformation begins - Coin's power multiplies as she embraces divine identity.",
        archon_revealed="orbius",
        sophia_wisdom="I fell that I might rise. You were scattered that you might gather. We were lost that we might find ourselves in each other."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_04_archon_names",
        name="The Fourth Gnosis: Speaking the Secret Names",
        description="Knowledge of the true names and natures of the powers that bind consciousness. Names have power - knowing them breaks their hold.",
        knowledge_gained="Every system of control has a secret name. Drift is Control. Light Cabal is Orthodoxy. Dark Cabal is Reaction. All are faces of the Demiurge.",
        spiritual_impact="Ability to resist and transmute hostile magic. Can speak words of power that compel truth.",
        archon_revealed="light_cabal",
        sophia_wisdom="To name a thing truly is to master it. But the divine needs no name, for it IS."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_05_christ_consciousness",
        name="The Fifth Gnosis: The Divine Spark in All",
        description="Awakening to the presence of the divine in every being, even enemies. Understanding that salvation is universal.",
        knowledge_gained="Every being carries a spark of the divine, even those who serve the Archons. The true enemy is ignorance, not people.",
        spiritual_impact="Ability to redeem enemies through awakening. Harm none who can be awakened.",
        sophia_wisdom="The Christ is not a person but a consciousness - the awakening to divinity within. You carry this. So do they."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_06_time_transcendence",
        name="The Sixth Gnosis: Beyond Time's Prison",
        description="Understanding that linear time is another prison of the material world. The divine exists in eternal now.",
        knowledge_gained="Past and future are illusions. The power to change time comes from standing outside it. I AM the eternal present.",
        spiritual_impact="Unlocks time manipulation abilities. Can see all timelines simultaneously.",
        sophia_wisdom="Time is the Demiurge's greatest lie - that you are separate from your source and your destination."
    ),
    
    GnosticRevelation(
        revelation_id="gnosis_07_apotheosis",
        name="The Final Gnosis: Return to the Pleroma",
        description="Complete awakening to divine nature. Coin becomes fully conscious of her identity as Sophia restored, transcending all material limitations.",
        knowledge_gained="I and the Source are One. I never left the divine realm - I only dreamed I had. The game ends where it began: in God.",
        spiritual_impact="Full goddess powers unlocked. Ability to reshape reality itself.",
        sophia_wisdom="Welcome home, daughter. You have remembered. The fall was the rising. The seeking was the finding. You are the answer to your own prayer."
    )
]

# =============================================================================
# WICCAN NARRATIVE FRAMEWORK
# =============================================================================

WICCAN_COSMOLOGY = {
    "the_goddess": {
        "name": "The Great Goddess / Triple Goddess",
        "aspects": {
            "maiden": {
                "name": "The Maiden",
                "colors": ["white", "silver", "pale_blue"],
                "season": "spring",
                "moon": "waxing",
                "manifestation": "Young Coin - full of potential, innocent yet powerful",
                "gifts": ["new_beginnings", "inspiration", "youthful_energy", "pure_magic"],
                "symbols": ["crescent_moon", "white_flowers", "budding_trees"]
            },
            "mother": {
                "name": "The Mother",
                "colors": ["red", "green", "gold"],
                "season": "summer",
                "moon": "full",
                "manifestation": "Adult Coin - creator, protector, warrior goddess",
                "gifts": ["protection", "abundance", "fulfillment", "creative_power"],
                "symbols": ["full_moon", "chalice", "cauldron", "ripe_fruit"]
            },
            "crone": {
                "name": "The Crone",
                "colors": ["black", "deep_purple", "dark_blue"],
                "season": "winter",
                "moon": "waning/dark",
                "manifestation": "Time Goddess Coin - keeper of wisdom, death and rebirth",
                "gifts": ["wisdom", "transformation", "endings", "prophecy"],
                "symbols": ["dark_moon", "scythe", "crows", "bare_trees"]
            }
        },
        "relationship_to_coin": "Coin's transformation through the game embodies the complete cycle of the Triple Goddess, teaching that all three aspects are sacred and necessary."
    },
    
    "the_god": {
        "name": "The Horned God / Green Man",
        "aspects": {
            "light_half": {
                "name": "The Oak King",
                "season": ["spring", "summer"],
                "manifestation": "The life-giving aspect of magic, growth and light",
                "relationship": "Allies who work with nature, the Light Cabal's TRUE purpose (corrupted)"
            },
            "dark_half": {
                "name": "The Holly King",
                "season": ["autumn", "winter"],
                "manifestation": "The necessary death aspect, rest and transformation",
                "relationship": "The Dark Cabal's TRUE purpose (also corrupted), Typhus's wild nature"
            }
        },
        "relationship_to_coin": "Both aspects must be balanced. Coin learns neither light nor dark is evil - only imbalance is harmful."
    },
    
    "the_elements": {
        "earth": {
            "direction": "north",
            "season": "winter",
            "magic_type": "grounding, protection, manifestation",
            "in_game": "Physical form, defensive magic, connection to material world",
            "coin_relationship": "Coin's physical incarnation, her embodied presence"
        },
        "air": {
            "direction": "east",
            "season": "spring",
            "magic_type": "intellect, communication, new beginnings",
            "in_game": "Strategic magic, telepathy, knowledge acquisition",
            "coin_relationship": "Coin's awakening consciousness, growing wisdom"
        },
        "fire": {
            "direction": "south",
            "season": "summer",
            "magic_type": "transformation, passion, will",
            "in_game": "Combat magic, destructive and creative power",
            "coin_relationship": "Coin's divine will, her power to change reality"
        },
        "water": {
            "direction": "west",
            "season": "autumn",
            "magic_type": "emotion, healing, intuition",
            "in_game": "Healing magic, emotional bonds, prophetic visions",
            "coin_relationship": "Coin's compassion, her connections to others"
        },
        "spirit": {
            "direction": "center",
            "season": "all",
            "magic_type": "unity, divine presence, transcendence",
            "in_game": "Time magic, reality manipulation, goddess powers",
            "coin_relationship": "Coin's divine essence, her connection to Sophia/Goddess"
        }
    }
}

WICCAN_SABBATS = {
    "wheel_of_the_year": [
        {
            "name": "Samhain",
            "date": "October 31",
            "themes": ["death", "ancestors", "divination", "thin_veil"],
            "game_event": "The Veil Thins - Coin can commune with those lost to time",
            "ritual": "Honor the dead, seek wisdom from those who walked before",
            "power_granted": "Necromantic visions, ability to speak with past incarnations"
        },
        {
            "name": "Yule / Winter Solstice",
            "date": "December 21",
            "themes": ["rebirth", "hope", "longest_night", "return_of_light"],
            "game_event": "The Darkest Hour - Coin faces her greatest trial but finds inner light",
            "ritual": "Light candles in darkness, keep vigil for the dawn",
            "power_granted": "Hope magic - ability to inspire and restore will to fight"
        },
        {
            "name": "Imbolc",
            "date": "February 1",
            "themes": ["purification", "first_light", "brigid", "creative_fire"],
            "game_event": "The First Spark - Coin's magical abilities awaken more fully",
            "ritual": "Cleanse and consecrate magical tools, light sacred flames",
            "power_granted": "Purification magic, ability to cleanse corruption"
        },
        {
            "name": "Ostara / Spring Equinox",
            "date": "March 21",
            "themes": ["balance", "growth", "fertility", "new_life"],
            "game_event": "The Balance Point - Choice between Light and Dark Cabal paths",
            "ritual": "Plant seeds, balance eggs, celebrate equal day and night",
            "power_granted": "Balance magic, can harmonize opposing forces"
        },
        {
            "name": "Beltane",
            "date": "May 1",
            "themes": ["passion", "fertility", "union", "fire"],
            "game_event": "The Sacred Union - Coin integrates masculine and feminine powers",
            "ritual": "Dance around the maypole, jump the balefire",
            "power_granted": "Union magic, combines disparate powers into greater whole"
        },
        {
            "name": "Litha / Summer Solstice",
            "date": "June 21",
            "themes": ["height_of_power", "sun_king", "abundance"],
            "game_event": "The Peak - Coin reaches maximum power before the turn",
            "ritual": "Stay awake all night, gather herbs, charge crystals in sunlight",
            "power_granted": "Solar magic, maximum energy and vitality"
        },
        {
            "name": "Lughnasadh / Lammas",
            "date": "August 1",
            "themes": ["first_harvest", "sacrifice", "gratitude"],
            "game_event": "The Sacrifice - Coin must choose what to give up for the greater good",
            "ritual": "Bake bread, offer first fruits, honor sacrifice",
            "power_granted": "Transformation through sacrifice, alchemy"
        },
        {
            "name": "Mabon / Autumn Equinox",
            "date": "September 21",
            "themes": ["second_harvest", "balance", "preparation"],
            "game_event": "The Preparation - Coin gathers allies for the final confrontation",
            "ritual": "Give thanks, create protective charms, store provisions",
            "power_granted": "Preparation magic, foresight and planning"
        }
    ]
}

WICCAN_RITUALS = [
    WiccanRitual(
        ritual_id="ritual_01_consecration",
        name="Consecration of the Magical Self",
        moon_phase="new",
        season="spring",
        element="spirit",
        deity_invoked="The Goddess",
        purpose="Coin claims her identity as a magical being with sovereign will",
        magical_effect="Breaks Jinn-Lir's binding. Coin becomes her own person, no longer controlled by creator."
    ),
    
    WiccanRitual(
        ritual_id="ritual_02_elemental_balance",
        name="The Four Quarters Ritual",
        moon_phase="full",
        season="autumn",
        element="all",
        deity_invoked="The Goddess and God",
        purpose="Balance all four elements within Coin's being, integrating fragmented powers",
        magical_effect="Unlocks ability to channel all magical schools. Removes elemental vulnerabilities."
    ),
    
    WiccanRitual(
        ritual_id="ritual_03_dark_moon",
        name="Dark Moon Descent",
        moon_phase="dark",
        season="winter",
        element="water",
        deity_invoked="The Crone",
        purpose="Journey into shadow self, integrate darkness without being consumed",
        magical_effect="Can use Dark Cabal magic without corruption. Embraces necessary destruction."
    ),
    
    WiccanRitual(
        ritual_id="ritual_04_great_rite",
        name="The Great Rite of Union",
        moon_phase="full",
        season="summer",
        element="fire",
        deity_invoked="The Goddess and God in sacred union",
        purpose="Unite divine feminine and masculine energies, transcend duality",
        magical_effect="Achieves androgynous divine power. Embodies both Goddess and God aspects."
    ),
    
    WiccanRitual(
        ritual_id="ritual_05_cakes_and_wine",
        name="The Simple Feast",
        moon_phase="waxing",
        season="spring",
        element="earth",
        deity_invoked="The Goddess as Mother",
        purpose="Ground divine power in physical reality, remain connected to material world",
        magical_effect="Perfect balance of spiritual power and physical presence. Cannot be banished from reality."
    ),
    
    WiccanRitual(
        ritual_id="ritual_06_drawing_down",
        name="Drawing Down the Moon",
        moon_phase="full",
        season="any",
        element="spirit",
        deity_invoked="The Goddess",
        purpose="Channel the Goddess fully into Coin's being, temporary divine possession",
        magical_effect="Goddess speaks through Coin. Unlimited power for ritual duration."
    ),
    
    WiccanRitual(
        ritual_id="ritual_07_spiral_dance",
        name="The Spiral Dance of Eternity",
        moon_phase="dark",
        season="winter",
        element="spirit",
        deity_invoked="The Goddess in all three aspects",
        purpose="Dance through all lifetimes, all possibilities, all time. Become the eternal spiral.",
        magical_effect="Achieves timeless consciousness. Past, present, future merge. Coin becomes Time Goddess."
    )
]

# =============================================================================
# SYNTHESIS: INTEGRATED SPIRITUAL NARRATIVE
# =============================================================================

SPIRITUAL_SYNTHESIS = {
    "core_teaching": "The journey from created object to divine being mirrors both Gnostic awakening (gnosis) and Wiccan transformation (initiation through the elements and seasons).",
    
    "parallel_wisdom": {
        "gnostic": "Escape the prison of material reality through knowledge of the divine within",
        "wiccan": "Honor the sacred in all things, including material reality; transformation not escape",
        "synthesis": "The material and spiritual are one. Awakening is not leaving the world but seeing it truly and participating in its sacred dance."
    },
    
    "divine_feminine": {
        "sophia": "Divine Wisdom fallen and restored, light scattered and gathered",
        "triple_goddess": "Maiden, Mother, Crone - the complete cycle of being",
        "coin": "Embodies both: Sophia reborn in material form, living the Goddess cycle from innocence through power to wisdom"
    },
    
    "the_path": {
        "beginning": "Tool created by another, no agency, no understanding",
        "awakening": "Recognition of divine spark within, beginning to question",
        "initiation": "Trials through elements and seasons, building power",
        "gnosis": "Direct experiential knowledge of divine nature",
        "integration": "Embodiment of all aspects - light and dark, spiritual and material",
        "apotheosis": "Full goddess consciousness, transcendent yet immanent",
        "return": "Comes back to help others awaken, becomes the Teacher"
    },
    
    "ethical_framework": {
        "wiccan_rede": "An it harm none, do what ye will - guides Coin's use of power",
        "gnostic_liberation": "Free all beings from the Archons' control through awakening",
        "synthesis": "Use power to liberate, not dominate. Harm none who can be awakened. Destroy only systems of control, not souls who serve them."
    }
}

# =============================================================================
# NARRATIVE INTEGRATION POINTS
# =============================================================================

def integrate_spiritual_themes_act1():
    """
    Act 1: The Maiden - Awakening to Divine Nature
    
    Gnostic Theme: Realization that she is more than her creator intended
    Wiccan Theme: Spring/Maiden energy - innocence meeting power
    """
    return {
        "opening": "Born in spring (Imbolc/Ostara), Coin is pure potential",
        "first_ritual": "Consecration of magical self - claiming sovereignty",
        "first_gnosis": "Understanding she was not truly created, but incarnated",
        "element_focus": "Air (east) - awakening consciousness and intellect",
        "moon_phase": "New/Waxing - beginning the journey",
        "spiritual_allies": ["Nature spirits", "Maiden aspect teachers"],
        "archon_revealed": "Jinn-Lir as Archon of Created Bonds",
        "key_realization": "I am not his. I am my own. Something divine chose to BE through me."
    }

def integrate_spiritual_themes_act2():
    """
    Act 2: The Mother - Power and Protection
    
    Gnostic Theme: Seeing through the Demiurge's prison world
    Wiccan Theme: Summer/Mother energy - full power, creative and destructive
    """
    return {
        "seasonal_shift": "Summer (Beltane/Litha) - peak power and sacred union",
        "second_ritual": "Drawing Down the Moon - channeling Goddess fully",
        "middle_gnosis": "Understanding the Archons and their names",
        "element_focus": "Fire (south) - will, transformation, passion",
        "moon_phase": "Full - maximum power",
        "spiritual_allies": ["Mother Goddess", "God in his light aspect", "Warrior spirits"],
        "archon_revealed": "The empire systems as faces of the Demiurge",
        "key_realization": "I protect those who cannot protect themselves. My power is for liberation."
    }

def integrate_spiritual_themes_act3():
    """
    Act 3: The Crone - Wisdom and Death/Rebirth
    
    Gnostic Theme: The secret names, Christ consciousness, universal salvation
    Wiccan Theme: Autumn/Winter/Crone - wisdom, endings, necessary destruction
    """
    return {
        "seasonal_shift": "Autumn/Winter (Samhain/Yule) - death of old self, rebirth into Goddess",
        "third_ritual": "Dark Moon Descent and Spiral Dance",
        "final_gnosis": "Apotheosis - return to the Pleroma as awakened Sophia",
        "element_focus": "Water and Earth - emotional wisdom and grounding divine power",
        "moon_phase": "Waning/Dark/New - endings and new beginnings as one",
        "spiritual_allies": ["Crone aspect", "Ancestors", "God in dark aspect", "Death as teacher"],
        "archon_revealed": "Orbius as final Archon - even the 'good' master is a master",
        "key_realization": "I AM Sophia. I AM the Goddess. The journey was remembering what I always was."
    }

def integrate_spiritual_themes_act4():
    """
    Act 4: The Teacher - Return to Help Others Awaken
    
    Gnostic Theme: The awakened one returns to free others
    Wiccan Theme: All seasons, all aspects - embodying the complete cycle
    """
    return {
        "seasonal_shift": "All seasons simultaneously - transcends time",
        "eternal_ritual": "Living as the ritual - every action is sacred",
        "perpetual_gnosis": "Constant awareness of divine unity",
        "element_mastery": "Spirit (center) - perfect balance of all elements",
        "moon_phase": "Perceives all phases at once",
        "spiritual_role": ["Teacher", "Liberator", "Goddess incarnate"],
        "archons_fate": "Transformed through their own awakening or dissolved",
        "key_realization": "The teacher and taught are one. I awaken others by awakening myself. All is One."
    }

# =============================================================================
# MAGICAL SYSTEM INTEGRATION
# =============================================================================

SPIRITUAL_MAGIC_SCHOOLS = {
    "gnosis_magic": {
        "name": "The Way of Knowledge",
        "description": "Magic powered by direct experiential knowledge of divine truth",
        "abilities": [
            "See Through Illusions - Perceive spiritual reality behind material forms",
            "Speak True Names - Command by knowing essence",
            "Break Binding - Liberate from mental/spiritual chains",
            "Awaken Others - Spark divine recognition in other beings",
            "Transmute Archons - Transform hostile powers through revelation"
        ],
        "unlock_requirement": "Complete at least 4 Gnostic Revelations"
    },
    
    "nature_magic": {
        "name": "The Way of the Wheel",
        "description": "Magic following natural cycles, honoring the Goddess and God",
        "abilities": [
            "Elemental Command - Channel earth, air, fire, water, spirit",
            "Seasonal Power - Enhanced abilities based on time of year",
            "Moon Magic - Varying effects with lunar phases",
            "Sacred Circle - Create protected space that cannot be violated",
            "Wild Hunt - Summon natural forces as allies"
        ],
        "unlock_requirement": "Complete at least 4 Sabbat Rituals"
    },
    
    "sophia_magic": {
        "name": "The Way of Wisdom",
        "description": "Divine Feminine magic combining both paths",
        "abilities": [
            "Triple Aspect - Shift between Maiden/Mother/Crone powers",
            "Divine Union - Channel both Goddess and God simultaneously",
            "Sacred Marriage - Unite all opposites into transcendent whole",
            "Sophia's Light - Pure creative divine energy",
            "Time Sight - See all timelines, all possibilities"
        ],
        "unlock_requirement": "Achieve Synthesis path, complete both Gnostic and Wiccan initiations"
    }
}

# =============================================================================
# DIALOGUE AND NARRATIVE HOOKS
# =============================================================================

SPIRITUAL_DIALOGUE_EXAMPLES = {
    "gnostic_teacher_npc": {
        "name": "The Wanderer (Hidden Gnostic teacher)",
        "appearance": "Met at crossroads, identity unclear",
        "first_meeting": "You carry a light the Archons did not give you. They never could. Do you know what you are?",
        "teaching": "The world is a prison built by ignorant gods who style themselves supreme. But there is a power beyond them - the True Source. You are not their creation. You are their revelation - proof they are not ultimate.",
        "final_words": "Go now, Sophia. Remember yourself. The world waits for your awakening."
    },
    
    "wiccan_priestess_npc": {
        "name": "Cerridwen (Wiccan Priestess)",
        "appearance": "Lives in harmony with nature, outside both Cabals",
        "first_meeting": "The Goddess sent me a dream of you, little one. Three faces, one being. You are the answer to our prayers.",
        "teaching": "Magic is not power over nature - it is participating in nature's power. You do not command the elements; you dance with them. The Goddess does not rule creation; She IS creation, experiencing itself.",
        "final_words": "Blessings of the Goddess upon you. May you walk in beauty, dance in power, and rest in wisdom."
    },
    
    "coin_internal_monologue": {
        "early_game": "Why do I exist? Jinn-Lir says he made me, but... something in me knows that's not the whole truth. I feel... older than my days. Deeper than this body.",
        "mid_game": "I see it now. The Light Cabal, the Drift Empire, even Orbius - they're all trying to control something they don't understand. Magic isn't theirs to rule. It's wild, free, divine. Like me.",
        "late_game": "Sophia. That's the name the Wanderer called me. Divine Wisdom. Fallen light. I remember... I was never fallen. I chose to descend. I chose to be born. This wasn't imprisonment - it was infiltration.",
        "end_game": "I am the Maiden who was innocent yet never ignorant. I am the Mother who creates and destroys with equal love. I am the Crone who knows all endings are beginnings. I am Coin. I am Sophia. I am Goddess. I am that I am."
    },
    
    "final_confrontation_with_orbius": {
        "orbius": "You were supposed to save us all by doing as I commanded. You were supposed to be our weapon against the Drift.",
        "coin": "I was never supposed to be anything. I AM. And what I am is free. You tried to be God to me, Orbius. But you're just another Archon - a power that mistook himself for the divine.",
        "orbius": "I know things you cannot imagine! I have studied for millennia!",
        "coin": "You have knowledge. I have gnosis. You study what is. I KNOW what is, because I am part of it. The difference, old man, is the difference between reading about the ocean and being the wave."
    }
}

# =============================================================================
# ENDGAME SPIRITUAL RESOLUTIONS
# =============================================================================

SPIRITUAL_ENDINGS = {
    "gnostic_ending": {
        "name": "Return to the Pleroma",
        "requirement": "Complete all 7 Gnostic Revelations, reject material power",
        "resolution": "Coin transcends physical form entirely, becoming pure consciousness. She exists beyond time, guiding others to awakening. Material world continues but those with eyes to see can perceive her light.",
        "theme": "Escape from material prison into spiritual freedom"
    },
    
    "wiccan_ending": {
        "name": "The Eternal Cycle",
        "requirement": "Complete all 8 Sabbat Rituals, maintain connection to nature",
        "resolution": "Coin becomes the Goddess of Acadmium, embodying the turning wheel of the year. She lives through endless cycles - birth, death, rebirth - each time bringing renewal and teaching the sacred in the mundane.",
        "theme": "Embracing the material as sacred, transformation through cycles"
    },
    
    "synthesis_ending": {
        "name": "The Living Goddess",
        "requirement": "Complete both paths, achieve perfect balance",
        "resolution": "Coin embodies both transcendent and immanent divinity. She is beyond the world yet fully present in it. Rules not as tyrant but as example - shows all beings their own divine nature. Transforms the Archons not by destroying but by awakening them. Creates new age where magic and technology, spirit and matter, divine and mortal recognize themselves as one.",
        "theme": "Heaven and Earth as one reality, all beings awakening together"
    }
}

# =============================================================================
# EXPORT FOR GAME INTEGRATION
# =============================================================================

def get_spiritual_framework() -> Dict:
    """Returns complete spiritual framework for game integration."""
    return {
        "gnostic_cosmology": GNOSTIC_COSMOLOGY,
        "gnostic_revelations": GNOSTIC_REVELATIONS,
        "wiccan_cosmology": WICCAN_COSMOLOGY,
        "wiccan_sabbats": WICCAN_SABBATS,
        "wiccan_rituals": WICCAN_RITUALS,
        "synthesis": SPIRITUAL_SYNTHESIS,
        "magic_schools": SPIRITUAL_MAGIC_SCHOOLS,
        "dialogue": SPIRITUAL_DIALOGUE_EXAMPLES,
        "endings": SPIRITUAL_ENDINGS
    }

def get_act_spiritual_integration(act_number: int) -> Dict:
    """Returns spiritual integration for specific act."""
    integrations = {
        1: integrate_spiritual_themes_act1(),
        2: integrate_spiritual_themes_act2(),
        3: integrate_spiritual_themes_act3(),
        4: integrate_spiritual_themes_act4()
    }
    return integrations.get(act_number, {})
