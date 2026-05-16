"""
Valid Matches for the parser
"""
from typing import Callable

from ..constants.char_ability import Team
from ..constants.enemies import *
from ..constants.stage import Stage
from .matches_ability_char import PARSER_ABILITY_MAPPING, PARSER_FORMATION_CHARACTER_MAPPING
from .matches_enemies import PARSER_ENEMY_MAPPING
from .matches_stage_obj import PARSER_STAGE_OBJ_MAPPING
from .matches_tricks import PARSER_TRICK_MAPPING



PARSER_ALL_MATCHES: dict[str, Callable[[Team, Stage], str]] = \
{
    **PARSER_FORMATION_CHARACTER_MAPPING,
    **PARSER_ABILITY_MAPPING,
    **PARSER_ENEMY_MAPPING,
    **PARSER_STAGE_OBJ_MAPPING,
    **PARSER_TRICK_MAPPING,
}