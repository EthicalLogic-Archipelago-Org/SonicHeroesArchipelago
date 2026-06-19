"""
Functions used by the parser related to Hint Rings (for exporting to C#)
"""
import csv
import os

from .functions_hint_ring import get_hint_ring_csv_file_name
from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .rule_parser_c_sharp_functions import get_parsed_export_entry_str
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.hint_rings import HINT_RING, HintRingData
from ..constants.stage import Stage, StageType



def get_hint_ring_list() -> dict[Team, dict[Stage, list[HintRingData]]]:
    _result: dict[Team, dict[Stage, list[HintRingData]]] = \
    {
        team: get_hint_ring_list_for_team(team=team)
        for team in Team
    }

    return _result



def get_hint_ring_list_for_team(team: Team) -> dict[Stage, list[HintRingData]]:
    _result: dict[Stage, list[HintRingData]] = \
    {
        stage: get_hint_ring_list_for_team_and_stage(team=team, stage=stage)
        for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)
    }
    return _result



def get_hint_ring_list_for_team_and_stage(team: Team, stage: Stage) -> list[HintRingData]:
    if team is not Team.DARK or stage is not Stage.SEASIDE_HILL:
        return []
    return parsed_data.parser_hint_ring_mapping[stage][team]



def get_hint_ring_export_string_for_team(team: Team) -> str:
    _result: str = ""
    if team is Team.ANY_TEAM:
        return _result

    _result += f"public static List<HintRingsData> {team.value.replace(" ", "")}HintRings = new()\n{{\n"

    for stage, hint_ring_list in get_hint_ring_list_for_team(team=team).items():
        for hint_ring in hint_ring_list:
            params_dict: dict[str, str] = \
                {
                    "team": f"Team.{hint_ring.team.value}",
                    "levelid": f"LevelId.{hint_ring.stage.stage_name.replace(" ", "")}",
                    "region": f"\"{hint_ring.region_name.replace(f"{hint_ring.stage.stage_name} {hint_ring.team.value} ", "")}\"",
                    "voicelineid": f"{hint_ring.voice_line}",
                    "linkid": f"{hint_ring.link_id}",
                    "x": f"{hint_ring.x}f",
                    "y": f"{hint_ring.y}f",
                    "z": f"{hint_ring.z}f",
                }
            _result += f"    {get_parsed_export_entry_str(entry_class_name="HintRingsData", params=params_dict)},\n"

    _result += f"}};\n\n"
    return _result


def get_hint_ring_export_string() -> str:
    _result: str = ""

    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_hint_ring_export_string_for_team(team=team)

    return _result













