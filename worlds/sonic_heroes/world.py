"""
The World
"""
from typing import override, ClassVar, Any

from BaseClasses import CollectionState, Item, ItemClassification, MultiWorld, Region
from rule_builder.rules import Has


from .helper_functions import get_playable_char_item_name, get_stage_obj_item_name, \
    get_spawn_position_item_name
from .items import create_items, create_precollected_items
from .options import *
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
        self.apworld_version: str = "99.9.9"


    @override
    def create_item(self, name: str) -> Item:
        temp_items: list[SonicHeroesItemData] = [item_data for item_data in FULL_ITEM_LIST if item_data.item_name == name]
        if len(temp_items) == 0:
            return Item(name=name, classification=ItemClassification.progression, code=None, player=self.player)
        return Item(name=name, classification=temp_items[0].classification, code=self.item_name_to_id[name], player=self.player)


    @override
    def get_filler_item_name(self) -> str:
        filler_items: list[SonicHeroesItemData] = [item_data for item_data in FULL_ITEM_LIST if item_data.classification is ItemClassification.filler and item_data.fillerweight > 0] # or ItemClassification.trap in item_data.classification]
        return self.random.choice(seq=filler_items).item_name


    @override
    def generate_early(self) -> None:
        #do early gen stuff here
        super().generate_early()
        #UT

        # check options

        # handle options
        self.handle_options_at_gen_early()


        if self.options.starting_character_dark == StartingCharacterDark.option_shadow:
            self.starting_inventory_amounts[get_playable_char_item_name(character=Character.SHADOW)] = 1
        if self.options.starting_character_dark == StartingCharacterDark.option_rouge:
            self.starting_inventory_amounts[get_playable_char_item_name(character=Character.ROUGE)] = 1
        if self.options.starting_character_dark == StartingCharacterDark.option_omega:
            self.starting_inventory_amounts[get_playable_char_item_name(character=Character.OMEGA)] = 1


        self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.CHECKPOINT)] = 1
        self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.RINGS)] = 1
        # self.starting_inventory_amounts[get_stage_obj_item_name(team=Team.DARK, stage_obj=StageObj.ITEM_BOX)] = 1
        self.starting_inventory_amounts[get_spawn_position_item_name(team=Team.DARK, stage=Stage.SEASIDE_HILL, checkpoint=3)] = 1


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
        # self.make_puml()
        return \
        {
            "options": self.options.as_dict(*OPTION_ATTR_NAMES),

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


    def force_enable_required_acts_and_sanities(self) -> None:
        if not self.options.enabled_acts_dark.is_act_a_enabled() and not self.options.enabled_acts_dark.is_act_b_enabled():
            self.options.enabled_acts_dark.value = EnabledActsDark.option_act_a

        if self.options.ring_sanity_dark == RingSanityDark.option_disabled:
            self.options.ring_sanity_dark.value = RingSanityDark.option_groups

        if self.options.hint_ring_sanity_dark == HintRingSanityDark.option_disabled:
            self.options.hint_ring_sanity_dark.value = HintRingSanityDark.option_groups

        if self.options.item_box_balloon_sanity_dark == ItemBoxBalloonSanityDark.option_disabled:
            self.options.item_box_balloon_sanity_dark.value = ItemBoxBalloonSanityDark.option_groups

        if self.options.enemy_sanity_dark == EnemySanityDark.option_disabled:
            self.options.enemy_sanity_dark.value = EnemySanityDark.option_groups


    def handle_individual_sanity_option_for_team_at_gen_early(self, team: Team, loc_type: LocationType) -> None:
        if self.options.both_sanity_location_sets:
            self.enabled_sanity_acts[team][loc_type] = Act.BOTH_ACTS
        else:
            self.enabled_sanity_acts[team][loc_type] = Act.ACT_A



    def handle_options_at_gen_early(self) -> None:
        self.force_enable_required_acts_and_sanities()

        # enabled acts
        self.enabled_team_acts_flag: EnabledTeamActs = EnabledTeamActs.NONE

        if self.options.both_sanity_location_sets:
            self.options.enabled_acts_dark.value = EnabledActsDark.option_both_acts

        if self.options.enabled_acts_dark.is_act_a_enabled():
            self.enabled_team_acts_flag |= EnabledTeamActs.DARK_ACT_A
        if self.options.enabled_acts_dark.is_act_b_enabled():
            self.enabled_team_acts_flag |= EnabledTeamActs.DARK_ACT_B


        # force checkpoint and key sanities
        self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.CHECKPOINT_SANITY)
        self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.KEY_SANITY)


        # enabled sanities
        # Obj Sanity
        if self.options.obj_sanity_dark:
            if not self.options.enabled_acts_dark.is_act_b_enabled():
                raise OptionError(f"Obj Sanity for Team Dark requires Act B to be enabled")
            self.enabled_sanity_acts[Team.DARK][LocationType.OBJ_SANITY] = Act.ACT_B

        # Ring Sanity Group
        if self.options.ring_sanity_dark.is_group_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.RING_SANITY_GROUP)

        # Ring Sanity Full
        if self.options.ring_sanity_dark.is_full_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.RING_SANITY_FULL)


        # Hint Ring Sanity Group
        if self.options.hint_ring_sanity_dark.is_group_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.HINT_RING_SANITY_GROUP)

        # Hint Ring Sanity Full
        if self.options.hint_ring_sanity_dark.is_full_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.HINT_RING_SANITY_FULL)

        # Item Box Sanity Group
        if self.options.item_box_balloon_sanity_dark.is_group_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.ITEM_BOX_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.ITEM_BALLOON_SANITY_GROUP)

        # Item Box Sanity Full
        if self.options.item_box_balloon_sanity_dark.is_full_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.ITEM_BOX_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.ITEM_BALLOON_SANITY_FULL)


        # Enemy Sanity Group
        if self.options.enemy_sanity_dark.is_group_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_FLAPPER_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_PAWN_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.KLAGEN_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.FALCO_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_HAMMER_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.CAMERON_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.RHINO_LINER_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_BISHOP_SANITY_GROUP)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.E2000_SANITY_GROUP)


        # Enemy Sanity Full
        if self.options.enemy_sanity_dark.is_full_enabled():
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_FLAPPER_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_PAWN_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.KLAGEN_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.FALCO_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_HAMMER_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.CAMERON_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.RHINO_LINER_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.EGG_BISHOP_SANITY_FULL)
            self.handle_individual_sanity_option_for_team_at_gen_early(team=Team.DARK, loc_type=LocationType.E2000_SANITY_FULL)






