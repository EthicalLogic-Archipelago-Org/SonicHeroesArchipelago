"""
Helper Functions for custom rule builder rules related to enemies
"""
from rule_builder.rules import Rule, False_, True_

from ..constants.char_ability import Formation, Team
from ..constants.enemies import E2000, Cameron, CameronType, E2000Type, EggBishop, EggFlapperWeapon, EggHammer, EggHammerType, EggPawn, EggPawnShield, EggPawnType, EggPawnWeapon, Klagen, KlagenType, Rhino, EggFlapper, EggFlapperArmor, EnemyHeight, SonicHeroesEnemyBase, Falco
from ..constants.stage import Stage
from ..options import *
from ..rule_builder.custom_rules import HasEnemyItem, SonicHeroesMacroRule
from ..world_base import SonicHeroesWorldBase
from .functions_ability_char import can_auto_power_attack_rule, can_belly_flop_rule, can_break_things_rule, can_combo_finisher_rule, \
    can_fire_dunk_rule, can_homing_attack_rule, can_jump_rule, can_light_attack_rule, can_power_attack_rule, \
    can_rocket_accel_rule, can_team_blast_rule, can_thundershoot_rule, can_tornado_rule, can_flight_rule, can_kick_rule, has_all_3_chars_rule, has_flying_and_1_more_char_rule, has_flying_and_tall_char_rule, has_formation_char_rule, has_full_flying_stack_with_tall_char, has_tall_character
from .functions_stage_obj import has_bobsled_rule

def has_enemy_obj(team: Team, stage: Stage, enemy: SonicHeroesEnemyBase) -> Rule[SonicHeroesWorldBase]:
    return HasEnemyItem(team=team, stage=stage, enemy=enemy)


def can_kill_red_flapper(team: Team, stage: Stage, flapper: EggFlapper, height: EnemyHeight, color_str: str) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height is EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FLIGHT_THUNDERSHOOT:
        rule = can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.THUNDERSHOOT:
        rule = can_thundershoot_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")


    if height is EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) & has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FULL_FLY_STACK_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) | has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.TALL_CHAR_JUMP:
        rule = (can_jump_rule(team=team, stage=stage) & (has_tall_character(team=team) | has_flying_and_1_more_char_rule(team=team))) | can_thundershoot_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP:
        rule = can_jump_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.HALF_JUMP:
        rule = can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.GROUND:
        rule = can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))
        return SonicHeroesMacroRule(child=can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.HALF_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    print(f"HOW DID WE GET HERE? Height: Height.{height.name} in can_kill_red_flapper")
    return False_[SonicHeroesWorldBase]()


def can_kill_green_shot_flapper_homing_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=1)


def can_kill_green_shot_flapper(team: Team, stage: Stage, flapper: EggFlapper, height: EnemyHeight, color_str: str) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height is EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FLIGHT_THUNDERSHOOT:
        rule = can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) & has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FULL_FLY_STACK_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) | has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.TALL_CHAR_JUMP:
        rule = (can_jump_rule(team=team, stage=stage) & (has_tall_character(team=team) | has_flying_and_1_more_char_rule(team=team))) | can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP:
        rule = can_jump_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.HALF_JUMP:
        rule = can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.GROUND:
        rule = can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))
        return SonicHeroesMacroRule(child=can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.HALF_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    print(f"HOW DID WE GET HERE? Height: Height.{height.name} in can_kill_green_shot_flapper")
    return False_[SonicHeroesWorldBase]()


def can_kill_green_lightning_flapper(team: Team, stage: Stage, flapper: EggFlapper, height: EnemyHeight, color_str: str) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height is EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FLIGHT_THUNDERSHOOT:
        rule = can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP_THUNDERSHOOT:
        rule = can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FLIGHT_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) & has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP_THUNDERSHOOT, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.FULL_FLY_STACK_JUMP:
        rule = can_jump_rule(team=team, stage=stage) & (has_all_3_chars_rule(team=team) | has_flying_and_tall_char_rule(team=team))
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.TALL_CHAR_JUMP:
        rule = (can_jump_rule(team=team, stage=stage) & (has_tall_character(team=team) | has_flying_and_1_more_char_rule(team=team))) | can_thundershoot_rule(team=team, stage=stage, level=1)
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.FULL_FLY_STACK_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.JUMP:
        rule = can_jump_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.TALL_CHAR_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.HALF_JUMP:
        rule = can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if height is EnemyHeight.GROUND:
        rule = can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))
        return SonicHeroesMacroRule(child=can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=EnemyHeight.HALF_JUMP, color_str=color_str) | rule, name=f"Kill {flapper.get_enemy_str()} as Team {team} in {stage.stage_name}")

    print(f"HOW DID WE GET HERE? Height: Height.{height.name} in can_kill_green_lightning_flapper")
    return False_[SonicHeroesWorldBase]()


