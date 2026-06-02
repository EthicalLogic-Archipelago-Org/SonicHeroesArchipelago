"""
Parsed Data Mapping for Connections
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.loc_region import SonicHeroesConnectionData
from ..constants.stage import Stage


parser_connection_mapping: dict[Stage, dict[Team, list[SonicHeroesConnectionData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkConnections.CONNECTIONS,  # pyright: ignore[reportAny]
        }
}
