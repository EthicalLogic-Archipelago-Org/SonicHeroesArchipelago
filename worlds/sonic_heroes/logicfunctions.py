from __future__ import annotations

from BaseClasses import CollectionState
from .constants import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from worlds.sonic_heroes.options import UnlockType

def can_parkour(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    """
    Walk along tricky collision / dangerous terrain
    Think cliffsides of Seaside Hill 4 Egg Pawns
    """
    return False

def can_homing_hover(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    """
    Use Hover frames reset of homing attack
    """
    return False

def can_tornado_hover(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    """
    Use Hover frames of Regular Tornado
    """
    return False

def can_rocket_accel_jump(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, both_kicks: bool = False) -> bool:
    """
    Perform a rocket accel and jump off of ledge while maintaining momentum
    """
    #swap to flying
    return False


def can_team_blast(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):

    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #return False
    region: str = get_region_name_from_level(world, level)
    item_requirements = []
    for char_name in team_char_names[team]:
        item_requirements += get_all_ability_item_names_for_character_and_region(world, team, char_name, region)

    if not state.has_from_list_unique(item_requirements, world.player, len(item_requirements)):
        return False

    return has_char(world, team, level, state, speed=True, flying=True, power=True)

def has_char(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, speed: bool = False, flying: bool = False, power: bool = False, orcondition: bool = False) -> bool:
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    conditions = []
    if speed:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, speed=True)))
    if flying:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, flying=True)))
    if power:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, power=True)))


    if orcondition:
        return state.has_any(conditions, world.player)

    else:
        return state.has_all(conditions, world.player)


def has_char_levelup(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, levelup: int, speed: bool = False, flying: bool = False, power: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    region: str = get_region_name_from_level(world, level)
    if levelup < 1 or levelup > 3:
        print(f"Has Char LevelUp Called with bad LevelUp {levelup}")
        return False
    if sum([speed, flying, power]) != 1:
        print(f"Has Char LevelUp Called with bad number of chars. team {team} level {level} levelup {levelup} speed {speed} flying {flying} power {power}")
        return False
    #no abilities lvl 0
    #<= 49% lvl 1
    #<= 99% lvl 2
    #all abilities lvl 3
    if speed:
        char_name = team_char_names[team][0]
    elif power:
        char_name = team_char_names[team][1]
    else:       # flying
        char_name = team_char_names[team][2]


    abilities = get_all_ability_item_names_for_character_and_region(world, team, char_name, region)
    item_requirements: dict[int, float] = \
    {
        #0: 0,
        1: 1,
        2: len(abilities)/2,
        3: len(abilities),
    }

    return state.count_from_list_unique(abilities, world.player) >= item_requirements[levelup]


def can_homing_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, level_up: int = 0):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #name, amount = get_item_req_for_ability(world, get_char_name_from_team(team, speed=True), get_region_name_from_level(world, level), HOMINGATTACK)
    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), HOMINGATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_tornado(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), TORNADO)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_tornado_regular(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, level_up: int = 0):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), TORNADO)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_tornado_leaf_swirl(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, level_up: int = 0):
    return True

def can_tornado_hammer_tornado(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, level_up: int = 0):
    return True