def can_kill_silver_armor_flapper(team: Team, stage: Stage, height: EnemyHeight, color_str: str) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    can_kill_ground_silver_armor: Rule[SonicHeroesWorldBase] = can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1)

    if height.relative_value <= EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.JUMP_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.FULL_FLY_STACK_JUMP.relative_value:
        rule |= can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.TALL_CHAR_JUMP.relative_value:
        rule |= can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor
    if height.relative_value <= EnemyHeight.JUMP.relative_value:
        rule |= (can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.HALF_JUMP.relative_value:
        rule |= can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False) | (can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_ground_silver_armor)
    if height.relative_value <= EnemyHeight.GROUND.relative_value:
        rule |= can_kill_ground_silver_armor
    return rule


def can_kill_egg_flapper(team: Team, stage: Stage, flapper: EggFlapper) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=flapper)
    color_str: str = "PLACEHOLDER COLOR"
    match flapper.armor:
        case EggFlapperArmor.NO_ARMOR:
            match flapper.weapon:
                case EggFlapperWeapon.NO_WEAPON:
                    color_str = "Red"
                    rule &= can_kill_red_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.NEEDLE:
                    color_str = "Gray"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.BAZOOKA:
                    color_str = "Green"
                    rule &= can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.MACHINE_GUN:
                    color_str = "Blue"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.LIGHTNING | EggFlapperWeapon.LASER:  # pyright: ignore[reportUnnecessaryComparison]
                    color_str = "Green"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.BOMB:
                    color_str = "Pink"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
                case EggFlapperWeapon.SEARCHLIGHT:
                    color_str = "Yellow"
                    rule &= can_kill_green_shot_flapper(team=team, stage=stage, flapper=flapper, height=flapper.height, color_str=color_str)
        case EggFlapperArmor.SILVER_ARMOR:
            color_str = "Silver Armor"
            rule &= can_kill_silver_armor_flapper(team=team, stage=stage, height=flapper.height, color_str=color_str)

    return rule


def get_placeholder_basic_egg_pawn_on_ground_for_rules(team: Team, stage: Stage) -> EggPawn:
    return EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN)


def can_kill_basic_egg_pawn_homing_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=0)

def can_kill_basic_egg_pawn_thundershoot_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_thundershoot_rule(team=team, stage=stage, level=2)

def can_kill_basic_egg_pawn_power_attack_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_power_attack_rule(team=team, stage=stage, level=0)

def can_kill_basic_egg_pawn_belly_flop_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_belly_flop_rule(team=team, stage=stage, level=0)

def can_kill_basic_egg_pawn_fire_dunk_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_fire_dunk_rule(team=team, stage=stage, level=0)


