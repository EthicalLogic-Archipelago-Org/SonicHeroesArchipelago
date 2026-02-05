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
    extra_params: dict[str, bool | int | str | EggFlapperWeapon | EggFlapperArmor | EggPawnWeapon | EggPawnShield | EggPawnType] = field(default_factory=dict)

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




ability_rule_mapping_dict: dict[str, SonicHeroesRuleFunctionMapping] = \
{
    #all chars
    "Jump": SonicHeroesRuleFunctionMapping("can_jump"),
    "HeightFly": SonicHeroesRuleFunctionMapping("can_get_height", {"fly_valid": True}),
    "HeightFlyJump": SonicHeroesRuleFunctionMapping("can_get_height", {"fly_valid": True, "jump_valid": True}),
    "HeightComboFlyJump": SonicHeroesRuleFunctionMapping("can_get_height", {"combo_finisher_valid": True, "fly_valid": True, "jump_valid": True}),
    "HeightComboFlyJumpThundershoot": SonicHeroesRuleFunctionMapping("can_get_height", {"combo_finisher_valid": True, "fly_valid": True, "jump_valid": True, "thundershoot_valid": True}),
    "HeightComboThundershoot": SonicHeroesRuleFunctionMapping("can_get_height", {"combo_finisher_valid": True, "thundershoot_valid": True}),
    "HeightJump": SonicHeroesRuleFunctionMapping("can_get_height", {"jump_valid": True}),
    "HeightFlyNoJumpSolo": SonicHeroesRuleFunctionMapping("can_get_height", {"fly_solo_no_jump_valid": True}),
    "HeightFlyNoJumpSoloJump": SonicHeroesRuleFunctionMapping("can_get_height", {"fly_solo_no_jump_valid": True, "jump_valid": True}),
    "HeightThundershoot": SonicHeroesRuleFunctionMapping("can_get_height", {"thundershoot_valid": True}),
    "HoverFrame": SonicHeroesRuleFunctionMapping("can_hover_frame"),
    "Parkour": SonicHeroesRuleFunctionMapping("can_parkour"),





    #speed
    "HomingHover": SonicHeroesRuleFunctionMapping("can_homing_hover"),
    "TornadoHover": SonicHeroesRuleFunctionMapping("can_tornado_hover"),
    "TornadoRegular0": SonicHeroesRuleFunctionMapping("can_tornado_regular", {"level_up": 0}),
    "Homing0": SonicHeroesRuleFunctionMapping("can_homing_attack", {"level_up": 0}),
    "SpeedChar": SonicHeroesRuleFunctionMapping("has_char", {"speed": True}),
    "CannonSpeed": SonicHeroesRuleFunctionMapping("can_cannon_speed"),


    #power
    "BreakThings": SonicHeroesRuleFunctionMapping("can_break_things"),
    "Glide": SonicHeroesRuleFunctionMapping("can_glide"),
    "CannonPower": SonicHeroesRuleFunctionMapping("can_cannon_power"),


    #flying
    "FlyingChar": SonicHeroesRuleFunctionMapping("has_char", {"flying": True}),
    "FlyingAny": SonicHeroesRuleFunctionMapping("can_fly"),
    "FlyingFull": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True}),
    "FlyingOneChar": SonicHeroesRuleFunctionMapping("can_fly", {"speedreq": True, "powerreq": True, "orcondition": True}),
    "Thundershoot": SonicHeroesRuleFunctionMapping("can_thundershoot"),
    "CannonFlying": SonicHeroesRuleFunctionMapping("can_cannon_flying"),


}

