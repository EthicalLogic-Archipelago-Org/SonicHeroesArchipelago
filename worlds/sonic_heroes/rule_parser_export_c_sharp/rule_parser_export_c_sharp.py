"""
Functions used by the parser related to exporting parsed data to C#
"""
import os
from typing import Callable

from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_functions import *
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_egg_flappers import get_egg_flappers_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_egg_pawns import get_egg_pawns_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_hint_rings import get_hint_rings_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_item_balloons import get_item_balloons_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_item_boxes import get_item_boxes_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_rings import get_rings_export_string_for_team
from worlds.sonic_heroes.rule_parser_export_c_sharp.rule_parser_export_triple_springs import get_triple_springs_export_string_for_team





def export_stage_obj(namespace_name: str, record_class: str, record_parent_class: str, stage_obj_type: str, custom_record_vars: list[str], stage_obj_export_team_function: Callable[[str, str, Team], str]) -> None:
    # _str_to_write: str = get_triple_springs_export_string(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars)

    _result: str = ""
    _result += get_file_header(namespace_class_name=namespace_name)
    _result += get_parsed_export_record_class_definition(record_class_name=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars)

    for team in Team:
        if team is Team.ANY_TEAM:
            continue
        _result += stage_obj_export_team_function(namespace_name, record_class, team)


    _result += get_all_lists_concatenated(file_class_name=namespace_name, record_class_name=record_class)
    _result += get_file_footer()

    file_path: str = f"../../../../../Sonic-Heroes-AP-Client/Sonic Heroes AP Client/src/Sanity/{namespace_name}/{namespace_name}Data.cs"

    # with Path(file_path).open(mode="a", encoding="utf-8") as output_file:
    with open(file=os.path.relpath(path=file_path, start=os.getcwd()), mode="w") as output_file:
        # print(f"Writing File here: {output_file}")
        _ = output_file.write(_result)
    # print(_str_to_write)



def export_triple_springs() -> None:
    namespace_name: str = "TripleSprings"
    record_class: str = "TripleSpringData"
    record_parent_class: str = "StageObjDataBase"
    stage_obj_type: str = "TripleSpring"
    custom_record_vars: list[str] = \
    [
        "float Power",
        "int NoControlTime",
        "ItemReward ItemReward",
        "float Scale",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_triple_springs_export_string_for_team)


def export_rings() -> None:
    namespace_name: str = "Rings"
    record_class: str = "RingData"
    record_parent_class: str = "StageObjDataBase"
    stage_obj_type: str = "Rings"
    custom_record_vars: list[str] = \
    [
        "int NumRings",
        "RingType RingType",
        "float Length",
        "float Radius",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_rings_export_string_for_team)


def export_hint_rings() -> None:
    namespace_name: str = "HintRings"
    record_class: str = "HintRingData"
    record_parent_class: str = "StageObjDataBase"
    stage_obj_type: str = "HintRing"
    custom_record_vars: list[str] = \
    [
        "ushort VoiceLineID",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_hint_rings_export_string_for_team)


def export_item_boxes() -> None:
    namespace_name: str = "ItemBoxes"
    record_class: str = "ItemBoxData"
    record_parent_class: str = "StageObjDataBase"
    stage_obj_type: str = "ItemBox"
    custom_record_vars: list[str] = \
    [
        "ItemReward ItemReward",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_item_boxes_export_string_for_team)


def export_item_balloons() -> None:
    namespace_name: str = "ItemBalloons"
    record_class: str = "ItemBalloonData"
    record_parent_class: str = "StageObjDataBase"
    stage_obj_type: str = "ItemBalloon"
    custom_record_vars: list[str] = \
    [
        "ItemReward ItemReward",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_item_balloons_export_string_for_team)


def export_egg_flappers() -> None:
    namespace_name: str = "EggFlappers"
    record_class: str = "EggFlapperData"
    record_parent_class: str = "EnemyData.BaseEnemyData"
    stage_obj_type: str = "EggFlapper"
    custom_record_vars: list[str] = \
    [
        "EggFlapperWeapon Weapon",
        "EggFlapperArmor Armor",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_egg_flappers_export_string_for_team)



def export_egg_pawns() -> None:
    namespace_name: str = "EggPawns"
    record_class: str = "EggPawnData"
    record_parent_class: str = "EnemyData.BaseEnemyData"
    stage_obj_type: str = "EggPawn"
    custom_record_vars: list[str] = \
    [
        "EggPawnWeapon Weapon",
        "EggPawnShield Shield",
        "EggPawnType SpecialType",
    ]
    print(f"Exporting {namespace_name}")
    export_stage_obj(namespace_name=namespace_name, record_class=record_class, record_parent_class=record_parent_class, stage_obj_type=stage_obj_type, custom_record_vars=custom_record_vars, stage_obj_export_team_function=get_egg_pawns_export_string_for_team)



# export_triple_springs()
# export_rings()
# export_hint_rings()
# export_item_boxes()
# export_item_balloons()
# export_egg_flappers()
export_egg_pawns()








