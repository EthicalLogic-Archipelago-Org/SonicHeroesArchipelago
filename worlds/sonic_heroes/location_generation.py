"""
generate locations programmatically
"""
from _collections_abc import Sequence

from rule_builder.rules import Rule, True_, Has, False_

from .constants.char_ability import Team
from .constants.enemies import *
from .constants.items_events import *
from .constants.loc_region import *
from .constants.hint_rings import *
from .constants.item_balloon_box import ItemBoxData, ItemBalloonData
from .constants.rings import RING_GROUP, RingData
from .constants.stage import Stage, StageType, Act
from .constants.stage_objs import StageObj, STAGE_OBJ_INVALID_ID_OFFSET

from .rule_builder.custom_rules import CanGetEmerald, CanGoalStage
from .rule_builder.functions_stage_obj import has_stage_obj_rule, can_break_key_cage
from .helper_functions import get_obj_sanity_event_item_name
from .rule_parser.functions_parser import get_parsed_data_module_for_team_stage


loc_id: int = LOCATION_START_ID
already_used_loc_ids: list[int] = []
FULL_LOCATION_DICT: dict[Stage, dict[Team, list[SonicHeroesLocationData]]] = \
{
    stage:
    {
        team: []
        for team in Team
    }
    for stage in Stage
}

TEAM_STAGES_TO_GENERATE_SANITIES: dict[Team, list[Stage]] = \
{
    Team.ANY_TEAM: [],
    Team.SONIC: [],
    Team.DARK:
    [
        Stage.SEASIDE_HILL,
    ],
    Team.ROSE: [],
    Team.CHAOTIX: [],
    Team.SUPER_HARD_MODE: [],
}

FULL_LOCATION_GROUPS: dict[str, set[str]] = \
{
    STAGE_LOCATION_GROUP: set(),
    BOSS_LOCATION_GROUP: set(),
    EMERALD_LOCATION_GROUP: set(),
    OBJ_SANITY_LOCATION_GROUP: set(),
    KEY_SANITY_LOCATION_GROUP: set(),
    CHECKPOINT_SANITY_LOCATION_GROUP: set(),
    EGG_FLAPPER_SANITY_LOCATION_GROUP_GROUP: set(),
    EGG_FLAPPER_SANITY_LOCATION_GROUP_FULL: set(),
    EGG_PAWN_SANITY_LOCATION_GROUP_GROUP: set(),
    EGG_PAWN_SANITY_LOCATION_GROUP_FULL: set(),
    KLAGEN_SANITY_LOCATION_GROUP_GROUP: set(),
    KLAGEN_SANITY_LOCATION_GROUP_FULL: set(),
    FALCO_SANITY_LOCATION_GROUP_GROUP: set(),
    FALCO_SANITY_LOCATION_GROUP_FULL: set(),
    EGG_HAMMER_SANITY_LOCATION_GROUP_GROUP: set(),
    EGG_HAMMER_SANITY_LOCATION_GROUP_FULL: set(),
    CAMERON_SANITY_LOCATION_GROUP_GROUP: set(),
    CAMERON_SANITY_LOCATION_GROUP_FULL: set(),
    RHINO_LINER_SANITY_LOCATION_GROUP_GROUP: set(),
    RHINO_LINER_SANITY_LOCATION_GROUP_FULL: set(),
    EGG_BISHOP_SANITY_LOCATION_GROUP_GROUP: set(),
    EGG_BISHOP_SANITY_LOCATION_GROUP_FULL: set(),
    E2000_SANITY_LOCATION_GROUP_GROUP: set(),
    E2000_SANITY_LOCATION_GROUP_FULL: set(),
    HINT_RING_SANITY_LOCATION_GROUP_GROUP: set(),
    HINT_RING_SANITY_LOCATION_GROUP_FULL: set(),
    ITEM_BOX_SANITY_LOCATION_GROUP_GROUP: set(),
    ITEM_BOX_SANITY_LOCATION_GROUP_FULL: set(),
    ITEM_BALLOON_SANITY_LOCATION_GROUP_GROUP: set(),
    ITEM_BALLOON_SANITY_LOCATION_GROUP_FULL: set(),
    RING_SANITY_LOCATION_GROUP_GROUP: set(),
    RING_SANITY_LOCATION_GROUP_FULL: set(),
    BINGO_CHIP_SANITY_LOCATION_GROUP_GROUP: set(),
    BINGO_CHIP_SANITY_LOCATION_GROUP_FULL: set(),
}




RING_GROUP_NO_ACT_START_ID_OFFSET: int = 0x100000
RING_GROUP_ACT_A_START_ID_OFFSET: int = 0x110000
RING_GROUP_ACT_B_START_ID_OFFSET: int = 0x120000
RING_FULL_NO_ACT_START_ID_OFFSET: int = 0x130000
RING_FULL_ACT_A_START_ID_OFFSET: int = 0x140000
RING_FULL_ACT_B_START_ID_OFFSET: int = 0x150000


HINT_RING_GROUP_NO_ACT_START_ID_OFFSET: int = 0x2400
HINT_RING_GROUP_ACT_A_START_ID_OFFSET: int = 0x2600
HINT_RING_GROUP_ACT_B_START_ID_OFFSET: int = 0x2800
HINT_RING_FULL_NO_ACT_START_ID_OFFSET: int = 0x2A00
HINT_RING_FULL_ACT_A_START_ID_OFFSET: int = 0x2C00
HINT_RING_FULL_ACT_B_START_ID_OFFSET: int = 0x2E00

