"""
Functions used by the parser related to Hint Rings (for exporting to C#)
"""
from .rule_parser_export_functions import get_parsed_export_entry_str
from ..rule_parser.functions_parser import *
from ..constants.char_ability import Team
from ..constants.stage import Stage, StageType
from ..constants.hint_rings import *


def get_hint_rings_export_string_for_team(team: Team, parsed_data: dict[Stage, list[HintRingData]]) -> str:
    _result: str = ""
    class_str: str = "HintRingsData"
    list_name: str = "HintRings"
    tab_char: str = "    "

    if team is Team.ANY_TEAM:
        return _result

    _result += f"{tab_char}public static List<{class_str}> {team.value.replace(" ", "")}{list_name} = new()\n{tab_char}{{\n"

    for stage, parsed_list in parsed_data.items():
        for parsed_entry in parsed_list:
            params_dict: dict[str, str] = \
            {
                "team": f"Team.{parsed_entry.team.value}",
                "levelid": f"LevelId.{parsed_entry.stage.stage_name.replace(" ", "")}",
                "region": f"\"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")}\"",
                "voicelineid": f"{parsed_entry.voice_line}",
                "linkid": f"{parsed_entry.link_id}",
                "x": f"{parsed_entry.x}f",
                "y": f"{parsed_entry.y}f",
                "z": f"{parsed_entry.z}f",
            }

            _result += f"{tab_char}{tab_char}{get_parsed_export_entry_str(entry_class_name=class_str, params=params_dict)},\n"

    if _result[-2:] != ",\n":
        _result += f"{tab_char}{tab_char}\n"
    _result += f"{tab_char}}};\n\n"
    return _result




def get_hint_rings_export_string() -> str:
    _result: str = ""
    full_parsed_data: dict[Team, dict[Stage, list[HintRingData]]] = get_all_hint_rings()
    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_hint_rings_export_string_for_team(team=team, parsed_data=full_parsed_data[team])
    return _result