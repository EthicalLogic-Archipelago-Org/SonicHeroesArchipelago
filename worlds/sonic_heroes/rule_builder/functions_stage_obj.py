"""
Helper Functions for custom rule builder rules related to tricks
"""
from rule_builder.rules import Rule, Has

from ..constants.stage_objs import StageObj
from ..helper_functions import get_stage_obj_item_name
from ..world_base import SonicHeroesWorldBase


def has_stage_obj_rule(stage_obj: StageObj) -> Rule[SonicHeroesWorldBase]:
    return Has(item_name=get_stage_obj_item_name(stage_obj=stage_obj))