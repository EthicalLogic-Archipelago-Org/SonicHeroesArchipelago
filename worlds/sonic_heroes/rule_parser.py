
import regex
from dataclasses import dataclass, field


from worlds.sonic_heroes.constants import *


@dataclass
class SonicHeroesRuleFunctionMapping:
    function_name: str
    #team: str
    #level: str
    # noinspection PyDataclass
    extra_params: dict[str, bool | int | str] = field(default_factory=dict)

    def get_func_call_str(self, team: str, level: str) -> str:
        extra_param_str = ""
        for param, value in self.extra_params.items():
            extra_param_str += f", {param} = {value}"
        return f"{self.function_name}(world, {team.upper().replace(" ", "")}, {level.upper().replace(" ", "")}, state{extra_param_str})"

level_str_to_level: dict[str, str] = \
{
    "SH": SEASIDEHILL,
    "OP": OCEANPALACE,
    "GM": GRANDMETROPOLIS,
    "PP": POWERPLANT,
    "CP": CASINOPARK,
    "BH": BINGOHIGHWAY,
    "RC": RAILCANYON,
    "BS": BULLETSTATION,
    "Frog": FROGFOREST,
    "LJ": LOSTJUNGLE,
    "HC": HANGCASTLE,
    "MM": MYSTICMANSION,
    "EF": EGGFLEET,
    "Final": FINALFORTRESS,
}

team_strs: list[str] = ["Sonic", "Dark", "Rose", "Chaotix", "SuperHardMode"]
#level_strs: list[str] = ["SH", "OP", "GM", "PP", "CP", "BH", "RC", "BS", "Frog", "LJ", "HC", "MM", "EF", "Final"]

individual_rule_team: str | None = None
individual_rule_level: str | None = None

result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []

team_level_strs: list[str] = [f"{team}{level}" for team in team_strs for level in level_str_to_level.keys()]

and_condition_pattern = regex.compile(r"(and)", regex.IGNORECASE)
or_condition_pattern = regex.compile(r"(?<!T)(or)", regex.IGNORECASE)
outer_parentheses_pattern = regex.compile(r"\((?>[^()]|(?R))*\)", regex.IGNORECASE)


rule_mapping_dict = \
{
    "FlyingAny": SonicHeroesRuleFunctionMapping("can_fly"),
    "FlyingOneChar": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True, "orcondition": True}),
    "FlyingFull": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True}),
    "FloatingDice": SonicHeroesRuleFunctionMapping("can_floating_dice"),
    "Switch": SonicHeroesRuleFunctionMapping("can_regular_switch"),
    "Weight": SonicHeroesRuleFunctionMapping("can_regular_weight"),
    "PushPullSwitch": SonicHeroesRuleFunctionMapping("can_push_pull_switch"),
}


def is_there_team_level_str(rule: str) -> str | None:
    for team_lvl in team_level_strs:
        if rule.endswith(team_lvl):
            return team_lvl
    return None

def get_team_and_level(rule: str) -> tuple[str, str]:
    if is_there_team_level_str(rule) is None:
        return "", ""

    team: str = ""
    level: str = ""

    for lvl in level_str_to_level.keys():
        if rule.endswith(lvl):
            level = lvl

    temp_rule = rule[:-len(level)]  # type: ignore

    for t in team_strs:
        if temp_rule.endswith(t):
            team = t

    return team, level_str_to_level[level]


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
    global individual_rule_team, individual_rule_level, result_str_list, parens_mapping_list
    if rule == '':
        return

    print(f"Rule: {rule}")

    if rule.lower() == 'or':
        result_str_list.append('OR')
        return

    if rule.lower() == 'and':
        result_str_list.append('AND')
        return

    ## This is a problem (not anymore as I dont remove the TeamLevel Identifier until the end)
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
        #result_str_list.append(team_lvl)
        return

    result_str_list.append(rule)


def handle_full_rule_string(rule: str) -> str:
    #TODO make these world vars if running during generation
    global individual_rule_team, individual_rule_level, result_str_list, parens_mapping_list
    result_str_list = []
    parens_mapping_list = []
    result_str: str = "lambda state:"
    individual_rule_team, individual_rule_level = get_team_and_level(rule)
    if individual_rule_team == "" or individual_rule_level == "":
        print(f"BIG ERROR: NOT TEAM IN RULE: {rule}")
        return "ERROR"
    handle_rule(rule)


    #now handle output
    for rule_piece in result_str_list:
        if rule_piece == "(":
            result_str += f" {rule_piece}"
            continue
        if rule_piece == ")":
            result_str += f"{rule_piece} "
            continue
        if rule_piece == "AND" or rule_piece == "OR":
            result_str += f" {rule_piece.lower()} "
            continue

        result_str += f"{rule_mapping_dict[rule_piece].get_func_call_str(individual_rule_team, individual_rule_level)}"

    return result_str


test_rule = "(FlyingAnyorFlyingOneChar)or(FlyingFullandFlyingAny)SonicFrog"
print(handle_full_rule_string(test_rule))

test_rule3 = "((FloatingDiceandSwitch)orWeight)and(FlyingAnyandPushPullSwitch)SonicBH"
print(handle_full_rule_string(test_rule3))