ITEM_BOX_GROUP_NO_ACT_START_ID_OFFSET: int = 0x3000
ITEM_BOX_GROUP_ACT_A_START_ID_OFFSET: int = 0x3500
ITEM_BOX_GROUP_ACT_B_START_ID_OFFSET: int = 0x3A00
ITEM_BOX_FULL_NO_ACT_START_ID_OFFSET: int = 0x4000
ITEM_BOX_FULL_ACT_A_START_ID_OFFSET: int = 0x4500
ITEM_BOX_FULL_ACT_B_START_ID_OFFSET: int = 0x4A00

ITEM_BALLOON_GROUP_NO_ACT_START_ID_OFFSET: int = 0x5000
ITEM_BALLOON_GROUP_ACT_A_START_ID_OFFSET: int = 0x5500
ITEM_BALLOON_GROUP_ACT_B_START_ID_OFFSET: int = 0x5A00
ITEM_BALLOON_FULL_NO_ACT_START_ID_OFFSET: int = 0x6000
ITEM_BALLOON_FULL_ACT_A_START_ID_OFFSET: int = 0x6500
ITEM_BALLOON_FULL_ACT_B_START_ID_OFFSET: int = 0x6A00

EGG_FLAPPER_GROUP_NO_ACT_START_ID_OFFSET: int = 0x10000
EGG_FLAPPER_GROUP_ACT_A_START_ID_OFFSET: int = 0x14000
EGG_FLAPPER_GROUP_ACT_B_START_ID_OFFSET: int = 0x18000
EGG_FLAPPER_FULL_NO_ACT_START_ID_OFFSET: int = 0x1C000
EGG_FLAPPER_FULL_ACT_A_START_ID_OFFSET: int = 0x20000
EGG_FLAPPER_FULL_ACT_B_START_ID_OFFSET: int = 0x24000

EGG_PAWN_GROUP_NO_ACT_START_ID_OFFSET: int = 0x28000
EGG_PAWN_GROUP_ACT_A_START_ID_OFFSET: int = 0x2C000
EGG_PAWN_GROUP_ACT_B_START_ID_OFFSET: int = 0x30000
EGG_PAWN_FULL_NO_ACT_START_ID_OFFSET: int = 0x34000
EGG_PAWN_FULL_ACT_A_START_ID_OFFSET: int = 0x38000
EGG_PAWN_FULL_ACT_B_START_ID_OFFSET: int = 0x3C000






def append_location(name: str, team: Team, stage: Stage, code: int, act: int, parent_region: str, rule_str: str, rule: Rule[SonicHeroesWorldBase], loc_type: LocationType, location_groups: list[str], locked_item: str = "", num_to_increment_id: int = 1) -> None:
    global loc_id
    if code > 0:
        loc_id = code
    code = loc_id
    if not loc_type.is_real:
        code = EVENT_LOCATION_ID
    elif code in already_used_loc_ids:
        raise ValueError(f"DUPLICATE LOCATION ID!! Loc Name: {name} Code: {code} Loc_Type: {loc_type} Locked_Item: {locked_item}")
    already_used_loc_ids.append(code)

    add_location_to_dict(name=name, team=team, stage=stage, code=code, act=act, parent_region=parent_region, rule_str=rule_str, rule=rule, loc_type=loc_type, locked_item=locked_item)

    for location_group in location_groups:
        FULL_LOCATION_GROUPS[location_group].add(name)


    if loc_type.is_real:
        loc_id += num_to_increment_id


def add_location_to_dict(name: str, team: Team, stage: Stage, code: int, act: int, parent_region: str, rule_str: str, rule: Rule[SonicHeroesWorldBase], loc_type: LocationType, locked_item: str = "") -> None:
    FULL_LOCATION_DICT[stage][team].append(SonicHeroesLocationData(name=name, team=team, stage=stage, code=code, act=act, parent_region=parent_region, rule_str=rule_str, rule=rule, loc_type=loc_type, locked_item=locked_item))


def append_sanity_location_with_act(name: str, team: Team, stage: Stage, code: int, act: int, parent_region: str, rule_str: str, rule: Rule[SonicHeroesWorldBase], loc_type: LocationType, location_groups: list[str], locked_item: str = "", num_to_increment_id: int = 1) -> None:
    match act:
        case 0:
            name = f"{stage.stage_name} {team} {name}"
        case 1:
            name = f"{stage.stage_name} {team} {Act.ACT_A.get_act_str()} {name}"
        case 2:
            name = f"{stage.stage_name} {team} {Act.ACT_B.get_act_str()} {name}"
        case _:
            raise ValueError(f"Invalid Act for append_sanity_location_with_act: name: {name} team: {team} stage {stage.stage_name} act: {act}")
    append_location(name=name, team=team, stage=stage, code=code, act=act, parent_region=parent_region, rule_str=rule_str, rule=rule, loc_type=loc_type, location_groups=location_groups, locked_item=locked_item, num_to_increment_id=num_to_increment_id)