def can_kick(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    Speed Char Kick (before Rocket Accel)
    """
    return has_char(world, team, level, state, speed=True) and True

def can_rocket_accel(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), ROCKETACCEL)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player) and has_char(world, team, level, state, flying=True, power=True, orcondition=True)

def can_light_dash(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), LIGHTDASH)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_triangle_jump(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), TRIANGLEJUMP)
    name2 = get_ability_item_name(world, team, get_region_name_from_level(world, level), HOMINGATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player) and state.has(name2, world.player)

def can_light_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), LIGHTATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_speed_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, tornado: bool = False, rocket: bool = False,lightdash: bool = False, triangle: bool = False, lightattack: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not homing and not tornado and not rocket and not lightdash and not triangle and not lightattack:
        return False
    result = not orcondition
    if homing:
        if orcondition:
            result = result or can_homing_attack(world, team, level, state)
        else:
            result = result and can_homing_attack(world, team, level, state)
    if tornado:
        if orcondition:
            result = result or can_tornado(world, team, level, state)
        else:
            result = result and can_tornado(world, team, level, state)
    if rocket:
        if orcondition:
            result = result or can_rocket_accel(world, team, level, state)
        else:
            result = result and can_rocket_accel(world, team, level, state)
    if lightdash:
        if orcondition:
            result = result or can_light_dash(world, team, level, state)
        else:
            result = result and can_light_dash(world, team, level, state)
    if triangle:
        if orcondition:
            result = result or can_triangle_jump(world, team, level, state)
        else:
            result = result and can_triangle_jump(world, team, level, state)
    if lightattack:
        if orcondition:
            result = result or can_light_attack(world, team, level, state)
        else:
            result = result and can_light_attack(world, team, level, state)
    return result

def can_thundershoot_ground(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #name, amount = get_item_req_for_ability(world, get_char_name_from_team(team, flying=True), get_region_name_from_level(world, level), THUNDERSHOOT)
    #return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True, power=True, orcondition=True) and state.has(name, world.player, amount)

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True, power=True, orcondition=True) and state.has(name, world.player)

def can_thundershoot_air(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True,power=True, orcondition=True) and state.has(name, world.player)

def can_thundershoot_both(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    return can_thundershoot_ground(world, team, level, state) and can_thundershoot_air(world, team, level, state)


def can_fly(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, speedreq: bool = False, powerreq: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FLIGHT)
    name2 = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    result = True
    if speedreq or powerreq:
        result = result and has_char(world, team, level, state, speed=speedreq, power=powerreq, orcondition=orcondition)
    return has_char(world, team, level, state, flying=True) and state.has(name, world.player) and result and state.has(name2, world.player)

def can_flower_sting(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FLOWERSTING)
    return has_char(world, team, level, state, flying=True) and state.has(name, world.player) and team == CHAOTIX


def can_fake_ring_toss(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), DUMMYRINGS)
    return (team == SONIC or team == DARK or team == SUPERHARDMODE) and (has_char(world, team, level, state, flying=True) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True)) and state.has(name, world.player)


"""
def can_cheese_cannon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    
    return team == ROSE and (has_char(world, team, level, state, flying=True) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True))

def can_flower_sting_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    
    return can_flower_sting(world, team, level, state) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True)
