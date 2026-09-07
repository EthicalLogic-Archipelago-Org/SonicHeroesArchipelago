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
    can_fire_dunk_rule, can_flower_sting_rule, can_homing_attack_rule, can_jump_rule, can_light_attack_rule, can_power_attack_rule, \
    can_rocket_accel_rule, can_shuriken_rule, can_team_blast_rule, can_thundershoot_rule, can_tornado_rule, can_flight_rule, can_kick_rule, has_all_3_chars_rule, has_flying_and_1_more_char_rule, has_flying_and_tall_char_rule, has_formation_char_rule, has_full_flying_stack_with_tall_char, has_tall_character
from .functions_stage_obj import has_bobsled_rule

def has_enemy_obj(team: Team, stage: Stage, enemy: SonicHeroesEnemyBase) -> Rule[SonicHeroesWorldBase]:
    return HasEnemyItem(team=team, stage=stage, enemy=enemy)


def can_kill_egg_flapper(team: Team, stage: Stage, flapper: EggFlapper) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_flapper: EggFlapper = EggFlapper(team=team, stage=stage, height=flapper.height.next_higher, weapon=flapper.weapon, armor=flapper.armor)
    macro_str: str = f"Kill {flapper.get_enemy_str()} as Team {team.value} in {stage.stage_name}"
    match flapper.height:
        case EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
            rule = can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & _can_kill_egg_flapper_thundershoot_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.FLIGHT_THUNDERSHOOT:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & _can_kill_egg_flapper_thundershoot_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.JUMP_THUNDERSHOOT:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= can_jump_rule(team=team, stage=stage) & _can_kill_egg_flapper_thundershoot_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.THUNDERSHOOT:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= _can_kill_egg_flapper_thundershoot_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= has_all_3_chars_rule(team=team) & has_flying_and_tall_char_rule(team=team) & _can_kill_egg_flapper_jump_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.FULL_FLY_STACK_JUMP:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= (has_all_3_chars_rule(team=team) | has_flying_and_tall_char_rule(team=team)) & _can_kill_egg_flapper_jump_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.TALL_CHAR_JUMP:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= (has_tall_character(team=team) | has_flying_and_1_more_char_rule(team=team)) & _can_kill_egg_flapper_jump_only(team=team, stage=stage, flapper=flapper)
        case EnemyHeight.JUMP:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= _can_kill_egg_flapper_jump_only(team=team, stage=stage, flapper=flapper) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_homing_attack_rule(team=team, stage=stage, level=1)
        case EnemyHeight.HALF_JUMP:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=False)
        case EnemyHeight.GROUND:
            rule = can_kill_egg_flapper(team=team, stage=stage, flapper=higher_flapper)
            rule |= can_kill_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))
    return SonicHeroesMacroRule(child=has_enemy_obj(team=team, stage=stage, enemy=flapper) & rule, name=macro_str)


def can_kill_green_shot_flapper_homing_only(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=1)


def can_kill_grounded_silver_armor_flapper(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Kill Grounded Silver Armor Egg Flapper as Team {team} in {stage.stage_name}")


def _can_kill_egg_flapper_jump_only(team: Team, stage: Stage, flapper: EggFlapper) -> Rule[SonicHeroesWorldBase]:
    match flapper.armor:
        case EggFlapperArmor.NO_ARMOR:
            match flapper.weapon:
                case EggFlapperWeapon.NO_WEAPON | EggFlapperWeapon.BAZOOKA | EggFlapperWeapon.MACHINE_GUN | EggFlapperWeapon.BOMB | EggFlapperWeapon.SEARCHLIGHT:
                    return can_jump_rule(team=team, stage=stage)
                case EggFlapperWeapon.NEEDLE | EggFlapperWeapon.LIGHTNING:
                    return False_[SonicHeroesWorldBase]()
        case EggFlapperArmor.SILVER_ARMOR:
            return False_[SonicHeroesWorldBase]()


def _can_kill_egg_flapper_thundershoot_only(team: Team, stage: Stage, flapper: EggFlapper) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match flapper.armor:
        case EggFlapperArmor.NO_ARMOR:
            match flapper.weapon:
                case EggFlapperWeapon.NO_WEAPON:
                    rule &= can_thundershoot_rule(team=team, stage=stage, level=0)
                case EggFlapperWeapon.BAZOOKA | EggFlapperWeapon.LIGHTNING | EggFlapperWeapon.SEARCHLIGHT:
                    rule &= can_thundershoot_rule(team=team, stage=stage, level=1)
                case EggFlapperWeapon.MACHINE_GUN | EggFlapperWeapon.NEEDLE | EggFlapperWeapon.BOMB:
                    rule &= can_thundershoot_rule(team=team, stage=stage, level=2)
        case EggFlapperArmor.SILVER_ARMOR:
            rule &= can_thundershoot_rule(team=team, stage=stage, level=0) & can_kill_grounded_silver_armor_flapper(
                team=team, stage=stage)
    return rule


def get_placeholder_basic_egg_pawn_on_ground_for_rules(team: Team, stage: Stage) -> EggPawn:
    return EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN)


