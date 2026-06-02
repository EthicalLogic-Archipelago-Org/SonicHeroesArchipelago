"""
Parsed Data Mapping for Enemies
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.enemies import *
from ..constants.stage import Stage


parser_enemy_mapping: dict[Stage, dict[Team, list[SonicHeroesEnemyBase]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkEnemies.ENEMIES,  # pyright: ignore[reportAny]
        }
}