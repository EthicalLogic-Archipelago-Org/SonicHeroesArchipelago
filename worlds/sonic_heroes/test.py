from __future__ import annotations

from BaseClasses import CollectionState
from typing import TYPE_CHECKING

from worlds.sonic_heroes.constants import *

if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from dataclasses import dataclass

import regex  # type: ignore




@dataclass
class SonicHeroesRegexRuleResult:
    rule_result_str: str
    required_params: list[str]

world_param: str = "world"
team_param: str = "team"
level_param: str = "level"
state_param: str = "state"

regular_param: str = "regular"
push_push_param: str = "push_pull"


team_strs: list[str] = ["Sonic", "Dark", "Rose", "Chaotix", "SuperHardMode"]
level_strs: list[str] = ["SH", "OP", "GM", "PP", "CP", "BH", "RC", "BS", "Frog", "LJ", "HC", "MM", "EF", "Final"]

team_level_strs: list[str] = [f"{team}{level}" for team in team_strs for level in level_strs]

rules = \
[
    "FlyingFullorRuinsSonicSH",
    "FlyingOneCharorTripleSpringSonicSH",
    "FlyingFullor(RuinsandSingleSpringandSmallStonePlatform)SonicSH",
    "DashRampSonicSH",
    "DashPanelorSpeedSonicSH",
    "SingleSpringSonicSH",
    "(BreakandSingleSpring)orFlyingAnySonicSH",
    "FlyingAnySonicSH",
    "FlyingAnyandSmallStonePlatformSonicSH",
    "(BreakandTripleSpring)orFlyingAnySonicSH",
    "FlyingAnyorTripleSpringSonicSH",
    "BreakorFlyingAnyorHomingSonicSH",
    "BreakorFlyingAnySonicSH",
    "(CannonAnyorFlyingFull)andRuinsSonicSH",
    "FlyingFullandRuinsSonicSH",
    "CannonFlyingSonicSH",
    "CannonPowerSonicSH",
    "DashRingorFlyingAnySonicSH",
    "DashRampandDashRingandFlyingAnySonicSH",
    "RuinsSonicSH",
    "FlyingAnyandRuinsSonicSH",
    "FlyingFullSonicSH",
    "DashPanelor(DashRingandFlyingAny)orSpeedSonicSH",
    "((BreakorHoming)andSingleSpring)orFlyingAnySonicSH",
    "TripleSpringSonicSH",
    "DashRingandFlyingAnyandSingleSpringSonicSH",
    "Breakand(DashRingorFlyingAny)andSingleSpringSonicSH",
    "DashRingandFlyingAnySonicSH",
    "CannonSpeedSonicSH",
    "GlideandRuinsandTripleSpringSonicSH",
]

rule_mapping_dict_here: dict[str, SonicHeroesRegexRuleResult] = \
{
    "FloatingDice": SonicHeroesRegexRuleResult("can_floating_dice({})", [team_param, level_param]),
    "FlyingAny": SonicHeroesRegexRuleResult("can_fly({})", [team_param, level_param]),
    "PushPullSwitch": SonicHeroesRegexRuleResult("can_switch({}, push_pull = True)", [team_param, level_param]),
    "Switch": SonicHeroesRegexRuleResult("please_change_switch({}, regular = True)", [team_param, level_param]),
    "Weight":  SonicHeroesRegexRuleResult("please_change_weight({}, regular = True)", [team_param, level_param]),
}

test_rule = "TestRuleor((BreakorHoming)andSingleSpring)orFlyingAnySonicSH"

test_rule2 = "((FloatingDiceandSwitch)orWeight)andFlyingAnyandPushPullSwitchSonicBH"

test_rule3 = "((FloatingDiceandSwitch)orWeight)and(FlyingAnyandPushPullSwitch)SonicBH"


and_condition_pattern = regex.compile(r"(and)", regex.IGNORECASE)
or_condition_pattern = regex.compile(r"(?<!T)(or)", regex.IGNORECASE)
outer_parentheses_pattern = regex.compile(r"\((?>[^()]|(?R))*\)", regex.IGNORECASE)

#match - only look at start of str (bad)
#search - only find first match
#findall - match all but only return str
#finditer - match all return list of match obj
#split - split
#sub


#match object has:
#start - start index (inclusive)
#end - end index (exclusive)
#group - string match (0 is entire, 1 is first grouping match ())

outer_match = outer_parentheses_pattern.finditer(test_rule)

for match in outer_match:
    print(match)

print(outer_parentheses_pattern.split(test_rule))

print(or_condition_pattern.split(outer_parentheses_pattern.split(test_rule)[1]))


result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []


def is_there_team_level_str(rule: str) -> str | None:
    for team_lvl in team_level_strs:
        if team_lvl in rule:
            return team_lvl
    return None

def is_there_parens(rule: str) -> bool:
    if '(' in rule and ')' in rule:
        return True
    return False

def is_there_and(rule: str) -> bool:
    if 'and' in rule.lower():
        return True
    return False

def is_there_or(rule: str) -> bool:
    if 'or' in rule.lower():
        return True
    return False


def handle_rule(rule: str):
    if rule == '':
        return

    print(f"Rule: {rule}")

    if rule.lower() == 'or':
        result_str_list.append('OR')
        return

    if rule.lower() == 'and':
        result_str_list.append('AND')
        return

    ## This is a problem
    if rule[0] == '(' and rule[-1] == ')':
        handle_rule(rule[1:-1])
        return


    if is_there_parens(rule):
        temp_var = outer_parentheses_pattern.split(rule)
        print(f"temp_var={temp_var}")
        handle_rule(temp_var[0])

        temp_scanner = outer_parentheses_pattern.finditer(rule)

        for index, scan_match in enumerate(temp_scanner):
            temp_index = len(result_str_list)
            result_str_list.append('(')
            temp_tuple = (temp_index, temp_index)
            handle_rule(scan_match.group())
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

            handle_rule(temp_var[index + 1])


        """
        for scan_match in temp_scanner:
            temp_index = len(result_str_list)
            result_str_list.append('(')
            temp_tuple = (temp_index, temp_index)
            handle_rule(scan_match.group())
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

        handle_rule(temp_var[1])
        """
        return

    if is_there_and(rule):
        temp_var = and_condition_pattern.split(rule)
        #print(f"Temp AND Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split)
            #if index < len(temp_var) - 1:
                #result_str_list.append('AND')
        return

    if is_there_or(rule):
        temp_var = or_condition_pattern.split(rule)
        #print(f"Temp OR Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split)
        return

    team_lvl = is_there_team_level_str(rule)

    if team_lvl is not None:
        handle_rule(rule.replace(team_lvl, ""))
        result_str_list.append(team_lvl)
        return

    result_str_list.append(rule)


print(f"\n\nRule: {test_rule}")
handle_rule(test_rule)

print(result_str_list)
print(parens_mapping_list)



result_str_list = []
parens_mapping_list = []

print(f"\n\nRule: {test_rule2}")
handle_rule(test_rule2)

print(result_str_list)
print(parens_mapping_list)


result_str_list = []
parens_mapping_list = []

print(f"\n\nRule: {test_rule3}")
handle_rule(test_rule3)

print(result_str_list)
print(parens_mapping_list)




def check_for_kwarg(key: str, **kwargs) -> bool:
    if key in kwargs.keys():
        return True
    print(f"{key} not in **kwargs")
    return False


def get_rule_func_str(rule, **kwargs) -> str:

    if not check_for_kwarg(TEAM, **kwargs):
        return ""

    if not check_for_kwarg(LEVEL, **kwargs):
        return ""

    return ""





test_rule_str = f"lambda state: "