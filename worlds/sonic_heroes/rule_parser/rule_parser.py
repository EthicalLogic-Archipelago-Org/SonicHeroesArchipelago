"""
Regex Rule Parsing
"""

from worlds.sonic_heroes.constants.char_ability import Team
from worlds.sonic_heroes.constants.stage import Stage, StageType
from worlds.sonic_heroes.constants.stage_objs import StageObj

from worlds.sonic_heroes.rule_parser.functions_connections import parse_connection_csv
from worlds.sonic_heroes.rule_parser.functions_mappings import export_all_mappings
from worlds.sonic_heroes.rule_parser.functions_regions import parse_region_csv
from worlds.sonic_heroes.rule_parser.functions_stage_objs import parse_stage_objs_csv

from worlds.sonic_heroes.rule_parser.functions_parser import handle_full_rule_string

from worlds.sonic_heroes.parsed_data import *



TEAM_STAGES_TO_PARSE: dict[Team, list[Stage]] = \
{
    Team.ANY_TEAM: [],
    Team.SONIC: [],
    Team.DARK: [Stage.SEASIDE_HILL],
    Team.ROSE: [],
    Team.CHAOTIX: [],# [Stage.SEASIDE_HILL],
    Team.SUPER_HARD_MODE: [],
}




def parse_stage_obj_csv(team: Team, stage: Stage) -> None:
    # check if secret here
    parse_stage_objs_csv(team=team, stage=stage, secret=False)


def parse_team_stage(team: Team, stage: Stage, parsed_team_stages: dict[Team, list[Stage]]) -> None:
    if stage not in TEAM_STAGES_TO_PARSE[team]:
        return
    if team not in parsed_team_stages.keys():
        parsed_team_stages[team] = []
    if stage not in parsed_team_stages[team]:
        parsed_team_stages[team].append(stage)

    parse_region_csv(team=team, stage=stage)
    parse_connection_csv(team=team, stage=stage)
    parse_stage_obj_csv(team=team, stage=stage)
    pass

def parse_team(team: Team, parsed_team_stages: dict[Team, list[Stage]]) -> None:
    for stage in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
        parse_team_stage(team=team, stage=stage, parsed_team_stages=parsed_team_stages)

def parse_stage(stage: Stage, parsed_team_stages: dict[Team, list[Stage]]) -> None:
    for team in Team:
        parse_team_stage(team=team, stage=stage, parsed_team_stages=parsed_team_stages)


def parse() -> None:
    parsed_team_stages: dict[Team, list[Stage]] = {}
    for team in Team:
        parse_team(team=team, parsed_team_stages=parsed_team_stages)

    # export_all_mappings(parsed_team_stages)
    pass


def parse_specific_rule() -> None:
    test_str: str = handle_full_rule_string(rule_str="RuinsNoTriggerAND((TripleSpring)OR(JumpANDFlyAny)OR(JumpANDBellyFlop0)", team=Team.CHAOTIX, stage=Stage.SEASIDE_HILL, line_number=0, print_steps=True)
    pass



parse()
# parse_specific_rule()


# for stage_obj in StageObj:
#     print(stage_obj.value)


