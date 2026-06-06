"""
generate items programmatically
"""

from BaseClasses import ItemClassification, Item

from worlds.sonic_heroes.world_base import SonicHeroesWorldBase
from .constants.char_ability import Team, Character, Ability
from .constants.items_events import *
from .constants.stage import Act, Stage, StageType
from .constants.stage_objs import StageObj, SEASIDE_HILL_DARK_STAGE_OBJS

from .helper_functions import get_abilities_for_char, get_all_characters_for_team, get_correct_ability_item_name, get_playable_char_item_name, get_stage_obj_item_name, get_spawn_position_item_name


def create_item_and_append(world: SonicHeroesWorldBase, name: str, classification: ItemClassification, amount: int = 1) -> None:
    if name in world.starting_inventory_amounts.keys():
        temp_amount: int = amount
        amount -= world.starting_inventory_amounts[name]
        world.starting_inventory_amounts[name] = max(world.starting_inventory_amounts[name] - temp_amount, 0)
        if amount < 1:
            return

    for _ in range(amount):
        world.multiworld.itempool.append(Item(name=name, code=world.item_name_to_id[name], classification=classification, player=world.player))
        world.unplaced_items -= 1


def create_items(world: SonicHeroesWorldBase) -> None:
    world.unplaced_items = len(world.multiworld.get_unfilled_locations(world.player))

    print(f"Total items to place: {world.unplaced_items}")

    #emblems (not needed)
    create_emblem_items(world=world)
    #emeralds
    create_emerald_items(world=world)
    #playable chars
    create_playable_char_items(world=world)
    #abilities
    create_ability_items(world=world)
    #stage objs
    create_stage_obj_items(world=world)
    #spawn positions
    create_spawn_position_items(world=world)


    print(f"Total filler to place: {world.unplaced_items}")
    #filler at end
    create_filler_items(world=world)
    pass


def create_emblem_items(world: SonicHeroesWorldBase) -> None:
    # emblems not in rando
    pass


def create_emerald_items(world: SonicHeroesWorldBase) -> None:
    for emerald in ChaosEmerald:
        create_item_and_append(world=world, name=emerald, classification=ItemClassification.progression)


def create_playable_char_items(world: SonicHeroesWorldBase) -> None:
    for team, act in world.enabled_team_acts.items():  # pyright: ignore[reportAny]
        if act is not Act.NONE:
            create_playable_char_items_for_team(world=world, team=team)  # pyright: ignore[reportAny]


def create_playable_char_items_for_team(world: SonicHeroesWorldBase, team: Team) -> None:
    for character in get_all_characters_for_team(world=world, team=team):
        create_item_and_append(world=world, name=get_playable_char_item_name(character=character), classification=ItemClassification.progression)


def create_ability_items(world: SonicHeroesWorldBase) -> None:
    for team, act in world.enabled_team_acts.items():  # pyright: ignore[reportAny]
        if act is not Act.NONE:
            create_ability_items_for_team(world=world, team=team)  # pyright: ignore[reportAny]


def create_ability_items_for_team(world: SonicHeroesWorldBase, team: Team) -> None:
    create_item_and_append(world=world, name=get_correct_ability_item_name(world=world, team=team, ability=Ability.JUMP), classification=ItemClassification.progression)
    for character in get_all_characters_for_team(world=world, team=team):
        create_ability_items_for_character_and_team(world=world, team=team, character=character)


def create_ability_items_for_character_and_team(world: SonicHeroesWorldBase, team: Team, character: Character) -> None:
    ability_list: list[Ability] = get_abilities_for_char(world=world, character=character)
    if True: # <- should make progressive abilities
        for ability in ability_list:
            if ability is Ability.HOMING_ATTACK or ability is Ability.TRIANGLE_JUMP:
                if Ability.HOMING_ATTACK in ability_list and Ability.TRIANGLE_JUMP in ability_list:
                    create_item_and_append(world=world, name=f"{PROGRESSIVE} {team.value} {Ability.HOMING_ATTACK.ability_name}", classification=ItemClassification.progression)
                    continue

            if ability is Ability.THUNDER_SHOOT or ability is Ability.FLIGHT or ability is Ability.DUMMY_RINGS or ability is Ability.CHEESE_CANNON:
                if Ability.THUNDER_SHOOT in ability_list and Ability.FLIGHT in ability_list:
                    if ability is Ability.DUMMY_RINGS or ability is Ability.CHEESE_CANNON:
                        continue
                    create_item_and_append(world=world, name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}", classification=ItemClassification.progression)
                    continue

            if ability is Ability.POWER_ATTACK or ability is Ability.COMBO_FINISHER:
                if Ability.POWER_ATTACK in ability_list and Ability.COMBO_FINISHER in ability_list:
                    create_item_and_append(world=world, name=f"{PROGRESSIVE} {team.value} {Ability.POWER_ATTACK.ability_name}", classification=ItemClassification.progression)

            create_item_and_append(world=world, name=get_correct_ability_item_name(world=world, team=team, ability=ability), classification=ItemClassification.progression)


def create_stage_obj_items(world: SonicHeroesWorldBase) -> None:
    for stage_obj in SEASIDE_HILL_DARK_STAGE_OBJS:
        create_item_and_append(world=world, name=get_stage_obj_item_name(stage_obj=stage_obj), classification=ItemClassification.progression)


def create_spawn_position_items(world: SonicHeroesWorldBase) -> None:
    for team, act in world.enabled_team_acts.items():  # pyright: ignore[reportAny]
        if act is not Act.NONE:
            create_spawn_position_items_for_team(world=world, team=team)  # pyright: ignore[reportAny]


def create_spawn_position_items_for_team(world: SonicHeroesWorldBase, team: Team) -> None:
    create_spawn_position_items_for_team_and_stage(world=world, team=team, stage=Stage.SEASIDE_HILL)
    # for reg_lvl in Stage.get_stages_of_type(stage_type=StageType.NORMAL_STAGE):
    #     create_spawn_position_items_for_team_and_stage(world=world, team=team, stage=reg_lvl)


def create_spawn_position_items_for_team_and_stage(world: SonicHeroesWorldBase, team: Team, stage: Stage) -> None:
    for checkpoint in range(stage.checkpoints[team] + 1):
        create_item_and_append(world=world, name=get_spawn_position_item_name(team=team, stage=stage, checkpoint=checkpoint), classification=ItemClassification.progression)


def create_filler_items(world: SonicHeroesWorldBase) -> None:
    for _ in range(world.unplaced_items):
        create_item_and_append(world=world, name=world.get_filler_item_name(), classification=ItemClassification.filler)



def create_precollected_items(world: SonicHeroesWorldBase) -> None:
    for item_name, amount in world.starting_inventory_amounts.items():
        for _ in range(amount):
            world.push_precollected(item=Item(name=item_name, classification=ItemClassification.progression, code=world.item_name_to_id[item_name], player=world.player))