def handle_sanity_locations_from_list(team: Team, stage: Stage, loc_list: Sequence[StageObjBase], id_offset_1_set: int, id_offset_act_a: int, id_offset_act_b: int, loc_footnote: str, rule_str: str, loc_type: LocationType, location_groups: list[str], num_to_increment_id: int = 1) -> None:
    # covariant moment with loc_list
    if len(loc_footnote) > 0:
        loc_footnote = f" {loc_footnote}"

    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + id_offset_1_set

    for loc_data in loc_list:
        append_sanity_location_with_act(name=f"{loc_data.location_name}{loc_footnote}", team=team, stage=stage, code=-999, act=0, parent_region=f"{loc_data.region_name}", rule_str=rule_str, rule=loc_data.rule, loc_type=loc_type, location_groups=location_groups, num_to_increment_id=num_to_increment_id)

    loc_id = LOCATION_START_ID_OFFSET + id_offset_act_a
    for loc_data in loc_list:
        append_sanity_location_with_act(name=f"{loc_data.location_name}{loc_footnote}", team=team, stage=stage, code=-999, act=1, parent_region=f"{loc_data.region_name}", rule_str=rule_str, rule=loc_data.rule, loc_type=loc_type, location_groups=location_groups, num_to_increment_id=num_to_increment_id)

    loc_id = LOCATION_START_ID_OFFSET + id_offset_act_b
    for loc_data in loc_list:
        append_sanity_location_with_act(name=f"{loc_data.location_name}{loc_footnote}", team=team, stage=stage, code=-999, act=2, parent_region=f"{loc_data.region_name}", rule_str=rule_str, rule=loc_data.rule, loc_type=loc_type, location_groups=location_groups, num_to_increment_id=num_to_increment_id)



def generate_level_goal_locations_for_not_super_hard_mode() -> None:
    global loc_id
    loc_id = LOCATION_START_ID
    generate_level_goal_locations_for_team_not_super_hard_mode(team=Team.SONIC)
    generate_level_goal_locations_for_team_not_super_hard_mode(team=Team.DARK)
    generate_level_goal_locations_for_team_not_super_hard_mode(team=Team.ROSE)
    generate_level_goal_locations_for_team_not_super_hard_mode(team=Team.CHAOTIX)