def can_kill_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    higher_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_pawn: EggPawn = EggPawn(team=team, stage=stage, height=pawn.height.next_higher, weapon=pawn.weapon, shield=pawn.shield, special_type=pawn.special_type)
    macro_str: str = f"Kill {pawn.get_enemy_str()} as Team {team.value} in {stage.stage_name}"
    match pawn.height:
        # case EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
        #     rule = can_jump_rule(team=team, stage=stage) & can_flight_rule(team=team, stage=stage, num_other_chars=0) & _can_kill_egg_pawn_thundershoot_only(team=team, stage=stage, pawn=pawn)
        # case EnemyHeight.FLIGHT_THUNDERSHOOT:
        #     rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
        #     rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & _can_kill_egg_pawn_thundershoot_only(team=team, stage=stage, pawn=pawn)
        # case EnemyHeight.JUMP_THUNDERSHOOT:
        #     rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
        #     rule |= can_jump_rule(team=team, stage=stage) & _can_kill_egg_pawn_thundershoot_only(team=team, stage=stage, pawn=pawn)
        case EnemyHeight.THUNDERSHOOT:
            higher_rule |= _can_remove_pawn_shield(team=team, stage=stage, pawn=pawn) & _can_kill_egg_pawn_thundershoot_only(team=team, stage=stage, pawn=pawn)
        # case EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
        #     rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
        #     rule |= has_all_3_chars_rule(team=team) & has_flying_and_tall_char_rule(team=team) & _can_kill_egg_pawn_jump_only(team=team, stage=stage, pawn=pawn)
        # case EnemyHeight.FULL_FLY_STACK_JUMP:
        #     rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
        #     rule |= (has_all_3_chars_rule(team=team) | has_flying_and_tall_char_rule(team=team)) & _can_kill_egg_pawn_jump_only(team=team, stage=stage, pawn=pawn)
        # case EnemyHeight.TALL_CHAR_JUMP:
        #     rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
        #     rule |= (has_tall_character(team=team) | has_flying_and_1_more_char_rule(team=team)) & _can_kill_egg_pawn_jump_only(team=team, stage=stage, pawn=pawn)

        case EnemyHeight.JUMP:
            higher_pawn.height = EnemyHeight.THUNDERSHOOT
            higher_rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
            higher_rule |= _can_remove_pawn_shield(team=team, stage=stage, pawn=pawn) & (_can_kill_egg_pawn_jump_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_homing_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_belly_flop_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_fire_dunk_only(team=team, stage=stage, pawn=pawn))

        case EnemyHeight.HALF_JUMP:
            higher_rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
            higher_rule |= _can_remove_pawn_shield(team=team, stage=stage, pawn=pawn) & _can_kill_egg_pawn_auto_power_attack_only(team=team, stage=stage, pawn=pawn)
        case EnemyHeight.GROUND:
            higher_rule = can_kill_egg_pawn(team=team, stage=stage, pawn=higher_pawn)
            higher_rule |= _can_remove_pawn_shield(team=team, stage=stage, pawn=pawn) & (_can_kill_egg_pawn_kick_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_shuriken_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_flower_sting_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_power_attack_only(team=team, stage=stage, pawn=pawn) | _can_kill_egg_pawn_combo_finisher_only(team=team, stage=stage, pawn=pawn))
        case _:
            raise ValueError(f"Bad Height: {pawn.height.description} in can_kill_egg_pawn")
    return SonicHeroesMacroRule(child=has_enemy_obj(team=team, stage=stage, enemy=pawn) & higher_rule, name=macro_str)


def _can_remove_pawn_shield(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    higher_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    higher_pawn: EggPawn = EggPawn(team=team, stage=stage, height=pawn.height.next_higher, weapon=pawn.weapon, shield=pawn.shield, special_type=pawn.special_type)
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    macro_str: str = f"Break {pawn.shield.value} as Team {team.value} in {stage.stage_name}"
    match pawn.shield:
        case EggPawnShield.NO_SHIELD:
            rule= True_[SonicHeroesWorldBase]()
        case EggPawnShield.PLAIN_SHIELD:
            match pawn.height:
                case EnemyHeight.JUMP:
                    rule = can_homing_attack_rule(team=team, stage=stage, level=3) | can_tornado_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_team_blast_rule(team=team, stage=stage)
                case EnemyHeight.HALF_JUMP:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=True)
                case EnemyHeight.GROUND:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1) | can_power_attack_rule(team=team, stage=stage, level=0)
                case _:
                    rule = False_[SonicHeroesWorldBase]()

        case EggPawnShield.SPIKE_SHIELD:
            match pawn.height:
                case EnemyHeight.THUNDERSHOOT:
                    rule = can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)
                case EnemyHeight.JUMP:
                    higher_pawn.height = EnemyHeight.THUNDERSHOOT
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_homing_attack_rule(team=team, stage=stage, level=3) | can_tornado_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=3) | can_fire_dunk_rule(team=team, stage=stage, level=3)
                case EnemyHeight.HALF_JUMP:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=True)
                case EnemyHeight.GROUND:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1) | can_combo_finisher_rule(team=team, stage=stage, level=3)
                case _:
                    rule = False_[SonicHeroesWorldBase]()

        case EggPawnShield.CONCRETE_SHIELD:
            match pawn.height:
                case EnemyHeight.THUNDERSHOOT:
                    rule = can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)
                case EnemyHeight.JUMP:
                    higher_pawn.height = EnemyHeight.THUNDERSHOOT
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_homing_attack_rule(team=team, stage=stage, level=3) | can_tornado_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)
                case EnemyHeight.HALF_JUMP:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_auto_power_attack_rule(team=team, stage=stage, need_speed_lvl_3=True)
                case EnemyHeight.GROUND:
                    higher_rule = _can_remove_pawn_shield(team=team, stage=stage, pawn=higher_pawn)
                    rule = higher_rule | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1) | can_combo_finisher_rule(team=team, stage=stage, level=3)
                case _:
                    rule = False_[SonicHeroesWorldBase]()

    return SonicHeroesMacroRule(child=rule, name=macro_str)


