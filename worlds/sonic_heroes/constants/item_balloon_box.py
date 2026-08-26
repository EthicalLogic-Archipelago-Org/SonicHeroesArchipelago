"""
Constants related to Hint Rings
"""
import dataclasses
import enum

from rule_builder.rules import Rule


from .char_ability import Team
from .stage import Stage
from .stage_objs import StageObjBase, StageObj
from ..helper_functions import get_default_true_rule
from ..world_base import SonicHeroesWorldBase


ITEM_BALLOON: str = "Item Balloon"
ITEM_BOX: str = "Item Box"


class ItemReward(enum.StrEnum):
    NoneItemBox = "NoneItemBox"
    Rings5 = "Rings5"
    Rings10 = "Rings10"
    Rings20 = "Rings20"
    Shield = "Shield"
    ExtraLife = "ExtraLife"
    SpeedShoes = "SpeedShoes"
    TeamBlastRefill = "TeamBlastRefill"
    Invincibility = "Invincibility"
    LevelUpSpeed = "LevelUpSpeed"
    LevelUpFly = "LevelUpFly"
    LevelUpPower = "LevelUpPower"
    RefillFlightGauge = "RefillFlightGauge"
    None3Spring = "None3Spring"



@dataclasses.dataclass
class ItemBoxData(StageObjBase):
    item: ItemReward

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.ITEM_BOX)


@dataclasses.dataclass
class ItemBalloonData(StageObjBase):
    item: ItemReward

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.ITEM_BALLOON)





