"""
Helper Functions for custom rule builder rules related to enemies
"""
from rule_builder.rules import Rule, False_

from ..constants.char_ability import Team
from ..constants.enemies import E2000, Cameron, CameronType, E2000Type, EggBishop, EggFlapperWeapon, EggHammer, EggHammerType, EggPawn, EggPawnShield, EggPawnType, EggPawnWeapon, Klagen, KlagenType, Rhino, EggFlapper, EggFlapperArmor, EnemyHeight, SonicHeroesEnemy, Falco
from ..constants.stage import Stage
from ..options import *
from ..rule_builder.custom_rules import HasEnemyItem, SonicHeroesMacroRule
from ..world_base import SonicHeroesWorldBase
from .functions_ability_char import can_auto_power_attack_rule, can_belly_flop_rule, can_break_things_rule, can_combo_finisher_rule, \
    can_fire_dunk_rule, can_homing_attack_rule, can_jump_rule, can_power_attack_rule, \
    can_rocket_accel_rule, can_team_blast_rule, can_thundershoot_rule, can_tornado_rule, can_flight_rule, can_kick


def has_enemy_obj(team: Team, stage: Stage, enemy: SonicHeroesEnemy) -> Rule[SonicHeroesWorldBase]:
    return HasEnemyItem(team=team, stage=stage, enemy=enemy)


def can_kill_red_flapper(team: Team, stage: Stage, height: EnemyHeight) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height.relative_value <= EnemyHeight.FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.JUMP_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.HOMING.relative_value:
        rule |= can_homing_attack_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.JUMP.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.GROUND.relative_value:
        rule |= can_kill_basic_egg_pawn(team=team, stage=stage)
    return rule


def can_kill_green_shot_flapper(team: Team, stage: Stage, height: EnemyHeight) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height.relative_value <= EnemyHeight.FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.JUMP_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.HOMING.relative_value:
        rule |= can_homing_attack_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.JUMP.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.GROUND.relative_value:
        rule |= can_kill_basic_egg_pawn(team=team, stage=stage)
    return rule


def can_kill_green_lightning_flapper(team: Team, stage: Stage, height: EnemyHeight) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height.relative_value <= EnemyHeight.FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.JUMP_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.HOMING.relative_value:
        rule |= can_homing_attack_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=1)
    if height.relative_value <= EnemyHeight.JUMP.relative_value:
        rule |= can_thundershoot_rule(team=team, stage=stage, level=1) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.GROUND.relative_value:
        rule |= can_kill_basic_egg_pawn(team=team, stage=stage)
    return rule


def can_kill_silver_armor_flapper(team: Team, stage: Stage, height: EnemyHeight) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
    if height.relative_value <= EnemyHeight.FLIGHT_THUNDERSHOOT.relative_value:
        rule |= can_flight_rule(team=team, stage=stage, num_other_chars=0) & can_thundershoot_rule(team=team, stage=stage, level=0) & (can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1))
    if height.relative_value <= EnemyHeight.JUMP_THUNDERSHOOT.relative_value:
        rule |= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=0) & (can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1))
    if height.relative_value <= EnemyHeight.HOMING.relative_value:
        rule |= can_thundershoot_rule(team=team, stage=stage, level=0) & (can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1))
    if height.relative_value <= EnemyHeight.JUMP.relative_value:
        rule |= (can_thundershoot_rule(team=team, stage=stage, level=0) & can_power_attack_rule(team=team, stage=stage, level=0)) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0)
    if height.relative_value <= EnemyHeight.GROUND.relative_value:
        rule |= can_power_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_combo_finisher_rule(team=team, stage=stage, level=1)
    return rule


def can_kill_egg_flapper(team: Team, stage: Stage, flapper: EggFlapper, height: EnemyHeight) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=flapper)
    color_str: str = "PLACEHOLDER"
    match flapper.armor:
        case EggFlapperArmor.NO_ARMOR:
            match flapper.weapon:
                case EggFlapperWeapon.NO_WEAPON:
                    color_str = "Red"
                    rule &= can_kill_red_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.NEEDLE:
                    color_str = "Gray"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.SHOT:
                    color_str = "Green"
                    rule &= can_kill_green_shot_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.MACHINE_GUN:
                    color_str = "Blue"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.LIGHTNING | EggFlapperWeapon.LASER:  # pyright: ignore[reportUnnecessaryComparison]
                    color_str = "Green"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.BOMB:
                    color_str = "Pink"
                    rule &= can_kill_green_lightning_flapper(team=team, stage=stage, height=height)
                case EggFlapperWeapon.SEARCHLIGHT:
                    color_str = "Yellow"
                    rule &= can_kill_green_shot_flapper(team=team, stage=stage, height=height)
        case EggFlapperArmor.SILVER_ARMOR:
            color_str = "Silver Armor"
            rule &= can_kill_silver_armor_flapper(team=team, stage=stage, height=height)

    return SonicHeroesMacroRule(child=rule, name=f"Kill {color_str} Flapper with {flapper.weapon} at {height.description} Height as Team: {team} in {stage.stage_name}")


