"""
Functions used by the parser related to Hint Rings
"""
import csv
import os


from .functions_parser import handle_full_rule_string, get_csv_file_name, get_parsed_entry_str
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.triple_spring import *
from ..constants.stage import Stage


def get_triple_spring_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="TripleSprings", secret=secret)



def parse_triple_spring_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_triple_spring_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        triple_spring_str_list: list[str] = []
        for x in reader:
            parsed_rule_str: str = ""
            if x[RULE_HEADER] == "":
                parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
            elif x[RULE_HEADER] == "NOTPOSSIBLE":
                parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
            else:
                print(f"Rule String here: {x[RULE_HEADER]}")
                parsed_rule_str = handle_full_rule_string(rule_str=x[RULE_HEADER], team=team, stage=stage)

            team_str: str = f"{team.__class__.__name__}.{team.name}"
            stage_str: str = f"{stage.__class__.__name__}.{stage.name}"
            region_name: str = f"{stage.stage_name} {team} {x[REGION_HEADER]}"
            item_reward: ItemReward = ItemReward(value=x[ITEM_HEADER])
            item_str: str = f"{item_reward.__class__.__name__}.{item_reward.name}"



            class_str: str = "TripleSpringData"
            name_str: str = f"{x[REGION_HEADER]} {x[NAME_HEADER]}"


            params_dict: dict[str, str] = \
            {
                "team": team_str,
                "stage": stage_str,
                "location_name": f"\"{name_str}\"",
                "region_name": f"\"{region_name}\"",
                "power": x[POWER_HEADER],
                "no_control_time": x[NO_CONTROL_TIME_HEADER],
                "item": item_str,
                "link_id": str(x[LINK_ID_HEADER]),
                "scale": x[SCALE_HEADER],
                "x": str(x[X_HEADER]),
                "y": str(x[Y_HEADER]),
                "z": str(x[Z_HEADER]),
                "rule": parsed_rule_str,
            }

            triple_spring_str_list.append(get_parsed_entry_str(entry_class_name=f"{class_str}", params=params_dict))

    list_name: str = "TRIPLE_SPRINGS"
    # list_name: str = f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}ItemBalloonBoxes"

    parsed_result: str = f"\n{TRIPLE_SPRING_PARSER_FILE_HEADER}\n{list_name}: list[TripleSpringData] = \\\n[\n    {',\n    '.join(triple_spring_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)