"""
Helper Functions for custom rule builder rules related to stages
"""

from rule_builder.rules import HasFromListUnique, Rule, True_, False_
from worlds.sonic_heroes.rule_builder.functions_ability_char import can_team_blast_rule


from ..helper_functions import is_this_team_enabled
from .custom_rules import CanTeamBlast
from .functions_stage_obj import has_stage_obj_rule

from ..constants.char_ability import Team
from ..constants.items_events import ChaosEmerald
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj

from ..world_base import SonicHeroesWorldBase



def can_goal_rule(world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
    team_blast_rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    stage_objs_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()

    teams_list: list[Team] = [team for team in Team if is_this_team_enabled(world=world, team=team)]

    for team in teams_list:
        team_blast_rule &= CanTeamBlast(team=team)
        stage_objs_rule |= (has_stage_obj_rule(team=team, stage=Stage.SEASIDE_HILL, stage_obj=StageObj.SINGLE_SPRING) & has_stage_obj_rule(team=team, stage=Stage.SEASIDE_HILL, stage_obj=StageObj.TRIPLE_SPRING) & has_stage_obj_rule(team=team, stage=Stage.SEASIDE_HILL, stage_obj=StageObj.GOAL_RING) & has_stage_obj_rule(team=team, stage=Stage.SEASIDE_HILL, stage_obj=StageObj.MOVING_RUIN_PLATFORM))

    return team_blast_rule & stage_objs_rule & HasFromListUnique(*[emerald.value for emerald in ChaosEmerald], count=7)
