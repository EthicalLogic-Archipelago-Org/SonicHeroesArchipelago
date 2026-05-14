"""

"""
from typing import Callable

from ..constants.char_ability import Team
from ..constants.stage import Stage
from .parser_functions import get_func_str



PARSER_TRICK_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "BadnikBounce": lambda team, stage: get_func_str(func_name="can_badnik_bounce_rule", params={}),
    "CollisAbuse": lambda team, stage: get_func_str(func_name="can_collis_abuse_rule", params={}),
    "HoverFrame": lambda team, stage: get_func_str(func_name="can_hover_frame_rule", params={"includes_tornado": False}),
    "Tornado0Hover": lambda team, stage: get_func_str(func_name="can_tornado_hover_rule", params={"team": team, "stage": stage, "level": 0}),
    "Parkour": lambda team, stage: get_func_str(func_name="can_parkour_rule", params={}),
    "FlyDepleteBoost": lambda team, stage: get_func_str(func_name="can_fly_deplete_boost_rule", params={"team": team, "stage": stage}),
    "FlyGroundBounce": lambda team, stage: get_func_str(func_name="can_fly_ground_bounce_rule", params={"team": team, "stage": stage, "needs_jump": True}),
    "FlyGroundBounceNoJump": lambda team, stage: get_func_str(func_name="can_fly_ground_bounce_rule", params={"team": team, "stage": stage, "needs_jump": False}),
}