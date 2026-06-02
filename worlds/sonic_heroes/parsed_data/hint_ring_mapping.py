"""
Parsed Data Mapping for Hint Rings
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.hint_rings import HintRingData
from ..constants.stage import Stage


parser_hint_ring_mapping: dict[Stage, dict[Team, list[HintRingData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkHintRings.HINT_RINGS,  # pyright: ignore[reportAny]
        }
}