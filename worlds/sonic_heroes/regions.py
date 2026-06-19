"""
Regions
"""


from BaseClasses import Region, Location
from rule_builder.rules import Has, Rule, True_

from .constants.apworld import VICTORY_ITEM, VICTORY_LOCATION
from .constants.char_ability import Team
from .constants.items_events import OBJ_SANITY, SPAWN_POSITION
from .constants.loc_region import MENU_REGION_NAME, METAL_OVERLORD_REGION_NAME
from .constants.stage import Stage, Act

from .helper_functions import get_spawn_position_item_name, is_this_team_enabled
from .rule_builder.functions_stages import can_goal_rule
from .locations import append_locations_to_region

from .parsed_data import parser_connection_mapping, parser_region_mapping

from .world_base import SonicHeroesWorldBase




def create_regions(world: SonicHeroesWorldBase) -> None:
    stage: Stage = Stage.SEASIDE_HILL
    team: Team = Team.DARK

    menu_region: Region = Region(name=MENU_REGION_NAME, player=world.player, multiworld=world.multiworld)
    world.multiworld.regions.append(region=menu_region)

    create_regions_for_team_stage(world=world, team=team, stage=stage)

    metal_overlord_region: Region = Region(name=METAL_OVERLORD_REGION_NAME, player=world.player, multiworld=world.multiworld)
    victory_location: Location = Location(name=VICTORY_LOCATION, address=None, parent=metal_overlord_region, player=world.player)
    victory_location.place_locked_item(item=world.create_item(name=VICTORY_ITEM))
    metal_overlord_region.locations.append(victory_location)
    world.multiworld.regions.append(region=metal_overlord_region)
    pass


def create_regions_for_team_stage(world: SonicHeroesWorldBase, team: Team, stage: Stage) -> None:
    for region_data in parser_region_mapping[stage][team]:
        # print(f"Creating region: {region_data.region_name}")
        region: Region = Region(name=region_data.region_name, player=world.player, multiworld=world.multiworld)
        append_locations_to_region(world=world, region=region, team=team, stage=stage)
        world.multiworld.regions.append(region=region)


def create_entrance(world: SonicHeroesWorldBase, name: str, source: str, target: str, rule: Rule[SonicHeroesWorldBase]) -> None:
    source_region: Region = world.get_region(region_name=source)
    target_region: Region = world.get_region(region_name=target)
    _ = source_region.connect(connecting_region=target_region, name=name, rule=rule)


def create_entrances(world: SonicHeroesWorldBase) -> None:
    for team in Team:
        if team is not Team.ANY_TEAM:
            if is_this_team_enabled(world=world, team=team):
                create_entrances_for_team(world=world, team=team)

    create_entrance(world=world, name=f"{MENU_REGION_NAME} -> {METAL_OVERLORD_REGION_NAME}", source=MENU_REGION_NAME, target=METAL_OVERLORD_REGION_NAME, rule=can_goal_rule())


def create_entrances_for_team(world: SonicHeroesWorldBase, team: Team) -> None:
    create_entrances_for_team_stage(world=world, team=team, stage=Stage.SEASIDE_HILL)
    pass


def create_entrances_for_team_stage(world: SonicHeroesWorldBase, team: Team, stage: Stage) -> None:
    for checkpoint in range(stage.checkpoints[team] + 1):
        target_region: str = f"{stage.stage_name} {team.value} Start" if checkpoint == 0 else f"{stage.stage_name} {team.value} Checkpoint {checkpoint}"
        create_entrance(world=world, name=f"{MENU_REGION_NAME} -> {target_region}", source=MENU_REGION_NAME, target=target_region, rule=Has(item_name=get_spawn_position_item_name(team=team, stage=stage, checkpoint=checkpoint)))

    # TODO check if OBJ Sanity exists (or force it to always)
    create_entrance(world=world, name=f"{MENU_REGION_NAME} -> {stage.stage_name} {team.value} {OBJ_SANITY}", source=MENU_REGION_NAME, target=f"{stage.stage_name} {team.value} {OBJ_SANITY}", rule=True_[SonicHeroesWorldBase]())

    for connection in parser_connection_mapping[stage][team]:
        create_entrance(world=world, name=connection.name, source=connection.source_region, target=connection.target_region, rule=connection.rule)











