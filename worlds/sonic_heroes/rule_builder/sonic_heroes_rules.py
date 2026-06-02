"""
Many Many rules
"""
# import dataclasses
#
# from rule_builder.rules import Rule
#
# from ..constants.char_ability import Ability, Formation, Team
# from ..constants.stage import Stage
# from ..constants.stage_objs import StageObj
# from .functions_ability_char import can_team_blast_rule, can_ability_rule, has_formation_char_rule
# from .functions_stage_obj import has_stage_obj_rule
# from ..world_base import SonicHeroesWorldBase
#
#
# @dataclasses.dataclass(init=False)
# class SonicHeroesRules:
#     has_formation_char_rules: dict[Team, dict[Formation, Rule[SonicHeroesWorldBase]]]
#     """Does the team have a character of the formation?"""
#     has_stage_obj_rules: dict[StageObj, Rule[SonicHeroesWorldBase]]
#     """Do you have the stage obj?"""
#     can_team_blast_rules: dict[Team, dict[Stage, Rule[SonicHeroesWorldBase]]]
#     """Can you team blast with the team and stage"""
#     ability_rules: dict[Ability, dict[Team, dict[Stage, dict[int, dict[int, Rule[SonicHeroesWorldBase]]]]]]
#     """Ability to Team to Level to Other Chars mapping of rules"""
#
#
#     def __init__(self) -> None:
#         self.has_formation_char_rules = {team: {} for team in Team}
#         self.has_stage_obj_rules = {}
#         self.can_team_blast_rules = {team: {} for team in Team}
#         self.ability_rules = {ability: {team: {} for team in Team} for ability in Ability}
#
#
#     def get_formation_character_rule(self, team: Team, formation: Formation) -> Rule[SonicHeroesWorldBase]:
#         rule: Rule[SonicHeroesWorldBase] | None = self.has_formation_char_rules[team].get(formation)
#         if rule is not None:
#             return rule
#         created_rule: Rule[SonicHeroesWorldBase] = has_formation_char_rule(team=team, formation=formation)
#         self.has_formation_char_rules[team][formation] = created_rule
#         return created_rule
#
#
#     def get_stage_obj_rule(self, stage_obj: StageObj) -> Rule[SonicHeroesWorldBase]:
#         rule: Rule[SonicHeroesWorldBase] | None = self.has_stage_obj_rules.get(stage_obj)
#         if rule is not None:
#             return rule
#         created_rule: Rule[SonicHeroesWorldBase] = has_stage_obj_rule(stage_obj=stage_obj)
#         self.has_stage_obj_rules[stage_obj] = created_rule
#         return created_rule
#
#
#     def get_team_blast_rule(self, team: Team, stage: Stage) -> Rule[SonicHeroesWorldBase]:
#         rule: Rule[SonicHeroesWorldBase] | None = self.can_team_blast_rules[team].get(stage)
#         if rule is not None:
#             return rule
#         created_rule: Rule[SonicHeroesWorldBase] = can_team_blast_rule(team=team, stage=stage)
#         self.can_team_blast_rules[team][stage] = created_rule
#         return created_rule
#
#
#     def get_ability_rule(self, team: Team, stage: Stage, ability: Ability, level: int = 0, other_chars: int = 0) -> Rule[SonicHeroesWorldBase]:
#         if stage not in self.ability_rules[ability][team].keys():
#             self.ability_rules[ability][team][stage] = {}
#         if level not in self.ability_rules[ability][team][stage].keys():
#             self.ability_rules[ability][team][stage][level] = {}
#         if other_chars not in self.ability_rules[ability][team][stage][level].keys():
#             created_rule: Rule[SonicHeroesWorldBase] = can_ability_rule(team=team, stage=stage, ability=ability, level=level, other_chars=other_chars)
#             self.ability_rules[ability][team][stage][level][other_chars] = created_rule
#             return created_rule
#         return self.ability_rules[ability][team][stage][level][other_chars]
#
#
# RULES: SonicHeroesRules = SonicHeroesRules()

