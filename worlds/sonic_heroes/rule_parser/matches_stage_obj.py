"""

"""
from typing import Callable

from worlds.sonic_heroes.constants.stage_objs import StageObj

from .parser_functions import get_func_str
from ..constants.char_ability import Team, Formation
from ..constants.stage import Stage


PARSER_STAGE_OBJ_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "BobsledAny": lambda team, stage: get_func_str(func_name="has_bobsled_rule", params={"team": team, "stage": stage}),

    "SingleSpring": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.SINGLE_SPRING}),

    "TripleSpring": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.TRIPLE_SPRING}),

    "DashRamp": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.DASH_RAMP}),

    "DashPanel": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.DASH_PANEL}),

    "DashRing": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.DASH_RING}),

    "RainbowHoop": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.RAINBOW_HOOPS}),

    "Cannon": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.CANNON}),

    "GoalRing": lambda team, stage: get_func_str(func_name="has_stage_obj_rule", params={"stage_obj": StageObj.GOAL_RING}),

    "RuinsNoTrigger": lambda team, stage: get_func_str(func_name="has_moving_ruins_rule", params={"needs_trigger": False}),

    "RuinsTrigger": lambda team, stage: get_func_str(func_name="has_moving_ruins_rule", params={"needs_trigger": True}),
}



