"""
Helper Functions for custom rule builder rules related to tricks
"""

from rule_builder.options import OptionFilter
from rule_builder.rules import Rule

from ..constants.char_ability import Team
from ..constants.stage import Stage
from ..options import *
from ..rule_builder.custom_rules import TrickRule, SonicHeroesMacroRule
from ..world_base import SonicHeroesWorldBase
from .functions_ability_char import can_homing_attack_rule, can_jump_rule, can_tornado_rule, can_flight_rule


def can_medium_diff_rule() -> Rule[SonicHeroesWorldBase]:
    return TrickRule(option_filter=OptionFilter(option=Difficulty, value=Difficulty.option_medium, operator="ge"))


def can_badnik_bounce_rule() -> Rule[SonicHeroesWorldBase]:
    return TrickRule(option_filter=OptionFilter(option=BadnikBounce, value=BadnikBounce.option_true)) & can_hover_frame_rule(
        includes_homing_or_tornado=False)


def can_collis_abuse_rule() -> Rule[SonicHeroesWorldBase]:
    return TrickRule(option_filter=OptionFilter(option=CollisAbuse, value=CollisAbuse.option_true))


def can_hover_frame_rule(includes_homing_or_tornado: bool = False) -> Rule[SonicHeroesWorldBase]:
    if includes_homing_or_tornado:
        return TrickRule(option_filter=OptionFilter(option=HoverFrame, value=HoverFrame.option_jump_and_homing_or_tornado_hover))
    return TrickRule(option_filter=OptionFilter(option=HoverFrame, value=HoverFrame.option_jump_hover, operator="ge"))


def can_homing_hover_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=level) & can_hover_frame_rule(
        includes_homing_or_tornado=True)


def can_tornado_hover_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    return can_tornado_rule(team=team, stage=stage, level=level) & can_hover_frame_rule(includes_homing_or_tornado=True)


def can_parkour_rule() -> Rule[SonicHeroesWorldBase]:
    return TrickRule(option_filter=OptionFilter(option=Parkour, value=Parkour.option_true))


def can_fly_deplete_boost_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_flight_rule(team=team, stage=stage, num_other_chars=0) & TrickRule(option_filter=OptionFilter(option=FlyDepleteBoost, value=FlyDepleteBoost.option_true))


def can_fly_ground_bounce_rule(team: Team, stage: Stage, needs_jump: bool = True) -> Rule[SonicHeroesWorldBase]:
    if needs_jump:
        # Fly Jump and Trick
        # jumpless or'd with Macro for jump
        return can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & TrickRule(option_filter=OptionFilter(option=FlyGroundBounce, value=FlyGroundBounce.option_with_jump, operator="ge"))

    return TrickRule(option_filter=OptionFilter(option=FlyGroundBounce, value=FlyGroundBounce.option_without_jump))


