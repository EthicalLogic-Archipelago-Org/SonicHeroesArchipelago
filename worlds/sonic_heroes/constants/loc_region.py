"""
Constants related to Locations, Regions, and Connections
"""
from __future__ import annotations
import dataclasses
import enum
from typing import override, Any, TYPE_CHECKING, Self

from rule_builder.rules import Rule

from ..helper_functions import get_default_true_rule, is_this_act_enabled, is_this_specific_act_enabled, is_this_team_enabled
from ..options import RingSanityDark

from .char_ability import Team
from .rings import RING_GROUP
from .stage import Act, Stage

from ..world_base import SonicHeroesWorldBase

LOCATION_START_ID_OFFSET: int = 0x0
LOCATION_START_ID: int = LOCATION_START_ID_OFFSET + 0xA0 #MUST start with 0xA0


STAGE_LOCATION_GROUP: str = "Stage"
BOSS_LOCATION_GROUP: str = "Boss"
EMERALD_LOCATION_GROUP: str = "Emerald"
OBJ_SANITY_LOCATION_GROUP: str = "ObjSanity"
KEY_SANITY_LOCATION_GROUP: str = "KeySanity"
CHECKPOINT_SANITY_LOCATION_GROUP: str = "CheckpointSanity"

EGG_FLAPPER_SANITY_LOCATION_GROUP = "EggFlapperSanity"
EGG_PAWN_SANITY_LOCATION_GROUP = "EggPawnSanity"
KLAGEN_SANITY_LOCATION_GROUP = "KlagenSanity"
FALCO_SANITY_LOCATION_GROUP = "FalcoSanity"
EGG_HAMMER_SANITY_LOCATION_GROUP = "EggHammerSanity"
CAMERON_SANITY_LOCATION_GROUP = "CameronSanity"
RHINO_LINER_SANITY_LOCATION_GROUP = "RhinoLinerSanity"
EGG_BISHOP_SANITY_LOCATION_GROUP = "EggBishopSanity"
E2000_SANITY_LOCATION_GROUP = "E2000Sanity"

HINT_RING_SANITY_LOCATION_GROUP: str = "HintRingSanity"
ITEM_BOX_SANITY_LOCATION_GROUP: str = "ItemBoxSanity"
ITEM_BALLOON_SANITY_LOCATION_GROUP: str = "ItemBalloonSanity"
RING_SANITY_LOCATION_GROUP: str = "RingSanity"
BINGO_CHIP_SANITY_LOCATION_GROUP: str = "BingoChipSanity"


REGION: str = "Region"
CONNECTION: str = "Connection"
MENU_REGION_NAME: str = "Menu"
METAL_OVERLORD_REGION_NAME: str = "Metal Overlord"


@dataclasses.dataclass(frozen=True, kw_only=True)
class _LocationType:
    type_name: str
    sort_key: str
    is_real: bool = True
    is_sanity: bool = False


