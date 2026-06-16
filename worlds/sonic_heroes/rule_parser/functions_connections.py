"""
Functions used by the parser related to Connections
"""
import csv
import os

from .functions_parser import get_parsed_entry_str, handle_full_rule_string, get_csv_file_name
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.stage import Stage

connection_id: int = 0


def get_connection_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="Connections", secret=secret)


def parse_connection_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    global connection_id
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_connection_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        connection_str_list: list[str] = []
        for x in reader:
            connection_id += 1
            connection_name: str = f"{stage.stage_name} {team} {x[SOURCE_HEADER]} -> {x[TARGET_HEADER]}"
            source_reg: str = f"{stage.stage_name} {team} {x[SOURCE_HEADER]}"
            target_reg: str = f"{stage.stage_name} {team} {x[TARGET_HEADER]}"
            parsed_rule_str: str = ""
            if x[RULE_HEADER] == "":
                parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
            elif x[RULE_HEADER] == "NOTPOSSIBLE":
                parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
            else:
                # print(f"Rule String here: {x[RULE_HEADER]}")
                parsed_rule_str = handle_full_rule_string(rule_str=x[RULE_HEADER], team=team, stage=stage)

            class_str: str = "SonicHeroesConnectionData"

            params_dict: dict[str, str] = \
            {
                "name": f"\"{connection_name}\"",
                "source_region": f"\"{source_reg}\"",
                "target_region": f"\"{target_reg}\"",
                "rule": parsed_rule_str,
            }

            connection_str_list.append(get_parsed_entry_str(entry_class_name=class_str, params=params_dict))

            #connection_str_list.append(f"SonicHeroesConnectionData(name=\"{connection_name}\", source_region=\"{source_reg}\", target_region=\"{target_reg}\", rule={parsed_rule_str})")

    list_name: str = "CONNECTIONS"
    # list_name: str = f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Connections"

    parsed_result: str = f"\n{CONNECTION_PARSER_FILE_HEADER}\n{list_name}: list[SonicHeroesConnectionData] = \\\n[\n    {',\n    '.join(connection_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)

