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
                    "team": f"Team.{parsed_entry.team.value}",
                    "levelid": f"LevelId.{parsed_entry.stage.stage_name.replace(" ", "")}",
                    "region": f"\"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")}\"",
                    "loc_name": f"\"{parsed_entry.location_name.replace(f"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")} ", "")}\"",
                    "num_rings": f"{parsed_entry.num_rings}",
                    "ring_type": f"RingType.{parsed_entry.layout.value}",
                    "length": f"{parsed_entry.length}f",
                    "radius": f"{parsed_entry.radius}f",
                    "group": f"{parsed_entry.group}",
                    "id_offset_group": f"{parsed_entry.id_offset_group}",
                    "id_offset_full": f"{parsed_entry.id_offset_full}",
                    "linkid": f"{parsed_entry.link_id}",
                    "x": f"{parsed_entry.x}f",
                    "y": f"{parsed_entry.y}f",
                    "z": f"{parsed_entry.z}f",
                    "rule": f"\"{parsed_entry.rule}\"",
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

