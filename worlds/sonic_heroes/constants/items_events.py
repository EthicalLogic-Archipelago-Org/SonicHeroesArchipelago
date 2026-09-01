"""
Constants related to Items and Events
"""
import dataclasses
import enum
from typing import override, Any

import BaseClasses

FORCE_UNLOCK: str = "Force Unlock"
FORCE_LOCK: str = "Force Lock"

PROGRESSIVE: str = "Progressive"
PLAYABLE: str = "Playable"
CHAOS_EMERALD: str = "Chaos Emerald"
EMBLEM: str = "Emblem"
UT_GLITCH_ITEM: str = "UT Glitch Item"

ITEM_START_ID_OFFSET: int = 0x0
ITEM_START_ID: int = ITEM_START_ID_OFFSET + 0x1

BONUS_KEY: str = "Bonus Key"

EVENT_LOCATION_ID: int = -999999 #not used as this is event
EVENT: str = "Event"
EVENT_LOCATION: str = f"{EVENT} Location"
EVENT_ITEM: str = f"{EVENT} Item"
LEVEL_COMPLETION: str = "Level Completion"

LEVEL_GOAL_ALL_TEAMS_EVENT_ITEM: str = f"{LEVEL_COMPLETION} {EVENT_ITEM}"
LEVEL_GOAL_PER_TEAM_EVENT_ITEM_WITHOUT_TEAM: str = f"{LEVEL_COMPLETION} {EVENT_ITEM} For Team"

OBJ_SANITY: str = f"ObjSanity"
OBJ_SANITY_EVENT_ITEM: str = f"{OBJ_SANITY} {EVENT_ITEM}"
DARK_OBJ_SANITY_AMOUNT: int = 100
ROSE_OBJ_SANITY_AMOUNT: int = 200


SPAWN_POSITION: str = "Spawn Position"

FILLER_ITEM_GROUP: str = "Filler"
TRAP_ITEM_GROUP: str = "Trap"
EMBLEM_ITEM_GROUP: str = "Emblem"
EMERALD_ITEM_GROUP: str = "Emerald"
CHARACTER_ITEM_GROUP: str = "Character"
ABILITY_ITEM_GROUP: str = "Ability"
STAGE_OBJECT_ITEM_GROUP: str = "Stage Object"
BOBSLED_ITEM_GROUP: str = "Bobsled"
SPAWN_POSITION_ITEM_GROUP: str = f"{SPAWN_POSITION}"





BOBSLED_ITEM_NAME: str = "Bobsled"


EXTRA_LIFE: str = "Extra Life"
RINGS_5: str = "5 Ring Bundle"
RINGS_10: str = "10 Ring Bundle"
RINGS_20: str = "20 Ring Bundle"
SHIELD: str = "Shield"
INVINCIBILITY: str = "Invincibility"
SPEED_LEVEL_UP: str = "Speed Level Up"
POWER_LEVEL_UP: str = "Power Level Up"
FLYING_LEVEL_UP: str = "Flying Level Up"
TEAM_LEVEL_UP: str = "Team Level Up"
TEAM_BLAST_REFILL: str = "Team Blast Refill"
RING_MAGNET: str = "Ring Magnet"

TRAP: str = "Trap"
STEALTHTRAP: str = f"Stealth {TRAP}"
FREEZETRAP: str = f"Freeze {TRAP}"
NOSWAPTRAP: str = f"No Swap {TRAP}"
RINGTRAP: str = f"Ring {TRAP}"
CHARMYTRAP: str = f"Charmy {TRAP}"


@dataclasses.dataclass(kw_only=True, frozen=True)
class SonicHeroesItemData:
    item_name: str
    code: int = dataclasses.field(metadata={'hex_num': lambda value: f"0x{value:X}"})  # pyright: ignore[reportUnknownLambdaType]
    classification: BaseClasses.ItemClassification = BaseClasses.ItemClassification.useful
    amount: int = 1
    fillerweight: int = 50

    @override
    def __repr__(self) -> str:
        """Returns a string representation of this object (with hex for the code)"""

        def get_formatted_field(class_field: dataclasses.Field[SonicHeroesItemData]) -> str:
            hex_formatter: Any = class_field.metadata.get('hex_num', repr)  # pyright: ignore[reportAny, reportExplicitAny]
            return f"{class_field.name}={hex_formatter(self.__getattribute__(class_field.name))}"

        class_fields: tuple[dataclasses.Field[Any], ...] = dataclasses.fields(class_or_instance=self)  # pyright: ignore[reportExplicitAny]
        formatted_fields: list[str] = []
        for field in class_fields:
            if field.repr:
                formatted_fields.append(get_formatted_field(class_field=field))

        return f"{self.__class__.__name__}({", ".join(formatted_fields)})"



class ChaosEmerald(enum.StrEnum):
    GREEN = f"Green {CHAOS_EMERALD}"
    BLUE = f"Blue {CHAOS_EMERALD}"
    YELLOW = f"Yellow {CHAOS_EMERALD}"
    WHITE = f"White {CHAOS_EMERALD}"
    CYAN = f"Cyan {CHAOS_EMERALD}"
    PURPLE = f"Purple {CHAOS_EMERALD}"
    RED = f"Red {CHAOS_EMERALD}"
