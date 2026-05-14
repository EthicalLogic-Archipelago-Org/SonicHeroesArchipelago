"""
Constants used by the parser
"""
import dataclasses
import enum
from typing import Protocol

from rule_builder.rules import Rule

from ..constants.char_ability import Team
from ..constants.stage import Stage
from ..constants.stage_objs import StageObj
from ..rule_builder.sonic_heroes_rules import RULES
from ..world_base import SonicHeroesWorldBase


RULES_NAME: str = "RULES"
GET_FORMATION_CHAR_RULE: str = f"{RULES_NAME}.get_formation_character_rule"
GET_STAGE_OBJ_RULE: str = f"{RULES_NAME}.get_stage_obj_rule"
GET_TEAM_BLAST_RULE: str = f"{RULES_NAME}.get_team_blast_rule"
GET_ABILITY_RULE: str = f"{RULES_NAME}.get_ability_rule"


TEAM_REF: str = "Team"


STAGE_REF: str = "Stage"


FORMATION_REF: str = "Formation"




# only pass in team and stage and manually handle each match



