"""
Constants related to Hint Rings
"""
import dataclasses
import enum

from rule_builder.rules import Rule


from .char_ability import Team
from .stage import Stage
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
class ItemBalloonBoxData:
    team: Team
    stage: Stage
    region_name: str
    item: ItemReward
    x: float
    y: float
    z: float
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)

    @property
    def pos(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z





