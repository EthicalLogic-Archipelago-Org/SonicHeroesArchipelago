"""
Regex Rule Parsing
"""
from __future__ import annotations

import enum

import regex

from ..constants.char_ability import Ability, Formation, Team
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj

AND_CONDITION_PATTERN: regex.Pattern[str] = regex.compile(r"(AND)")
OR_CONDITION_PATTERN: regex.Pattern[str] = regex.compile(r"(OR)")
OUTER_PARENS_PATTERN: regex.Pattern[str] = regex.compile(r"\((?>[^()]|(?R))*\)")


TEAM_REF_STR: str = "Team"
FORMATION_REF_STR: str = "Formation"
HAS_FORM_CHAR_FOR_TEAM_DICT_NAME: str = "HAS_FORMATION_CHAR_RULES"

ABILITY_REF_STR: str = "Ability"
ABILITY_DICT_NAME: str = "CHAR_ABILITY_RULES"

STAGE_OBJ_REF_STR: str = "StageObj"
STAGE_OBJ_RULE_DICT_NAME: str = "STAGE_OBJ_RULES"