def can_kill_basic_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_pawn: EggPawn = EggPawn(team=team, stage=stage, height=pawn.height.next_higher, weapon=pawn.weapon, shield=pawn.shield, special_type=pawn.special_type)
    if pawn.height is EnemyHeight.JUMP:
        rule |= (can_jump_rule(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_homing_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_thundershoot_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_belly_flop_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_fire_dunk_only(team=team, stage=stage) |
                 can_light_attack_rule(team=team, stage=stage) |
                 can_team_blast_rule(team=team, stage=stage))
        return SonicHeroesMacroRule(child=rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if pawn.height is EnemyHeight.HALF_JUMP:
        rule |= can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        return SonicHeroesMacroRule(child=can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn) | rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if pawn.height is EnemyHeight.GROUND:
        rule |= (can_kick_rule(team=team, stage=stage) |
                 can_break_things_rule(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_power_attack_only(team=team, stage=stage))
        return SonicHeroesMacroRule(child=can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn) | rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    raise ValueError(f"Basic Egg Pawn Height {pawn.height} not checked for")


def can_kill_egg_pawn_bazooka(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    return can_kill_basic_egg_pawn(team=team, stage=stage, pawn=pawn)

def can_kill_basic_egg_pawn_lance_homing_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=1)

def can_kill_basic_egg_pawn_lance_thundershoot_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_thundershoot_rule(team=team, stage=stage, level=2)

def can_kill_basic_egg_pawn_lance_power_attack_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_power_attack_rule(team=team, stage=stage, level=1)

def can_kill_basic_egg_pawn_lance_bell_flop_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_belly_flop_rule(team=team, stage=stage, level=1)

def can_kill_basic_egg_pawn_lance_fire_dunk_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_fire_dunk_rule(team=team, stage=stage, level=1)


def can_kill_egg_pawn_lance(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_pawn: EggPawn = EggPawn(team=team, stage=stage, height=pawn.height.next_higher, weapon=pawn.weapon, shield=pawn.shield, special_type=pawn.special_type)
    if pawn.height is EnemyHeight.JUMP:
        rule |= (can_kill_basic_egg_pawn_lance_homing_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_lance_thundershoot_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_lance_bell_flop_only(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_lance_fire_dunk_only(team=team, stage=stage) |
                 can_light_attack_rule(team=team, stage=stage) |
                 can_team_blast_rule(team=team, stage=stage))
        return SonicHeroesMacroRule(child=rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if pawn.height is EnemyHeight.HALF_JUMP:
        rule |= can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        return SonicHeroesMacroRule(child=can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn) | rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    if pawn.height is EnemyHeight.GROUND:
        rule |= (can_kick_rule(team=team, stage=stage) |
                 can_break_things_rule(team=team, stage=stage) |
                 can_kill_basic_egg_pawn_lance_power_attack_only(team=team, stage=stage))
        return SonicHeroesMacroRule(child=can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn) | rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    raise ValueError(f"Egg Pawn Lance Height {pawn.height} not checked for")


def can_kill_egg_pawn_machine_gun(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_pawn: EggPawn = EggPawn(team=team, stage=stage, height=pawn.height.next_higher, weapon=pawn.weapon, shield=pawn.shield, special_type=pawn.special_type)

    if pawn.height is EnemyHeight.GROUND:
        rule |= can_homing_attack_rule(team=team, stage=stage, level=0) | can_kick_rule(team=team, stage=stage) | can_auto_power_attack_rule(team=team, stage=stage) | can_break_things_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage)
        return SonicHeroesMacroRule(child=rule, name=f"Kill {pawn.get_enemy_str()} as Team {team} in {stage.stage_name}")

    raise ValueError(f"Egg Pawn Machine Gun Height {pawn.height} not checked for")


def can_remove_shield(team: Team, stage: Stage, height: EnemyHeight = EnemyHeight.GROUND) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_homing_attack_rule(team=team, stage=stage, level=3) | (can_tornado_rule(team=team, stage=stage, level=0) | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1)) | can_team_blast_rule(team=team, stage=stage), name=f"Remove shield at {height} Height as Team {team} in {stage.stage_name}")


def can_break_concrete_shield(team: Team, stage: Stage, height: EnemyHeight = EnemyHeight.GROUND) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_combo_finisher_rule(team=team, stage=stage, level=2) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_light_attack_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage), name=f"Break Concrete Shield at {height} Height as Team {team} in {stage.stage_name}")


def can_break_plain_shield(team: Team, stage: Stage, height: EnemyHeight = EnemyHeight.GROUND) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_break_things_rule(team=team, stage=stage) | can_light_attack_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage), name=f"Break Plain Shield at {height} Height as Team {team} in {stage.stage_name}")


