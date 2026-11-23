"""
Functions used by the parser related to Triple Springs (for exporting to C#)
"""
from .rule_parser_export_functions import get_file_footer, get_file_header, get_parsed_export_entry_str, \
    get_parsed_export_record_class_definition, get_parsed_export_entry_list_str, get_all_lists_concatenated
from ..rule_parser.functions_parser import *
from ..constants.char_ability import Team
from ..constants.stage import Stage, StageType
from ..constants.triple_spring import *



def get_triple_springs_export_string_for_team(namespace_name: str, record_class: str, team: Team) -> str:
    team_entries: list[dict[str, str]] = []
    team_parsed_data: dict[Stage, list[TripleSpringData]] = get_all_triple_springs()[team]

    for stage, parsed_list in team_parsed_data.items():
        for parsed_entry in parsed_list:
            params_dict: dict[str, str] = \
            {
                "Team": f"Team.{parsed_entry.team.value}",
                "LevelId": f"LevelId.{parsed_entry.stage.stage_name.replace(" ", "")}",
                "Region": f"\"{parsed_entry.region_name.replace(f"{parsed_entry.stage.stage_name} {parsed_entry.team.value} ", "")}\"",
                "LocName": f"\"{parsed_entry.location_name}\"",
                "Power": f"{parsed_entry.power}f",
                "NoControlTime": f"{parsed_entry.no_control_time}",
                "ItemReward": f"ItemReward.{parsed_entry.item.name}",
                "Scale": f"{parsed_entry.scale}f",
                "Group": f"{parsed_entry.group}",
                "IdOffsetGroup": f"{parsed_entry.id_offset_group}",
                "IdOffsetFull": f"{parsed_entry.id_offset_full}",
                "LinkID": f"{parsed_entry.link_id}",
                "SpawnCoords": f"new Vector3(x: {parsed_entry.x}f, y: {parsed_entry.y}f, z: {parsed_entry.z}f)",
            }
            team_entries.append(params_dict)
    return get_parsed_export_entry_list_str(file_class_name=namespace_name, record_class_name=record_class, team=team.value, parsed_entries_params=team_entries)


