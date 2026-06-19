"""
Functions used by the parser for exporting to C#
"""
import csv
import os


from .functions_hint_ring import get_hint_ring_csv_file_name
from .functions_parser import get_csv_file_name, get_parsed_entry_str, handle_full_rule_string
from .parser_constants import *
from .. import csv_data
from .. import parsed_data
from ..constants.char_ability import Team
from ..constants.hint_rings import HINT_RING, HintRingData
from ..constants.rings import RingData
from ..constants.stage import Stage, StageType



def get_parsed_export_entry_str(entry_class_name: str, params: dict[str, str]) -> str:
    _result: str = f"new {entry_class_name}("

    for key, value in params.items():
        _result += f"{key}: {value}, "
    if _result[-2:] == ", ":
        _result = _result[:-2]

    _result += ")"
    return _result