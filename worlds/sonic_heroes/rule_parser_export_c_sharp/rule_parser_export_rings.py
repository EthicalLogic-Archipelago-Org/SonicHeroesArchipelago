"""
Functions used by the parser related to Rings (for exporting to C#)
"""
from .rule_parser_export_functions import get_parsed_export_entry_str
from ..rule_parser.functions_parser import *
from ..constants.char_ability import Team
from ..constants.stage import Stage, StageType
from ..constants.rings import *




def get_rings_export_string_for_team(team: Team, parsed_data: dict[Stage, list[RingData]]) -> str:
    _result: str = ""
    class_str: str = "RingData"
    list_name: str = "Rings"
    tab_char: str = "    "

    if team is Team.ANY_TEAM:
        return _result

    _result += f"{tab_char}public static List<{class_str}> {team.value.replace(" ", "")}{list_name} = new()\n{tab_char}{{\n"

    for stage, ring_list in parsed_data.items():
        for parsed_entry in ring_list:
            params_dict: dict[str, str] = \
                {
                    "Team": f"Team.{parsed_entry.team.value}",
                    "LevelId": f"LevelId.{parsed_entry.stage.stage_name.replace(" ", "")}",
                    "Region": f"\"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")}\"",
                    "LocName": f"\"{parsed_entry.location_name}\"",
                    "NumRings": f"{parsed_entry.num_rings}",
                    "RingType": f"RingType.{parsed_entry.layout.value}",
                    "Length": f"{parsed_entry.length}f",
                    "Radius": f"{parsed_entry.radius}f",
                    "Group": f"{parsed_entry.group}",
                    "IdOffsetGroup": f"{parsed_entry.id_offset_group}",
                    "IdOffsetFull": f"{parsed_entry.id_offset_full}",
                    "LinkID": f"{parsed_entry.link_id}",
                    "SpawnCoords": f"new Vector3(x: {parsed_entry.x}f, y: {parsed_entry.y}f, z: {parsed_entry.z}f)",
                    # "rule": f"\"{parsed_entry.rule}\"",
                }
            _result += f"{tab_char}{tab_char}{get_parsed_export_entry_str(entry_class_name=class_str, params=params_dict)},\n"

            # if parsed_entry.id_offset >= 0:
            #     start_id_offset += parsed_entry.num_rings

    if _result[-2:] != ",\n":
        _result += f"{tab_char}{tab_char}\n"
    _result += f"{tab_char}}};\n\n"
    return _result




def get_rings_export_string() -> str:
    _result: str = ""
    full_parsed_data: dict[Team, dict[Stage, list[RingData]]] = get_all_rings()
    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_rings_export_string_for_team(team=team, parsed_data=full_parsed_data[team])
    return _result

