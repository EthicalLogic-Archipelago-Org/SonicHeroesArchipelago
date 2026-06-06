"""
Helper Functions for custom rule builder rules related to stages
"""

from rule_builder.rules import HasFromListUnique, Rule, True_
from worlds.sonic_heroes.constants.items_events import ChaosEmerald

from .custom_rules import CanTeamBlast

from ..constants.char_ability import Team
from ..constants.stage import Stage
from ..world_base import SonicHeroesWorldBase


def can_goal_rule() -> Rule[SonicHeroesWorldBase]:
    return CanTeamBlast(team=Team.DARK, stage=Stage.SEASIDE_HILL) & HasFromListUnique(*[emerald.value for emerald in ChaosEmerald], count=7)