def can_break_spike_shield(team: Team, stage: Stage, height: EnemyHeight = EnemyHeight.GROUND) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_break_things_rule(team=team, stage=stage) | can_light_attack_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage), name=f"Break Spike Shield at {height} Height as Team {team} in {stage.stage_name}")


def can_kill_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=pawn)

    match pawn.shield:
        case EggPawnShield.NO_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= can_kill_basic_egg_pawn(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.BAZOOKA:
                    rule &= can_kill_egg_pawn_bazooka(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.LANCE:
                    rule &= can_kill_egg_pawn_lance(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= can_kill_egg_pawn_machine_gun(team=team, stage=stage, pawn=pawn)
        case EggPawnShield.CONCRETE_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_concrete_shield(team=team, stage=stage, height=pawn.height)) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_concrete_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_bazooka(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_concrete_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_lance(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_concrete_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage, pawn=pawn)
        case EggPawnShield.PLAIN_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_plain_shield(team=team, stage=stage, height=pawn.height)) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_plain_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_bazooka(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_plain_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_lance(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_plain_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage, pawn=pawn)
        case EggPawnShield.SPIKE_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_spike_shield(team=team, stage=stage, height=pawn.height)) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_spike_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_bazooka(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_spike_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_lance(team=team, stage=stage, pawn=pawn)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage, height=pawn.height) | can_break_spike_shield(team=team, stage=stage, height=pawn.height)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage, pawn=pawn)

    return rule



def can_kill_egg_pawn_with_bobsled(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    enemy_str: str = ""
    if pawn.special_type is EggPawnType.KING_PAWN:
        enemy_str += "King "
    if pawn.special_type is EggPawnType.CASINO_PAWN_1 or pawn.special_type is EggPawnType.CASINO_PAWN_2:
        enemy_str += "Casino "
    enemy_str += "Egg Pawn"

    return SonicHeroesMacroRule(child=has_enemy_obj(team=team, stage=stage, enemy=pawn) & has_bobsled_rule(team=team, stage=stage) & (has_formation_char_rule(team=team, formation=Formation.SPEED) | has_formation_char_rule(team=team, formation=Formation.POWER)), name=f"Kill {enemy_str} with {pawn.shield} and {pawn.weapon} as Team: {team} in {stage.stage_name} with Bobsled")


def can_kill_egg_pawn_with_seaside_hill_first_bobsled(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    return False_[SonicHeroesWorldBase]()


def can_kill_regular_klagen(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_jump_rule(team=team, stage=stage) | can_homing_attack_rule(team=team, stage=stage, level=0) | can_auto_power_attack_rule(team=team, stage=stage) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage)


def can_kill_klagen(team: Team, stage: Stage, klagen: Klagen) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=klagen)
    enemy_str: str = ""
    match klagen.special_type:
        case KlagenType.REGULAR_KLAGEN:
            enemy_str = "Klagen"
            rule &= can_kill_regular_klagen(team=team, stage=stage)
        case KlagenType.GOLD_KLAGEN:
            enemy_str = "Gold Klagen"
            rule &= can_kill_regular_klagen(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team {team} in {stage.stage_name}")


def can_kill_falco(team: Team, stage: Stage, falco: Falco) -> Rule[SonicHeroesWorldBase]:
    """
    Not intending to route falco's as they are annoying
    """
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=falco)
    rule &= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=2)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Falco as Team {team} in {stage.stage_name}")


def can_kill_regular_egg_hammer(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_belly_flop_rule(team=team, stage=stage, level=3) | can_fire_dunk_rule(team=team, stage=stage, level=3) | can_combo_finisher_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)


def can_knock_down_heavy_egg_hammer(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_jump_rule(team=team, stage=stage) | can_homing_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Knock Down Egg Hammer as Team {team} in {stage.stage_name}")


def can_kill_heavy_egg_hammer(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return (can_knock_down_heavy_egg_hammer(team=team, stage=stage) & can_power_attack_rule(team=team, stage=stage, level=3) & can_combo_finisher_rule(team=team, stage=stage, level=3)) | can_team_blast_rule(team=team, stage=stage)


def can_kill_egg_hammer(team: Team, stage: Stage, egg_hammer: EggHammer) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=egg_hammer)
    enemy_str: str = ""
    match egg_hammer.special_type:
        case EggHammerType.REGULAR_EGG_HAMMER:
            enemy_str = "Egg Hammer"
            rule &= can_kill_regular_egg_hammer(team=team, stage=stage)
        case EggHammerType.HEAVY_EGG_HAMMER:
            enemy_str = "Heavy Egg Hammer"
            rule &= can_kill_heavy_egg_hammer(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team {team} in {stage.stage_name}")


def can_kill_regular_cameron(team: Team, stage: Stage, cameron: Cameron) -> Rule[SonicHeroesWorldBase]:
    return (can_remove_shield(team=team, stage=stage, height=cameron.height) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))) | can_break_things_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage)


