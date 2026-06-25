"""
Functions used by the parser related to Triple Springs (for exporting to C#)
"""
import csv
import os


from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_functions import get_parsed_export_entry_str

from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.triple_spring import *
from ..constants.stage import Stage, StageType




def get_triple_springs_list() -> dict[Team, dict[Stage, list[TripleSpringData]]]:
    _result: dict[Team, dict[Stage, list[TripleSpringData]]] = \
    {
        team: get_triple_springs_list_for_team(team=team)
        for team in Team
    }

    return _result



def get_triple_springs_list_for_team(team: Team) -> dict[Stage, list[TripleSpringData]]:
    _result: dict[Stage, list[TripleSpringData]] = \
    {
        stage: get_triple_springs_list_for_team_and_stage(team=team, stage=stage)
        for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)
    }
    return _result



def get_triple_springs_list_for_team_and_stage(team: Team, stage: Stage) -> list[TripleSpringData]:
    if team is not Team.DARK or stage is not Stage.SEASIDE_HILL:
        return []
    return parsed_data.parser_triple_spring_mapping[stage][team]



def get_triple_springs_export_string_for_team(team: Team) -> str:
    _result: str = ""
    if team is Team.ANY_TEAM:
        return _result

    _result += f"public static List<TripleSpringsData> {team.value.replace(" ", "")}TripleSprings = new()\n{{\n"

    for stage, triple_spring_list in get_triple_springs_list_for_team(team=team).items():
        for triple_spring in triple_spring_list:
            params_dict: dict[str, str] = \
            {
                "team": f"Team.{triple_spring.team.value}",
                "levelid": f"LevelId.{triple_spring.stage.stage_name.replace(" ", "")}",
                "region": f"\"{triple_spring.region_name.replace(f"{triple_spring.stage.stage_name} {triple_spring.team.value} ", "")}\"",
                "loc_name": f"\"{triple_spring.location_name.replace(f"{triple_spring.region_name.replace(f"{triple_spring.stage.stage_name} {triple_spring.team.value} ", "")} ", "")}\"",
                "power": f"{triple_spring.power}f",
                "no_control_time": f"{triple_spring.no_control_time}",
                "item_reward": f"ItemReward.{triple_spring.item.name}",
                "scale": f"{triple_spring.scale}f",
                "stage_obj_type": f"StageObjTypes.{triple_spring.obj_id.value.replace(" ", "")}",
                "linkid": f"{triple_spring.link_id}",
                "x": f"{triple_spring.x}f",
                "y": f"{triple_spring.y}f",
                "z": f"{triple_spring.z}f",
            }

            _result += f"    {get_parsed_export_entry_str(entry_class_name="TripleSpringsData", params=params_dict)},\n"

    _result += f"}};\n\n"
    return _result


def get_triple_springs_export_string() -> str:
    _result: str = ""

    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_triple_springs_export_string_for_team(team=team)

    return _result



