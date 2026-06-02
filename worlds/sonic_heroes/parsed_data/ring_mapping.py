"""
Parsed Data Mapping for Rings
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.rings import RingData
from ..constants.stage import Stage


parser_ring_mapping: dict[Stage, dict[Team, list[RingData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkRings.RINGS,  # pyright: ignore[reportAny]
        }
}