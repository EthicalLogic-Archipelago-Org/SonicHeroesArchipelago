"""
Parsed Data Mapping for Triple Springs
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.triple_spring import TripleSpringData
from ..constants.stage import Stage


parser_triple_spring_mapping: dict[Stage, dict[Team, list[TripleSpringData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkTripleSprings.TRIPLE_SPRINGS,  # pyright: ignore[reportAny]
        }
}