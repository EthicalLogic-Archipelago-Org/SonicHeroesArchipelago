import csv

import regex
from dataclasses import dataclass, field


from worlds.sonic_heroes.constants import *
from worlds.sonic_heroes.csvdata import Connections

@dataclass
class SonicHeroesRuleFunctionMapping:
    """
    Funny Data Class Here
    """
    function_name: str
    #team: str
    #level: str
    # noinspection PyDataclass
    extra_params: dict[str, bool | int | str] = field(default_factory=dict)

    def get_func_call_str(self, team: str, level: str) -> str:
        if self.function_name == "":
            return "True"
        if self.function_name == "NOTPOSSIBLE":
            return "False"
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

difficulty_strs: list[str] = \
[
    #"EasyDiff", #<- default
    "MediumDiff",
    "HardDiff",
    "ExpertDiff",
]

individual_rule_team: str = ""
individual_rule_level: str = ""

result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []

team_level_strs: list[str] = [f"{team}{level}" for team in team_strs for level in level_str_to_level.keys()]

and_condition_pattern = regex.compile(r"(AND)")
or_condition_pattern = regex.compile(r"(OR)")
outer_parentheses_pattern = regex.compile(r"\((?>[^()]|(?R))*\)")


rule_mapping_dict = \
{
    "": SonicHeroesRuleFunctionMapping(""),
    "NOTPOSSIBLE": SonicHeroesRuleFunctionMapping("NOTPOSSIBLE"),
    "AccelRoad": SonicHeroesRuleFunctionMapping("can_accel_road"),
    "BreakKeyCage": SonicHeroesRuleFunctionMapping("can_break_key_cage"),
    "DashRing": SonicHeroesRuleFunctionMapping("can_dash_ring"),
    "EnergyColumn": SonicHeroesRuleFunctionMapping("can_energy_column"),
    "FlyingAny": SonicHeroesRuleFunctionMapping("can_fly"),
    "FlyingOneChar": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True, "orcondition": True}),
    "FlyingFull": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True}),
    "FloatingDice": SonicHeroesRuleFunctionMapping("can_floating_dice"),
    "Glide": SonicHeroesRuleFunctionMapping("can_glide"),
    "KillFlyingEnemyRedNothing": SonicHeroesRuleFunctionMapping("can_kill_flying_enemy", {"red_flapper": True, "nothing": True}),
    "KillFlyingEnemyGreenLightningNothingHomingFireDunk": SonicHeroesRuleFunctionMapping("can_kill_flying_enemy", {"green_lightning": True, "nothing": True, "homing": True, "fire_dunk": True}),
    "PPUpwardPath": SonicHeroesRuleFunctionMapping("can_energy_road_upward_effect"),
    "SingleSpring": SonicHeroesRuleFunctionMapping("can_spring", {"single": True}),
    "Switch": SonicHeroesRuleFunctionMapping("can_regular_switch"),
    "Weight": SonicHeroesRuleFunctionMapping("can_regular_weight"),
    "PushPullSwitch": SonicHeroesRuleFunctionMapping("can_push_pull_switch"),
    "Ruins": SonicHeroesRuleFunctionMapping("can_ruins"),
    "SmallStonePlatform": SonicHeroesRuleFunctionMapping("can_small_stone_platform"),
    "TripleSpring": SonicHeroesRuleFunctionMapping("can_spring", {"triple": True}),
    "DashRamp": SonicHeroesRuleFunctionMapping("can_dash_ramp"),
    "DashPanel": SonicHeroesRuleFunctionMapping("can_dash_panel"),
    "Speed": SonicHeroesRuleFunctionMapping("has_char", {"speed": True}),
    "BreakThings": SonicHeroesRuleFunctionMapping("can_break_things"),
    "EggPawnNothing": SonicHeroesRuleFunctionMapping("can_egg_pawn"),
    "Homing0": SonicHeroesRuleFunctionMapping("can_homing", {"level_up": 0}),
    "KillEggPawnNothing": SonicHeroesRuleFunctionMapping("can_kill_ground_enemy", {"nothing": True}),
    "TornadoRegular0": SonicHeroesRuleFunctionMapping("can_tornado_regular", {"level_up": 0}),
    "Parkour": SonicHeroesRuleFunctionMapping("can_parkour"),

}