"""

def can_flying_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, thundershootair: bool = False, thundershootground: bool = False, thundershootboth: bool = False, flyany: bool = False, flyonechar: bool = False, flyspeed: bool = False, flypower: bool = False, flyfull: bool = False, flowersting: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not thundershootair and not thundershootground and not thundershootboth and not flyany and not flyonechar and not flyspeed and not flypower and not flyfull and not flowersting:
        return False
    result = not orcondition
    if thundershootair:
        if orcondition:
            result = result or can_thundershoot_air(world, team, level, state)
        else:
            result = result and can_thundershoot_air(world, team, level, state)
    if thundershootground:
        if orcondition:
            result = result or can_thundershoot_ground(world, team, level, state)
        else:
            result = result and can_thundershoot_ground(world, team, level, state)
    if thundershootboth:
        if orcondition:
            result = result or can_thundershoot_both(world, team, level, state)
        else:
            result = result and can_thundershoot_both(world, team, level, state)
    if flyany:
        if orcondition:
            result = result or can_fly(world, team, level, state)
        else:
            result = result and can_fly(world, team, level, state)
    if flyonechar:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True, powerreq=True, orcondition=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True, powerreq=True, orcondition=True)
    if flyspeed:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True)
    if flypower:
        if orcondition:
            result = result or can_fly(world, team, level, state, powerreq=True)
        else:
            result = result and can_fly(world, team, level, state, powerreq=True)
    if flyfull:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True, powerreq=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True, powerreq=True)
    if flowersting:
        if orcondition:
            result = result or can_flower_sting(world, team, level, state)
        else:
            result = result and can_flower_sting(world, team, level, state)
    return result


def can_power_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), POWERATTACK)
    return has_char(world, team, level, state, power=True)  # and state.has(name, world.player)

def can_break_things(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), POWERATTACK)
    return has_char(world, team, level, state, power=True)# and state.has(name, world.player)

def can_break_key_cage(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    return True

def can_belly_flop(world: SonicHeroesWorld, team: str, level: str, state):
    return False

def can_fire_dunk(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FIREDUNK)
    return has_char(world, team, level, state, power=True) and has_char(world, team, level, state, speed=True, flying=True, orcondition=True) and state.has(name, world.player)

def can_glide(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), GLIDE)
    return has_char(world, team, level, state, power=True) and state.has(name, world.player)


def can_combo_finsh(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, lvl: int = 1):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), COMBOFINISHER)
    return has_char(world, team, level, state, power=True) and state.has(name, world.player) and has_char_levelup(world, team, level, state, lvl, power=True)

def can_power_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, breaknotcage=False, breakcage=False, firedunk=False, glide=False, combofinsh=False, orcondition=False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not breaknotcage and not breakcage and not firedunk and not glide and not combofinsh:
        return False
    result = not orcondition
    if breaknotcage:
        if orcondition:
            result = result or can_break_things(world, team, level, state)
        else:
            result = result and can_break_things(world, team, level, state)
    if breakcage:
        if orcondition:
            result = result or can_break_key_cage(world, team, level, state)
        else:
            result = result and can_break_key_cage(world, team, level, state)
    if firedunk:
        if orcondition:
            result = result or can_fire_dunk(world, team, level, state)
        else:
            result = result and can_fire_dunk(world, team, level, state)
    if glide:
        if orcondition:
            result = result or can_glide(world, team, level, state)
        else:
            result = result and can_glide(world, team, level, state)
    if combofinsh:
        if orcondition:
            result = result or can_combo_finsh(world, team, level, state)
        else:
            result = result and can_combo_finsh(world, team, level, state)
    return result


def can_remove_ground_enemy_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True)) or ((can_tornado(world, team, level, state) or can_rocket_accel(world, team, level, state)) and has_char_levelup(world, team, level, state, 1, speed=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_nothing(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_kill_egg_pawn_nothing(world: SonicHeroesWorld, team: str, level: str, state):
    return True

def can_kill_ground_enemy_spear(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 1, speed=True)) or can_break_things(world, team, level, state) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 1, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_plain_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_nothing(world, team, level, state) and can_remove_ground_enemy_shield(world, team, level, state)) or (can_break_things(world, team, level, state) and has_char_levelup(world, team, level, state, 1, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_concrete_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_nothing(world, team, level, state) and can_remove_ground_enemy_shield(world, team, level, state)) or (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 2, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_spike_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_kill_ground_enemy_concrete_shield(world, team, level, state)

def can_kill_ground_enemy_klagen(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_kill_ground_enemy_nothing(world, team, level, state)

def can_kill_ground_enemy_cameron(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_remove_ground_enemy_shield(world, team, level, state) or can_break_things(world, team, level, state) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_goldcameron(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_remove_ground_enemy_shield(world, team, level, state) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_rhinoliner(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_eggbishop(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 2, speed=True)) or (can_fire_dunk(world, team, level, state) and has_char_levelup(world, team, level, state, 2, power=True)) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_e2000(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_combo_finsh(world, team, level, state, 3) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)


def can_kill_ground_enemy_e2000r(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_e2000(world, team, level, state)
            and (can_remove_ground_enemy_shield(world, team, level, state) or can_team_blast(world, team, level, state)))

def can_kill_ground_enemy_egghammer(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 3, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_heavyegghammer(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return ((can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True)) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True))) and can_fire_dunk(world, team, level, state) and (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 3, power=True) and can_team_blast(world, team, level, state))

def can_kill_ground_enemy_cannon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True #and can_cannon_obj(world, team, level, state)


def can_kill_ground_enemy(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, spear: bool = False, plainshield: bool = False, concreteshield: bool = False, spikeshield: bool = False, klagen: bool = False, cameron: bool = False, goldcameron: bool = False, rhinoliner: bool = False, eggbishop: bool = False, e2000: bool = False, e2000r: bool = False, egghammer: bool = False, heavyegghammer: bool = False, cannon: bool = False, orcondition: bool = False):
    if not nothing and not spear and not plainshield and not spikeshield and not klagen and not cameron and not goldcameron and not rhinoliner and not eggbishop and not e2000 and not e2000r and not egghammer and not heavyegghammer and not cannon:
        return can_kill_ground_enemy_nothing(world, team, level, state)
    result = not orcondition
    if nothing:
        if orcondition:
            result = result or can_kill_ground_enemy_nothing(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_nothing(world, team, level, state)
    if spear:
        if orcondition:
            result = result or can_kill_ground_enemy_spear(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_spear(world, team, level, state)
    if plainshield:
        if orcondition:
            result = result or can_kill_ground_enemy_plain_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_plain_shield(world, team, level, state)
    if concreteshield:
        if orcondition:
            result = result or can_kill_ground_enemy_concrete_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_concrete_shield(world, team, level, state)
    if spikeshield:
        if orcondition:
            result = result or can_kill_ground_enemy_spike_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_spike_shield(world, team, level, state)
    if klagen:
        if orcondition:
            result = result or can_kill_ground_enemy_klagen(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_klagen(world, team, level, state)
    if cameron:
        if orcondition:
            result = result or can_kill_ground_enemy_cameron(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_cameron(world, team, level, state)
    if goldcameron:
        if orcondition:
            result = result or can_kill_ground_enemy_goldcameron(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_goldcameron(world, team, level, state)
    if rhinoliner:
        if orcondition:
            result = result or can_kill_ground_enemy_rhinoliner(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_rhinoliner(world, team, level, state)
    if eggbishop:
        if orcondition:
            result = result or can_kill_ground_enemy_eggbishop(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_eggbishop(world, team, level, state)
    if e2000:
        if orcondition:
            result = result or can_kill_ground_enemy_e2000(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_e2000(world, team, level, state)
    if e2000r:
        if orcondition:
            result = result or can_kill_ground_enemy_e2000r(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_e2000r(world, team, level, state)
    if egghammer:
        if orcondition:
            result = result or can_kill_ground_enemy_egghammer(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_egghammer(world, team, level, state)
    if heavyegghammer:
        if orcondition:
            result = result or can_kill_ground_enemy_heavyegghammer(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_heavyegghammer(world, team, level, state)
    if cannon:
        if orcondition:
            result = result or can_kill_ground_enemy_cannon(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_cannon(world, team, level, state)
    return result


def can_kill_flying_enemy_red_flapper(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, homing: bool = False, firedunk: bool = False):
    if nothing:
        return True
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_green_shot(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, homing: bool = False, firedunk: bool = False):
    if nothing:
        return True
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_green_lightning(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    condition = False
    if homing:
        condition = condition or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 1, speed=True))
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 1, flying=True)) or condition or can_team_blast(world, team, level, state)
    # homing 1 or thundershoot 1 or SFA

def can_kill_flying_enemy_yellow_light(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_blue_mgun(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    condition = False
    if homing:
        condition = condition or (can_homing_attack(world, team, level, state, level_up=2) and has_char_levelup(world, team, level, state, 2, speed=True))
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) or condition or can_team_blast(world, team, level, state)
    # homing 2 or thundershoot 2 or SFA

def can_kill_flying_enemy_black_spikey(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_blue_mgun(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_purple_bombs(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_blue_mgun(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_silver_armor(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, firedunk=False):
    condition = False
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return ((can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) and can_break_things(world, team, level, state)) or condition or can_team_blast(world, team, level, state)
    #thundershoot 2 and break or SFA

def can_kill_flying_enemy_falco(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)
    #thundershoot 3 or SFA


def can_kill_flying_enemy(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, red_flapper=False, green_shot=False, green_lightning=False, yellow_light=False, blue_mgun=False, black_spikey=False, silver_armor=False, purple_bombs=False, falco=False, nothing=False, homing=False, fire_dunk=False, orcondition=False):
    if not red_flapper and not green_shot and not green_lightning and not yellow_light and not blue_mgun and not black_spikey and not silver_armor and not purple_bombs and not falco:
        return False
    result = not orcondition
    if red_flapper:
        if orcondition:
            result = result or can_kill_flying_enemy_red_flapper(world, team, level, state, nothing=nothing, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_red_flapper(world, team, level, state, nothing=nothing, homing=homing, firedunk=fire_dunk)
    if green_shot:
        if orcondition:
            result = result or can_kill_flying_enemy_green_shot(world, team, level, state, nothing=nothing, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_green_shot(world, team, level, state, nothing=nothing, homing=homing, firedunk=fire_dunk)
    if green_lightning:
        if orcondition:
            result = result or can_kill_flying_enemy_green_lightning(world, team, level, state, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_green_lightning(world, team, level, state, homing=homing, firedunk=fire_dunk)
    if yellow_light:
        if orcondition:
            result = result or can_kill_flying_enemy_yellow_light(world, team, level, state, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_yellow_light(world, team, level, state, homing=homing, firedunk=fire_dunk)
    if blue_mgun:
        if orcondition:
            result = result or can_kill_flying_enemy_blue_mgun(world, team, level, state, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_blue_mgun(world, team, level, state, homing=homing, firedunk=fire_dunk)
    if black_spikey:
        if orcondition:
            result = result or can_kill_flying_enemy_black_spikey(world, team, level, state, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_black_spikey(world, team, level, state, homing=homing, firedunk=fire_dunk)
    if silver_armor:
        if orcondition:
            result = result or can_kill_flying_enemy_silver_armor(world, team, level, state, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_silver_armor(world, team, level, state, firedunk=fire_dunk)
    if purple_bombs:
        if orcondition:
            result = result or can_kill_flying_enemy_purple_bombs(world, team, level, state, homing=homing, firedunk=fire_dunk)
        else:
            result = result and can_kill_flying_enemy_purple_bombs(world, team, level, state, homing=homing, firedunk=fire_dunk)
    if falco:
        if orcondition:
            result = result or can_kill_flying_enemy_falco(world, team, level, state)
        else:
            result = result and can_kill_flying_enemy_falco(world, team, level, state)
    return result



#Objs Here
#in case I remove tp triggers here
def has_tp_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_single_spring_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_triple_spring_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_ring_group_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_hint_ring_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_regular_switch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_push_pull_switch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_target_switch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_dash_panel_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_dash_ring_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_rainbow_hoop_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_checkpoint_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_dash_ramp_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_cannon_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_cannon_speed(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_cannon_obj(world, team, level, state) and has_char(world, team, level, state, speed=True)

def can_cannon_flying(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_cannon_obj(world, team, level, state) and has_char(world, team, level, state, flying=True)

def can_cannon_power(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_cannon_obj(world, team, level, state) and has_char(world, team, level, state, power=True)

def has_regular_weight_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_breakable_weight_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_spike_ball_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_laser_fence_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_item_box_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_item_balloon_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_goal_ring_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_pulley_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_wood_container_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_break_wood_container(world: SonicHeroesWorld, team: str, level: str, state):
    return can_kick(world, team, level, state) or can_tornado(world, team, level, state) or can_break_things(world, team, level, state) or can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state) or can_thundershoot_both(world, team, level, state)

def can_break_in_ground_wood_container(world, team: str, level: str, state: CollectionState):
    #return not has_wood_container_obj(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))
    #CANNOT lose access when getting item
    return can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state)

def has_iron_container_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_break_iron_container(world: SonicHeroesWorld, team: str, level: str, state):
    return can_kick(world, team, level, state) or can_tornado(world, team, level, state) or can_break_things(world, team, level, state) or can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state) or can_thundershoot_both(world, team, level, state)

def can_break_in_ground_iron_container(world, team: str, level: str, state: CollectionState):
    #return not has_iron_container_obj(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))
    #CANNOT lose access when getting item
    return can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state)

def has_unbreakable_container_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_break_unbreakable_container(world: SonicHeroesWorld, team: str, level: str, state):
    return False

def can_break_in_ground_unbreakable_container(world, team: str, level: str, state: CollectionState):
    #return not has_unbreakable_container_obj(world, team, level, state) or False
    #CANNOT lose access when getting item
    return False

def has_chao_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_cage_box_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_break_cage_box(world: SonicHeroesWorld, team: str, level: str, state):
    return True

def has_propeller_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_propeller(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_propeller_obj(world, team, level, state) and (can_tornado(world, team, level, state) or can_rocket_accel(world, team, level, state)) or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True))

def has_pole_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_pole(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, air: bool = False):
    return has_pole_obj(world, team, level, state) and (can_tornado(world, team, level, state) or (can_rocket_accel(world, team, level, state) and not air)) or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True))

def has_gong_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_gong(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    #fire dunk / belly flop is possible (YAML option)
    return has_gong_obj(world, team, level, state) and (can_power_attack(world, team, level, state) or (False and (can_fire_dunk(world, team, level, state) or can_belly_flop(world, team, level, state))))

def has_fan_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_fan(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_fan_obj(world, team, level, state) and can_glide(world, team, level, state)

def has_case_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_warp_flower_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_warp_flower(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_warp_flower_obj(world, team, level, state) and can_flower_sting(world, team, level, state)

def has_bonus_key_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_teleport_trigger_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_cement_block_on_rails_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_cement_sliding_block_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_cement_block_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_moving_ruins_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_trigger_ruins_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_hermit_crab_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_small_stone_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_crumbling_stone_pillar_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_falling_stone_structure_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    #this obj can not be disabled without editing collision mask (will always be true)
    return True

def has_moving_item_balloon_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_energy_road_section_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_metro_road_cap_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_metro_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_falling_drawbridge_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_tilting_bridge_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_blimp_platform_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_energy_road_speed_effect_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_energy_road_upward_section_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_energy_column_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_elevator_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_lava_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_liquid_lava_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_energy_road_upward_effect_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_shutter_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_pinball(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    Helper function for all pinball actions
    """
    return True

