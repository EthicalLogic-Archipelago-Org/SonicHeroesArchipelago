"""
Helper Functions for custom rule builder rules related to Abilities and Characters
"""


from rule_builder.rules import Rule

from ..constants.char_ability import Ability, Formation, Team
from ..constants.stage import Stage
from .custom_rules import *
from ..world_base import SonicHeroesWorldBase


def has_formation_char_rule(team: Team, formation: Formation) -> Rule[SonicHeroesWorldBase]:
    return HasFormationCharForTeam(team=team, formation=formation)


def has_flying_and_1_more_char_rule(team: Team) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasFlyingAnd1MoreChar(team=team), name=f"Has Flying and 1 More Char as Team: {team}")


def has_flying_and_tall_char_rule(team: Team) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=has_formation_char_rule(team=team, formation=Formation.FLYING) & has_tall_character(team=team), name=f"Has Flying and Tall Char as Team: {team}")


def has_all_3_chars_rule(team: Team) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasAll3Char(team=team), name=f"Has All 3 Chars as Team: {team}")


def has_tall_character(team: Team) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasTallChar(team=team), name=f"Has Tall Char as Team: {team}")


def has_full_flying_stack_with_tall_char(team: Team) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasFullFlyingStackWithTallChar(team=team), name=f"Full Flying Stack with Tall Char as Team: {team}")


# def can_ability_rule(team: Team, stage: Stage, ability: Ability, level: int = 0, other_chars: int = 0) -> Rule[SonicHeroesWorldBase]:
#     match ability:
#         case Ability.JUMP:
#             return can_jump_rule(team=team, stage=stage)
#         case Ability.AMY_HAMMER_HOVER:
#             return can_amy_hammer_hover_rule(team=team, stage=stage)
#         case Ability.HOMING_ATTACK:
#             return can_homing_attack_rule(team=team, stage=stage, level=level)
#         case Ability.TORNADO:
#             return can_tornado_rule(team=team, stage=stage, level=level)
#         case Ability.ROCKET_ACCEL:
#             return can_rocket_accel_rule(team=team, stage=stage, num_other_chars=other_chars)
#         case Ability.LIGHT_DASH:
#             return can_light_dash_rule(team=team, stage=stage)
#         case Ability.TRIANGLE_JUMP:
#             return can_triangle_jump_rule(team=team, stage=stage)
#         case Ability.LIGHT_ATTACK:
#             return can_light_attack_rule(team=team, stage=stage)
#         case Ability.INVISIBILITY:
#             return can_invisibility_rule(team=team, stage=stage)
#         case Ability.SHURIKEN:
#             return can_shuriken_rule(team=team, stage=stage)
#         case Ability.DUMMY_RINGS:
#             return can_dummy_rings_rule(team=team, stage=stage)
#         case Ability.CHEESE_CANNON:
#             return can_cheese_cannon_rule(team=team, stage=stage)
#         case Ability.FLOWER_STING:
#             return can_flower_sting_rule(team=team, stage=stage)
#         case Ability.THUNDER_SHOOT:
#             return can_thundershoot_rule(team=team, stage=stage, level=level)
#         case Ability.FLIGHT:
#             return can_flight_rule(team=team, stage=stage, num_other_chars=other_chars)
#         case Ability.POWER_ATTACK:
#             return can_power_attack_rule(team=team, stage=stage, level=level)
#         case Ability.BELLY_FLOP:
#             return can_belly_flop_rule(team=team, stage=stage, level=level)
#         case Ability.FIRE_DUNK:
#             return can_fire_dunk_rule(team=team, stage=stage, level=level)
#         case Ability.ULTIMATE_FIRE_DUNK:
#             return can_ultimate_fire_dunk_rule(team=team, stage=stage, level=level)
#         case Ability.GLIDE:
#             return can_glide_rule(team=team, stage=stage)
#         case Ability.COMBO_FINISHER:
#             return can_combo_finisher_rule(team=team, stage=stage, level=level)


def can_break_things_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    if team == Team.SONIC:
        return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Break Things as Team: {team} in {stage.stage_name}")
    return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1), name=f"Break Things as Team: {team} in {stage.stage_name}")