stage_obj_rule_mapping_dict: dict[str, SonicHeroesRuleFunctionMapping] = \
{
    #bobsled
    "BobsledAny": SonicHeroesRuleFunctionMapping("can_bobsled"),

    #shared Objs
    "SingleSpring": SonicHeroesRuleFunctionMapping("has_single_spring_obj"),
    "TripleSpring": SonicHeroesRuleFunctionMapping("has_triple_spring_obj"),
    "StageRing": SonicHeroesRuleFunctionMapping("has_ring_group_obj"),
    "HintRing": SonicHeroesRuleFunctionMapping("has_ring_group_obj"),
    "RegularSwitch": SonicHeroesRuleFunctionMapping("has_regular_switch_obj"),
    "PushPullSwitch": SonicHeroesRuleFunctionMapping("has_push_pull_switch_obj"),
    "TargetSwitch": SonicHeroesRuleFunctionMapping("has_target_switch_obj"),
    "DashPanel": SonicHeroesRuleFunctionMapping("has_dash_panel_obj"),
    "DashRing": SonicHeroesRuleFunctionMapping("has_dash_ring_obj"),
    "RainbowHoops": SonicHeroesRuleFunctionMapping("has_rainbow_hoops_obj"),
    "DashRamp": SonicHeroesRuleFunctionMapping("has_dash_ramp_obj"),
    "CannonObj": SonicHeroesRuleFunctionMapping("has_cannon_obj"),
    "RegularWeight": SonicHeroesRuleFunctionMapping("has_regular_weight_obj"),
    "BreakableWeight": SonicHeroesRuleFunctionMapping("has_breakable_weight_obj"),
    #"SpikeBall": SonicHeroesRuleFunctionMapping("has_spike_ball_obj"),
    #"LaserFence": SonicHeroesRuleFunctionMapping("has_laser_fence_obj"),
    #"ItemBox": SonicHeroesRuleFunctionMapping("has_item_box_obj"),
    #"ItemBalloon": SonicHeroesRuleFunctionMapping("has_item_balloon_obj"),
    #"AllItemObjs": SonicHeroesRuleFunctionMapping("has_all_item_obj"),
    #"AllItemBalloonObjs": SonicHeroesRuleFunctionMapping("has_all_item_balloon_obj"),
    #"GoalRing": SonicHeroesRuleFunctionMapping("has_goal_ring_obj"),
    "Pulley": SonicHeroesRuleFunctionMapping("has_pulley_obj"),
    "WoodContainer": SonicHeroesRuleFunctionMapping("has_wood_container_obj"),
    "BreakWoodContainer": SonicHeroesRuleFunctionMapping("can_break_wood_container"),
    "BreakInGroundWoodContainer": SonicHeroesRuleFunctionMapping("can_break_in_ground_wood_container"),
    "IronContainer": SonicHeroesRuleFunctionMapping("has_iron_container_obj"),
    "BreakIronContainer": SonicHeroesRuleFunctionMapping("can_break_iron_container"),
    "BreakInGroundIronContainer": SonicHeroesRuleFunctionMapping("can_break_in_ground_Iron_container"),
    "UnbreakableContainer": SonicHeroesRuleFunctionMapping("has_unbreakable_container_obj"),
    "BreakUnbreakableContainer": SonicHeroesRuleFunctionMapping("can_break_unbreakable_container"),
    "BreakInGroundUnbreakableContainer": SonicHeroesRuleFunctionMapping("can_break_in_ground_unbreakable_container"),
    "LostChao": SonicHeroesRuleFunctionMapping("has_chao_obj"),
    #"CageBox": SonicHeroesRuleFunctionMapping("has_cage_box_obj"),
    #"Propeller": SonicHeroesRuleFunctionMapping("has_propeller_obj"),
    "Propeller": SonicHeroesRuleFunctionMapping("can_propeller"),
    #"Pole": SonicHeroesRuleFunctionMapping("has_pole_obj"),
    "Pole": SonicHeroesRuleFunctionMapping("can_pole"),
    #"Gong": SonicHeroesRuleFunctionMapping("has_gong_obj"),
    "Gong": SonicHeroesRuleFunctionMapping("can_gong"),
    #"Fan": SonicHeroesRuleFunctionMapping("has_fan_obj"),
    "Fan": SonicHeroesRuleFunctionMapping("can_fan"),
    "Case": SonicHeroesRuleFunctionMapping("has_case_obj"),
    #"WarpFlower": SonicHeroesRuleFunctionMapping("has_warp_flower_obj"),
    "WarpFlower": SonicHeroesRuleFunctionMapping("can_warp_flower"),
    "BonusKey": SonicHeroesRuleFunctionMapping("has_bonus_key_obj"),
    "TeleportTrigger": SonicHeroesRuleFunctionMapping("has_teleport_trigger_obj"),
    #Seaside Hill Objs
    #"CementBlockRails": SonicHeroesRuleFunctionMapping("has_cement_block_rails_obj"),
    "CementBlock": SonicHeroesRuleFunctionMapping("has_cement_block_obj"),
    "RuinsNoTrigger": SonicHeroesRuleFunctionMapping("has_moving_ruins_obj"),
    "RuinsTrigger": SonicHeroesRuleFunctionMapping("has_moving_ruins_obj_and_trigger_obj"),
    "HermitCrab": SonicHeroesRuleFunctionMapping("has_hermit_crab_obj"),
    "SmallStonePlatform": SonicHeroesRuleFunctionMapping("has_small_stone_platform_obj"),
    #Ocean Palace Objs
    "CrumblingStonePillar": SonicHeroesRuleFunctionMapping("has_crumbling_stone_pillar_obj"),
    "FallingStoneStructure": SonicHeroesRuleFunctionMapping("has_falling_stone_structure_obj"),
    "MovingItemBalloon": SonicHeroesRuleFunctionMapping("has_moving_item_balloon_obj"),

    #Grand Metro Objs


    #Enemy Objs
    "EggFlapperRed": SonicHeroesRuleFunctionMapping("has_egg_flapper_obj"),
    "EggFlapperGreenShot": SonicHeroesRuleFunctionMapping("has_egg_flapper_obj", {"weapon": EggFlapperWeapon.SHOT}),

    "EggPawnNoWeapon": SonicHeroesRuleFunctionMapping("has_egg_pawn_obj", {"weapon": EggPawnWeapon.NONE}),
    "KillEggPawnNoWeapon": SonicHeroesRuleFunctionMapping("can_kill_egg_pawn_nothing"),
    "EggPawnBazooka": SonicHeroesRuleFunctionMapping("has_egg_pawn_obj", {"weapon": EggPawnWeapon.BAZOOKA}),
    "KillEggPawnBazooka": SonicHeroesRuleFunctionMapping("can_kill_egg_pawn_nothing"),
}


