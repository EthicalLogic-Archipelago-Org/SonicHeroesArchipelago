"""
generate items programmatically
"""

from BaseClasses import ItemClassification
from worlds.sonic_heroes.helper_functions import get_spawn_position_item_name
from .constants.char_ability import Character, Ability, Team
from .constants.items_events import *
from .constants.loc_region import *
from .constants.stage import Stage, StageType, Act
from .constants.stage_objs import StageObj

item_id: int = ITEM_START_ID
already_used_item_ids: list[int] = []
FULL_ITEM_LIST: list[SonicHeroesItemData] = []
FULL_ITEM_GROUPS: dict[str, set[str]] = \
{
    FILLER_ITEM_GROUP: set(),
    TRAP_ITEM_GROUP: set(),
    EMBLEM_ITEM_GROUP: set(),
    EMERALD_ITEM_GROUP: set(),
    CHARACTER_ITEM_GROUP: set(),
    ABILITY_ITEM_GROUP: set(),
    STAGE_OBJECT_ITEM_GROUP: set(),
    BOBSLED_ITEM_GROUP: set(),
    SPAWN_POSITION_ITEM_GROUP: set(),
}



def round_item_id_to_nearest_value_multiple(value: int) -> None:
    global item_id
    hex_mod: int = item_id % value
    if hex_mod > 0:
        print(f"Rounding Item Id to nearest {hex(value)} old id: {hex(item_id)} added: {hex(value - hex_mod)}")
        item_id += value - hex_mod
    else:
        print(f"Item Id doesn't need rounding. {hex(value)} old id: {hex(item_id)}")


def append_item(name: str, classification: ItemClassification, item_groups: list[str], amount: int = 1, fillerweight: int = 50, num_to_increment_id: int = 1) -> None:
    global item_id

    if item_id in already_used_item_ids:
        raise ValueError(f"DUPLICATE ITEM ID!! Item Name: {name} Code: {item_id}")
    already_used_item_ids.append(item_id)

    #append here
    FULL_ITEM_LIST.append(SonicHeroesItemData(item_name=name, code=item_id, classification=classification, amount=amount, fillerweight=fillerweight))

    for item_group in item_groups:
        FULL_ITEM_GROUPS[item_group].add(name)

    item_id += num_to_increment_id


def generate_emblem_item() -> None:
    global item_id
    item_id = ITEM_START_ID
    append_item(name=EMBLEM, classification=ItemClassification.progression, item_groups=[EMBLEM_ITEM_GROUP])


def generate_chaos_emerald_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 2
    for emerald in ChaosEmerald:
        append_item(name=emerald, classification=ItemClassification.progression, item_groups=[EMERALD_ITEM_GROUP])


def generate_playable_char_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 9
    for char in Character:
        append_item(name=char.get_playable_item_name(), classification=ItemClassification.progression, item_groups=[CHARACTER_ITEM_GROUP])


def generate_progressive_ability_items_for_team(team: Team) -> None:
    append_item(name=f"{PROGRESSIVE} {team.value} {Ability.HOMING_ATTACK.ability_name}", classification=ItemClassification.progression, item_groups=[ABILITY_ITEM_GROUP])
    append_item(name=f"{PROGRESSIVE} {team.value} {Ability.TORNADO.ability_name}", classification=ItemClassification.progression, item_groups=[ABILITY_ITEM_GROUP])

    append_item(name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}", classification=ItemClassification.progression, item_groups=[ABILITY_ITEM_GROUP])

    append_item(name=f"{PROGRESSIVE} {team.value} {Ability.POWER_ATTACK.ability_name}", classification=ItemClassification.progression, item_groups=[ABILITY_ITEM_GROUP])


def generate_ability_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 0x200
    for team in Team:
        round_item_id_to_nearest_value_multiple(value=0x200)
        for ability in Ability:
            item_name: str = f"{team.value} {ability.ability_name}" if team is not Team.ANY_TEAM else ability.ability_name
            append_item(name=item_name, classification=ItemClassification.progression, item_groups=[ABILITY_ITEM_GROUP])

        generate_progressive_ability_items_for_team(team=team)


def generate_stage_obj_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 0x1000
    for team in Team:
        round_item_id_to_nearest_value_multiple(value=0x1000)
        for stage_obj in StageObj:
            item_name: str = f"{team.value} {stage_obj.value}" if team is not Team.ANY_TEAM else stage_obj.value
            append_item(name=item_name, classification=ItemClassification.progression, item_groups=[STAGE_OBJECT_ITEM_GROUP])

    append_item(name=BOBSLED_ITEM_NAME, classification=ItemClassification.progression, item_groups=[BOBSLED_ITEM_GROUP])


def generate_spawn_position_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 0x7000
    for team in Team:
        if team is Team.ANY_TEAM:
            continue
        round_item_id_to_nearest_value_multiple(value=0x100)
        for reg_level in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            round_item_id_to_nearest_value_multiple(value=0x10)
            for checkpoint in range(reg_level.checkpoints[team] + 1):
                append_item(name=get_spawn_position_item_name(team=team, stage=reg_level, checkpoint=checkpoint), classification=ItemClassification.progression, item_groups=[SPAWN_POSITION_ITEM_GROUP])




def generate_filler_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 0x8000

    append_item(name=EXTRA_LIFE, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])
    append_item(name=RINGS_5, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])
    append_item(name=RINGS_10, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])
    append_item(name=RINGS_20, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])
    append_item(name=SHIELD, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])
    append_item(name=INVINCIBILITY, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP], fillerweight=0)
    append_item(name=SPEED_LEVEL_UP, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP], fillerweight=0)
    append_item(name=POWER_LEVEL_UP, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP], fillerweight=0)
    append_item(name=FLYING_LEVEL_UP, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP], fillerweight=0)
    append_item(name=TEAM_LEVEL_UP, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP], fillerweight=0)
    append_item(name=TEAM_BLAST_REFILL, classification=ItemClassification.filler, item_groups=[FILLER_ITEM_GROUP])


def generate_trap_items() -> None:
    global item_id
    item_id = ITEM_START_ID_OFFSET + 0x8100

    append_item(name=STEALTHTRAP, classification=ItemClassification.trap, item_groups=[TRAP_ITEM_GROUP])
    append_item(name=FREEZETRAP, classification=ItemClassification.trap, item_groups=[TRAP_ITEM_GROUP])
    append_item(name=NOSWAPTRAP, classification=ItemClassification.trap, item_groups=[TRAP_ITEM_GROUP])
    append_item(name=RINGTRAP, classification=ItemClassification.trap, item_groups=[TRAP_ITEM_GROUP])
    append_item(name=CHARMYTRAP, classification=ItemClassification.trap, item_groups=[TRAP_ITEM_GROUP])



def generate_item_list() -> None:
    generate_emblem_item()
    generate_chaos_emerald_items()
    generate_playable_char_items()
    generate_ability_items()
    generate_stage_obj_items()
    generate_spawn_position_items()

    generate_filler_items()
    generate_trap_items()
    pass



generate_item_list()