def can_remove_shield(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_homing_attack_rule(team=team, stage=stage, level=3) | (can_tornado_rule(team=team, stage=stage, level=0) | can_rocket_accel_rule(team=team, stage=stage, num_other_chars=1)) | can_team_blast_rule(team=team, stage=stage), name=f"Remove shield as Team: {team} in {stage.stage_name}")


def can_kill_basic_egg_pawn(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_jump_rule(team=team, stage=stage) | can_homing_attack_rule(team=team, stage=stage, level=0) | can_kick(team=team, stage=stage) | can_auto_power_attack_rule(team=team, stage=stage) | can_break_things_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage)


def can_kill_egg_pawn_bazooka(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_kill_basic_egg_pawn(team=team, stage=stage)


def can_kill_egg_pawn_lance(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=0) | can_kick(team=team, stage=stage) | can_auto_power_attack_rule(team=team, stage=stage) | can_break_things_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage)


def can_kill_egg_pawn_machine_gun(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_homing_attack_rule(team=team, stage=stage, level=0) | can_kick(team=team, stage=stage) | can_auto_power_attack_rule(team=team, stage=stage) | can_break_things_rule(team=team, stage=stage) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage)


def can_break_concrete_shield(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_combo_finisher_rule(team=team, stage=stage, level=2) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage), name=f"Break Concrete Shield as Team: {team} in {stage.stage_name}")


def can_break_plain_shield(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_break_things_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage), name=f"Break Plain Shield as Team: {team} in {stage.stage_name}")


def can_break_spike_shield(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_break_things_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage), name=f"Break Spike Shield as Team: {team} in {stage.stage_name}")


def can_kill_regular_egg_pawn(team: Team, stage: Stage, pawn: EggPawn, is_king: bool = False, is_casino: bool = False) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=pawn)
    enemy_str: str = ""
    if is_king:
        enemy_str += "King "
    if is_casino:
        enemy_str += "Casino "
    enemy_str += "Egg Pawn"

    match pawn.shield:
        case EggPawnShield.NO_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= can_kill_basic_egg_pawn(team=team, stage=stage)
                case EggPawnWeapon.BAZOOKA:
                    rule &= can_kill_egg_pawn_bazooka(team=team, stage=stage)
                case EggPawnWeapon.LANCE:
                    rule &= can_kill_egg_pawn_lance(team=team, stage=stage)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= can_kill_egg_pawn_machine_gun(team=team, stage=stage)
        case EggPawnShield.CONCRETE_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_concrete_shield(team=team, stage=stage)) & can_kill_basic_egg_pawn(team=team, stage=stage)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_concrete_shield(team=team, stage=stage)) & can_kill_egg_pawn_bazooka(team=team, stage=stage)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_concrete_shield(team=team, stage=stage)) & can_kill_egg_pawn_lance(team=team, stage=stage)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_concrete_shield(team=team, stage=stage)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage)
        case EggPawnShield.PLAIN_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_plain_shield(team=team, stage=stage)) & can_kill_basic_egg_pawn(team=team, stage=stage)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_plain_shield(team=team, stage=stage)) & can_kill_egg_pawn_bazooka(team=team, stage=stage)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_plain_shield(team=team, stage=stage)) & can_kill_egg_pawn_lance(team=team, stage=stage)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_plain_shield(team=team, stage=stage)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage)
        case EggPawnShield.SPIKE_SHIELD:
            match pawn.weapon:
                case EggPawnWeapon.NO_WEAPON:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_spike_shield(team=team, stage=stage)) & can_kill_basic_egg_pawn(team=team, stage=stage)
                case EggPawnWeapon.BAZOOKA:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_spike_shield(team=team, stage=stage)) & can_kill_egg_pawn_bazooka(team=team, stage=stage)
                case EggPawnWeapon.LANCE:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_spike_shield(team=team, stage=stage)) & can_kill_egg_pawn_lance(team=team, stage=stage)
                case EggPawnWeapon.MACHINE_GUN:
                    rule &= (can_remove_shield(team=team, stage=stage) | can_break_spike_shield(team=team, stage=stage)) & can_kill_egg_pawn_machine_gun(team=team, stage=stage)

    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} with {pawn.shield} and {pawn.weapon} as Team: {team} in {stage.stage_name}")


