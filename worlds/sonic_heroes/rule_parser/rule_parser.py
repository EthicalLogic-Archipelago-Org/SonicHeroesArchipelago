"""
Regex Rule Parsing
"""
import csv
import os.path

from worlds.sonic_heroes.constants.char_ability import Team
from worlds.sonic_heroes.constants.stage import Stage

from worlds.sonic_heroes.rule_parser.functions_connections import parse_connection_csv
from worlds.sonic_heroes.rule_parser.functions_hint_ring import parse_hint_ring_csv
from worlds.sonic_heroes.rule_parser.functions_item_balloon_box import parse_item_box_balloon_csv
from worlds.sonic_heroes.rule_parser.functions_regions import parse_region_csv


def parse_team_stage(team: Team, stage: Stage) -> None:
    parse_region_csv(team=team, stage=stage)
    parse_connection_csv(team=team, stage=stage)
    parse_hint_ring_csv(team=team, stage=stage)
    parse_item_box_balloon_csv(team=team, stage=stage)


parse_team_stage(team=Team.DARK, stage=Stage.SEASIDE_HILL)





