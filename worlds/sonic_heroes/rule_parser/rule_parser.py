"""
Regex Rule Parsing
"""
import csv
import os.path

from worlds.sonic_heroes.constants import item_balloon_box
from worlds.sonic_heroes.constants.char_ability import Team
from worlds.sonic_heroes.constants.item_balloon_box import ItemReward
from worlds.sonic_heroes.constants.stage import Stage

from worlds.sonic_heroes import csv_data
from worlds.sonic_heroes import parsed_data

from worlds.sonic_heroes.rule_parser.parser_constants import *
from worlds.sonic_heroes.rule_parser.parser_matches import PARSER_ALL_MATCHES

result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []
connection_id: int = 0


# def is_rule_in_mapping(rule_str: str) -> bool:
#     return rule_str in PARSER_ALL_MATCHES


def is_there_parens(rule_str: str) -> bool:
    return '(' in rule_str and ')' in rule_str


def is_there_and(rule_str: str) -> bool:
    return 'AND' in rule_str


def is_there_or(rule_str: str) -> bool:
    return 'OR' in rule_str


def do_start_and_end_parens_match(rule_str: str) -> bool:
    if not (rule_str[0] == '(' and rule_str[-1] == ')'):
        return False
    paren_match: int = 0
    for index, char in enumerate(rule_str):
        if char == '(':
            paren_match += 1
            continue
        if char == ')':
            paren_match -= 1
        if paren_match == 0:
            return index == len(rule_str) - 1
    return False


def handle_rule_str(rule_str: str, team: Team, stage: Stage, print_steps: bool = False) -> None:
    global result_str_list, parens_mapping_list
    if rule_str == '':
        return

    if print_steps:
        print(f"Rule: {rule_str}")

    if rule_str == "OR":
        result_str_list.append(rule_str)
        return

    if rule_str == "AND":
        result_str_list.append(rule_str)
        return

    if do_start_and_end_parens_match(rule_str):
        handle_rule_str(rule_str=rule_str[1:-1], team=team, stage=stage, print_steps=print_steps)
        return


    # parens handling
    if is_there_parens(rule_str):
        temp_var: list[str] = OUTER_PARENS_PATTERN.split(string=rule_str)  # pyright: ignore[reportRedeclaration]
        if print_steps:
            print(f"temp_var={temp_var}")
        handle_rule_str(rule_str=temp_var[0], team=team, stage=stage, print_steps=print_steps)

        temp_scanner = OUTER_PARENS_PATTERN.finditer(string=rule_str)

        for index, scan_match in enumerate(temp_scanner):
            temp_index: int = len(result_str_list)
            result_str_list.append('(')
            temp_tuple: tuple[int, int] = (temp_index, temp_index)
            handle_rule_str(rule_str=scan_match.group(), team=team, stage=stage, print_steps=print_steps)
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

            handle_rule_str(rule_str=temp_var[index + 1], team=team, stage=stage, print_steps=print_steps)

        return


    if is_there_and(rule_str):
        temp_var: list[str] = AND_CONDITION_PATTERN.split(string=rule_str)  # pyright: ignore[reportRedeclaration]
        if print_steps:
            print(f"Temp AND Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule_str(rule_str=split, team=team, stage=stage, print_steps=print_steps)
            #if index < len(temp_var) - 1:
                #result_str_list.append('AND')
        return

    if is_there_or(rule_str):
        temp_var: list[str] = OR_CONDITION_PATTERN.split(string=rule_str)
        if print_steps:
            print(f"Temp OR Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule_str(rule_str=split, team=team, stage=stage, print_steps=print_steps)
        return

    result_str_list.append(rule_str)


def handle_full_rule_string(rule_str: str, team: Team, stage: Stage, print_steps: bool = False) -> str:
    global result_str_list, parens_mapping_list
    result_str_list = []
    parens_mapping_list = []
    result_str: str = ""
    handle_rule_str(rule_str=rule_str, team=team, stage=stage, print_steps=print_steps)

    #now handle output
    for index, rule_piece in enumerate(result_str_list):
        if rule_piece != ")" and result_str[-1:] != " " and result_str[-1:] != "(" and index != 0:
            result_str += " "

        if rule_piece == "(":
            result_str += f"{rule_piece}"
            continue
        if rule_piece == ")":
            result_str += f"{rule_piece}"
            continue
        if rule_piece == "AND":
            result_str += f"&"
            continue
        if rule_piece == "OR":
            result_str += f"|"
            continue
        result_str += f"{PARSER_ALL_MATCHES[rule_piece](team, stage)}"
    return result_str


# test_rule3 = "(FlyAnyOR(JumpAND(Homing0ORTornado0HoverORGlide)))ANDRuinsNoTrigger"
# print(handle_full_rule_string(rule_str=test_rule3, team=Team.DARK, stage=Stage.SEASIDE_HILL, print_steps=True))


def get_region_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Regions"


def get_connection_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Connections"


def get_hint_ring_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}HintRings"


def get_item_balloon_box_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}ItemBalloonBoxes"


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
            connection_name: str = f"{stage.stage_name} {team} Connection {connection_id}"
            source_reg: str = f"{stage.stage_name} {team} {x[SOURCE_HEADER]}"
            target_reg: str = f"{stage.stage_name} {team} {x[TARGET_HEADER]}"
            parsed_rule_str: str = ""
            if x[RULE_HEADER] == "":
                parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
            elif x[RULE_HEADER] == "NOTPOSSIBLE":
                parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
            else:
                print(f"Rule String here: {x[RULE_HEADER]}")
                parsed_rule_str = handle_full_rule_string(rule_str=x[RULE_HEADER], team=team, stage=stage)

            connection_str_list.append(f"SonicHeroesConnectionData(name=\"{connection_name}\", source_region=\"{source_reg}\", target_region=\"{target_reg}\", rule={parsed_rule_str})")

    parsed_result: str = f"\n{CONNECTION_PARSER_FILE_HEADER}\n{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Connections: list[SonicHeroesConnectionData] = \\\n[\n    {',\n    '.join(connection_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)


def parse_hint_ring_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_hint_ring_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        hint_ring_str_list: list[str] = []
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
            voice_line: int = int(x[VOICE_LINE_HEADER])


            hint_ring_str_list.append(f"HintRingData(team={team_str}, stage={stage_str}, region_name=\"{region_name}\", voice_line={voice_line}, x={float(x[X_HEADER])}, y={float(x[Y_HEADER])}, z={float(x[Z_HEADER])}, rule={parsed_rule_str})")


    parsed_result: str = f"\n{HINT_RING_PARSER_FILE_HEADER}\n{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}HintRings: list[HintRingData] = \\\n[\n    {',\n    '.join(hint_ring_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parse_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)


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



# parse_region_csv(team=Team.DARK, stage=Stage.SEASIDE_HILL)
# parse_connection_csv(team=Team.DARK, stage=Stage.SEASIDE_HILL)
# parse_hint_ring_csv(team=Team.DARK, stage=Stage.SEASIDE_HILL)
# parse_item_box_balloon_csv(team=Team.DARK, stage=Stage.SEASIDE_HILL)




