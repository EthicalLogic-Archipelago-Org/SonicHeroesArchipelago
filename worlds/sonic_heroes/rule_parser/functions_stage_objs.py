"""
Functions used by the parser related to All Stage Objs
"""
import csv
import os


from rule_builder.rules import True_, Rule

from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string, get_parsed_data_module_for_team_stage
from .parser_constants import *

from ..world_base import SonicHeroesWorldBase
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.enemies import EggFlapperArmor, EggFlapperWeapon, EggPawnShield, EggPawnType, EggPawnWeapon, EnemyHeight
from ..constants.item_balloon_box import ItemReward
from ..constants.rings import RingLayout
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj

def get_stage_objs_csv_file_name(team: Team, stage: Stage, stage_obj: str = "StageObjs", secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type=stage_obj, secret=secret)


def parse_csv_entry_triple_spring(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    item_reward: ItemReward = ItemReward(value=entry[TRIPLE_SPRING_ITEM_HEADER])
    item_str: str = f"{item_reward.__class__.__name__}.{item_reward.name}"
    params_dict["power"] = entry[TRIPLE_SPRING_POWER_HEADER]
    params_dict["no_control_time"] = entry[TRIPLE_SPRING_NO_CONTROL_TIME_HEADER]
    params_dict["item"] = item_str
    params_dict["scale"] = entry[TRIPLE_SPRING_SCALE_HEADER]
    return params_dict


def get_export_string_triple_spring(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "TRIPLE_SPRINGS"
    class_str: str = "TripleSpringData"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="TripleSprings", secret=secret)
    return class_str, list_name, file_name, TRIPLE_SPRING_PARSER_FILE_HEADER


def parse_csv_entry_rings(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    ring_layout: RingLayout = RingLayout(value=entry[RING_TYPE_HEADER])
    ring_layout_str: str = f"{ring_layout.__class__.__name__}.{ring_layout.name}"
    params_dict["layout"] = ring_layout_str
    params_dict["num_rings"] = entry[RING_NUM_RINGS_HEADER]
    params_dict["length"] = entry[RING_LENGTH_HEADER]
    params_dict["radius"] = entry[RING_RADIUS_HEADER]
    params_dict["id_offset"] = entry[RING_ID_OFFSET_HEADER]
    return params_dict


def get_export_string_rings(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "RINGS"
    class_str: str = "RingData"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="Rings", secret=secret)
    return class_str, list_name, file_name, RING_PARSER_FILE_HEADER


def parse_csv_entry_hint_ring(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    params_dict["voice_line"] = entry[HINT_RING_VOICELINE_HEADER]
    return params_dict


def get_export_string_hint_ring(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "HINT_RINGS"
    class_str: str = "HintRingData"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="HintRings", secret=secret)
    return class_str, list_name, file_name, HINT_RING_PARSER_FILE_HEADER


def parse_csv_entry_item_box(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    item_reward: ItemReward = ItemReward(value=entry[ITEM_BOX_ITEM_HEADER])
    item_str: str = f"{item_reward.__class__.__name__}.{item_reward.name}"
    params_dict["item"] = item_str
    return params_dict


def get_export_string_item_box(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "ITEM_BOXES"
    class_str: str = "ItemBoxData"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="ItemBoxes", secret=secret)
    return class_str, list_name, file_name, ITEM_BALLOON_BOX_PARSER_FILE_HEADER


def parse_csv_entry_item_balloon(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    item_reward: ItemReward = ItemReward(value=entry[ITEM_BALLOON_ITEM_HEADER])
    item_str: str = f"{item_reward.__class__.__name__}.{item_reward.name}"
    params_dict["item"] = item_str
    return params_dict


def get_export_string_item_balloon(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "ITEM_BALLOONS"
    class_str: str = "ItemBalloonData"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="ItemBalloons", secret=secret)
    return class_str, list_name, file_name, ITEM_BALLOON_BOX_PARSER_FILE_HEADER









def parse_csv_entry_egg_flapper(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    weapon: EggFlapperWeapon = EggFlapperWeapon(value=entry[EGG_FLAPPER_WEAPON_HEADER])
    weapon_str: str = f"{weapon.__class__.__name__}.{weapon.name}"
    armor: EggFlapperArmor = EggFlapperArmor(value=entry[EGG_FLAPPER_ARMOR_HEADER])
    armor_str: str = f"{armor.__class__.__name__}.{armor.name}"
    height: EnemyHeight = EnemyHeight.match(input_str=entry[EGG_FLAPPER_HEIGHT_HEADER])
    height_str: str = f"{height.__class__.__name__}.{height.name}"

    params_dict["weapon"] = weapon_str
    params_dict["armor"] = armor_str
    params_dict["height"] = height_str
    return params_dict


def get_export_string_egg_flapper(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "EGG_FLAPPERS"
    class_str: str = "EggFlapper"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="EggFlappers", secret=secret)
    return class_str, list_name, file_name, ENEMY_PARSER_FILE_HEADER


def parse_csv_entry_egg_pawn(entry: dict[str, str], params_dict: dict[str, str]) -> dict[str, str]:
    pawn_type: EggPawnType = EggPawnType(value=entry[EGG_PAWN_SPECIAL_TYPE_HEADER])
    pawn_type_str: str = f"{pawn_type.__class__.__name__}.{pawn_type.name}"
    weapon: EggPawnWeapon = EggPawnWeapon(value=entry[EGG_PAWN_WEAPON_HEADER])
    weapon_str: str = f"{weapon.__class__.__name__}.{weapon.name}"
    shield: EggPawnShield = EggPawnShield(value=entry[EGG_PAWN_SHIELD_HEADER])
    shield_str: str = f"{shield.__class__.__name__}.{shield.name}"
    height: EnemyHeight = EnemyHeight.match(input_str=entry[EGG_PAWN_HEIGHT_HEADER])
    height_str: str = f"{height.__class__.__name__}.{height.name}"

    params_dict["special_type"] = pawn_type_str
    params_dict["weapon"] = weapon_str
    params_dict["shield"] = shield_str
    params_dict["height"] = height_str
    return params_dict


def get_export_string_egg_pawn(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    list_name: str = "EGG_PAWNS"
    class_str: str = "EggPawn"
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, stage_obj="EggPawns", secret=secret)
    return class_str, list_name, file_name, ENEMY_PARSER_FILE_HEADER




def parse_individual_stage_obj_csv_entry(entry: dict[str, str]) -> tuple[StageObj, dict[str, str]]:
    stage_obj: StageObj = StageObj(value=entry[STAGE_OBJ_HEADER])
    _result: str = ""
    team: Team = Team(value=entry[TEAM_HEADER])
    stage: Stage = Stage.match_stage_name(stage_name=entry[LEVEL_HEADER])
    region_str: str = f"{stage.stage_name} {team} {entry[REGION_HEADER]}"
    name_str: str = f"{entry[REGION_HEADER]} {entry[NAME_HEADER]}"
    parsed_rule_str: str = ""
    link_id_str: str = f"{entry[LINK_ID_HEADER]}"
    x_str: str = f"{entry[X_HEADER]}"
    y_str: str = f"{entry[Y_HEADER]}"
    z_str: str = f"{entry[Z_HEADER]}"

    if entry[RULE_HEADER] == "":
        parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
    elif entry[RULE_HEADER] == "NOTPOSSIBLE":
        parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
    else:
        print(f"Rule String here: {entry[RULE_HEADER]}")
        parsed_rule_str = handle_full_rule_string(rule_str=entry[RULE_HEADER], team=team, stage=stage)


    params_dict: dict[str, str] = \
    {
        "team": f"{team.__class__.__name__}.{team.name}",
        "stage": f"{stage.__class__.__name__}.{stage.name}",
        "location_name": f"\"{name_str}\"",
        "region_name": f"\"{region_str}\"",
    }

    match stage_obj:
        case StageObj.ALL_STAGE_OBJECTS:
            raise ValueError(f"All Stage Objects passed to parse_individual_stage_obj_csv_entry. Entry: {entry}")
        case StageObj.TRIPLE_SPRING:
            params_dict = parse_csv_entry_triple_spring(entry=entry, params_dict=params_dict)
        case StageObj.RINGS:
            params_dict = parse_csv_entry_rings(entry=entry, params_dict=params_dict)
        case StageObj.HINT_RING:
            params_dict = parse_csv_entry_hint_ring(entry=entry, params_dict=params_dict)

        case StageObj.ITEM_BOX:
            params_dict = parse_csv_entry_item_box(entry=entry, params_dict=params_dict)
        case StageObj.ITEM_BALLOON:
            params_dict = parse_csv_entry_item_balloon(entry=entry, params_dict=params_dict)

        case StageObj.EGG_FLAPPER:
            params_dict = parse_csv_entry_egg_flapper(entry=entry, params_dict=params_dict)
        case StageObj.EGG_PAWN:
            params_dict = parse_csv_entry_egg_pawn(entry=entry, params_dict=params_dict)

        case _:
            pass

    params_dict["link_id"] = link_id_str
    params_dict["x"] = x_str
    params_dict["y"] = y_str
    params_dict["z"] = z_str
    params_dict["rule"] = parsed_rule_str

    return stage_obj, params_dict


def get_export_names_for_stage_obj(stage_obj: StageObj, team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    class_str: str = PLACEHOLDER_CLASS
    list_name: str = PLACEHOLDER_LIST_NAME
    file_name: str = PLACEHOLDER_FILE_NAME
    file_header: str = PLACEHOLDER_FILE_HEADER
    match stage_obj:
        case StageObj.ALL_STAGE_OBJECTS:
            raise ValueError(f"All Stage Objects passed to export_stage_obj_entries")
        case StageObj.TRIPLE_SPRING:
            class_str, list_name, file_name, file_header = get_export_string_triple_spring(team=team, stage=stage, secret=secret)
        case StageObj.RINGS:
            class_str, list_name, file_name, file_header = get_export_string_rings(team=team, stage=stage, secret=secret)
        case StageObj.HINT_RING:
            class_str, list_name, file_name, file_header = get_export_string_hint_ring(team=team, stage=stage, secret=secret)
        case StageObj.ITEM_BOX:
            class_str, list_name, file_name, file_header = get_export_string_item_box(team=team, stage=stage, secret=secret)
        case StageObj.ITEM_BALLOON:
            class_str, list_name, file_name, file_header = get_export_string_item_balloon(team=team, stage=stage, secret=secret)

        case StageObj.EGG_FLAPPER:
            class_str, list_name, file_name, file_header = get_export_string_egg_flapper(team=team, stage=stage, secret=secret)
        case StageObj.EGG_PAWN:
            class_str, list_name, file_name, file_header = get_export_string_egg_pawn(team=team, stage=stage, secret=secret)

        case _:
            pass
            # raise ValueError(f"Stage Obj: {stage_obj.value} passed to export_stage_obj_entries")
    return class_str, list_name, file_name, file_header



def export_stage_obj_entries(stage_obj: StageObj, entries: list[dict[str, str]], team: Team, stage: Stage, secret: bool = False) -> None:
    class_str, list_name, file_name, file_header = get_export_names_for_stage_obj(stage_obj=stage_obj, team=team, stage=stage, secret=secret)

    entries_str_list: list[str] = [get_parsed_entry_str(entry_class_name=class_str, params=entry) for entry in entries]
    parser_result_string: str = f"\n{file_header}\n{list_name}: list[{class_str}] = \\\n[\n    {',\n    '.join(entries_str_list)}\n]"

    # noinspection PyTypeChecker
    file_to_write: str = f"{os.path.dirname(get_parsed_data_module_for_team_stage(team=team, stage=stage).__file__)}/{file_name}.py"  # pyright: ignore[reportCallIssue, reportArgumentType]

    if file_name == PLACEHOLDER_FILE_NAME:
        # Dont write file if placeholder
        return

    with open(file=file_to_write, mode="w") as output_file:
        print(f"Writing File here: {file_to_write}")
        _ = output_file.write(parser_result_string)


def parse_stage_objs_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_stage_objs_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")
    stage_obj_params_list: dict[StageObj, list[dict[str, str]]] = {stage_obj: [] for stage_obj in StageObj if stage_obj is not StageObj.ALL_STAGE_OBJECTS}

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        for x in reader:
            if x[REGION_HEADER] == "":
                continue

            stage_obj, params_dict = parse_individual_stage_obj_csv_entry(entry=x)
            stage_obj_params_list[stage_obj].append(params_dict)


    for stage_obj, params_dict in stage_obj_params_list.items():
        export_stage_obj_entries(stage_obj=stage_obj, entries=params_dict, team=team, stage=stage, secret=secret)
        pass



