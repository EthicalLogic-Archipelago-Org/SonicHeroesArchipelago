"""
Functions used by the parser related to Mappings
"""
import os


from .functions_connections import get_connection_export_names
from .functions_parser import *
from .functions_regions import get_region_export_names
from .functions_stage_objs import get_export_names_for_stage_obj
from .parser_constants import *
from .. import csv_data
from .. import parsed_data

from ..constants.char_ability import Team
from ..constants.loc_region import CONNECTION, REGION
from ..constants.stage import Stage, StageType
from ..constants.stage_objs import StageObj


def export_top_level_mappings(parsed_team_stages: dict[Team, list[Stage]]) -> None:

    top_level_mapping_file_header: str = \
        f"""{PARSER_DOCSTRING_MSG}
from types import ModuleType
from ..constants.stage import Stage
"""
    top_level_mapping_file_header += "from . import "
    top_level_mapping_file_header += f"{", ".join([f"{stage.stage_name.replace(" ", "")}" for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)])}\n\n"
    top_level_mapping_file_header += f"parser_level_result_mapping: dict[Stage, ModuleType] = \\\n{{\n    "
    top_level_mapping_file_header += f"{",\n    ".join([f"{stage.__class__.__name__}.{stage.name}: {stage.stage_name.replace(" ", "")}" for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE)])}\n}}\n"

    # noinspection PyTypeChecker
    file_to_write: str = f"{os.path.dirname(parsed_data.__file__)}/__init__.py"
    with open(file=file_to_write, mode="w") as output_file:
        print(f"Writing File here: {file_to_write}")
        _ = output_file.write(top_level_mapping_file_header)
    pass





def export_level_init_mappings(stage: Stage) -> None:
    level_init_file_header: str = \
    f"""{PARSER_DOCSTRING_MSG}
from types import ModuleType
from . import Sonic, Dark, Rose, Chaotix, SuperHardMode, AnyTeam
from ...constants.char_ability import Team

parser_team_result_mapping: dict[Team, ModuleType] = \\
{{
    Team.SONIC: Sonic,
    Team.DARK: Dark,
    Team.ROSE: Rose,
    Team.CHAOTIX: Chaotix,
    Team.SUPER_HARD_MODE: SuperHardMode,
    Team.ANY_TEAM: AnyTeam,
}}

__all__ = ["parser_team_result_mapping"]
"""

    # noinspection PyTypeChecker
    file_to_write: str = f"{os.path.dirname(get_parsed_data_module_for_stage(stage=stage).__file__)}/__init__.py"  # pyright: ignore[reportCallIssue, reportArgumentType]
    with open(file=file_to_write, mode="w") as output_file:
        print(f"Writing File here: {file_to_write}")
        _ = output_file.write(level_init_file_header)




def get_file_header_for_team_init_mappings(team: Team, stage: Stage) -> str:
    _result: str = f"{PARSER_DOCSTRING_MSG}\n"
    # class_str: str = "PLACEHOLDER_CLASS"
    # list_name: str = "PLACEHOLDER_LIST_NAME"
    # file_name: str = "PLACEHOLDER_FILE_NAME"
    # file_header: str = "PLACEHOLDER_FILE_HEADER"
    for thing_to_parse in THINGS_TO_PARSE:
        if thing_to_parse == REGION:
            class_str, list_name, file_name, file_header = get_region_export_names(team=team, stage=stage, secret=False)
        elif thing_to_parse == CONNECTION:
            class_str, list_name, file_name, file_header = get_connection_export_names(team=team, stage=stage, secret=False)
        else:
            stage_obj: StageObj = StageObj(value=thing_to_parse)
            class_str, list_name, file_name, file_header = get_export_names_for_stage_obj(stage_obj=stage_obj, team=team, stage=stage, secret=False)
        _result += f"from .{file_name} import *\n"
    _result += f"\n"
    return _result


def get_export_for_team_init_mappings_with_secret(team: Team, stage: Stage) -> None:
    #This will be painful btw
    pass


def get_export_for_team_init_mappings_without_secret(team: Team, stage: Stage) -> str:
    _result: str = get_file_header_for_team_init_mappings(team=team, stage=stage)

    for thing_to_parse in THINGS_TO_PARSE:
        if thing_to_parse == REGION:
            class_str, list_name, file_name, file_header = get_region_export_names(team=team, stage=stage, secret=False)
        elif thing_to_parse == CONNECTION:
            class_str, list_name, file_name, file_header = get_connection_export_names(team=team, stage=stage, secret=False)
        else:
            stage_obj: StageObj = StageObj(value=thing_to_parse)
            class_str, list_name, file_name, file_header = get_export_names_for_stage_obj(stage_obj=stage_obj, team=team, stage=stage, secret=False)

        _result += f"{list_name.lower()}: list[{class_str}] = {list_name}\n"
    return _result


def export_team_init_mappings(team: Team, stage: Stage) -> None:
    str_to_write: str = get_export_for_team_init_mappings_without_secret(team=team, stage=stage)
    # noinspection PyTypeChecker
    file_to_write: str = f"{os.path.dirname(get_parsed_data_module_for_team_stage(team=team, stage=stage).__file__)}/__init__.py"  # pyright: ignore[reportCallIssue, reportArgumentType]
    with open(file=file_to_write, mode="w") as output_file:
        print(f"Writing File here: {file_to_write}")
        _ = output_file.write(str_to_write)




def export_all_mappings(parsed_team_stages: dict[Team, list[Stage]]) -> None:
    export_top_level_mappings(parsed_team_stages=parsed_team_stages)
    for team, stage_list in parsed_team_stages.items():
        for stage in stage_list:

            export_level_init_mappings(stage=stage)
            export_team_init_mappings(team=team, stage=stage)
            pass





