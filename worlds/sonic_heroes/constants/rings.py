"""
Constants related to Rings
"""
import dataclasses
import enum

from rule_builder.rules import Rule

from .stage_objs import DEFAULT_STAGE_OBJ_COORD, StageObj, StageObjBase
from ..helper_functions import get_default_true_rule
from ..world_base import SonicHeroesWorldBase


RING: str = "Ring"
RINGS: str = "Rings"
RING_GROUP: str = "Ring Group"


class RingLayout(enum.StrEnum):
    NORMAL = "Normal"
    LINE = "Line"
    CIRCLE = "Circle"
    ARCH = "Arch"
    WARP_TO_PLAYER_IF_AT_SPAWN = "WarpToPlayerIfAtSpawn"
    SCATTERED = WARP_TO_PLAYER_IF_AT_SPAWN


@dataclasses.dataclass(kw_only=True)
class RingData(StageObjBase):
    layout: RingLayout
    num_rings: int
    length: float = DEFAULT_STAGE_OBJ_COORD
    radius: float = DEFAULT_STAGE_OBJ_COORD
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)
    id_offset: int = 0

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.RINGS)