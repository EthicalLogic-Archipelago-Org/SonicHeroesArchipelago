"""
Functions used by the parser related to Connections
"""
import csv
import os

from .functions_parser import handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.stage import Stage



def get_enemy_csv_file_name(team: Team, stage: Stage, secret: bool = False) -> str:  # pyright: ignore[reportUnusedParameter]
    return f"{stage.stage_name.replace(" ", "")}{team.replace(" ", "")}Enemies"


