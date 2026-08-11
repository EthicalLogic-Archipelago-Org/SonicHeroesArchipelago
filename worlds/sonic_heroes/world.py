"""
The World
"""
from typing import override, ClassVar, Any

from BaseClasses import CollectionState, Item, ItemClassification, MultiWorld, Region
from rule_builder.rules import Has


from .helper_functions import get_playable_char_item_name, get_stage_obj_item_name, \
    get_spawn_position_item_name
from .items import create_items, create_precollected_items
from .regions import create_regions, create_entrances

from .item_generation import FULL_ITEM_GROUPS, FULL_ITEM_LIST
from .location_generation import FULL_LOCATION_DICT, FULL_LOCATION_GROUPS

from .constants.apworld import SONIC_HEROES, VICTORY_ITEM
from .constants.char_ability import Team, Character
from .constants.items_events import SonicHeroesItemData
from .constants.loc_region import MENU_REGION_NAME, LocationType, SonicHeroesLocationData
from .constants.stage import Act, EnabledTeamActs, Stage
from .constants.stage_objs import StageObj
from .ut.ut_world import SonicHeroesUTWorld


class SonicHeroesWorld(SonicHeroesUTWorld):
    """
    Sonic Heroes is a great game with no issues. The PC port is a great port of the first Sonic Game to release on multiple consoles (from the start).
    """
    game: ClassVar[str] = SONIC_HEROES
    item_name_groups: ClassVar[dict[str, set[str]]] = FULL_ITEM_GROUPS
    location_name_groups: ClassVar[dict[str, set[str]]] = FULL_LOCATION_GROUPS
    item_name_to_id: ClassVar[dict[str, int]] = {item_data.item_name: item_data.code for item_data in FULL_ITEM_LIST}
    location_name_to_id: ClassVar[dict[str, int]] = {location_data.name: location_data.code for stage, team_location_dict in FULL_LOCATION_DICT.items() for team, location_list in team_location_dict.items() for location_data in location_list}

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)
        self.apworld_version: str = "2.2.0"


    @override
    def create_item(self, name: str) -> Item:
        temp_items: list[SonicHeroesItemData] = [item_data for item_data in FULL_ITEM_LIST if item_data.item_name == name]
        if len(temp_items) == 0:
            return Item(name=name, classification=ItemClassification.progression, code=None, player=self.player)
        return Item(name=name, classification=temp_items[0].classification, code=self.item_name_to_id[name], player=self.player)


    @override
    def get_filler_item_name(self) -> str:
        filler_items: list[SonicHeroesItemData] = [item_data for item_data in FULL_ITEM_LIST if item_data.classification is ItemClassification.filler] # or ItemClassification.trap in item_data.classification]
        return self.random.choice(seq=filler_items).item_name


    @override
    def generate_early(self) -> None:
        #do early gen stuff here
        super().generate_early()
        #UT

        # check options

        # handle options
        # self.enabled_team_acts_flag |= EnabledTeamActs.DARK_ACT_A  # pyright: ignore[reportUnannotatedClassAttribute]
        self.enabled_team_acts_flag |= EnabledTeamActs.DARK_ACT_B  # pyright: ignore[reportUnannotatedClassAttribute]
        self.enabled_sanity_acts[Team.DARK] = {loc_type: Act.ACT_B for loc_type in LocationType.get_sanity_types()}
        # self.enabled_sanity_acts[Team.DARK][LocationType.OBJ_SANITY] = Act.NONE
        self.enabled_sanity_acts[Team.DARK][LocationType.RING_SANITY_GROUP] = Act.NONE
        # self.enabled_sanity_acts[Team.DARK][LocationType.ENEMY_SANITY] = Act.NONE

        self.starting_inventory_amounts[get_playable_char_item_name(character=Character.OMEGA)] = 1
        self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.CHECKPOINT)] = 1
        self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.RINGS)] = 1
        # self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.RINGS)] = 1
        self.starting_inventory_amounts[get_spawn_position_item_name(team=Team.DARK, stage=Stage.SEASIDE_HILL, checkpoint=1)] = 1


        #level gates here (not needed)


    @override
    def create_regions(self) -> None:
        #create all regions (and all locations as well)
        create_regions(world=self)
        pass

    @override
    def create_items(self) -> None:
        # do precollected here
        create_precollected_items(world=self)

        # create items here
        create_items(world=self)
        pass

    @override
    def set_rules(self) -> None:
        self.set_completion_rule(rule=Has(item_name=VICTORY_ITEM))
        pass

    @override
    def connect_entrances(self) -> None:
        #entrances must be done after this
        create_entrances(world=self)
        pass

    @override
    def generate_basic(self) -> None:
        #should not be needed here
        return super().generate_basic()

    @override
    def pre_fill(self) -> None:
        # should not be needed here
        # self.make_puml()
        pass

    # @override
    # def fill_hook(self, progitempool: list[Item], usefulitempool: list[Item], filleritempool: list[Item], fill_locations: list[Location]) -> None:
    #     # should not be needed here
    #     pass

    @override
    def post_fill(self) -> None:
        # if self.should_make_puml_earlier:
        # self.make_puml()
        pass

    # @override
    # def generate_output(self, output_directory: str) -> None:
    #     pass
    #
    # @override
    # def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
    #     # Location: "Hint"
    #     pass

    @override
    def fill_slot_data(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        self.make_puml()
        return \
        {
            "options": self.options.as_dict("progressive_ability_items", "ring_sanity_dark", "difficulty", "badnik_bounce", "collis_abuse", "hover_frame", "parkour", "fly_deplete_boost", "fly_ground_bounce"),

            "APWorldVersion": self.apworld_version,
            "UnlockType": 0,
            "AbilityUnlocks": 1,
            "LegacyNumberOfLevelGates": 0,
            "LegacyLevelGatesAllowedBosses": [],
            "RequiredRank": 0,

            "FinalBoss": 2,
            "GoalUnlockConditions": ["Emeralds"],
            "GoalLevelCompletions": 0,
            "GoalLevelCompletionsPerStory": 0,

            "GateEmblemCosts": [0],
            "ShuffledLevels": [f"D{x}" for x in range(2, 16)],
            "ShuffledBosses": ["B23"],
            "GateLevelCounts": [14],

            "ActsAndSanities":
            {
                "EnabledActs": self.enabled_team_acts_flag.value,
                "SanityData":
                {
                    team.value.replace(" ", ""):
                    {
                        sanity_type.type_name: act.get_slot_data_int()
                        for sanity_type, act in self.enabled_sanity_acts[team].items()
                    }
                    for team in Team if team is not Team.ANY_TEAM
                },
            },

            "DarkSanity": 1,
            "RoseSanity": 0,
            "ChaotixSanity": 0,
        }

    # @override
    # def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
    #     # print(self.item_name_groups)
    #     # print(self.location_name_groups)
    #     pass
    #
    # @override
    # def write_spoiler(self, spoiler_handle: TextIO) -> None:
    #     pass
    #
    # @override
    # def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
    #     pass



    def make_puml(self) -> None:
        if self.player_name[0:1].isdigit():
            return
        print(f"Making PUML for {self.player_name} here")
        from Utils import visualize_regions
        state: CollectionState = self.multiworld.get_all_state()
        state.update_reachable_regions(self.player)
        reachable_regions: set[Region] = set(state.reachable_regions[self.player])
        unreachable_regions: set[Region] = set()  # type: ignore
        for region in self.multiworld.regions:
            if region not in reachable_regions:
                unreachable_regions.add(region)
        visualize_regions(root_region=self.get_region(region_name=MENU_REGION_NAME), file_name=f"{self.player_name}_world.puml", show_entrance_names=True, regions_to_highlight=unreachable_regions)

        # !pragma layout smetana
        # put this at top to display PUML (after start UML)