def can_kill_gold_cameron(team: Team, stage: Stage, cameron: Cameron) -> Rule[SonicHeroesWorldBase]:
    return (can_remove_shield(team=team, stage=stage, height=cameron.height) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))) | can_team_blast_rule(team=team, stage=stage)


def can_kill_cameron(team: Team, stage: Stage, cameron: Cameron) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=cameron)
    enemy_str: str = ""
    match cameron.special_type:
        case CameronType.REGULAR_CAMERON:
            enemy_str = "Cameron"
            rule &= can_kill_regular_cameron(team=team, stage=stage, cameron=cameron)
        case CameronType.GOLD_CAMERON:
            enemy_str = "Gold Cameron"
            rule &= can_kill_gold_cameron(team=team, stage=stage, cameron=cameron)
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team {team} in {stage.stage_name}")


def can_kill_rhino(team: Team, stage: Stage, rhino: Rhino) -> Rule[SonicHeroesWorldBase]:
    """
    Dont want to route these
    """
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=rhino)
    rule &= can_thundershoot_rule(team=team, stage=stage, level=2) | can_team_blast_rule(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Rhino as Team {team} in {stage.stage_name}")


def can_kill_egg_bishop(team: Team, stage: Stage, bishop: EggBishop) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=bishop)
    rule &= can_homing_attack_rule(team=team, stage=stage, level=2) | can_belly_flop_rule(team=team, stage=stage, level=2) | can_fire_dunk_rule(team=team, stage=stage, level=2) | can_combo_finisher_rule(team=team, stage=stage, level=2) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Egg Bishop as Team {team} in {stage.stage_name}")


def can_kill_regular_e2000(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_belly_flop_rule(team=team, stage=stage, level=3) | can_fire_dunk_rule(team=team, stage=stage, level=3) | can_combo_finisher_rule(team=team, stage=stage, level=3) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)


def can_kill_e2000_r(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return (can_homing_attack_rule(team=team, stage=stage, level=0) & can_combo_finisher_rule(team=team, stage=stage, level=3)) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)


def can_kill_e2000(team: Team, stage: Stage, e2000: E2000) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=e2000)
    enemy_str: str = ""
    match e2000.special_type:
        case E2000Type.E2000:
            enemy_str = "E2000"
            rule &= can_kill_regular_e2000(team=team, stage=stage)
        case E2000Type.E2000R:
            enemy_str = "E2000R"
            rule &= can_kill_e2000_r(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team {team} in {stage.stage_name}")


