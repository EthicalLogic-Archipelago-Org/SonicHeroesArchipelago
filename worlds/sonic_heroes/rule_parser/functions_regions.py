"""
Functions used by the parser related to Regions
"""
import csv
import os

from worlds.sonic_heroes.rule_parser.functions_parser import get_csv_file_name

from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.stage import Stage


def get_region_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="Regions", secret=secret)


def parse_region_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_region_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        region_str_list: list[str] = []
        for x in reader:
            region_name: str = f"{stage.stage_name} {team} {x[NAME_HEADER]}"

            region_str_list.append(f"SonicHeroesRegionData(region_name=\"{region_name}\", obj_checks={x[OBJ_CHECKS_HEADER]})")

    parsed_result: str = f"\n{REGION_PARSER_FILE_HEADER}\n{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Regions: list[SonicHeroesRegionData] = \\\n[\n    {',\n    '.join(region_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)

