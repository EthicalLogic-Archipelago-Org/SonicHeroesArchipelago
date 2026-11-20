"""
Functions used by the parser related to Triple Springs (for exporting to C#)
"""
from .rule_parser_export_functions import get_parsed_export_entry_str
from ..rule_parser.functions_parser import *
from ..constants.char_ability import Team
from ..constants.stage import Stage, StageType
from ..constants.triple_spring import *


def get_triple_springs_export_string_for_team(team: Team, parsed_data: dict[Stage, list[TripleSpringData]]) -> str:
    _result: str = ""
    class_str: str = "TripleSpringData"
    list_name: str = "TripleSprings"
    tab_char: str = "    "

    if team is Team.ANY_TEAM:
        return _result

    _result += f"{tab_char}public static List<{class_str}> {team.value.replace(" ", "")}{list_name} = new()\n{tab_char}{{\n"

    for stage, parsed_list in parsed_data.items():
        for parsed_entry in parsed_list:
            params_dict: dict[str, str] = \
            {
                "Team": f"Team.{parsed_entry.team.value}",
                "LevelId": f"LevelId.{parsed_entry.stage.stage_name.replace(" ", "")}",
                "Region": f"\"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")}\"",
                "LocName": f"\"{parsed_entry.location_name}\"",
                "Power": f"{parsed_entry.power}f",
                "NoControlTime": f"{parsed_entry.no_control_time}",
                "ItemReward": f"ItemReward.{parsed_entry.item.name}",
                "Scale": f"{parsed_entry.scale}f",
                "Group": f"{parsed_entry.group}",
                "IdOffsetGroup": f"{parsed_entry.id_offset_group}",
                "IdOffsetFull": f"{parsed_entry.id_offset_full}",
                "LinkID": f"{parsed_entry.link_id}",
                "SpawnCoords": f"new Vector3(x: {parsed_entry.x}f, y: {parsed_entry.y}f, z: {parsed_entry.z}f)",
            }

            _result += f"{tab_char}{tab_char}{get_parsed_export_entry_str(entry_class_name=class_str, params=params_dict)},\n"

    if _result[-2:] != ",\n":
        _result += f"{tab_char}{tab_char}\n"
    _result += f"{tab_char}}};\n\n"
    return _result




def get_triple_springs_export_string() -> str:
    _result: str = ""
    full_parsed_data: dict[Team, dict[Stage, list[TripleSpringData]]] = get_all_triple_springs()
    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_triple_springs_export_string_for_team(team=team, parsed_data=full_parsed_data[team])
    return _result