def generate_level_goal_locations_for_team_not_super_hard_mode(team: Team) -> None:
    # Act 1 Goal
    # Act 2 Goal
    # Egg Hawk Goal
    if team != Team.SUPER_HARD_MODE and team != Team.ANY_TEAM:
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            append_location(name=f"{reg_lvl.stage_name} {team} {Act.ACT_A.get_act_str()}", team=team, stage=reg_lvl, code=-999, act=1, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_A), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])

            if team is Team.DARK or team is Team.ROSE:
                append_location(name=f"{reg_lvl.stage_name} {team} {Act.ACT_B.get_act_str()}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} {OBJ_SANITY}", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])

            elif team is Team.CHAOTIX:
                if reg_lvl.chaotix_obj_sanity_checks[Act.ACT_B] > 0:
                    append_location(name=f"{reg_lvl.stage_name} {team} {Act.ACT_B.get_act_str()}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} {OBJ_SANITY}", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])
                else:
                    append_location(name=f"{reg_lvl.stage_name} {team} {Act.ACT_B.get_act_str()}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])
            else:
                append_location(name=f"{reg_lvl.stage_name} {team} {Act.ACT_B.get_act_str()}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])

        for boss in Stage.get_stages_of_type(stage_type=StageType.BOSS_STAGE):
            append_location(name=f"{boss.stage_name} {team}", team=team, stage=boss, code=-999, act=0, parent_region=f"{boss.stage_name}", rule_str="", rule=True_[SonicHeroesWorldBase](), loc_type=LocationType.BOSS, location_groups=[BOSS_LOCATION_GROUP], num_to_increment_id=2)
            # increment id one additional time

    # elif team == Team.SUPER_HARD_MODE:
    #     #Super Hard Mode
    #     for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
    #         append_location(name=f"{reg_lvl.stage_name} {team}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str="", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])
    else:
        print(f"BIG PROBLEM!! Team {team} in generate_level_goal_locations_for_team")


def generate_emerald_locations() -> None:
    # starts at 0x148
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x148
    for reg_lvl, bonus_lvl in Stage.get_stage_to_bonus_stage().items():
        if "Emerald Stage" in bonus_lvl.stage_name:
            append_location(name=f"{reg_lvl.stage_name} Emerald", team=Team.ANY_TEAM, stage=bonus_lvl, code=-999, act=0, parent_region=f"{bonus_lvl.stage_name}", rule_str="", rule=CanGetEmerald(stage=bonus_lvl), loc_type=LocationType.EMERALD, location_groups=[EMERALD_LOCATION_GROUP])


def generate_dark_obj_sanity() -> None:
    # starts at 0x150
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x150

    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        for x in range(100):
            append_location(name=f"{reg_lvl.stage_name} {Team.DARK} {Act.ACT_B.get_act_str()} Enemies Killed: {x + 1}", team=Team.DARK, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {Team.DARK} {OBJ_SANITY}", rule_str="", rule=Has(item_name=get_obj_sanity_event_item_name(team=Team.DARK, stage=reg_lvl, act=Act.ACT_B), count=x + 1), loc_type=LocationType.OBJ_SANITY, location_groups=[OBJ_SANITY_LOCATION_GROUP])
    pass


def generate_rose_obj_sanity() -> None:
    # starts at 0x6C8
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x6C8
    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        for x in range(200):
            append_location(name=f"{reg_lvl.stage_name} {Team.ROSE} {Act.ACT_B.get_act_str()} Rings Collected: {x + 1}", team=Team.ROSE, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl} {Team.ROSE} {OBJ_SANITY}", rule_str="", rule=Has(item_name=get_obj_sanity_event_item_name(team=Team.ROSE, stage=reg_lvl, act=Act.ACT_B), count=x + 1), loc_type=LocationType.OBJ_SANITY, location_groups=[OBJ_SANITY_LOCATION_GROUP])


def generate_chaotix_obj_sanity() -> None:
    # starts at 0x11B8
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x11B8

    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        for act_index, act in enumerate([Act.ACT_A, Act.ACT_B]):
            for x in range(reg_lvl.chaotix_obj_sanity_checks[act]):
                append_location(name=f"{reg_lvl.stage_name} {Team.CHAOTIX} {act.get_act_str()} {reg_lvl.chaotix_obj_sanity_str[act]}: {x + 1}", team=Team.CHAOTIX, stage=reg_lvl, code=-999, act=act_index + 1, parent_region=f"{reg_lvl.stage_name} {Team.CHAOTIX} {OBJ_SANITY}", rule_str="", rule=Has(item_name=get_obj_sanity_event_item_name(team=Team.CHAOTIX, stage=reg_lvl, act=act), count=x + 1), loc_type=LocationType.OBJ_SANITY, location_groups=[OBJ_SANITY_LOCATION_GROUP])
    pass


def generate_key_sanity() -> None:
    global loc_id

    # Act 0
    loc_id = LOCATION_START_ID_OFFSET + 0x1700
    for team in Team:
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.bonus_keys[team]):
                append_sanity_location_with_act(name=f"{BONUS_KEY} {x + 1}", team=team, stage=reg_lvl, code=-999, act=0, parent_region=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {x + 1}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])
            if team is Team.ROSE and reg_lvl is Stage.CASINO_PARK:
                append_location(name=f"SUPER SECRET HIDDEN {BONUS_KEY}", team=team, stage=reg_lvl, code=-999, act=0, parent_region=f"SUPER SECRET HIDDEN {BONUS_KEY}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])

    # Act 1
    loc_id = LOCATION_START_ID_OFFSET + 0x1800
    for team in Team:
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.bonus_keys[team]):
                append_sanity_location_with_act(name=f"{BONUS_KEY} {x + 1}", team=team, stage=reg_lvl, code=-999, act=1, parent_region=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {x + 1}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])
            if team is Team.ROSE and reg_lvl is Stage.CASINO_PARK:
                append_location(name=f"SUPER SECRET HIDDEN {Act.ACT_A.get_act_str()} {BONUS_KEY}", team=team, stage=reg_lvl, code=-999, act=1, parent_region=f"SUPER SECRET HIDDEN {BONUS_KEY}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])

    # Act 2
    loc_id = LOCATION_START_ID_OFFSET + 0x1900
    for team in Team:
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.bonus_keys[team]):
                append_sanity_location_with_act(name=f"{BONUS_KEY} {x + 1}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {x + 1}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])
            if team is Team.ROSE and reg_lvl is Stage.CASINO_PARK:
                append_location(name=f"SUPER SECRET HIDDEN {Act.ACT_B.get_act_str()} {BONUS_KEY}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"SUPER SECRET HIDDEN {BONUS_KEY}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.KEY_SANITY, location_groups=[KEY_SANITY_LOCATION_GROUP])


def generate_checkpoint_sanity_for_not_super_hard_mode() -> None:
    global loc_id

    # Act 0
    loc_id = LOCATION_START_ID_OFFSET + 0x2000
    for team in Team:
        if team == Team.SUPER_HARD_MODE:
            continue
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.checkpoints[team]):
                append_sanity_location_with_act(name=f"Checkpoint {x + 1}", team=team, stage=reg_lvl, code=-999, act=0, parent_region=f"{reg_lvl.stage_name} {team} Checkpoint {x + 1}", rule_str=f"Checkpoint", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.CHECKPOINT), loc_type=LocationType.CHECKPOINT_SANITY, location_groups=[CHECKPOINT_SANITY_LOCATION_GROUP])

    # Act 1
    loc_id = LOCATION_START_ID_OFFSET + 0x2100
    for team in Team:
        if team == Team.SUPER_HARD_MODE:
            continue
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.checkpoints[team]):
                append_sanity_location_with_act(name=f"Checkpoint {x + 1}", team=team, stage=reg_lvl, code=-999, act=1, parent_region=f"{reg_lvl.stage_name} {team} Checkpoint {x + 1}", rule_str=f"Checkpoint", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.CHECKPOINT), loc_type=LocationType.CHECKPOINT_SANITY, location_groups=[CHECKPOINT_SANITY_LOCATION_GROUP])

    # Act 2
    loc_id = LOCATION_START_ID_OFFSET + 0x2200
    for team in Team:
        if team == Team.SUPER_HARD_MODE:
            continue
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.checkpoints[team]):
                append_sanity_location_with_act(name=f"Checkpoint {x + 1}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Checkpoint {x + 1}", rule_str=f"Checkpoint", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.CHECKPOINT), loc_type=LocationType.CHECKPOINT_SANITY, location_groups=[CHECKPOINT_SANITY_LOCATION_GROUP])


def generate_checkpoint_sanity_super_hard_mode() -> None:
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x22C0

    team: Team = Team.SUPER_HARD_MODE
    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        for x in range(reg_lvl.checkpoints[team]):
            append_location(name=f"{reg_lvl.stage_name} {team} Checkpoint {x + 1}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Checkpoint {x + 1}", rule_str=f"Checkpoint", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.CHECKPOINT), loc_type=LocationType.CHECKPOINT_SANITY, location_groups=[CHECKPOINT_SANITY_LOCATION_GROUP])


