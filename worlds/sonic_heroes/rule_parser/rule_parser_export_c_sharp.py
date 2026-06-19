"""
Functions used by the parser related to exporting parsed data to C#
"""

from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_enemies import get_enemy_export_string
from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_hint_rings import get_hint_ring_export_string
from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_item_balloon_boxes import get_item_balloon_boxes_export_string
from worlds.sonic_heroes.rule_parser.rule_parser_c_sharp_rings import get_ring_export_string


def export_hint_rings() -> None:
    print(get_hint_ring_export_string())

def export_item_balloon_boxes_rings() -> None:
    print(get_item_balloon_boxes_export_string())

def export_enemies() -> None:
    print(get_enemy_export_string())

def export_rings() -> None:
    print(get_ring_export_string())



# export_hint_rings()
# export_item_balloon_boxes_rings()
export_enemies()
# export_rings()