class LocationType(enum.Enum):
    LEVEL = _LocationType(type_name="Level", sort_key="9996") #third to last
    BOSS = _LocationType(type_name="Boss", sort_key="9997") # second to last
    EMERALD = _LocationType(type_name="Emerald", sort_key="9998")  # last

    OBJ_SANITY = _LocationType(type_name="ObjSanity", sort_key="9900", is_sanity=True) # last sanity (before goals/emerald)
    KEY_SANITY = _LocationType(type_name="KeySanity", sort_key="0010", is_sanity=True) # second sanity (after checkpoint)
    CHECKPOINT_SANITY = _LocationType(type_name="CheckpointSanity", sort_key="0000", is_sanity=True) # first sanity
    BINGO_CHIP_SANITY = _LocationType(type_name="BingoChipSanity", sort_key="0050", is_sanity=True) # fourth sanity
    HINT_RING_SANITY = _LocationType(type_name="HintRingSanity", sort_key="0040", is_sanity=True) #fifth sanity
    ITEM_BOX_SANITY = _LocationType(type_name="ItemBoxSanity", sort_key="0060", is_sanity=True) # sixth sanity
    ITEM_BALLOON_SANITY = _LocationType(type_name="ItemBalloonSanity", sort_key="0070", is_sanity=True) #seventh sanity

    EGG_FLAPPER_SANITY = _LocationType(type_name="EggFlapperSanity", sort_key="9900", is_sanity=True) # first enemy sanity (last in order before OBJ)
    EGG_PAWN_SANITY = _LocationType(type_name="EggPawnSanity", sort_key="9910", is_sanity=True) # second enemy sanity (last in order before OBJ)
    KLAGEN_SANITY = _LocationType(type_name="KlagenSanity", sort_key="9920", is_sanity=True) # third enemy sanity
    FALCO_SANITY = _LocationType(type_name="FalcoSanity", sort_key="9930", is_sanity=True)  # fourth enemy sanity
    EGG_HAMMER_SANITY = _LocationType(type_name="EggHammerSanity", sort_key="9940", is_sanity=True)  # fifth enemy sanity
    CAMERON_SANITY = _LocationType(type_name="CameronSanity", sort_key="9950", is_sanity=True)  # sixth enemy sanity
    RHINO_LINER_SANITY = _LocationType(type_name="RhinoLinerSanity", sort_key="9960", is_sanity=True)  # seventh enemy sanity
    EGG_BISHOP_SANITY = _LocationType(type_name="EggBishopSanity", sort_key="9970", is_sanity=True)  # eighth enemy sanity
    E2000_SANITY = _LocationType(type_name="E2000Sanity", sort_key="9980", is_sanity=True)  # ninth enemy sanity

    RING_SANITY_GROUP = _LocationType(type_name="RingSanityGroup", sort_key="0020", is_sanity=True)  # third sanity
    RING_SANITY_INDIVIDUAL = _LocationType(type_name="RingSanityIndividual", sort_key="0030", is_sanity=True)  # third sanity

    EVENT = _LocationType(type_name="Event Location", sort_key="9999", is_real=False)  # should not show up in UT



    def __new__(cls, data: _LocationType) -> Self:
        obj = object.__new__(cls)
        obj._value_ = data
        return obj

    def __init__(self, data: _LocationType) -> None:
        self.type_name: str = data.type_name
        self.sort_key: str = data.sort_key
        self.is_real: bool = data.is_real
        self.is_sanity: bool = data.is_sanity


    @classmethod
    def get_sanity_types(cls) -> list[LocationType]:
        return \
        [
            loc_type for loc_type in cls if loc_type.is_sanity # and loc_type.is_real
        ]



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


    @override
    def __repr__(self) -> str:
        """Returns a string representation of this object (with hex for the code)"""
        def get_formatted_field(class_field: dataclasses.Field[SonicHeroesLocationData]) -> str:
            hex_formatter: Any = class_field.metadata.get('hex_num', repr)  # pyright: ignore[reportAny, reportExplicitAny]
            return f"{class_field.name}={hex_formatter(self.__getattribute__(class_field.name))}"

        class_fields: tuple[dataclasses.Field[Any], ...] = dataclasses.fields(class_or_instance=self)  # pyright: ignore[reportExplicitAny]
        formatted_fields: list[str] = []
        for field in class_fields:
            if field.repr:
                formatted_fields.append(get_formatted_field(class_field=field))

        return f"{self.__class__.__name__}({", ".join(formatted_fields)})"


    def is_enabled(self, world: SonicHeroesWorldBase) -> bool:
        if self.act == 0:
            if self.team is not Team.ANY_TEAM and not is_this_team_enabled(world=world, team=self.team):
                return False
        else:
            if not is_this_act_enabled(world=world, team=self.team, act=Act(value=self.act)):
                return False

        match self.loc_type:
            case LocationType.LEVEL:
                return is_this_specific_act_enabled(world=world, team=self.team, act=Act(value=self.act))
            case LocationType.BOSS:
                return False
            case LocationType.EMERALD:
                return True
            case LocationType.OBJ_SANITY:
                # TODO handle check size here
                return is_this_act_enabled(world=world, team=self.team, act=Act(value=self.act)) and self.act & world.enabled_sanity_acts[self.team][self.loc_type] > 0  # pyright: ignore[reportAny]

            case LocationType.KEY_SANITY | LocationType.CHECKPOINT_SANITY | LocationType.HINT_RING_SANITY | LocationType.ITEM_BOX_SANITY | LocationType.ITEM_BALLOON_SANITY | LocationType.EGG_FLAPPER_SANITY | LocationType.EGG_PAWN_SANITY | LocationType.KLAGEN_SANITY | LocationType.FALCO_SANITY | LocationType.EGG_HAMMER_SANITY | LocationType.CAMERON_SANITY | LocationType.RHINO_LINER_SANITY | LocationType.EGG_BISHOP_SANITY | LocationType.E2000_SANITY | LocationType.BINGO_CHIP_SANITY:
                if Act(value=self.act) is Act.NONE:
                    #Only 1 Set
                    return world.enabled_sanity_acts[self.team][self.loc_type] is not Act.NONE and world.enabled_sanity_acts[self.team][self.loc_type] is not Act.BOTH_ACTS  # pyright: ignore[reportAny]
                return world.enabled_sanity_acts[self.team][self.loc_type] is Act.BOTH_ACTS  # pyright: ignore[reportAny]

            case LocationType.RING_SANITY_GROUP:
                should_add_group: bool = world.options.ring_sanity_dark == RingSanityDark.option_groups and RING_GROUP in self.name
                if Act(value=self.act) is Act.NONE:
                    # Only 1 Set
                    return should_add_group and world.enabled_sanity_acts[self.team][self.loc_type] is not Act.NONE and world.enabled_sanity_acts[self.team][self.loc_type] is not Act.BOTH_ACTS  # pyright: ignore[reportAny]
                return should_add_group and world.enabled_sanity_acts[self.team][self.loc_type] is Act.BOTH_ACTS  # pyright: ignore[reportAny]

            case LocationType.RING_SANITY_INDIVIDUAL:
                should_add_individual: bool = world.options.ring_sanity_dark == RingSanityDark.option_all_rings and RING_GROUP not in self.name
                if Act(value=self.act) is Act.NONE:
                    # Only 1 Set
                    return should_add_individual and world.enabled_sanity_acts[self.team][self.loc_type] is not Act.NONE and world.enabled_sanity_acts[self.team][self.loc_type] is not Act.BOTH_ACTS  # pyright: ignore[reportAny]
                return should_add_individual and world.enabled_sanity_acts[self.team][self.loc_type] is Act.BOTH_ACTS  # pyright: ignore[reportAny]


            case LocationType.EVENT:
                return True
        raise ValueError(f"LocationData is_enabled didnt return")




@dataclasses.dataclass
class SonicHeroesRegionData:
    region_name: str
    obj_checks: int


@dataclasses.dataclass(kw_only=True)
class SonicHeroesConnectionData:
    name: str
    """Connection Name"""
    source_region: str
    """Source Region Name"""
    target_region: str
    """Target Region Name"""
    rule: Rule[SonicHeroesWorldBase] = dataclasses.field(default_factory=get_default_true_rule)
    """Rule"""