def generate_level_goal_locations_for_super_hard_mode_hard_mode_goals() -> None:
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x2300

    team: Team = Team.SUPER_HARD_MODE
    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        append_location(name=f"{reg_lvl.stage_name} {team}", team=team, stage=reg_lvl, code=-999, act=2, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str=f"GoalRing", rule=CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])


def generate_metal_madness_extra_locations() -> None:
    global loc_id
    loc_id = LOCATION_START_ID_OFFSET + 0x230E

    append_location(name=f"{Stage.METAL_OVERLORD.stage_name}", team=Team.ANY_TEAM, stage=Stage.METAL_MADNESS, code=-999, act=0, parent_region=f"{Stage.METAL_MADNESS.stage_name}", rule_str=f"", rule=True_[SonicHeroesWorldBase](), loc_type=LocationType.LEVEL, location_groups=[STAGE_LOCATION_GROUP])



def get_all_parsed_stage_objects_of_type(team: Team, stage: Stage, stage_obj: StageObj) -> Sequence[StageObjBase]:
    try:
        match stage_obj:
            case StageObj.SINGLE_SPRING:
                return []
            case StageObj.TRIPLE_SPRING:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).triple_springs  # pyright: ignore[reportAny]
            case StageObj.RINGS:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).rings  # pyright: ignore[reportAny]
            case StageObj.HINT_RING:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).hint_rings  # pyright: ignore[reportAny]
            case StageObj.ITEM_BOX:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).item_boxes  # pyright: ignore[reportAny]
            case StageObj.ITEM_BALLOON:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).item_balloons  # pyright: ignore[reportAny]


            case StageObj.EGG_FLAPPER:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).egg_flappers  # pyright: ignore[reportAny]
            case StageObj.EGG_PAWN:
                return get_parsed_data_module_for_team_stage(team=team, stage=stage).egg_pawns  # pyright: ignore[reportAny]

    except Exception as e:
        print(e)

    return []




def generate_hint_rings_sanity_locations() -> None:
    generate_hint_rings_sanity_group_locations()
    generate_hint_rings_sanity_full_locations()


def generate_hint_rings_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.HINT_RING)
            hint_ring_list: list[HintRingData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, HintRingData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    hint_ring_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=hint_ring_list, id_offset_1_set=HINT_RING_GROUP_NO_ACT_START_ID_OFFSET, id_offset_act_a=HINT_RING_GROUP_ACT_A_START_ID_OFFSET, id_offset_act_b=HINT_RING_GROUP_ACT_B_START_ID_OFFSET, loc_footnote="Group", rule_str=f"HintRing", loc_type=LocationType.HINT_RING_SANITY_GROUP, location_groups=[HINT_RING_SANITY_LOCATION_GROUP_GROUP])


def generate_hint_rings_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.HINT_RING)
            hint_ring_list: list[HintRingData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, HintRingData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    hint_ring_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=hint_ring_list, id_offset_1_set=HINT_RING_FULL_NO_ACT_START_ID_OFFSET, id_offset_act_a=HINT_RING_FULL_ACT_A_START_ID_OFFSET, id_offset_act_b=HINT_RING_FULL_ACT_B_START_ID_OFFSET, loc_footnote="", rule_str=f"HintRing", loc_type=LocationType.HINT_RING_SANITY_FULL, location_groups=[HINT_RING_SANITY_LOCATION_GROUP_FULL])



def generate_item_boxes_sanity_locations() -> None:
    generate_item_boxes_sanity_group_locations()
    generate_item_boxes_sanity_full_locations()


def generate_item_boxes_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.ITEM_BOX)
            item_box_list: list[ItemBoxData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, ItemBoxData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    item_box_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=item_box_list, id_offset_1_set=ITEM_BOX_GROUP_NO_ACT_START_ID_OFFSET, id_offset_act_a=ITEM_BOX_GROUP_ACT_A_START_ID_OFFSET, id_offset_act_b=ITEM_BOX_GROUP_ACT_B_START_ID_OFFSET, loc_footnote="Group", rule_str=f"ItemBox", loc_type=LocationType.ITEM_BOX_SANITY_GROUP, location_groups=[ITEM_BOX_SANITY_LOCATION_GROUP_GROUP])


def generate_item_boxes_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.ITEM_BOX)
            item_box_list: list[ItemBoxData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, ItemBoxData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    item_box_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=item_box_list, id_offset_1_set=ITEM_BOX_FULL_NO_ACT_START_ID_OFFSET, id_offset_act_a=ITEM_BOX_FULL_ACT_A_START_ID_OFFSET, id_offset_act_b=ITEM_BOX_FULL_ACT_B_START_ID_OFFSET, loc_footnote="", rule_str=f"ItemBox", loc_type=LocationType.ITEM_BOX_SANITY_FULL, location_groups=[ITEM_BOX_SANITY_LOCATION_GROUP_FULL])



def generate_item_balloons_sanity_locations() -> None:
    generate_item_balloon_sanity_group_locations()
    generate_item_balloon_sanity_full_locations()



