"""
Functions used by the parser related to Regions
"""
import csv
import os

from .functions_parser import get_csv_file_name, get_parsed_entry_str

from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.stage import Stage
from ..helper_functions import *


def get_region_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="Regions", secret=secret)


def get_region_export_names(team: Team, stage: Stage, secret: bool = False) -> tuple[str, str, str, str]:
    class_str: str = "SonicHeroesRegionData"
    list_name: str = "REGIONS"
    file_name: str = get_region_csv_file_name(team=team, stage=stage, secret=secret)
    return class_str, list_name, file_name, REGION_PARSER_FILE_HEADER


def parse_region_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    class_str, list_name, file_name, file_header = get_region_export_names(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        region_str_list: list[str] = []
        for x in reader:
            region_name: str = f"{stage.stage_name} {team} {x[NAME_HEADER]}"

            params_dict: dict[str, str] = \
            {
                "region_name": f"\"{region_name}\"",
                "obj_checks": x[OBJ_CHECKS_HEADER],
            }

            region_str_list.append(get_parsed_entry_str(entry_class_name=class_str, params=params_dict))
            #region_str_list.append(f"SonicHeroesRegionData(region_name=\"{region_name}\", obj_checks={x[OBJ_CHECKS_HEADER]})")

    # list_name: str = f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Regions"

    parsed_result: str = f"\n{file_header}\n{list_name}: list[{class_str}] = \\\n[\n    {',\n    '.join(region_str_list)}\n]"

    # noinspection PyTypeChecker
    file_to_write: str = f"{os.path.dirname(get_parsed_data_module_for_team_stage(team=team, stage=stage).__file__)}/{file_name}.py"  # pyright: ignore[reportCallIssue, reportArgumentType]
    with open(file=file_to_write, mode="w") as output_file:
        print(f"Writing File here: {file_to_write}")
        _ = output_file.write(parsed_result)

