"""
Constants related to Characters, Abilities, and Teams
"""
import enum

from BaseClasses import ItemClassification

from .items_events import PLAYABLE
from ..world_base import SonicHeroesWorldBase


class Team(enum.StrEnum):
    ANY_TEAM = "Any Team"
    """Used for either All Teams or None"""
    SONIC = "Sonic"
    DARK = "Dark"
    ROSE = "Rose"
    CHAOTIX = "Chaotix"
    SUPER_HARD_MODE = "SuperHardMode"



class Formation(enum.StrEnum):
    SPEED = "Speed"
    FLYING = "Flying"
    POWER = "Power"


class AbilityQualities(enum.IntFlag):
    """
    What other vars are needed when logically using this ability?
    For example, Thundershoot cares about leader formation, leader level and number of other characters.
    """
    NONE = 0
    LEADER_FORMATION = enum.auto()
    LEADER_LEVEL = enum.auto()
    NUM_OTHER_CHARS = enum.auto()


class Ability(enum.Enum):
    JUMP = ("Jump", AbilityQualities.NONE, [Formation.SPEED, Formation.FLYING, Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    AMY_HAMMER_HOVER = ("Amy Hammer Hover", AbilityQualities.NONE, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    HOMING_ATTACK = ("Homing Attack", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    TORNADO = ("Tornado", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    ROCKET_ACCEL = ("Rocket Accel", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    LIGHT_DASH = ("Light Dash", AbilityQualities.LEADER_FORMATION, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    TRIANGLE_JUMP = ("Triangle Jump", AbilityQualities.LEADER_FORMATION, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    LIGHT_ATTACK = ("Light Attack", AbilityQualities.LEADER_FORMATION, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    INVISIBILITY = ("Invisibility", AbilityQualities.LEADER_FORMATION, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    SHURIKEN = ("Shuriken", AbilityQualities.LEADER_FORMATION, [Formation.SPEED], ItemClassification.progression | ItemClassification.useful)
    DUMMY_RINGS = ("Dummy Rings", AbilityQualities.LEADER_FORMATION, [Formation.FLYING], ItemClassification.progression | ItemClassification.useful)
    CHEESE_CANNON = ("Cheese Cannon", AbilityQualities.LEADER_FORMATION, [Formation.FLYING], ItemClassification.progression | ItemClassification.useful)
    FLOWER_STING = ("Flower Sting", AbilityQualities.LEADER_FORMATION, [Formation.FLYING], ItemClassification.progression | ItemClassification.useful)
    THUNDER_SHOOT = ("Thunder Shoot", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.FLYING], ItemClassification.progression | ItemClassification.useful)
    FLIGHT = ("Flight", AbilityQualities.LEADER_FORMATION, [Formation.FLYING], ItemClassification.progression | ItemClassification.useful)
    POWER_ATTACK = ("Power Attack", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    BELLY_FLOP = ("Belly Flop", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    FIRE_DUNK = ("Fire Dunk", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    ULTIMATE_FIRE_DUNK = ("Ultimate Fire Dunk", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    GLIDE = ("Glide", AbilityQualities.LEADER_FORMATION, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)
    COMBO_FINISHER = ("Combo Finisher", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER], ItemClassification.progression | ItemClassification.useful)

    def __init__(self, ability_name: str, ability_qual: AbilityQualities, valid_formations: list[Formation], classification: ItemClassification) -> None:
        self.ability_name: str = ability_name
        self.ability_qual: AbilityQualities = ability_qual
        self.valid_formations: list[Formation] = valid_formations
        self.classification: ItemClassification = classification



class Character(enum.Enum):
    SONIC = ("Sonic", Team.SONIC, Formation.SPEED, [Ability.HOMING_ATTACK, Ability.TORNADO, Ability.ROCKET_ACCEL, Ability.LIGHT_DASH, Ability.TRIANGLE_JUMP, Ability.LIGHT_ATTACK])
    TAILS = ("Tails", Team.SONIC, Formation.FLYING, [Ability.THUNDER_SHOOT, Ability.FLIGHT, Ability.DUMMY_RINGS])
    KNUCKLES = ("Knuckles", Team.SONIC, Formation.POWER, [Ability.POWER_ATTACK, Ability.FIRE_DUNK, Ability.GLIDE, Ability.COMBO_FINISHER])

    SHADOW = ("Shadow", Team.DARK, Formation.SPEED, [Ability.HOMING_ATTACK, Ability.TORNADO, Ability.ROCKET_ACCEL, Ability.LIGHT_DASH, Ability.TRIANGLE_JUMP])
    ROUGE = ("Rouge", Team.DARK, Formation.FLYING, [Ability.THUNDER_SHOOT, Ability.FLIGHT, Ability.DUMMY_RINGS])
    OMEGA = ("Omega", Team.DARK, Formation.POWER, [Ability.POWER_ATTACK, Ability.FIRE_DUNK, Ability.GLIDE, Ability.COMBO_FINISHER])

    AMY = ("Amy", Team.ROSE, Formation.SPEED, [Ability.AMY_HAMMER_HOVER, Ability.HOMING_ATTACK, Ability.TORNADO, Ability.ROCKET_ACCEL])
    CREAM = ("Cream", Team.ROSE, Formation.FLYING, [Ability.THUNDER_SHOOT, Ability.FLIGHT, Ability.CHEESE_CANNON])
    BIG = ("Big", Team.ROSE, Formation.POWER, [Ability.POWER_ATTACK, Ability.BELLY_FLOP, Ability.FIRE_DUNK, Ability.GLIDE, Ability.COMBO_FINISHER])

    ESPIO = ("Espio", Team.CHAOTIX, Formation.SPEED, [Ability.HOMING_ATTACK, Ability.TORNADO, Ability.ROCKET_ACCEL, Ability.TRIANGLE_JUMP, Ability.INVISIBILITY, Ability.SHURIKEN])
    CHARMY = ("Charmy", Team.CHAOTIX, Formation.FLYING, [Ability.THUNDER_SHOOT, Ability.FLIGHT, Ability.FLOWER_STING])
    VECTOR = ("Vector", Team.CHAOTIX, Formation.POWER, [Ability.POWER_ATTACK, Ability.BELLY_FLOP, Ability.FIRE_DUNK, Ability.GLIDE, Ability.COMBO_FINISHER])

    SUPER_HARD_MODE_SONIC = ("Super Hard Mode Sonic", Team.SONIC, Formation.SPEED, [Ability.HOMING_ATTACK, Ability.TORNADO, Ability.ROCKET_ACCEL, Ability.LIGHT_DASH, Ability.TRIANGLE_JUMP, Ability.LIGHT_ATTACK])
    SUPER_HARD_MODE_TAILS = ("Super Hard Mode Tails", Team.SONIC, Formation.FLYING, [Ability.THUNDER_SHOOT, Ability.FLIGHT, Ability.DUMMY_RINGS])
    SUPER_HARD_MODE_KNUCKLES = ("Super Hard Mode Knuckles", Team.SUPER_HARD_MODE, Formation.POWER, [Ability.POWER_ATTACK, Ability.FIRE_DUNK, Ability.GLIDE, Ability.COMBO_FINISHER])

    def __init__(self, char_name: str, team: Team, formation: Formation, abilities: list[Ability]) -> None:
        self.char_name: str = char_name
        self.default_team: Team = team
        self.formation: Formation = formation
        self.abilities: list[Ability] = abilities

    def get_abilities(self, world: SonicHeroesWorldBase) -> list[Ability]:
        return self.abilities

    def get_playable_item_name(self) -> str:
        return f"{PLAYABLE} {self.char_name}"

    def get_team(self, world: SonicHeroesWorldBase) -> Team:
        return self.default_team



ALL_ABILITIES: str = "All Abilities"





