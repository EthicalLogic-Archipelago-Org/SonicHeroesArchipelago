"""
Parsed Data Mapping for Regions
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.loc_region import SonicHeroesRegionData
from ..constants.stage import Stage


parser_region_mapping: dict[Stage, dict[Team, list[SonicHeroesRegionData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkRegions.REGIONS,  # pyright: ignore[reportAny]
        }
}