def sort_rule_mapping_dict_for_printing_to_console() -> None:
    dict_keys: list[str] = sorted(rule_mapping_dict.keys())  # type: ignore

    result = f"rule_mapping_dict = \\\n{{\n"

    for key in dict_keys:
        result += f"\t\"{key}\": SonicHeroesRuleFunctionMapping(\"{rule_mapping_dict[key].function_name}\""

        if len(rule_mapping_dict[key].extra_params.keys()) > 0:
            result += f", {{"

            index = 0
            for pair_key, pair_value in rule_mapping_dict[key].extra_params.items():
                result += f"\"{pair_key}\": "
                if type(pair_value) == str:
                    result += f"\"{pair_value}\""
                else:
                    result += f"{pair_value}"
                if index < len(rule_mapping_dict[key].extra_params.keys()) - 1:
                    result += f", "
                index += 1
            result += f"}}"
        result += f"),\n"

    result += "}\n"

    print(result)




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
    if 'AND' in rule:
        return True
    return False

def is_there_or(rule: str) -> bool:
    if 'OR' in rule:
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
        print(f"BIG ERROR: NO TEAM OR LEVEL IN RULE: {rule}")
        return "ERROR"
    handle_rule(rule)

    #now handle output
    for rule_piece in result_str_list:
        if rule_piece != ")" and result_str[-1:] != " " and result_str[-1:] != "(":
            result_str += " "

        if rule_piece == "(":
            result_str += f"{rule_piece}"
            continue
        if rule_piece == ")":
            result_str += f"{rule_piece}"
            continue
        if rule_piece == "AND" or rule_piece == "OR":
            result_str += f"{rule_piece.lower()}"
            continue

        result_str += f"{rule_mapping_dict[rule_piece].get_func_call_str(individual_rule_team, individual_rule_level)}"

    return result_str

def handle_rule_strs_in_list(rules: list[str]) -> str:
    result = ""
    return result

def handle_rule_strs_for_team_level(team: str, level: str, rule_list: list[str]) -> str:
    result: str = "\n"
    result += f"def create_logic_mapping_dict_{level.replace(" ", "_").lower()}_{team.replace(" ", "_").lower()}(world: SonicHeroesWorld): \n\treturn \\\n\t{{\n"

    for rule in rule_list:
        result += f"\t\t\"{rule}\": {handle_full_rule_string(rule)},\n"

    result += "\t}\n"

    return result


def handle_rule_strs_for_team(team: str) -> str:
    return ""

def handle_all_rule_strs(level: str) -> str:
    return ""

def open_connection_csv(team: str, level: str):
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa

    file_name = get_csv_file_name(team, level, CONNECTIONS, False)
    #print(f"File Name here: {file_name}")


    with files(Connections).joinpath(f"{file_name}.csv").open() as csv_file:
        reader = csv.DictReader(csv_file)
        rule_list_in_file: list[str] = []
        for x in reader:
            if "" == x[RULE] or "NOTPOSSIBLE" == x[RULE]:
                continue
            if x[RULE] not in rule_list_in_file:
                rule_list_in_file.append(x[RULE])

        print(f"Reading {team} {level} Connection Rules from csv:")
        print(handle_rule_strs_for_team_level(team, level, rule_list_in_file))



#open_connection_csv(SONIC, SEASIDEHILL)


sonic_power_plant_rules: list[str] = \
[
    "BreakKeyCageSonicPP",
    "DashRingSonicPP",
    "SingleSpringSonicPP",
    "FlyingAnyORGlideSonicPP",
    "KillFlyingEnemyRedNothingANDPPUpwardPathSonicPP",
    "KillFlyingEnemyGreenLightningNothingHomingFireDunkANDEnergyColumnSonicPP",
    "KillFlyingEnemyGreenLightningNothingHomingFireDunkANDPPUpwardPathSonicPP",
    "FlyingAnySonicPP",
    "AccelRoadANDKillFlyingEnemyGreenLightningNothingHomingFireDunkSonicPP",
    "PPUpwardPathSonicPP",
]




#def create_logic_mapping_dict_power_plant_sonic(world: SonicHeroesWorld):
    #return \
    #{
        #"BreakKeyCageSonicPP": lambda state: can_break_key_cage(world, SONIC, POWERPLANT, state),
    #}


#test_rule = "(FlyingAnyorFlyingOneChar)or(FlyingFullandFlyingAny)SonicFrog"
#print(handle_full_rule_string(test_rule))

#test_rule3 = "((FloatingDiceANDSwitch)ORWeight)AND(FlyingAnyANDPushPullSwitch)SonicBH"
#print(handle_full_rule_string(test_rule3))

test_rule4 = "BreakThingsOR(EggPawnNothingANDHoming0)OR(FlyingAny)OR(KillEggPawnNothingANDTornadoRegular0)ORParkourSonicSH"
#print(handle_full_rule_string(test_rule4))

#print(handle_rule_strs_for_team_level(SONIC, POWERPLANT))

