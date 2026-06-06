"""
Constants related to Characters, Abilities, and Teams
"""
import enum

from .items_events import PLAYABLE
from ..world_base import SonicHeroesWorldBase


class Team(enum.StrEnum):
    ANY_TEAM = "Any Team"
    """Used for either All Teams or None"""
    SONIC = "Sonic"
    DARK = "Dark"
    ROSE = "Rose"
    CHAOTIX = "Chaotix"
    SUPER_HARD_MODE = "Super Hard Mode"



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
    JUMP = ("Jump", AbilityQualities.NONE, [Formation.SPEED, Formation.FLYING, Formation.POWER])
    AMY_HAMMER_HOVER = ("Amy Hammer Hover", AbilityQualities.NONE, [Formation.SPEED])
    HOMING_ATTACK = ("Homing Attack", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.SPEED])
    TORNADO = ("Tornado", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.SPEED])
    ROCKET_ACCEL = ("Rocket Accel", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.SPEED])
    LIGHT_DASH = ("Light Dash", AbilityQualities.LEADER_FORMATION, [Formation.SPEED])
    TRIANGLE_JUMP = ("Triangle Jump", AbilityQualities.LEADER_FORMATION, [Formation.SPEED])
    LIGHT_ATTACK = ("Light Attack", AbilityQualities.LEADER_FORMATION, [Formation.SPEED])
    INVISIBILITY = ("Invisibility", AbilityQualities.LEADER_FORMATION, [Formation.SPEED])
    SHURIKEN = ("Shuriken", AbilityQualities.LEADER_FORMATION, [Formation.SPEED])
    DUMMY_RINGS = ("Dummy Rings", AbilityQualities.LEADER_FORMATION, [Formation.FLYING])
    CHEESE_CANNON = ("Cheese Cannon", AbilityQualities.LEADER_FORMATION, [Formation.FLYING])
    FLOWER_STING = ("Flower Sting", AbilityQualities.LEADER_FORMATION, [Formation.FLYING])
    THUNDER_SHOOT = ("Thunder Shoot", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.FLYING])
    FLIGHT = ("Flight", AbilityQualities.LEADER_FORMATION, [Formation.FLYING])
    POWER_ATTACK = ("Power Attack", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER])
    BELLY_FLOP = ("Belly Flop", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER])
    FIRE_DUNK = ("Fire Dunk", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.POWER])
    ULTIMATE_FIRE_DUNK = ("Ultimate Fire Dunk", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL | AbilityQualities.NUM_OTHER_CHARS, [Formation.POWER])
    GLIDE = ("Glide", AbilityQualities.LEADER_FORMATION, [Formation.POWER])
    COMBO_FINISHER = ("Combo Finisher", AbilityQualities.LEADER_FORMATION | AbilityQualities.LEADER_LEVEL, [Formation.POWER])

    def __init__(self, ability_name: str, ability_qual: AbilityQualities, valid_formations: list[Formation]) -> None:
        self.ability_name: str = ability_name
        self.ability_qual: AbilityQualities = ability_qual
        self.valid_formations: list[Formation] = valid_formations



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