def generate_item_balloon_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.ITEM_BALLOON)
            item_balloon_list: list[ItemBalloonData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, ItemBalloonData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    item_balloon_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=item_balloon_list, id_offset_1_set=ITEM_BALLOON_GROUP_NO_ACT_START_ID_OFFSET, id_offset_act_a=ITEM_BALLOON_GROUP_ACT_A_START_ID_OFFSET, id_offset_act_b=ITEM_BALLOON_GROUP_ACT_B_START_ID_OFFSET, loc_footnote="Group", rule_str=f"ItemBalloon", loc_type=LocationType.ITEM_BALLOON_SANITY_GROUP, location_groups=[ITEM_BALLOON_SANITY_LOCATION_GROUP_GROUP])


def generate_item_balloon_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.ITEM_BALLOON)
            item_balloon_list: list[ItemBalloonData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, ItemBalloonData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    item_balloon_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=item_balloon_list, id_offset_1_set=ITEM_BALLOON_FULL_NO_ACT_START_ID_OFFSET, id_offset_act_a=ITEM_BALLOON_FULL_ACT_A_START_ID_OFFSET, id_offset_act_b=ITEM_BALLOON_FULL_ACT_B_START_ID_OFFSET, loc_footnote="", rule_str=f"ItemBalloon", loc_type=LocationType.ITEM_BALLOON_SANITY_FULL, location_groups=[ITEM_BALLOON_SANITY_LOCATION_GROUP_FULL])





def generate_enemy_sanity_locations() -> None:
    generate_egg_flapper_sanity_locations()
    generate_egg_pawn_sanity_locations()


def generate_egg_flapper_sanity_locations() -> None:
    generate_egg_flapper_sanity_group_locations()
    generate_egg_flapper_sanity_full_locations()


def generate_egg_flapper_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.EGG_FLAPPER)
            egg_flapper_list: list[EggFlapper] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, EggFlapper):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    egg_flapper_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=egg_flapper_list, id_offset_1_set=EGG_FLAPPER_GROUP_NO_ACT_START_ID_OFFSET, id_offset_act_a=EGG_FLAPPER_GROUP_ACT_A_START_ID_OFFSET, id_offset_act_b=EGG_FLAPPER_GROUP_ACT_B_START_ID_OFFSET, loc_footnote="Group", rule_str=f"EggFlapper", loc_type=LocationType.EGG_FLAPPER_SANITY_GROUP, location_groups=[EGG_FLAPPER_SANITY_LOCATION_GROUP_GROUP])


def generate_egg_flapper_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.EGG_FLAPPER)
            egg_flapper_list: list[EggFlapper] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, EggFlapper):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    egg_flapper_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=egg_flapper_list, id_offset_1_set=EGG_FLAPPER_FULL_NO_ACT_START_ID_OFFSET, id_offset_act_a=EGG_FLAPPER_FULL_ACT_A_START_ID_OFFSET, id_offset_act_b=EGG_FLAPPER_FULL_ACT_B_START_ID_OFFSET, loc_footnote="", rule_str=f"EggFlapper", loc_type=LocationType.EGG_FLAPPER_SANITY_FULL, location_groups=[EGG_FLAPPER_SANITY_LOCATION_GROUP_FULL])


def generate_egg_pawn_sanity_locations() -> None:
    generate_egg_pawn_sanity_group_locations()
    generate_egg_pawn_sanity_full_locations()


def generate_egg_pawn_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.EGG_PAWN)
            egg_pawn_list: list[EggPawn] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, EggPawn):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    egg_pawn_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=egg_pawn_list, id_offset_1_set=EGG_PAWN_GROUP_NO_ACT_START_ID_OFFSET, id_offset_act_a=EGG_PAWN_GROUP_ACT_A_START_ID_OFFSET, id_offset_act_b=EGG_PAWN_GROUP_ACT_B_START_ID_OFFSET, loc_footnote="Group", rule_str=f"EggPawn", loc_type=LocationType.EGG_PAWN_SANITY_GROUP, location_groups=[EGG_PAWN_SANITY_LOCATION_GROUP_GROUP])



def generate_egg_pawn_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.EGG_PAWN)
            egg_pawn_list: list[EggPawn] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, EggPawn):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    egg_pawn_list.append(stage_obj)
            handle_sanity_locations_from_list(team=team, stage=stage, loc_list=egg_pawn_list, id_offset_1_set=EGG_PAWN_FULL_NO_ACT_START_ID_OFFSET, id_offset_act_a=EGG_PAWN_FULL_ACT_A_START_ID_OFFSET, id_offset_act_b=EGG_PAWN_FULL_ACT_B_START_ID_OFFSET, loc_footnote="", rule_str=f"EggPawn", loc_type=LocationType.EGG_PAWN_SANITY_FULL, location_groups=[EGG_PAWN_SANITY_LOCATION_GROUP_FULL])




def generate_ring_sanity_locations() -> None:
    generate_ring_sanity_group_locations()
    generate_ring_sanity_full_locations()



