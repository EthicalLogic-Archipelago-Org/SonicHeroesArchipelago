from types import ModuleType

from . import SeasideHill, OceanPalace, GrandMetropolis, PowerPlant, CasinoPark, BingoHighway, RailCanyon, BulletStation, FrogForest, LostJungle, HangCastle, MysticMansion, EggFleet, FinalFortress
from ..constants.char_ability import Team
from ..constants.stage import Stage


csv_data_mapping: dict[Stage, dict[Team, ModuleType]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.SONIC: SeasideHill.Sonic,
            Team.DARK: SeasideHill.Dark,
            Team.ROSE: SeasideHill.Rose,
            Team.CHAOTIX: SeasideHill.Chaotix,
            Team.SUPER_HARD_MODE: SeasideHill.SuperHardMode,
            Team.ANY_TEAM: SeasideHill.AnyTeam,
        },
    Stage.OCEAN_PALACE:
        {
            Team.SONIC: OceanPalace.Sonic,
            Team.DARK: OceanPalace.Dark,
            Team.ROSE: OceanPalace.Rose,
            Team.CHAOTIX: OceanPalace.Chaotix,
            Team.SUPER_HARD_MODE: OceanPalace.SuperHardMode,
            Team.ANY_TEAM: OceanPalace.AnyTeam,
        },
}




