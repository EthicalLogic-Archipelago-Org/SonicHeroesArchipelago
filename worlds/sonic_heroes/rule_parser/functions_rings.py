"""
Functions used by the parser related to Rings
"""
import csv
import os


from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.rings import RingLayout
from ..constants.stage import Stage


def get_ring_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="Rings", secret=secret)


def parse_ring_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_ring_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        ring_str_list: list[str] = []
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

            name_str: str = f"{stage.stage_name} {team} {x[REGION_HEADER]} {x[NAME_HEADER]}"

            layout: RingLayout = RingLayout(value=x[TYPE_HEADER])
            layout_str: str = f"{layout.__class__.__name__}.{layout.name}"

            class_str: str = "RingData"
            params_dict: dict[str, str] = \
            {
                "team": team_str,
                "stage": stage_str,
                "location_name": f"\"{name_str}\"",
                "region_name": f"\"{region_name}\"",
                "layout": layout_str,
                "num_rings": x[NUM_RINGS_HEADER],
                "length": x[LENGTH_HEADER],
                "radius": x[RADIUS_HEADER],
                "link_id": str(x[LINK_ID_HEADER]),
                "x": str(x[X_HEADER]),
                "y": str(x[Y_HEADER]),
                "z": str(x[Z_HEADER]),
                "rule": parsed_rule_str,
            }

            ring_str_list.append(get_parsed_entry_str(entry_class_name=class_str, params=params_dict))

            # ring_str_list.append(f"RingData(team={team_str}, stage={stage_str}, location_name=\"{name_str}\", region_name=\"{region_name}\", layout={layout_str}, num_rings={x[NUM_RINGS_HEADER]}, length={x[LENGTH_HEADER]}, radius={x[RADIUS_HEADER]}, link_id={x[LINK_ID_HEADER]}, x={float(x[X_HEADER])}, y={float(x[Y_HEADER])}, z={float(x[Z_HEADER])}, rule={parsed_rule_str})")

    list_name: str = "RINGS"

    parsed_result: str = f"\n{RING_PARSER_FILE_HEADER}\n{list_name}: list[RingData] = \\\n[\n    {',\n    '.join(ring_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)
