"""

"""
from typing import Callable

from ..constants.char_ability import Team
from ..constants.enemies import EggFlapper, EggFlapperArmor, EggFlapperWeapon, EggPawn, EggPawnShield, EggPawnType, EggPawnWeapon, EnemyHeight
from ..constants.stage import Stage
from .matches_functions import get_func_str


PARSER_ENEMY_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "RedFlapper": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON)}),
    "KillRedFlapperGround": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON, height=EnemyHeight.GROUND)}),
    "KillRedFlapperHalfJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON, height=EnemyHeight.HALF_JUMP)}),
    "KillRedFlapperJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON, height=EnemyHeight.JUMP)}),
    # "KillRedFlapperJumpHomingOnly"

    "GreenFlapperBazooka": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.BAZOOKA)}),
    "KillGreenFlapperBazookaHalfJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.BAZOOKA, height=EnemyHeight.HALF_JUMP)}),
    "KillGreenFlapperBazookaJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.BAZOOKA, height=EnemyHeight.JUMP)}),
    "KillGreenFlapperBazookaJumpHomingOnly": lambda team, stage: get_func_str(func_name="can_kill_green_shot_flapper_homing_only", params={"team": team, "stage": stage}),
    "KillGreenFlapperBazookaTallCharJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(team=team, stage=stage, armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.BAZOOKA, height=EnemyHeight.TALL_CHAR_JUMP)}),



    "EggPawnNothing": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD)}),

    "KillEggPawnNothing": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN, height=EnemyHeight.GROUND)}),
    "KillEggPawnNothingJump": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN, height=EnemyHeight.JUMP)}),
    "KillEggPawnNothingBobsled": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn_with_bobsled", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN)}),
    "KillEggPawnNothingSHFirstBobsled": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn_with_seaside_hill_first_bobsled", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.NO_WEAPON, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN)}),

    "EggPawnBazooka": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.BAZOOKA, shield=EggPawnShield.NO_SHIELD)}),
    "KillEggPawnBazooka": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.BAZOOKA, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN, height=EnemyHeight.GROUND)}),

    "EggPawnLance": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.LANCE, shield=EggPawnShield.NO_SHIELD)}),
    "KillEggPawnLance": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.LANCE, shield=EggPawnShield.NO_SHIELD, special_type=EggPawnType.REGULAR_PAWN, height=EnemyHeight.GROUND)}),

    "EggPawnLanceConcreteShield": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.LANCE, shield=EggPawnShield.CONCRETE_SHIELD)}),
    "KillEggPawnLanceConcreteShield": lambda team, stage: get_func_str(func_name="can_kill_egg_pawn", params={"team": team, "stage": stage, "pawn": EggPawn(team=team, stage=stage, weapon=EggPawnWeapon.LANCE, shield=EggPawnShield.CONCRETE_SHIELD, special_type=EggPawnType.REGULAR_PAWN, height=EnemyHeight.GROUND)}),














}