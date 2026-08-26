"""
Constants related to Triple Spring
"""
import dataclasses
import enum

from rule_builder.rules import Rule


from .char_ability import Team
from .item_balloon_box import ItemReward
from .stage import Stage
from .stage_objs import StageObjBase, StageObj
from ..helper_functions import get_default_true_rule
from ..world_base import SonicHeroesWorldBase


TRIPLE_SPRING: str = "Triple Spring"



@dataclasses.dataclass
class TripleSpringData(StageObjBase):
    power: float
    no_control_time: int
    item: ItemReward
    scale: float = 0

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.TRIPLE_SPRING)





