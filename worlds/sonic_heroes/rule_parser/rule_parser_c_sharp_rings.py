"""
Functions used by the parser related to Rings (for exporting to C#)
"""
import csv
import os

from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_functions import get_parsed_export_entry_str


from .functions_hint_ring import get_hint_ring_csv_file_name
from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.hint_rings import HINT_RING, HintRingData
from ..constants.rings import RingData
from ..constants.stage import Stage, StageType



start_id_offset: int = 0




def get_ring_list() -> dict[Team, dict[Stage, list[RingData]]]:
    _result: dict[Team, dict[Stage, list[RingData]]] = \
    {
        team: get_ring_list_for_team(team=team)
        for team in Team
    }

    return _result



def get_ring_list_for_team(team: Team) -> dict[Stage, list[RingData]]:
    _result: dict[Stage, list[RingData]] = \
    {
        stage: get_ring_list_for_team_and_stage(team=team, stage=stage)
        for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)
    }
    return _result



def get_ring_list_for_team_and_stage(team: Team, stage: Stage) -> list[RingData]:
    if team is not Team.DARK or stage is not Stage.SEASIDE_HILL:
        return []
    return parsed_data.parser_ring_mapping[stage][team]



def get_ring_export_string_for_team(team: Team) -> str:
    global start_id_offset
    _result: str = ""
    if team is Team.ANY_TEAM:
        return _result

    _result += f"public static List<RingsData> {team.value.replace(" ", "")}Rings = new()\n{{\n"

    for stage, ring_list in get_ring_list_for_team(team=team).items():
        for ring in ring_list:
            params_dict: dict[str, str] = \
            {
                "team": f"Team.{ring.team.value}",
                "levelid": f"LevelId.{ring.stage.stage_name.replace(" ", "")}",
                "region": f"\"{ring.region_name.replace(f"{ring.stage.stage_name} {ring.team.value} ", "")}\"",
                "loc_name": f"\"{ring.location_name.replace(f"{ring.region_name.replace(f"{ring.stage.stage_name} {ring.team.value} ", "")} ", "")}\"",
                "num_rings": f"{ring.num_rings}",
                "ring_type": f"RingType.{ring.layout.value}",
                "length": f"{ring.length}f",
                "radius": f"{ring.radius}f",
                "start_id_offset": f"{start_id_offset}",
                "id_offset": f"{ring.id_offset}",
                "linkid": f"{ring.link_id}",
                "x": f"{ring.x}f",
                "y": f"{ring.y}f",
                "z": f"{ring.z}f",
                "rule": f"\"{ring.rule}\"",
            }
            _result += f"    {get_parsed_export_entry_str(entry_class_name="RingsData", params=params_dict)},\n"

            if ring.id_offset >= 0:
                start_id_offset += ring.num_rings

    _result += f"}};\n\n"
    return _result


def get_ring_export_string() -> str:
    _result: str = ""

    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_ring_export_string_for_team(team=team)

    return _result


