"""
Parsed Data Mapping for Item Balloons/Boxes
"""

from . import SeasideHill, OceanPalace

from ..constants.char_ability import Team
from ..constants.item_balloon_box import ItemBalloonData, ItemBoxData
from ..constants.stage import Stage


parser_item_balloon_box_mapping: dict[Stage, dict[Team, list[ItemBalloonData | ItemBoxData]]] = \
{
    Stage.SEASIDE_HILL:
        {
            Team.DARK: SeasideHill.Dark.SeasideHillDarkItemBalloonBoxes.ITEM_BALLOON_BOXES,  # pyright: ignore[reportAny]
        }
}