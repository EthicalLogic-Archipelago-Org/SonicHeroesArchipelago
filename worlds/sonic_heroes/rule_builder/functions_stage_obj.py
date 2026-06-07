"""
Helper Functions for custom rule builder rules related to tricks
"""
from rule_builder.rules import Rule, Has, True_


from ..constants.char_ability import Team
from ..constants.items_events import BOBSLED_ITEM_NAME
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj
from ..helper_functions import get_stage_obj_item_name
from ..world_base import SonicHeroesWorldBase


def has_stage_obj_rule(team: Team, stage_obj: StageObj) -> Rule[SonicHeroesWorldBase]:
    # print(f"RULE IS CHECKING FOR item: {get_stage_obj_item_name(team=team, stage_obj=stage_obj)}")
    return Has(item_name=get_stage_obj_item_name(team=team, stage_obj=stage_obj))


def has_bobsled_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return Has(item_name=BOBSLED_ITEM_NAME)

def can_break_key_cage(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return True_[SonicHeroesWorldBase]()


def has_moving_ruins_rule(team: Team, needs_trigger: bool) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    if needs_trigger:
        rule &= has_stage_obj_rule(team=team, stage_obj=StageObj.TRIGGER_RUINS)
    rule &= has_stage_obj_rule(team=team, stage_obj=StageObj.MOVING_RUIN_PLATFORM)
    return rule