def can_break_wood_container_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    if team == Team.SONIC:
        return SonicHeroesMacroRule(child=can_kick_rule(team=team, stage=stage) | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1) | can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Break Wood Container as Team: {team} in {stage.stage_name}")
    return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1), name=f"Break Wood Container as Team: {team} in {stage.stage_name}")



def can_break_iron_container_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    if team == Team.SONIC:
        return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Break Iron Container as Team: {team} in {stage.stage_name}")
    return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1), name=f"Break Iron Container as Team: {team} in {stage.stage_name}")


def can_jump_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.JUMP
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_amy_hammer_hover_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.AMY_HAMMER_HOVER
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}", description=f"Hover in the air by spinning Amy's Hammer. Hold the jump button after jumping")


def can_homing_attack_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.HOMING_ATTACK
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_tornado_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.TORNADO
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_kick_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasFormationCharForTeam(team=team, formation=Formation.SPEED), name=F"Kick as Team: {team} in {stage.stage_name}")


def can_rocket_accel_rule(team: Team, stage: Stage, num_other_chars: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.ROCKET_ACCEL
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, num_other_chars=num_other_chars), name=f"{ability.ability_name} with {num_other_chars} other characters as Team: {team} in {stage.stage_name}")


def can_light_dash_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.LIGHT_DASH
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_triangle_jump_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.TRIANGLE_JUMP
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability) & can_homing_attack_rule(team=team, stage=stage, level=0) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_light_attack_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.LIGHT_ATTACK
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability) & can_jump_rule(team=team, stage=stage) & can_team_blast_rule(team=team, stage=stage), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_invisibility_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.INVISIBILITY
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability) & can_jump_rule(team=team, stage=stage) & can_tornado_rule(team=team, stage=stage, level=0), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_shuriken_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.SHURIKEN
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_dummy_rings_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.DUMMY_RINGS
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_cheese_cannon_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.CHEESE_CANNON
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_flower_sting_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.FLOWER_STING
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_thundershoot_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.THUNDER_SHOOT
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level, num_other_chars=1), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_flight_rule(team: Team, stage: Stage, num_other_chars: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.FLIGHT
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, num_other_chars=num_other_chars), name=f"{ability.ability_name} with {num_other_chars} other characters as Team: {team} in {stage.stage_name}")


def can_auto_power_attack_rule(team: Team, stage: Stage, need_speed_lvl_3: bool = False) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = CanAutoPowerAttack(team=team, need_speed_lvl_3=need_speed_lvl_3)
    speed_str: str = "" if not need_speed_lvl_3 else f" with Speed Level 3"
    return SonicHeroesMacroRule(child=rule, name=f"Power Formation Auto Attack{speed_str} as Team: {team} in {stage.stage_name}")


def can_power_attack_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.POWER_ATTACK
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_belly_flop_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.BELLY_FLOP
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_fire_dunk_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.FIRE_DUNK
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level, num_other_chars=1) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_ultimate_fire_dunk_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.ULTIMATE_FIRE_DUNK
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level, num_other_chars=1) & can_fire_dunk_rule(team=team, stage=stage, level=level) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_glide_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.GLIDE
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability) & can_jump_rule(team=team, stage=stage), name=f"{ability.ability_name} as Team: {team} in {stage.stage_name}")


def can_combo_finisher_rule(team: Team, stage: Stage, level: int) -> Rule[SonicHeroesWorldBase]:
    ability: Ability = Ability.COMBO_FINISHER
    return SonicHeroesMacroRule(child=HasAbilityForTeam(team=team, ability=ability, level=level) & can_power_attack_rule(team=team, stage=stage, level=level), name=f"{ability.ability_name} Level {level} as Team: {team} in {stage.stage_name}")


def can_combo_height_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=HasComboHeight(team=team) & can_power_attack_rule(team=team, stage=stage, level=0), name=f"Gain Height with {Ability.COMBO_FINISHER.ability_name} as Team: {team} in {stage.stage_name}")


def can_team_blast_rule(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=CanTeamBlast(team=team), name=f"Team Blast as Team: {team} in {stage.stage_name}", description="Team Blast Description Here")