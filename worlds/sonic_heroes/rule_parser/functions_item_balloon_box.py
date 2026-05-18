"""
Functions used by the parser related to Hint Rings
"""
import csv
import os


from .functions_parser import handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.item_balloon_box import *
from ..constants.stage import Stage


def get_item_balloon_box_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}ItemBalloonBoxes"


def parse_item_box_balloon_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_item_balloon_box_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        item_balloon_box_str_list: list[str] = []
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

            item_balloon_box_str_list.append(f"ItemBalloonBoxData(team={team_str}, stage={stage_str}, region_name=\"{region_name}\", item={item_str}, x={float(x[X_HEADER])}, y={float(x[Y_HEADER])}, z={float(x[Z_HEADER])}, rule={parsed_rule_str})")


    parsed_result: str = f"\n{ITEM_BALLOON_BOX_PARSER_FILE_HEADER}\n{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}ItemBalloonBoxes: list[ItemBalloonBoxData] = \\\n[\n    {',\n    '.join(item_balloon_box_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)


