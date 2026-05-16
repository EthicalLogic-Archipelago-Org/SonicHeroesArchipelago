from types import ModuleType

from . import SeasideHill, OceanPalace
from ..constants.stage import Stage


parse_result_mapping: dict[Stage, ModuleType] = \
{
    Stage.SEASIDE_HILL: SeasideHill,
    Stage.OCEAN_PALACE: OceanPalace,
}