rule_mapping_dict: dict[str, SonicHeroesRuleFunctionMapping] = \
{
    "": SonicHeroesRuleFunctionMapping(""),
    "NOTPOSSIBLE": SonicHeroesRuleFunctionMapping("NOTPOSSIBLE"),
    "BreakKeyCage": SonicHeroesRuleFunctionMapping("can_break_key_cage"),

    **ability_rule_mapping_dict,
    **stage_obj_rule_mapping_dict,
}


def sort_rule_mapping_dict_for_printing_to_console() -> None:
    dict_keys: list[str] = sorted(rule_mapping_dict.keys())  # type: ignore

    result = f"rule_mapping_dict = \\\n{{\n"

    for key in dict_keys:
        result += f"    \"{key}\": SonicHeroesRuleFunctionMapping(\"{rule_mapping_dict[key].function_name}\""

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


def handle_rule(rule: str, print_steps: bool = False):
    global individual_rule_team, individual_rule_level, result_str_list, parens_mapping_list
    if rule == '':
        return

    if print_steps:
        print(f"Rule: {rule}")

    if rule == 'OR':
        result_str_list.append('OR')
        return

    if rule == 'AND':
        result_str_list.append('AND')
        return

    ## This is a problem (not anymore as I dont remove the TeamLevel Identifier until the end)
    if rule[0] == '(' and rule[-1] == ')':
        handle_rule(rule[1:-1], print_steps)
        return


    if is_there_parens(rule):
        temp_var = outer_parentheses_pattern.split(rule)
        if print_steps:
            print(f"temp_var={temp_var}")
        handle_rule(temp_var[0], print_steps)

        temp_scanner = outer_parentheses_pattern.finditer(rule)

        for index, scan_match in enumerate(temp_scanner):
            temp_index = len(result_str_list)
            result_str_list.append('(')
            temp_tuple = (temp_index, temp_index)
            handle_rule(scan_match.group(), print_steps)
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

            handle_rule(temp_var[index + 1], print_steps)


        """
        for scan_match in temp_scanner:
            temp_index = len(result_str_list)
            result_str_list.append('(')
            temp_tuple = (temp_index, temp_index)
            handle_rule(scan_match.group(), print_steps)
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

        handle_rule(temp_var[1], print_steps)
        """
        return

    if is_there_and(rule):
        temp_var = and_condition_pattern.split(rule)
        if print_steps:
            print(f"Temp AND Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split, print_steps)
            #if index < len(temp_var) - 1:
                #result_str_list.append('AND')
        return

    if is_there_or(rule):
        temp_var = or_condition_pattern.split(rule)
        if print_steps:
            print(f"Temp OR Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split, print_steps)
        return

    team_lvl = is_there_team_level_str(rule)

    if team_lvl is not None:
        handle_rule(rule.replace(team_lvl, ""), print_steps)
        #result_str_list.append(team_lvl)
        return

    result_str_list.append(rule)


def handle_full_rule_string(rule: str, print_steps: bool = False) -> str:
    #TODO make these world vars if running during generation
    global individual_rule_team, individual_rule_level, result_str_list, parens_mapping_list
    result_str_list = []
    parens_mapping_list = []
    result_str: str = "lambda state:"
    individual_rule_team, individual_rule_level = get_team_and_level(rule)
    if individual_rule_team == "" or individual_rule_level == "":
        print(f"BIG ERROR: NO TEAM OR LEVEL IN RULE: {rule}")
        return "BIG ERROR"
    handle_rule(rule, print_steps)

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
    result += f"def create_logic_mapping_dict_{level.replace(" ", "_").lower()}_{team.replace(" ", "_").lower()}(world: SonicHeroesWorld): \n    return \\\n    {{\n"

    for rule in rule_list:
        result += f"        \"{rule}\": {handle_full_rule_string(rule)},\n\n"

    result += "    }\n"

    return result


def handle_rule_strs_for_team(team: str) -> str:
    return ""

def handle_all_rule_strs(level: str) -> str:
    return ""

def open_connection_csv(team: str, level: str, secret: bool = False) -> str:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa

    file_name: str = get_csv_file_name(team, level, CONNECTIONS, secret)
    #print(f"File Name here: {file_name}")

    with files(Connections).joinpath(f"{file_name}.csv").open() as csv_file:
        reader = csv.DictReader(csv_file)
        rule_list_in_file: list[str] = []
        for x in reader:
            if "" == x[RULE] or "NOTPOSSIBLE" == x[RULE]:
                continue
            if x[RULE] not in rule_list_in_file:
                rule_list_in_file.append(x[RULE])

        rule_list_in_file.sort(key=lambda rule_str: rule_str.replace("(", "").replace(")", ""))
        print(f"Reading {team} {level} Connection Rules from csv:")
        return handle_rule_strs_for_team_level(team, level, rule_list_in_file)



def do_connection_csv_mapping_for_team(team: str) -> str:
    level_list: list[str] = \
    [
        SEASIDEHILL,
        #OCEANPALACE,
    ]

    result = ""
    for level in level_list:
        result += open_connection_csv(team, level)

    return result



def do_connection_csv_for_all_teams() -> None:
    team_list = \
    [
        SONIC,
    ]

    big_result: str = "from __future__ import annotations\nfrom typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from worlds.sonic_heroes import SonicHeroesWorld\nfrom .constants import *\nfrom .logicfunctions import *\n\n"

    for team in team_list:
        big_result += f"#Team {team}\n" + do_connection_csv_mapping_for_team(team) + "\n\n"

    with open("test_mapping.py", "w") as file:
        file.write(big_result)




#open_connection_csv(SONIC, SEASIDEHILL)




#def create_logic_mapping_dict_power_plant_sonic(world: SonicHeroesWorld):
    #return \
    #{
        #"BreakKeyCageSonicPP": lambda state: can_break_key_cage(world, SONIC, POWERPLANT, state),
    #}


#test_rule = "BreakThingsOR((EggPawnNoWeaponOREggPawnBazooka)ANDHeightJumpANDHoming0)ORHeightFlyOR((KillEggPawnNoWeaponANDKillEggPawnBazooka)ANDHeightJumpANDTornadoHover)OR(HeightFlyNoJumpSoloJumpANDParkour)OR(HeightJumpANDThundershoot)SonicSH"
#print(handle_full_rule_string(test_rule, True))

#test_rule3 = "((FloatingDiceANDSwitch)ORWeight)AND(FlyingAnyANDPushPullSwitch)SonicBH"
#print(handle_full_rule_string(test_rule3))

#test_rule4 = "BreakThingsOR(EggPawnNothingANDHoming0)OR(FlyingAny)OR(KillEggPawnNothingANDTornadoRegular0)ORParkourSonicSH"
#print(handle_full_rule_string(test_rule4))

#print(handle_rule_strs_for_team_level(SONIC, POWERPLANT))

#sort_rule_mapping_dict_for_printing_to_console()


do_connection_csv_for_all_teams()