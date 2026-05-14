"""
Constants related to Locations, Regions, and Connections
"""
from __future__ import annotations
import dataclasses
import enum
from typing import override, Any, TYPE_CHECKING

from rule_builder.rules import Rule

from ..helper_functions import get_default_true_rule

if TYPE_CHECKING:
    from .char_ability import Team
    from .stage import Stage

from ..world_base import SonicHeroesWorldBase

LOCATION_START_ID_OFFSET: int = 0x0
LOCATION_START_ID: int = LOCATION_START_ID_OFFSET + 0xA0 #MUST start with 0xA0

class LocationType(enum.StrEnum):
    LEVEL = "Level"
    BOSS = "Boss"
    EMERALD = "Emerald"
    OBJ_SANITY = "ObjSanity"
    KEY_SANITY = "KeySanity"
    CHECKPOINT_SANITY = "CheckpointSanity"
    ENEMY_SANITY = "EnemySanity"
    HINT_RING_SANITY = "HintRingSanity"
    ITEM_BOX_BALLOON_SANITY = "ItemBoxBalloonSanity"
    RING_SANITY = "RingSanity"
    BINGO_CHIP_SANITY = "BingoChipSanity"

    EVENT = "Event Location"

    @property
    def is_actual_location(self) -> bool:
        return self.value != self.EVENT

    @property
    def is_sanity_location(self) -> bool:
        return self.value not in [self.LEVEL, self.BOSS, self.EMERALD, self.EVENT]


@dataclasses.dataclass(kw_only=True)
class SonicHeroesLocationData:
    name: str
    team: Team
    stage: Stage
    code: int = dataclasses.field(metadata={'hex_num': lambda value: f"0x{value:X}"})  # pyright: ignore[reportUnknownLambdaType]
    act: int
    parent_region: str
    rule_str: str
    loc_type: LocationType
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)
    locked_item: str = f""


    def __post_init__(self) -> None:
        # TODO handle rule str to Rule
        pass


    @override
    def __repr__(self) -> str:
        """Returns a string representation of this object (with hex for the code)"""
        def get_formatted_field(class_field: dataclasses.Field[SonicHeroesLocationData]) -> str:
            hex_formatter: Any = class_field.metadata.get('hex_num', repr)  # pyright: ignore[reportAny, reportExplicitAny]
            return f"{class_field.name}={hex_formatter(self.__getattribute__(class_field.name))}"

        class_fields: tuple[dataclasses.Field[Any], ...] = dataclasses.fields(self)  # pyright: ignore[reportExplicitAny]
        formatted_fields: list[str] = []
        for field in class_fields:
            if field.repr:
                formatted_fields.append(get_formatted_field(field))

        return f"{self.__class__.__name__}({", ".join(formatted_fields)})"


@dataclasses.dataclass
class SonicHeroesRegionData:
    region_name: str

    location_list: list[SonicHeroesLocationData] = dataclasses.field(default_factory=list)
    """Could make this custom class obj (and match off of name or something)"""


@dataclasses.dataclass(kw_only=True)
class SonicHeroesConnectionData:
    name: str
    """Connection Name"""
    source_region: str
    """Source Region Name"""
    target_region: str
    """Target Region Name"""
    rule_str: str
    """str repr of Rule"""
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)


    def __post_init__(self) -> None:
        # TODO handle rule str to Rule
        pass









