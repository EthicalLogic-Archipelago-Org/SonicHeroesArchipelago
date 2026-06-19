"""
Functions used by the parser related to Enemies (for exporting to C#)
"""
import csv
import os


from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_functions import get_parsed_export_entry_str

from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.enemies import *
from ..constants.stage import Stage, StageType




def get_enemy_list() -> dict[Team, dict[Stage, list[SonicHeroesEnemyBase]]]:
    _result: dict[Team, dict[Stage, list[SonicHeroesEnemyBase]]] = \
    {
        team: get_enemy_list_for_team(team=team)
        for team in Team
    }

    return _result



def get_enemy_list_for_team(team: Team) -> dict[Stage, list[SonicHeroesEnemyBase]]:
    _result: dict[Stage, list[SonicHeroesEnemyBase]] = \
    {
        stage: get_enemy_list_for_team_and_stage(team=team, stage=stage)
        for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)
    }
    return _result



def get_enemy_list_for_team_and_stage(team: Team, stage: Stage) -> list[SonicHeroesEnemyBase]:
    if team is not Team.DARK or stage is not Stage.SEASIDE_HILL:
        return []
    return parsed_data.parser_enemy_mapping[stage][team]



def get_enemy_export_string_for_team(team: Team) -> str:
    _result: str = ""
    if team is Team.ANY_TEAM:
        return _result

    _result += f"public static List<EnemySanityData> {team.value.replace(" ", "")}Enemies = new()\n{{\n"

    for stage, enemy_list in get_enemy_list_for_team(team=team).items():
        for enemy in enemy_list:
            params_dict: dict[str, str] = \
                {
                    "team": f"Team.{enemy.team.value}",
                    "levelid": f"LevelId.{enemy.stage.stage_name.replace(" ", "")}",
                    "region": f"\"{enemy.region_name.replace(f"{enemy.stage.stage_name} {enemy.team.value} ", "")}\"",
                    "loc_name": f"\"{enemy.location_name.replace(f"{enemy.region_name.replace(f"{enemy.stage.stage_name} {enemy.team.value} ", "")} ", "")}\"",
                    "linkid": f"{enemy.link_id}",
                    "x": f"{enemy.x}f",
                    "y": f"{enemy.y}f",
                    "z": f"{enemy.z}f",
                }
            _result += f"    {get_parsed_export_entry_str(entry_class_name="EnemySanityData", params=params_dict)},\n"

    _result += f"}};\n\n"
    return _result


def get_enemy_export_string() -> str:
    _result: str = ""

    for team in Team:
        print(f"Getting export string for {team}")
        _result += get_enemy_export_string_for_team(team=team)

    return _result













