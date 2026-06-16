"""
Locations
"""
from BaseClasses import Location, Region


from .constants.char_ability import Team
from .constants.items_events import OBJ_SANITY
from .constants.loc_region import SonicHeroesLocationData, LocationType
from .constants.stage import Stage, Act

from .helper_functions import is_this_act_enabled
from .location_generation import FULL_LOCATION_DICT

from .world_base import SonicHeroesWorldBase





def get_locations_for_region(world: SonicHeroesWorldBase, team: Team, stage: Stage, region_name: str) -> list[SonicHeroesLocationData]:
    _result: list[SonicHeroesLocationData] = []
    for loc_data in FULL_LOCATION_DICT[stage][team]:
        if loc_data.parent_region != region_name:
            continue
        if loc_data.is_enabled(world=world):
            _result.append(loc_data)
    return _result


def append_locations_to_region(world: SonicHeroesWorldBase, team: Team, stage: Stage, region: Region) -> None:
    for loc_data in get_locations_for_region(world=world, team=team, stage=stage, region_name=region.name):
        loc_id: int | None = None if loc_data.code < 1 else loc_data.code
        location: Location = Location(name=loc_data.name, address=loc_id, parent=region, player=world.player)
        if loc_data.locked_item != "":
            location.place_locked_item(item=world.create_item(name=loc_data.locked_item))
        world.set_rule(spot=location, rule=loc_data.rule)
        region.locations.append(location)