def can_kill_casino_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    return can_kill_regular_egg_pawn(team=team, stage=stage, pawn=pawn, is_casino=True)


def can_kill_king_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    return can_kill_regular_egg_pawn(team=team, stage=stage, pawn=pawn, is_king=True)


def can_kill_egg_pawn(team: Team, stage: Stage, pawn: EggPawn) -> Rule[SonicHeroesWorldBase]:
    match pawn.special_type:
        case EggPawnType.REGULAR_PAWN:
            return can_kill_regular_egg_pawn(team=team, stage=stage, pawn=pawn)
        case EggPawnType.KING_PAWN:
            return can_kill_king_egg_pawn(team=team, stage=stage, pawn=pawn)
        case EggPawnType.CASINO_PAWN_1:
            return can_kill_casino_egg_pawn(team=team, stage=stage, pawn=pawn)
        case EggPawnType.CASINO_PAWN_2:
            return can_kill_casino_egg_pawn(team=team, stage=stage, pawn=pawn)


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
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team: {team} in {stage.stage_name}")


def can_kill_falco(team: Team, stage: Stage, falco: Falco) -> Rule[SonicHeroesWorldBase]:
    """
    Not intending to route falco's as they are annoying
    """
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=falco)
    rule &= can_jump_rule(team=team, stage=stage) & can_thundershoot_rule(team=team, stage=stage, level=2)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Falco as Team: {team} in {stage.stage_name}")


def can_kill_regular_egg_hammer(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return can_belly_flop_rule(team=team, stage=stage, level=3) | can_fire_dunk_rule(team=team, stage=stage, level=3) | can_combo_finisher_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)


def can_knock_down_heavy_egg_hammer(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return SonicHeroesMacroRule(child=can_jump_rule(team=team, stage=stage) | can_homing_attack_rule(team=team, stage=stage, level=0) | can_belly_flop_rule(team=team, stage=stage, level=0) | can_fire_dunk_rule(team=team, stage=stage, level=0) | can_thundershoot_rule(team=team, stage=stage, level=1) | can_team_blast_rule(team=team, stage=stage), name=f"Knock Down Egg Hammer as Team: {team} in {stage.stage_name}")


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
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team: {team} in {stage.stage_name}")


def can_kill_regular_cameron(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return (can_remove_shield(team=team, stage=stage) & can_kill_basic_egg_pawn(team=team, stage=stage)) | can_break_things_rule(team=team, stage=stage) | can_team_blast_rule(team=team, stage=stage)


def can_kill_gold_cameron(team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
    return (can_remove_shield(team=team, stage=stage) & can_kill_basic_egg_pawn(team=team, stage=stage)) | can_team_blast_rule(team=team, stage=stage)


def can_kill_cameron(team: Team, stage: Stage, cameron: Cameron) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=cameron)
    enemy_str: str = ""
    match cameron.special_type:
        case CameronType.REGULAR_CAMERON:
            enemy_str = "Cameron"
            rule &= can_kill_regular_cameron(team=team, stage=stage)
        case CameronType.GOLD_CAMERON:
            enemy_str = "Gold Cameron"
            rule &= can_kill_gold_cameron(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team: {team} in {stage.stage_name}")


def can_kill_rhino(team: Team, stage: Stage, rhino: Rhino) -> Rule[SonicHeroesWorldBase]:
    """
    Dont want to route these
    """
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=rhino)
    rule &= can_thundershoot_rule(team=team, stage=stage, level=2) | can_team_blast_rule(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Rhino as Team: {team} in {stage.stage_name}")


def can_kill_egg_bishop(team: Team, stage: Stage, bishop: EggBishop) -> Rule[SonicHeroesWorldBase]:
    rule: Rule[SonicHeroesWorldBase] = has_enemy_obj(team=team, stage=stage, enemy=bishop)
    rule &= can_homing_attack_rule(team=team, stage=stage, level=2) | can_belly_flop_rule(team=team, stage=stage, level=2) | can_fire_dunk_rule(team=team, stage=stage, level=2) | can_combo_finisher_rule(team=team, stage=stage, level=2) | can_thundershoot_rule(team=team, stage=stage, level=3) | can_team_blast_rule(team=team, stage=stage)
    return SonicHeroesMacroRule(child=rule, name=f"Kill Egg Bishop as Team: {team} in {stage.stage_name}")


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
    return SonicHeroesMacroRule(child=rule, name=f"Kill {enemy_str} as Team: {team} in {stage.stage_name}")


