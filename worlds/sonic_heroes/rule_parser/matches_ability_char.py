"""

"""
from typing import Callable

from .parser_functions import get_func_str
from ..constants.char_ability import Team, Formation
from ..constants.stage import Stage



PARSER_FORMATION_CHARACTER_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "SpeedChar": lambda team, stage: get_func_str(func_name="has_formation_char_rule", params={"team": team, "formation": Formation.SPEED}),
    "PowerChar": lambda team, stage: get_func_str(func_name="has_formation_char_rule", params={"team": team, "formation": Formation.POWER}),
    "FlyingChar": lambda team, stage: get_func_str(func_name="has_formation_char_rule", params={"team": team, "formation": Formation.FLYING}),


    "FullFlyingStackwithTallChar": lambda team, stage: get_func_str(func_name="has_full_flying_stack_with_tall_char", params={"team": team}),
}


PARSER_ABILITY_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "BreakThings": lambda team, stage: get_func_str(func_name="can_break_things_rule", params={"team": team, "stage": stage}),
    "ComboHeight": lambda team, stage: get_func_str(func_name="can_combo_height_rule", params={"team": team, "stage": stage}),
    "Jump": lambda team, stage: get_func_str(func_name="can_jump_rule", params={"team": team, "stage": stage}),

    # Speed
    # AmyHammerHover
    # Homing
    "Homing0": lambda team, stage: get_func_str(func_name="can_homing_attack_rule", params={"team": team, "stage": stage, "level": 0}),
    "Homing1": lambda team, stage: get_func_str(func_name="can_homing_attack_rule", params={"team": team, "stage": stage, "level": 1}),
    "Homing2": lambda team, stage: get_func_str(func_name="can_homing_attack_rule", params={"team": team, "stage": stage, "level": 2}),
    "Homing3": lambda team, stage: get_func_str(func_name="can_homing_attack_rule", params={"team": team, "stage": stage, "level": 3}),
    # Tornado
    "Tornado0": lambda team, stage: get_func_str(func_name="can_tornado_rule", params={"team": team, "stage": stage, "level": 0}),
    "Tornado1": lambda team, stage: get_func_str(func_name="can_tornado_rule", params={"team": team, "stage": stage, "level": 1}),
    "Tornado2": lambda team, stage: get_func_str(func_name="can_tornado_rule", params={"team": team, "stage": stage, "level": 2}),
    "Tornado3": lambda team, stage: get_func_str(func_name="can_tornado_rule", params={"team": team, "stage": stage, "level": 3}),
    # Rocket Accel
    "AccelHalf": lambda team, stage: get_func_str(func_name="can_rocket_accel_rule", params={"team": team, "stage": stage, "num_other_chars": 1}),
    "AccelFull": lambda team, stage: get_func_str(func_name="can_rocket_accel_rule", params={"team": team, "stage": stage, "num_other_chars": 2}),
    # Light Dash
    # Triangle Jump
    # Light Attack
    # Invis
    # Shuriken

    # Flying
    # Dummy
    # Cheese
    # Flower
    # Thunder
    "Thundershoot0": lambda team, stage: get_func_str(func_name="can_thundershoot_rule", params={"team": team, "stage": stage, "level": 0}),
    # Flight
    "FlyAny": lambda team, stage: get_func_str(func_name="can_flight_rule", params={"team": team, "stage": stage, "num_other_chars": 0}),
    "FlyOneChar": lambda team, stage: get_func_str(func_name="can_flight_rule", params={"team": team, "stage": stage, "num_other_chars": 1}),
    "FlyFull": lambda team, stage: get_func_str(func_name="can_flight_rule", params={"team": team, "stage": stage, "num_other_chars": 2}),

    # Power
    # Power Attack
    "PowerAttack": lambda team, stage: get_func_str(func_name="can_power_attack_rule", params={"team": team, "stage": stage, "level": 0}),
    # Belly Flop
    # Fire Dunk
    # Ultimate Fire Dunk
    # Glide
    "Glide": lambda team, stage: get_func_str(func_name="can_glide_rule", params={"team": team, "stage": stage}),
    # Combo Finisher
}