def _can_kill_egg_pawn_thundershoot_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            rule &= can_thundershoot_rule(team=team, stage=stage, level=1)
        case EggPawnType.KING_PAWN:
            rule &= can_thundershoot_rule(team=team, stage=stage, level=2)
    return rule


def _can_kill_egg_pawn_jump_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.weapon:
        case EggPawnWeapon.LANCE:
            return False_[SonicHeroesWorldBase]()
        case EggPawnWeapon.NO_WEAPON | EggPawnWeapon.BAZOOKA | EggPawnWeapon.MACHINE_GUN:
            match pawn.special_type:
                case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
                    return can_jump_rule(team=team, stage=stage)
                case EggPawnType.KING_PAWN:
                    return False_[SonicHeroesWorldBase]()


def _can_kill_egg_pawn_homing_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            return can_homing_attack_rule(team=team, stage=stage, level=1)
        case EggPawnType.KING_PAWN:
            return can_homing_attack_rule(team=team, stage=stage, level=2)


def _can_kill_egg_pawn_belly_flop_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            return can_belly_flop_rule(team=team, stage=stage, level=0)
        case EggPawnType.KING_PAWN:
            return can_belly_flop_rule(team=team, stage=stage, level=1)


def _can_kill_egg_pawn_fire_dunk_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            return can_belly_flop_rule(team=team, stage=stage, level=0)
        case EggPawnType.KING_PAWN:
            return can_belly_flop_rule(team=team, stage=stage, level=2)


def _can_kill_egg_pawn_auto_power_attack_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    return can_auto_power_attack_rule(team=team, stage=stage)


def _can_kill_egg_pawn_kick_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.weapon:
        case EggPawnWeapon.LANCE:
            return False_[SonicHeroesWorldBase]()
        case EggPawnWeapon.NO_WEAPON | EggPawnWeapon.BAZOOKA | EggPawnWeapon.MACHINE_GUN:
            match pawn.special_type:
                case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
                    return can_kick_rule(team=team, stage=stage)
                case EggPawnType.KING_PAWN:
                    return False_[SonicHeroesWorldBase]()


def _can_kill_egg_pawn_shuriken_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    return can_shuriken_rule(team=team, stage=stage)


def _can_kill_egg_pawn_flower_sting_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    return can_flower_sting_rule(team=team, stage=stage)


def _can_kill_egg_pawn_power_attack_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            return can_power_attack_rule(team=team, stage=stage, level=0)
        case EggPawnType.KING_PAWN:
            return can_power_attack_rule(team=team, stage=stage, level=2)


def _can_kill_egg_pawn_combo_finisher_only(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    # rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN | EggPawnType.CASINO_PAWN_1 | EggPawnType.CASINO_PAWN_2:
            return can_combo_finisher_rule(team=team, stage=stage, level=1)
        case EggPawnType.KING_PAWN:
            return can_combo_finisher_rule(team=team, stage=stage, level=2)


def can_kill_egg_pawn_with_bobsled(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=has_enemy_obj(team=team, stage=stage, enemy=pawn) & has_bobsled_rule(team=team, stage=stage) & (has_formation_char_rule(team=team, formation=Formation.SPEED) | has_formation_char_rule(team=team, formation=Formation.POWER)), name=f"Kill {pawn.get_enemy_str()} as Team: {team} in {stage.stage_name} with Bobsled")


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
    return True_[SonicHeroesWorldBase]()

    # (can_remove_shield(team=team, stage=stage, height=cameron.height) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))) | can_break_things_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage)


def can_kill_gold_cameron(team: Team, stage: Stage, cameron: Cameron) -> Rule[SonicHeroesWorldBase]:
    return True_[SonicHeroesWorldBase]()

    # (can_remove_shield(team=team, stage=stage, height=cameron.height) & can_kill_basic_egg_pawn(team=team, stage=stage, pawn=get_placeholder_basic_egg_pawn_on_ground_for_rules(team=team, stage=stage))) | can_team_blast_rule(team=team, stage=stage)


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


