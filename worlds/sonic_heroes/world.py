"""
The World
"""
from typing import override, ClassVar

from BaseClasses import MultiWorld

from .constants.apworld import SONIC_HEROES
from .ut.ut_world import SonicHeroesUTWorld


class SonicHeroesWorld(SonicHeroesUTWorld):
    game: ClassVar[str] = SONIC_HEROES
    # item_name_groups = item_name_groups
    # location_name_groups = location_name_groups
    item_name_to_id: ClassVar[dict[str, int]] = {}
    location_name_to_id: ClassVar[dict[str, int]] = {}

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)


    @override
    def generate_early(self) -> None:
        #do early gen stuff here
        super().generate_early()
        pass