def generate_ring_sanity_group_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Group Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.RINGS)
            ring_list: list[RingData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, RingData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_group >= 0:
                    ring_list.append(stage_obj)

            # have list
            global loc_id
            loc_id = LOCATION_START_ID_OFFSET + RING_GROUP_NO_ACT_START_ID_OFFSET

            for ring_data in ring_list:
                append_sanity_location_with_act(name=f"{ring_data.location_name} {RING_GROUP}", team=team, stage=stage, code=-999, act=0, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_GROUP, location_groups=[RING_SANITY_LOCATION_GROUP_GROUP])

            loc_id = LOCATION_START_ID_OFFSET + RING_GROUP_ACT_A_START_ID_OFFSET

            for ring_data in ring_list:
                append_sanity_location_with_act(name=f"{ring_data.location_name} {RING_GROUP}", team=team, stage=stage, code=-999, act=1, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_GROUP, location_groups=[RING_SANITY_LOCATION_GROUP_GROUP])

            loc_id = LOCATION_START_ID_OFFSET + RING_GROUP_ACT_B_START_ID_OFFSET

            for ring_data in ring_list:
                append_sanity_location_with_act(name=f"{ring_data.location_name} {RING_GROUP}", team=team, stage=stage, code=-999, act=2, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_GROUP, location_groups=[RING_SANITY_LOCATION_GROUP_GROUP])


def generate_ring_sanity_full_locations() -> None:
    for team, stage_list in TEAM_STAGES_TO_GENERATE_SANITIES.items():
        for stage in stage_list:
            # Full Locations
            temp_sequence: Sequence[StageObjBase] = get_all_parsed_stage_objects_of_type(team=team, stage=stage, stage_obj=StageObj.RINGS)
            ring_list: list[RingData] = []
            for stage_obj in temp_sequence:
                if not isinstance(stage_obj, RingData):
                    raise TypeError(f"Wrong Type of stage object: {stage_obj.__class__.__name__}")
                if stage_obj.id_offset_full >= 0:
                    ring_list.append(stage_obj)

            # have list
            global loc_id
            loc_id = LOCATION_START_ID_OFFSET + RING_FULL_NO_ACT_START_ID_OFFSET

            for ring_data in ring_list:
                for x in range(ring_data.num_rings):
                    append_sanity_location_with_act(name=f"{ring_data.location_name} Ring {x + 1}", team=team, stage=stage, code=-999, act=0, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_FULL, location_groups=[RING_SANITY_LOCATION_GROUP_FULL])

            loc_id = LOCATION_START_ID_OFFSET + RING_FULL_ACT_A_START_ID_OFFSET

            for ring_data in ring_list:
                for x in range(ring_data.num_rings):
                    # print(f"{ring_data.location_name} Ring {x + 1} ::: 0x{loc_id:X}")
                    append_sanity_location_with_act(name=f"{ring_data.location_name} Ring {x + 1}", team=team, stage=stage, code=-999, act=1, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_FULL, location_groups=[RING_SANITY_LOCATION_GROUP_FULL])

            loc_id = LOCATION_START_ID_OFFSET + RING_FULL_ACT_B_START_ID_OFFSET

            for ring_data in ring_list:
                for x in range(ring_data.num_rings):
                    append_sanity_location_with_act(name=f"{ring_data.location_name} Ring {x + 1}", team=team, stage=stage, code=-999, act=2, parent_region=f"{ring_data.region_name}", rule_str=f"Ring", rule=ring_data.rule, loc_type=LocationType.RING_SANITY_FULL, location_groups=[RING_SANITY_LOCATION_GROUP_FULL])


def generate_all_event_locations() -> None:
    generate_boss_all_teams_events()
    generate_level_goal_events()
    generate_bonus_key_events()
    generate_dark_obj_sanity_events()
    pass


def generate_boss_all_teams_events() -> None:
    for boss in Stage.get_stages_of_type(stage_type=StageType.BOSS_STAGE):
        append_location(name=f"{boss.stage_name} {EVENT_LOCATION}", team=Team.ANY_TEAM, stage=boss, code=EVENT_LOCATION_ID, act=0, parent_region=f"{boss.stage_name}", rule_str="", rule=True_[SonicHeroesWorldBase](), loc_type=LocationType.EVENT, location_groups=[], locked_item=f"{boss.stage_name} {EVENT_ITEM}")


def generate_level_goal_events() -> None:
    generate_level_goal_all_teams_events()
    generate_level_goal_per_story_events()
    pass


def generate_level_goal_all_teams_events() -> None:
    for team in Team:
        if team == Team.ANY_TEAM:
            #do nothing on ANYTEAM
            continue
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            rule: Rule[SonicHeroesWorldBase] = CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_A) | CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B)
            append_location(name=f"{reg_lvl.stage_name} {team} Goal {EVENT_LOCATION}", team=team, stage=reg_lvl, code=EVENT_LOCATION_ID, act=0, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str=f"", rule=rule, loc_type=LocationType.EVENT, location_groups=[], locked_item=LEVEL_GOAL_ALL_TEAMS_EVENT_ITEM)


def generate_level_goal_per_story_events() -> None:
    for team in Team:
        if team == Team.ANY_TEAM:
            #do nothing on ANYTEAM
            continue
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            rule: Rule[SonicHeroesWorldBase] = CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_A) | CanGoalStage(team=team, stage=reg_lvl, act=Act.ACT_B)
            append_location(name=f"{reg_lvl.stage_name} {team} Goal {EVENT_LOCATION} For Team {team}", team=team, stage=reg_lvl, code=EVENT_LOCATION_ID, act=0, parent_region=f"{reg_lvl.stage_name} {team} Goal", rule_str=f"", rule=rule, loc_type=LocationType.EVENT, location_groups=[], locked_item=f"{LEVEL_GOAL_PER_TEAM_EVENT_ITEM_WITHOUT_TEAM} {team}")


def generate_bonus_key_events() -> None:
    for team in Team:
        for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
            for x in range(reg_lvl.bonus_keys[team]):
                append_location(name=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {x + 1} {EVENT_LOCATION}", team=team, stage=reg_lvl, code=EVENT_LOCATION_ID, act=0, parent_region=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {x + 1}", rule_str=f"THISSHOULDNOTMATTER(KEYCAGE)", rule=has_stage_obj_rule(team=team, stage_obj=StageObj.BONUS_KEY) & can_break_key_cage(team=team, stage=reg_lvl), loc_type=LocationType.EVENT, location_groups=[], locked_item=f"{reg_lvl.stage_name} {team} {BONUS_KEY} {EVENT_ITEM}")

        #not doing super secret hidden


