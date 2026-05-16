"""
Constants related to Items and Events
"""
import enum

PLAYABLE: str = "Playable"
CHAOS_EMERALD: str = "Chaos Emerald"
EMBLEM: str = "Emblem"
UT_GLITCH_ITEM: str = "UT Glitch Item"

ITEM_START_ID_OFFSET = 0x0
ITEM_START_ID = ITEM_START_ID_OFFSET + 0x1

EVENT_LOCATION_ID: int = -999999 #not used as this is event
LEVEL_GOAL_ALL_TEAMS_EVENT_ITEM = "Level Completion Event Item"
LEVEL_GOAL_PER_TEAM_EVENT_ITEM_WITHOUT_TEAM = "Level Completion Event Item For Team"

BOBSLED_ITEM_NAME: str = "Bobsled"


class ChaosEmerald(enum.StrEnum):
    GREEN = f"Green {CHAOS_EMERALD}"
    BLUE = f"Blue {CHAOS_EMERALD}"
    YELLOW = f"Yellow {CHAOS_EMERALD}"
    WHITE = f"White {CHAOS_EMERALD}"
    CYAN = f"Cyan {CHAOS_EMERALD}"
    PURPLE = f"Purple {CHAOS_EMERALD}"
    RED = f"Red {CHAOS_EMERALD}"
