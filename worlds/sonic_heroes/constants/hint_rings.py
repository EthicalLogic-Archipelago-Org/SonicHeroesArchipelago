"""
Constants related to Hint Rings
"""
import dataclasses

from rule_builder.rules import Rule

from .stage_objs import StageObj, StageObjBase
from ..helper_functions import get_default_true_rule
from ..world_base import SonicHeroesWorldBase


HINT_RING: str = "Hint Ring"
HINT_RINGS: str = "Hint Rings"

@dataclasses.dataclass(kw_only=True)
class HintRingData(StageObjBase):
    voice_line: int
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.HINT_RING)