def generate_dark_obj_sanity_events() -> None:
    team: Team = Team.DARK
    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        try:
            for egg_flapper in get_parsed_data_module_for_team_stage(team=team, stage=reg_lvl).egg_flappers:  # pyright: ignore[reportAny]
                if egg_flapper.id_offset_full != STAGE_OBJ_INVALID_ID_OFFSET:  # pyright: ignore[reportAny]
                    append_location(name=f"{reg_lvl.stage_name} {team.value} {egg_flapper.location_name} {OBJ_SANITY} {EVENT_LOCATION}", team=Team.DARK, stage=Stage.SEASIDE_HILL, code=EVENT_LOCATION_ID, act=2, parent_region=f"{egg_flapper.region_name}", rule_str=f"{egg_flapper.enemy_type} {EVENT_LOCATION}", rule=egg_flapper.rule, loc_type=LocationType.EVENT, location_groups=[], locked_item=get_obj_sanity_event_item_name(team=Team.DARK, stage=reg_lvl, act=Act.ACT_B))  # pyright: ignore[reportAny]
        except:
            pass
    for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        try:
            for egg_pawn in get_parsed_data_module_for_team_stage(team=team, stage=reg_lvl).egg_pawns:  # pyright: ignore[reportAny]
                if egg_pawn.id_offset_full != STAGE_OBJ_INVALID_ID_OFFSET:  # pyright: ignore[reportAny]
                    append_location(name=f"{reg_lvl.stage_name} {team.value} {egg_pawn.location_name} {OBJ_SANITY} {EVENT_LOCATION}", team=Team.DARK, stage=Stage.SEASIDE_HILL, code=EVENT_LOCATION_ID, act=2, parent_region=f"{egg_pawn.region_name}", rule_str=f"{egg_pawn.enemy_type} {EVENT_LOCATION}", rule=egg_pawn.rule, loc_type=LocationType.EVENT, location_groups=[], locked_item=get_obj_sanity_event_item_name(team=Team.DARK, stage=reg_lvl, act=Act.ACT_B))  # pyright: ignore[reportAny]
        except:
            pass



def print_full_dict() -> None:
    # classes_str = f""
    # enums_str = f""
    # item_constants_str = f""
    tab_str: str = f"    "

    team_enum_str: str = f"Team"
    stage_enum_str: str = f"Stage"
    location_type_enum_str: str = f"LocationType"
    location_start_id_offest_str: str = f"LOCATION_START_ID_OFFSET"
    sonic_heroes_location_data_str: str = f"SonicHeroesLocationData"

    import_str: str = f"from worlds.sonic_heroes.constants.enums import Team, Stage"
    import_str += f"\nfrom worlds.sonic_heroes.constants.item_constants import LOCATION_START_ID_OFFSET"

    big_result: str = f"{import_str}\n\nFULL_LOCATION_DICT: dict[{team_enum_str}, dict[{stage_enum_str}, list[{sonic_heroes_location_data_str}]]] = \\\n{{\n"

    for stage, team_data_pair in FULL_LOCATION_DICT.items():
        big_result += f"{tab_str}{stage_enum_str}.{stage.name}: \n{tab_str}{{\n"

        for team, loc_list in team_data_pair.items():
            big_result += f"{tab_str}{tab_str}{team_enum_str}.{team.name}: \n{tab_str}{tab_str}[\n"

            for loc_data in loc_list:
                team_str: str = f"{team_enum_str}.{loc_data.team.name}"
                stage_str: str = f"{stage_enum_str}.{loc_data.stage.name}"
                loc_type_str: str = f"{location_type_enum_str}.{loc_data.loc_type.name}"

                big_result += f"{tab_str}{tab_str}{tab_str}{sonic_heroes_location_data_str}(name=\"{loc_data.name}\", team={team_str}, stage={stage_str}, code={location_start_id_offest_str} + int(\"0x{loc_data.code:X}\", 16), act={loc_data.act}, parent_region=\"{loc_data.parent_region}\", rule_str=\"{loc_data.rule_str}\", loc_type={loc_type_str}, locked_item=\"{loc_data.locked_item}\"),\n"

            # list end
            big_result += f"{tab_str}{tab_str}],\n"

        # team dict end
        big_result += f"{tab_str}}},\n"
    big_result += "\n}\n\n"


    print(big_result)



def generate_all_locations() -> None:
    generate_level_goal_locations_for_not_super_hard_mode()
    generate_emerald_locations()
    generate_dark_obj_sanity()
    generate_rose_obj_sanity()
    generate_chaotix_obj_sanity()

    generate_key_sanity()
    generate_checkpoint_sanity_for_not_super_hard_mode()
    generate_checkpoint_sanity_super_hard_mode()
    generate_level_goal_locations_for_super_hard_mode_hard_mode_goals()
    generate_metal_madness_extra_locations()

    generate_hint_rings_sanity_locations()
    generate_item_boxes_sanity_locations()
    generate_item_balloons_sanity_locations()

    generate_enemy_sanity_locations()
    generate_ring_sanity_locations()


    #events
    generate_all_event_locations()



    pass


generate_all_locations()

