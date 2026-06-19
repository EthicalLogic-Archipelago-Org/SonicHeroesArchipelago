"""
Functions used by the parser related to Item Balloons Boxes (for exporting to C#)
"""
import csv
import os


from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_functions import get_parsed_export_entry_str

from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.item_balloon_box import ItemBalloonData, ItemBoxData
from ..constants.stage import Stage, StageType




def get_item_balloon_boxes_list() -> dict[Team, dict[Stage, list[ItemBalloonData | ItemBoxData]]]:
    _result: dict[Team, dict[Stage, list[ItemBalloonData | ItemBoxData]]] = \
    {
        team: get_item_balloon_boxes_list_for_team(team=team)
        for team in Team
    }

    return _result



def get_item_balloon_boxes_list_for_team(team: Team) -> dict[Stage, list[ItemBalloonData | ItemBoxData]]:
    _result: dict[Stage, list[ItemBalloonData | ItemBoxData]] = \
    {
        stage: get_item_balloon_boxes_list_for_team_and_stage(team=team, stage=stage)
        for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)
    }
    return _result



def get_item_balloon_boxes_list_for_team_and_stage(team: Team, stage: Stage) -> list[ItemBalloonData | ItemBoxData]:
    if team is not Team.DARK or stage is not Stage.SEASIDE_HILL:
        return []
    return parsed_data.parser_item_balloon_box_mapping[stage][team]



def get_item_balloon_boxes_export_string_for_team(team: Team) -> str:
    _result: str = ""
    if team is Team.ANY_TEAM:
        return _result

    _result += f"public static List<ItemBalloonBoxesData> {team.value.replace(" ", "")}ItemBalloonBoxes = new()\n{{\n"

    for stage, item_balloon_box_list in get_item_balloon_boxes_list_for_team(team=team).items():
        for item_balloon_box in item_balloon_box_list:
            params_dict: dict[str, str] = \
            {
                "team": f"Team.{item_balloon_box.team.value}",
                "levelid": f"LevelId.{item_balloon_box.stage.stage_name.replace(" ", "")}",
                "region": f"\"{item_balloon_box.region_name.replace(f"{item_balloon_box.stage.stage_name} {item_balloon_box.team.value} ", "")}\"",
                "loc_name": f"\"{item_balloon_box.location_name.replace(f"{item_balloon_box.region_name.replace(f"{item_balloon_box.stage.stage_name} {item_balloon_box.team.value} ", "")} ", "")}\"",
                "item_reward": f"ItemReward.{item_balloon_box.item.name}",
                "stage_obj_type": f"StageObjTypes.{item_balloon_box.obj_id.value.replace(" ", "")}",
                "linkid": f"{item_balloon_box.link_id}",
                "x": f"{item_balloon_box.x}f",
                "y": f"{item_balloon_box.y}f",
                "z": f"{item_balloon_box.z}f",
            }

            _result += f"    {get_parsed_export_entry_str(entry_class_name="ItemBalloonBoxesData", params=params_dict)},\n"

    _result += f"}};\n\n"
    return _result


def get_item_balloon_boxes_export_string() -> str:
    _result: str = ""

    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_item_balloon_boxes_export_string_for_team(team=team)

    return _result



