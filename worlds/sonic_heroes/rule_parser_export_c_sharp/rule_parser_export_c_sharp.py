"""
Functions used by the parser related to exporting parsed data to C#
"""

from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_egg_flappers import get_egg_flappers_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_egg_pawns import get_egg_pawns_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_hint_rings import get_hint_rings_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_item_balloons import get_item_balloons_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_item_boxes import get_item_boxes_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_rings import get_rings_export_string
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_triple_springs import get_triple_springs_export_string




# def export_enemies() -> None:
#     print(get_enemy_export_string())




def export_triple_springs() -> None:
    print(get_triple_springs_export_string())

def export_rings() -> None:
    print(get_rings_export_string())

def export_hint_rings() -> None:
    print(get_hint_rings_export_string())

def export_item_boxes() -> None:
    print(get_item_boxes_export_string())

def export_item_balloons() -> None:
    print(get_item_balloons_export_string())

def export_egg_flappers() -> None:
    print(get_egg_flappers_export_string())

def export_egg_pawns() -> None:
    print(get_egg_pawns_export_string())




# export_triple_springs()
# export_rings()
# export_hint_rings()
# export_item_boxes()
# export_item_balloons()
# export_egg_flappers()
export_egg_pawns()








