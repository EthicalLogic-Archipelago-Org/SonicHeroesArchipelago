"""
Constants related to Hint Rings
"""
import dataclasses

from rule_builder.rules import Rule


from .char_ability import Team
from .stage import Stage
from ..helper_functions import get_default_true_rule
from ..world_base import SonicHeroesWorldBase


HINT_RING: str = "Hint Ring"
HINT_RINGS: str = "Hint Rings"

@dataclasses.dataclass
class HintRingData:
    team: Team
    stage: Stage
    region_name: str
    voice_line: int
    x: float
    y: float
    z: float
    rule: Rule[SonicHeroesWorldBase] = get_default_true_rule()

    @property
    def pos(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z