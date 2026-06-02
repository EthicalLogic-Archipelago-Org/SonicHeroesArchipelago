"""
Constants related to Items and Events
"""
import enum

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
ROSE_OBJ_SANITY_AMOUNT: int = 100


BOBSLED_ITEM_NAME: str = "Bobsled"


class ChaosEmerald(enum.StrEnum):
    GREEN = f"Green {CHAOS_EMERALD}"
    BLUE = f"Blue {CHAOS_EMERALD}"
    YELLOW = f"Yellow {CHAOS_EMERALD}"
    WHITE = f"White {CHAOS_EMERALD}"
    CYAN = f"Cyan {CHAOS_EMERALD}"
    PURPLE = f"Purple {CHAOS_EMERALD}"
    RED = f"Red {CHAOS_EMERALD}"
