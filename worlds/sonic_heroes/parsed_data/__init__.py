from types import ModuleType

from ..constants.enemies import SonicHeroesEnemyBase
from ..constants.hint_rings import HintRingData
from ..constants.item_balloon_box import ItemBalloonData, ItemBoxData
from ..constants.rings import RingData

from . import SeasideHill, OceanPalace
from .connection_mapping import parser_connection_mapping
from .enemy_mapping import parser_enemy_mapping
from .hint_ring_mapping import parser_hint_ring_mapping
from .item_balloon_box_mapping import parser_item_balloon_box_mapping
from .region_mapping import parser_region_mapping
from .ring_mapping import parser_ring_mapping

from ..constants.char_ability import Team
from ..constants.loc_region import SonicHeroesConnectionData, SonicHeroesRegionData
from ..constants.stage import Stage


parser_connection_mapping: dict[Stage, dict[Team, list[SonicHeroesConnectionData]]] = parser_connection_mapping


parser_enemy_mapping: dict[Stage, dict[Team, list[SonicHeroesEnemyBase]]] = parser_enemy_mapping


parser_hint_ring_mapping: dict[Stage, dict[Team, list[HintRingData]]] = parser_hint_ring_mapping


parser_item_balloon_box_mapping: dict[Stage, dict[Team, list[ItemBalloonData | ItemBoxData]]] = parser_item_balloon_box_mapping


parser_region_mapping: dict[Stage, dict[Team, list[SonicHeroesRegionData]]] = parser_region_mapping


parser_ring_mapping: dict[Stage, dict[Team, list[RingData]]] = parser_ring_mapping


parser_result_mapping: dict[Stage, dict[Team, ModuleType]] = \
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



__all__ = ["parser_connection_mapping", "parser_enemy_mapping", "parser_hint_ring_mapping", "parser_item_balloon_box_mapping", "parser_region_mapping", "parser_ring_mapping", "parser_result_mapping",]