def has_small_bumper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_green_floating_bumper_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_pinball_flipper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_small_triangle_bumper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_star_glass_panel_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_star_glass_air_panel_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_large_triangle_bumper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_large_casino_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_breakable_glass_floor_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_break_glass_floor(world, team: str, level: str, state: CollectionState):
    #return not has_breakable_glass_floor_obj(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))
    #CANNOT lose access on getting item
    return can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state) or can_belly_flop(world, team, level, state)

def has_floating_dice_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_triple_slots_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_single_slots_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_bingo_chart_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_bingo_chip_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_dash_arrow_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_potato_chip_obj(world, team: str, level: str, state: CollectionState):
    """
    Also the Bingo Highway VIP Chips
    """
    return True

def can_rail(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    Helper function for all rail actions
    """
    return True

def has_switchable_rail_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_rail_switch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_switchable_arrow_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_switch_switchable_rail(world, team: str, level: str, state: CollectionState):
    return has_switchable_rail_obj(world, team, level, state) and has_rail_switch_obj(world, team, level, state)

def has_rail_booster_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_rail_crossing_roadblock_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_capsule_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_station_door_obj(world, team: str, level: str, state: CollectionState):
    """
    This is the Door in Rail Canyon (prob not needed imo)
    """
    return True

def has_floor_grate_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_rail_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_train_train_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_engine_core_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_big_gun_interior_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def has_barrel_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    This refers to the barrel deco obj in rail canyon / bullet station
    """
    return True

def has_canyon_bridge_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_train_top_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_green_frog_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_small_green_rain_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_small_bouncy_mushroom_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_tall_vertical_vine_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_tall_tree_platforms_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_grindable_growing_ivy_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_large_yellow_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_bouncy_fruit_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_large_bouncy_mushroom_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_swinging_vine_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_alligator_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_black_frog_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_bouncy_falling_fruit_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_tp_switch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_castle_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_castle_cracked_wall_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_castle_floating_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_flame_torch_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_pumpkin_ghost_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_mansion_floating_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_mansion_cracked_wall_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_mansion_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_castle_key_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_mansion_pumpkin_ghost_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_mystic_mansion_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_normal_cannon_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_large_cannon_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_horizontal_cannon_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_moving_cannon_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_rectangle_floating_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_egg_fleet_door_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_square_floating_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_falling_platform_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def has_self_destruct_tp_switch_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_self_destruct_tp_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_self_destruct_tp_switch_obj(world, team, level, state) and has_char(world, team, level, state, speed=True)

def has_eggman_cell_key_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def has_egg_flapper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_green_flapper_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_egg_pawn_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_klagen_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_falco_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_egg_hammer_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_cameron_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_rhino_liner_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_egg_bishop_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_e2000_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_special_stage_orbs_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_appear_chaos_emerald_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_special_stage_spring_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_special_stage_dash_panel_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_special_stage_dash_ring_obj(world, team: str, level: str, state: CollectionState):
    return True

def has_bobsled_obj(world, team: str, level: str, state: CollectionState):
    return True

def can_bobsled(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return has_bobsled_obj(world, team, level, state)
