"""
Functions used by the parser
"""
import dataclasses
import enum
from types import ModuleType
from typing import Any

from .. import parsed_data
from .parser_constants import *
from .parser_matches import PARSER_ALL_MATCHES
from ..constants.char_ability import Team
from ..constants.enemies import EggFlapper, EggPawn, SonicHeroesEnemyBase
from ..constants.hint_rings import HintRingData
from ..constants.item_balloon_box import ItemBoxData, ItemBalloonData
from ..constants.loc_region import CONNECTION, REGION
from ..constants.rings import RingData
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj
from ..constants.triple_spring import TripleSpringData


result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []

def get_stage_objs_to_parse() -> list[StageObj]:
    return \
    [
        StageObj.TRIPLE_SPRING,
        StageObj.RINGS,
        StageObj.HINT_RING,
        StageObj.ITEM_BOX,
        StageObj.ITEM_BALLOON,
        StageObj.EGG_FLAPPER,
        StageObj.EGG_PAWN,
    ]


THINGS_TO_PARSE: list[str | StageObj] = \
[
    REGION,
    CONNECTION,
    *get_stage_objs_to_parse(),
]


def get_parsed_data_module_for_stage(stage: Stage) -> ModuleType:
    return parsed_data.parser_level_result_mapping[stage]

def get_parsed_data_module_for_team_stage(team: Team, stage: Stage) -> ModuleType:
    return get_parsed_data_module_for_stage(stage).parser_team_result_mapping[team]  # pyright: ignore[reportAny]



def get_all_triple_springs() -> dict[Team, dict[Stage, list[TripleSpringData]]]:
    _result: dict[Team, dict[Stage, list[TripleSpringData]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for triple_spring in get_parsed_data_module_for_team_stage(team=team, stage=stage).triple_springs:  # pyright: ignore[reportAny]
                    _result[team][stage].append(triple_spring)  # pyright: ignore[reportAny]
            except:
                pass
    return _result



def get_all_rings() -> dict[Team, dict[Stage, list[RingData]]]:
    _result: dict[Team, dict[Stage, list[RingData]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for ring in get_parsed_data_module_for_team_stage(team=team, stage=stage).rings:  # pyright: ignore[reportAny]
                    _result[team][stage].append(ring)  # pyright: ignore[reportAny]
            except:
                pass
    return _result



def get_all_hint_rings() -> dict[Team, dict[Stage, list[HintRingData]]]:
    _result: dict[Team, dict[Stage, list[HintRingData]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for hint_ring in get_parsed_data_module_for_team_stage(team=team, stage=stage).hint_rings:  # pyright: ignore[reportAny]
                    _result[team][stage].append(hint_ring)  # pyright: ignore[reportAny]
            except:
                pass
    return _result



def get_all_item_boxes() -> dict[Team, dict[Stage, list[ItemBoxData]]]:
    _result: dict[Team, dict[Stage, list[ItemBoxData]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for item_box in get_parsed_data_module_for_team_stage(team=team, stage=stage).item_boxes:  # pyright: ignore[reportAny]
                    _result[team][stage].append(item_box)  # pyright: ignore[reportAny]
            except:
                pass
    return _result


def get_all_item_balloons() -> dict[Team, dict[Stage, list[ItemBalloonData]]]:
    _result: dict[Team, dict[Stage, list[ItemBalloonData]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for item_balloon in get_parsed_data_module_for_team_stage(team=team, stage=stage).item_balloons:  # pyright: ignore[reportAny]
                    _result[team][stage].append(item_balloon)  # pyright: ignore[reportAny]
            except:
                pass
    return _result


def get_all_egg_flappers() -> dict[Team, dict[Stage, list[EggFlapper]]]:
    _result: dict[Team, dict[Stage, list[EggFlapper]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for egg_flapper in get_parsed_data_module_for_team_stage(team=team, stage=stage).egg_flappers:  # pyright: ignore[reportAny]
                    _result[team][stage].append(egg_flapper)  # pyright: ignore[reportAny]
            except:
                pass
    return _result




def get_all_egg_pawns() -> dict[Team, dict[Stage, list[EggPawn]]]:
    _result: dict[Team, dict[Stage, list[EggPawn]]] = {}
    for team in Team:
        _result[team] = {}
        for stage in Stage:
            _result[team][stage] = []
            try:
                for egg_pawn in get_parsed_data_module_for_team_stage(team=team, stage=stage).egg_pawns:  # pyright: ignore[reportAny]
                    _result[team][stage].append(egg_pawn)  # pyright: ignore[reportAny]
            except:
                pass
    return _result






def get_csv_file_name(team: Team, stage: Stage, file_type: str, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}{file_type}"



def get_parsed_entry_str(entry_class_name: str, params: dict[str, str]) -> str:
    _result: str = f"{entry_class_name}("

    for key, value in params.items():
        _result += f"{key}={value}, "
    if _result[-2:] == ", ":
        _result = _result[:-2]

    _result += ")"
    return _result


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
    # I really hate this but it's needed
    import regex

    AND_CONDITION_PATTERN: regex.Pattern[str] = regex.compile(pattern=r"(AND)")
    OR_CONDITION_PATTERN: regex.Pattern[str] = regex.compile(pattern=r"(OR)")
    OUTER_PARENS_PATTERN: regex.Pattern[str] = regex.compile(pattern=r"\((?>[^()]|(?R))*\)")



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






