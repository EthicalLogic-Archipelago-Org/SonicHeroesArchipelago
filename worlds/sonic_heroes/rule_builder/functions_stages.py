"""
Helper Functions for custom rule builder rules related to stages
"""

from rule_builder.rules import HasFromListUnique, Rule, True_


from .custom_rules import CanTeamBlast
from .functions_stage_obj import has_stage_obj_rule

from ..constants.char_ability import Team
from ..constants.items_events import ChaosEmerald
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj
from ..world_base import SonicHeroesWorldBase


def can_goal_rule() -> Rule[SonicHeroesWorldBase]:
    return CanTeamBlast(team=Team.DARK) & HasFromListUnique(*[emerald.value for emerald in ChaosEmerald], count=7) & has_stage_obj_rule(team=Team.DARK, stage_obj=StageObj.SINGLE_SPRING) & has_stage_obj_rule(team=Team.DARK, stage_obj=StageObj.TRIPLE_SPRING) & has_stage_obj_rule(team=Team.DARK, stage_obj=StageObj.GOAL_RING) & has_stage_obj_rule(team=Team.DARK, stage_obj=StageObj.MOVING_RUIN_PLATFORM)