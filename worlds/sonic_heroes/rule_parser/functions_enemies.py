"""
Functions used by the parser related to Connections
"""
import csv
import os
from typing import Any

from .functions_parser import get_parsed_entry_str, handle_full_rule_string, get_csv_file_name
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.enemies import EggFlapper, EggFlapperArmor, EggPawnShield, EggPawnType, EggPawnWeapon, EnemyHeight, EnemyType, \
    SonicHeroesEnemyBase, EggPawn, EggFlapperWeapon
from ..constants.stage import Stage



def get_enemy_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:
    return get_csv_file_name(team=team, stage=stage, file_type="Enemies", secret=secret)


def parse_egg_flapper_csv_entry(team: Team, stage: Stage, entry: dict[str, str | Any], secret: bool = False) -> str:  # pyright: ignore[reportExplicitAny]
    class_str: str = "EggFlapper"
    team_str: str = f"{team.__class__.__name__}.{team.name}"
    stage_str: str = f"{stage.__class__.__name__}.{stage.name}"
    region_name: str = f"{stage.stage_name} {team} {entry[REGION_HEADER]}"
    loc_name_str: str = f"{entry[REGION_HEADER]} {entry[NAME_HEADER]}"
    weapon: EggFlapperWeapon = EggFlapperWeapon(value=entry[WEAPON_HEADER])
    weapon_str: str = f"{weapon.__class__.__name__}.{weapon.name}"
    armor: EggFlapperArmor = EggFlapperArmor(value=entry[ARMOR_HEADER])
    armor_str: str = f"{armor.__class__.__name__}.{armor.name}"
    height: EnemyHeight = EnemyHeight.match(input_str=entry[HEIGHT_HEADER])
    height_str: str = f"{height.__class__.__name__}.{height.name}"
    link_id: int = int(entry[LINK_ID_HEADER])
    x_coord: float = float(entry[X_HEADER])
    y_coord: float = float(entry[Y_HEADER])
    z_coord: float = float(entry[Z_HEADER])

    parsed_rule_str: str = ""
    if entry[RULE_HEADER] == "":
        parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
    elif entry[RULE_HEADER] == "NOTPOSSIBLE":
        parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
    else:
        print(f"Rule String here: {entry[RULE_HEADER]}")
        parsed_rule_str = handle_full_rule_string(rule_str=entry[RULE_HEADER], team=team, stage=stage)

    params_dict: dict[str, str] = \
    {
        "team": team_str,
        "stage": stage_str,
        "location_name": f"\"{loc_name_str}\"",
        "region_name": f"\"{region_name}\"",
        "weapon": weapon_str,
        "armor": armor_str,
        "height": height_str,
        "link_id": str(link_id),
        "x": str(x_coord),
        "y": str(y_coord),
        "z": str(z_coord),
        "rule": parsed_rule_str,
    }

    return get_parsed_entry_str(entry_class_name=class_str, params=params_dict)


def parse_egg_pawn_csv_entry(team: Team, stage: Stage, entry: dict[str, str | Any], secret: bool = False) -> str:  # pyright: ignore[reportExplicitAny]
    class_str: str = "EggPawn"
    team_str: str = f"{team.__class__.__name__}.{team.name}"
    stage_str: str = f"{stage.__class__.__name__}.{stage.name}"
    region_name: str = f"{stage.stage_name} {team} {entry[REGION_HEADER]}"
    loc_name_str: str = f"{entry[REGION_HEADER]} {entry[NAME_HEADER]}"
    special_type: EggPawnType = EggPawnType(value=entry[SPECIAL_TYPE_HEADER])
    special_type_str: str = f"{special_type.__class__.__name__}.{special_type.name}"
    weapon: EggPawnWeapon = EggPawnWeapon(value=entry[WEAPON_HEADER])
    weapon_str: str = f"{weapon.__class__.__name__}.{weapon.name}"
    shield: EggPawnShield = EggPawnShield(value=entry[SHIELD_HEADER])
    shield_str: str = f"{shield.__class__.__name__}.{shield.name}"
    height: EnemyHeight = EnemyHeight.match(input_str=entry[HEIGHT_HEADER])
    height_str: str = f"{height.__class__.__name__}.{height.name}"
    link_id: int = int(entry[LINK_ID_HEADER])
    x_coord: float = float(entry[X_HEADER])
    y_coord: float = float(entry[Y_HEADER])
    z_coord: float = float(entry[Z_HEADER])

    parsed_rule_str: str = ""
    if entry[RULE_HEADER] == "":
        parsed_rule_str = f"True_[SonicHeroesWorldBase]()"
    elif entry[RULE_HEADER] == "NOTPOSSIBLE":
        parsed_rule_str = f"False_[SonicHeroesWorldBase]()"
    else:
        print(f"Rule String here: {entry[RULE_HEADER]}")
        parsed_rule_str = handle_full_rule_string(rule_str=entry[RULE_HEADER], team=team, stage=stage)

    params_dict: dict[str, str] = \
    {
        "team": team_str,
        "stage": stage_str,
        "location_name": f"\"{loc_name_str}\"",
        "region_name": f"\"{region_name}\"",
        "special_type": special_type_str,
        "weapon": weapon_str,
        "shield": shield_str,
        "height": height_str,
        "link_id": str(link_id),
        "x": str(x_coord),
        "y": str(y_coord),
        "z": str(z_coord),
        "rule": parsed_rule_str,
    }

    return get_parsed_entry_str(entry_class_name=class_str, params=params_dict)


def parse_enemy_csv(team: Team, stage: Stage, secret: bool = False) -> None:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
    file_name: str = get_enemy_csv_file_name(team=team, stage=stage, secret=secret)
    print(f"File Name here: {file_name}")

    with files(csv_data.csv_data_mapping[stage][team]).joinpath(f"{file_name}.csv").open() as csv_file:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        reader: csv.DictReader[str] = csv.DictReader(csv_file)  # pyright: ignore[reportUnknownArgumentType]
        enemy_str_list: list[str] = []

        for x in reader:

            if x[TYPE_HEADER] == EnemyType.EGG_FLAPPER.value:
                enemy_str_list.append(parse_egg_flapper_csv_entry(team=team, stage=stage, entry=x, secret=secret))
                pass
            elif x[TYPE_HEADER] == EnemyType.EGG_PAWN.value:
                enemy_str_list.append(parse_egg_pawn_csv_entry(team=team, stage=stage, entry=x, secret=secret))
                pass
            else:
                raise ValueError(f"{x[TYPE_HEADER]} not mapped in parse_enemy_csv")

    list_name: str = "ENEMIES"
    # list_name: str = f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Enemies"

    parsed_result: str = f"\n{ENEMY_PARSER_FILE_HEADER}\n{list_name}: list[SonicHeroesEnemyBase] = \\\n[\n    {',\n    '.join(enemy_str_list)}\n]"

    # noinspection PyTypeChecker
    with open(file=f"{os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py", mode="w") as output_file:  # pyright: ignore[reportCallIssue, reportArgumentType]
        # noinspection PyTypeChecker
        print(f"Writing File here: {os.path.dirname(parsed_data.parser_result_mapping[stage][team].__file__)}/{file_name}.py")  # pyright: ignore[reportCallIssue, reportArgumentType]
        _ = output_file.write(parsed_result)


