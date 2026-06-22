"""
Constants related to Locations, Regions, and Connections
"""
from __future__ import annotations
import dataclasses
import enum
from typing import override, Any, TYPE_CHECKING

from rule_builder.rules import Rule
from worlds.sonic_heroes.constants.rings import RING_GROUP
from worlds.sonic_heroes.options import RingSanityDark

from ..helper_functions import get_default_true_rule, is_this_act_enabled, is_this_specific_act_enabled, is_this_team_enabled

# if TYPE_CHECKING:
from .char_ability import Team
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
ENEMY_SANITY_LOCATION_GROUP: str = "EnemySanity"
HINT_RING_SANITY_LOCATION_GROUP: str = "HintRingSanity"
ITEM_BALLOON_BOX_SANITY_LOCATION_GROUP: str = "ItemBalloonBoxSanity"
RING_SANITY_LOCATION_GROUP: str = "RingSanity"
BINGO_CHIP_SANITY_LOCATION_GROUP: str = "BingoChipSanity"


MENU_REGION_NAME: str = "Menu"
METAL_OVERLORD_REGION_NAME: str = "Metal Overlord"



class LocationType(enum.StrEnum):
    LEVEL = "Level"
    BOSS = "Boss"
    EMERALD = "Emerald"
    OBJ_SANITY = "ObjSanity"
    KEY_SANITY = "KeySanity"
    CHECKPOINT_SANITY = "CheckpointSanity"
    BINGO_CHIP_SANITY = "BingoChipSanity"
    HINT_RING_SANITY = "HintRingSanity"
    ITEM_BALLOON_BOX_SANITY = "ItemBalloonBoxSanity"
    ENEMY_SANITY = "EnemySanity"
    RING_SANITY_GROUP = "RingSanityGroup"
    RING_SANITY_INDIVIDUAL = "RingSanityIndividual"

    EVENT = "Event Location"

    @property
    def is_actual_location(self) -> bool:
        return self.value != self.EVENT

    @property
    def is_sanity_location(self) -> bool:
        return self.value not in [self.LEVEL, self.BOSS, self.EMERALD, self.EVENT]


    @classmethod
    def get_sanity_types(cls) -> list[LocationType]:
        return \
    [
        LocationType.OBJ_SANITY,
        LocationType.KEY_SANITY,
        LocationType.CHECKPOINT_SANITY,
        LocationType.BINGO_CHIP_SANITY,
        LocationType.HINT_RING_SANITY,
        LocationType.ITEM_BALLOON_BOX_SANITY,
        LocationType.ENEMY_SANITY,
        LocationType.RING_SANITY_GROUP,
        LocationType.RING_SANITY_INDIVIDUAL,
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

            case LocationType.KEY_SANITY | LocationType.CHECKPOINT_SANITY | LocationType.HINT_RING_SANITY | LocationType.ITEM_BALLOON_BOX_SANITY | LocationType.ENEMY_SANITY | LocationType.BINGO_CHIP_SANITY:
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









