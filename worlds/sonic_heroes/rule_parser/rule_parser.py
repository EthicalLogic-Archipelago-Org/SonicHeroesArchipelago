"""
Regex Rule Parsing
"""

from worlds.sonic_heroes.constants.char_ability import Team
from worlds.sonic_heroes.constants.stage import Stage

from worlds.sonic_heroes.location_generation import FULL_LOCATION_DICT, print_full_dict
from worlds.sonic_heroes.rule_parser.functions_connections import parse_connection_csv
from worlds.sonic_heroes.rule_parser.functions_enemies import parse_enemy_csv
from worlds.sonic_heroes.rule_parser.functions_hint_ring import parse_hint_ring_csv
from worlds.sonic_heroes.rule_parser.functions_item_balloon_box import parse_item_box_balloon_csv
from worlds.sonic_heroes.rule_parser.functions_regions import parse_region_csv
from worlds.sonic_heroes.rule_parser.functions_rings import parse_ring_csv

from worlds.sonic_heroes.item_generation import FULL_ITEM_LIST, generate_item_list
from worlds.sonic_heroes.parsed_data import *


def parse_team_stage(team: Team, stage: Stage) -> None:
    # parse_region_csv(team=team, stage=stage)
    # parse_connection_csv(team=team, stage=stage)
    # parse_hint_ring_csv(team=team, stage=stage)
    # parse_item_box_balloon_csv(team=team, stage=stage)
    # parse_ring_csv(team=team, stage=stage)
    # parse_enemy_csv(team=team, stage=stage)


    # do generation logic (AP)
    # review design after
    pass


# parse_team_stage(team=Team.DARK, stage=Stage.SEASIDE_HILL)

# print(f"{parser_connection_mapping[Stage.SEASIDE_HILL][Team.DARK][2]}")
# print(f"{parser_enemy_mapping[Stage.SEASIDE_HILL][Team.DARK][2]}")
# print(f"{parser_hint_ring_mapping[Stage.SEASIDE_HILL][Team.DARK][2]}")
# print(f"{parser_item_balloon_box_mapping[Stage.SEASIDE_HILL][Team.DARK][2]}")
# print(f"{parser_region_mapping[Stage.SEASIDE_HILL][Team.DARK][2]}")


# print_full_dict()
print(FULL_ITEM_LIST)