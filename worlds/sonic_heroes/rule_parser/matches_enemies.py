"""

"""
from typing import Callable

from worlds.sonic_heroes.constants.enemies import EggFlapper, EggFlapperArmor, EggFlapperWeapon, EnemyHeight

from .parser_functions import get_func_str
from ..constants.char_ability import Team
from ..constants.stage import Stage



PARSER_ENEMY_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "RedFlapper": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggFlapper(armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON)}),
    "KillRedFlapperJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.NO_WEAPON), "height": EnemyHeight.JUMP}),

    "GreenShot": lambda team, stage: get_func_str(func_name="has_enemy_obj", params={"team": team, "stage": stage, "enemy": EggFlapper(armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.SHOT)}),
    "KillGreenShotJump": lambda team, stage: get_func_str(func_name="can_kill_egg_flapper", params={"team": team, "stage": stage, "flapper": EggFlapper(armor=EggFlapperArmor.NO_ARMOR, weapon=EggFlapperWeapon.SHOT), "height": EnemyHeight.JUMP}),

}