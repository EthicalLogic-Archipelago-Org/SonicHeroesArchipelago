"""
Options for Sonic Heroes AP
"""
import dataclasses
from typing import ClassVar

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle, Visibility, OptionError


class SonicHeroesToggle(Toggle):
    """
    Stuff
    """
    display_name: str = "Sonic Heroes Toggle"

    @classmethod
    def handle_logic_trick_explain(cls, expected_value: int = Toggle.option_true) -> str:
        return cls.display_name


class SonicHeroesDefaultOnToggle(SonicHeroesToggle):
    """
    Stuff
    """
    default: ClassVar[int] = Toggle.option_true


class SonicHeroesEnabledActsChoice(Choice):
    """
    Placeholder Docstring
    """
    display_name: str = "Placeholder"
    act_a: int = 1
    act_b: int = 2

    option_disabled: int = 0
    option_act_a: int = act_a
    option_act_b: int = act_b
    option_both_acts: int = option_act_a + option_act_b
    default: ClassVar[int] = option_disabled

    def is_act_a_enabled(self) -> bool:
        return self.value & self.act_a == self.act_a

    def is_act_b_enabled(self) -> bool:
        return self.value & self.act_b == self.act_b


class SonicHeroesSanityChoice(Choice):
    """
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Placeholder"
    disabled: int = 0
    group: int = 1
    full: int = 2

    # Options are defined per child class to allow for differences in which options are allowed

    # option_disabled: int = 0
    # option_groups: int = group
    # option_full: int = full
    # option_both_groups_and_full: int = group + full
    # default: ClassVar[int] = option_disabled


    def is_group_enabled(self) -> bool:
        return self.value & self.group == self.group

    def is_full_enabled(self) -> bool:
        return self.value & self.full == self.full



class MakePuml(SonicHeroesToggle):
    """
    Should This APWorld Make a Puml File?
    """
    display_name: str = "Make Puml"
    visibility: Visibility = Visibility.none


class JumpRando(SonicHeroesToggle):
    """
    Should the ability to Jump be an item?
    This is per team.
    """
    display_name: str = "Jump Rando"


class StageObjRando(Choice):
    """
    Should Stage Objects (like Springs, Cannons, and Dash Ramps) be items?
    """
    display_name: str = "Stage Object Rando"

    option_disabled: int = 0
    option_: int = 1
    option_full: int = 2
    default: ClassVar[int] = option_disabled



class TeamRosterRando(Choice):
    """
    Should the rosters of each team be randomized?
    This will still result in 1 character of each formation for each team.
    Note: Team Blast will be permanently disabled when The Full Random Teams option is selected as certain combinations of characters will cause a crash on Team Blast.
    """
    display_name: str = "Team Roster Rando"
    visibility: Visibility = Visibility.none
    option_disabled: int = 0
    option_only_compatible_teams: int = 1
    option_full_random_teams: int = 2



class ProgressiveAbilityItems(SonicHeroesDefaultOnToggle):
    """
    Replace some (but not all) ability items with a progressive ability item
    Homing -> Triangle Jump
    Tornado -> Invisible
    Thundershoot -> Flight (Dummy Rings and Cheese Cannon)
    Power Attack -> Combo Finisher
    """
    display_name: str = "Progressive Ability Items"
    visibility: Visibility = Visibility.none


class BothSanityLocationSets(SonicHeroesToggle):
    """
    Should Sanity Locations be generated for each Act instead of only 1 set for that team?
    THIS WILL FORCE BOTH ACTS TO BE ENABLED FOR ALL ENABLED TEAMS.
    This will result in 2 sets of sanity locations if Both Acts are enabled for a team.
    """
    display_name: str = "Both Sanity Location Sets"



class EnabledActsDark(SonicHeroesEnabledActsChoice):
    """
    Which Team Dark Acts should be enabled?
    """
    display_name: str = "Enabled Acts For Team Dark"


class StartingCharacterDark(Choice):
    """
    Which Character should Team Dark start with?
    """
    display_name: str = "Starting Character For Team Dark"

    option_shadow: int = 0
    option_rouge: int = 1
    option_omega: int = 2
    default: ClassVar[str] = "random"




# Team Dark Sanity
class ObjSanityDark(Toggle):
    """
    Should Obj Sanity be enabled for Team Dark?
    This requires Act B to be enabled.
    """
    display_name: str = "Team Dark Obj Sanity"



class RingSanityDark(SonicHeroesSanityChoice):
    """
    How should Ring Sanity for Dark be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Ring Sanity Dark"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups


class HintRingSanityDark(SonicHeroesSanityChoice):
    """
    How should Hint Ring Sanity for Dark be handled?
    """
    display_name: str = "Hint Ring Sanity Dark"

    # option_disabled: int = SonicHeroesSanityChoice.disabled
    # option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    # option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_full


class ItemBoxBalloonSanityDark(SonicHeroesSanityChoice):
    """
    How should Item Box and Balloon Sanity for Dark be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Item Box and Balloon Sanity Dark"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups


class EnemySanityDark(SonicHeroesSanityChoice):
    """
    How should Enemy Sanity for Dark be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Enemy Sanity Dark"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups
    
    







class EnabledActsChaotix(SonicHeroesEnabledActsChoice):
    """
    Which Team Chaotix Acts should be enabled?
    """
    display_name: str = "Enabled Acts For Team Chaotix"


class StartingCharacterChaotix(Choice):
    """
    Which Character should Team Chaotix start with?
    """
    display_name: str = "Starting Character For Team Chaotix"

    option_espio: int = 0
    option_charmy: int = 1
    option_vector: int = 2
    default: ClassVar[str] = "random"




# Team Chaotix Sanity
class ObjSanityChaotix(Toggle):
    """
    Should Obj Sanity be enabled for Team Chaotix?
    """
    display_name: str = "Team Chaotix Obj Sanity"



class RingSanityChaotix(SonicHeroesSanityChoice):
    """
    How should Ring Sanity for Chaotix be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Ring Sanity Chaotix"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups


class HintRingSanityChaotix(SonicHeroesSanityChoice):
    """
    How should Hint Ring Sanity for Chaotix be handled?
    """
    display_name: str = "Hint Ring Sanity Chaotix"

    # option_disabled: int = SonicHeroesSanityChoice.disabled
    # option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    # option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_full


class ItemBoxBalloonSanityChaotix(SonicHeroesSanityChoice):
    """
    How should Item Box and Balloon Sanity for Chaotix be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Item Box and Balloon Sanity Chaotix"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups


class EnemySanityChaotix(SonicHeroesSanityChoice):
    """
    How should Enemy Sanity for Chaotix be handled?
    Groups is an easier option with only 1 location per "group of checks"
    Full is a location for each (this can be excessive with rings)
    Both is both
    """
    display_name: str = "Enemy Sanity Chaotix"
    # option_disabled: int = SonicHeroesSanityChoice.disabled
    option_groups: int = SonicHeroesSanityChoice.group
    option_full: int = SonicHeroesSanityChoice.full
    option_both_groups_and_full: int = option_groups + option_full
    default: ClassVar[int] = option_groups






class Difficulty(Choice):
    """
    Should various tricks be enabled based on difficulty?
    There are currently not a lot right now (mostly a placeholder)
    """
    display_name: str = "Difficulty"
    option_none: int = 0
    option_medium: int = 1
    default: ClassVar[int] = option_none

    @classmethod
    def handle_logic_trick_explain(cls, expected_value: int) -> str:
        match expected_value:
            case cls.option_none:
                return f"Base Difficulty"
            case cls.option_medium:
                return f"Medium Difficulty"
            case _:
                raise ValueError(f"Invalid expected value for handle logic trick explain")

    # OutofLogic[Difficulty >= 1]
    # Medium Difficulty


class BadnikBounce(SonicHeroesToggle):
    """
    Should Badnik Bounce trick be enabled logically?
    This involves jumping into enemies in order to gain extra height
    THIS WILL FORCE ENABLE HOVER FRAME (jump level) IF DISABLED
    """
    display_name: str = "Badnik Bounce"


class CollisAbuse(SonicHeroesToggle):
    """
    Should Collision Abuse trick be enabled logically?
    This refers to jumping into slanted walls and collision to gain extra height
    """
    display_name: str = "Collision Abuse"


class HoverFrame(Choice):
    """
    Should Hover Frames be enabled logically?
    Holding the jump button allows for a certain amount of "Hover Frames"
    Combining this with homing attack or tornado allows for extra height and distance
    """
    display_name: str = "Hover Frame"
    option_disabled: int = 0
    option_jump_hover: int = 1
    option_jump_and_homing_or_tornado_hover: int = 2
    default: ClassVar[int] = option_disabled

    @classmethod
    def handle_logic_trick_explain(cls, expected_value: int) -> str:
        match expected_value:
            case cls.option_disabled:
                return f"Hover Frame Disabled"
            case cls.option_jump_hover:
                return f"Jump Hover Frame"
            case cls.option_jump_and_homing_or_tornado_hover:
                return f"Jump and Homing/Tornado Hover Frame"
            case _:
                raise ValueError(f"Invalid expected value for handle logic trick explain")



class Parkour(SonicHeroesToggle):
    """
    Should Parkour be enabled logically?
    Parkour involves tricky collision like staying on the small "guardrails" on either side of the path on Seaside Hill
    """
    display_name: str = "Parkour"



class FlyDepleteBoost(SonicHeroesToggle):
    """
    Should the Fly Deplete Boost trick be enabled logically?
    Gaining height exactly when the fly meter completely fills allows for going above the height cap
    """
    display_name: str = "Fly Deplete Boost"



class FlyGroundBounce(Choice):
    """
    Should the FlyGroundBounce trick be enabled logically?
    Time the flight button on the frame when hitting the ground to get a bunch of height before starting flight
    It is possible but harder to do without jump (hence the separate option)
    """
    display_name: str = "Fly Ground Bounce"
    option_disabled: int = 0
    option_with_jump: int = 1
    option_without_jump: int = 2
    default: ClassVar[int] = option_disabled

    @classmethod
    def handle_logic_trick_explain(cls, expected_value: int) -> str:
        match expected_value:
            case cls.option_disabled:
                return f"Fly Ground Bounce Disabled"
            case cls.option_with_jump:
                return f"Fly Ground Bounce With Jump"
            case cls.option_without_jump:
                return f"Fly Ground Bounce Without Jump"
            case _:
                raise ValueError(f"Invalid expected value for handle logic trick explain")



class HammerHoverReset(SonicHeroesToggle):
    """
    Should the Hammer Hover trick be enabled logically?
    Amy's Hammer Hover can be done twice by Tornado'ing while holding the Jump button.
    """
    display_name: str = "Hammer Hover Reset"


class BellyFlopChain(SonicHeroesToggle):
    """
    Should the Belly Flop Chain trick be enabled logically?
    Belly Flop Chaining allows you to preserve Belly Flops when you dont have Jump.
    """
    display_name: str = "Belly Flop Chain"






sonic_heroes_option_groups: list[OptionGroup] = \
[
    OptionGroup(name="Meta",
                options = \
                [
                    JumpRando,
                    StageObjRando,
                    TeamRosterRando,
                    ProgressiveAbilityItems,
                    BothSanityLocationSets,
                ]),

    OptionGroup(name="Team Dark",
                options = \
                [
                    EnabledActsDark,
                    StartingCharacterDark
                ]),

    OptionGroup(name="Team Dark Sanity",
                options = \
                [
                    ObjSanityDark,
                    RingSanityDark,
                    HintRingSanityDark,
                    ItemBoxBalloonSanityDark,
                    EnemySanityDark,
                ]),

    OptionGroup(name="Team Chaotix",
                options = \
                [
                    EnabledActsChaotix,
                    StartingCharacterChaotix
                ]),

    OptionGroup(name="Team Chaotix Sanity",
                options = \
                [
                    ObjSanityChaotix,
                    RingSanityChaotix,
                    HintRingSanityChaotix,
                    ItemBoxBalloonSanityChaotix,
                    EnemySanityChaotix,
                ]),



    OptionGroup(name="Tricks",
                options = \
                [
                    Difficulty,
                    BadnikBounce,
                    CollisAbuse,
                    HoverFrame,
                    Parkour,
                    FlyDepleteBoost,
                    FlyGroundBounce,
                    HammerHoverReset,
                    BellyFlopChain,
                ]),
    OptionGroup(name="Hidden",
                options = \
                [
                    MakePuml,
                ]),
]

@dataclasses.dataclass
class SonicHeroesOptions(PerGameCommonOptions):
    make_puml: MakePuml
    jump_rando: JumpRando
    stage_obj_rando: StageObjRando
    team_roster_rando: TeamRosterRando
    progressive_ability_items: ProgressiveAbilityItems


    both_sanity_location_sets: BothSanityLocationSets

    enabled_acts_dark: EnabledActsDark
    starting_character_dark: StartingCharacterDark

    obj_sanity_dark: ObjSanityDark
    ring_sanity_dark: RingSanityDark
    hint_ring_sanity_dark: HintRingSanityDark
    item_box_balloon_sanity_dark: ItemBoxBalloonSanityDark
    enemy_sanity_dark: EnemySanityDark

    enabled_acts_chaotix: EnabledActsChaotix
    starting_character_chaotix: StartingCharacterChaotix

    obj_sanity_chaotix: ObjSanityChaotix
    ring_sanity_chaotix: RingSanityChaotix
    hint_ring_sanity_chaotix: HintRingSanityChaotix
    item_box_balloon_sanity_chaotix: ItemBoxBalloonSanityChaotix
    enemy_sanity_chaotix: EnemySanityChaotix


    difficulty: Difficulty
    badnik_bounce: BadnikBounce
    collis_abuse: CollisAbuse
    hover_frame: HoverFrame
    parkour: Parkour
    fly_deplete_boost: FlyDepleteBoost
    fly_ground_bounce: FlyGroundBounce
    hammer_hover_reset: HammerHoverReset
    belly_flop_chain: BellyFlopChain


OPTION_ATTR_NAMES: list[str] = \
[
    "jump_rando",
    "stage_obj_rando",
    "team_roster_rando",
    "progressive_ability_items",


    "both_sanity_location_sets",

    "enabled_acts_dark",
    "starting_character_dark",

    "obj_sanity_dark",
    "ring_sanity_dark",
    "hint_ring_sanity_dark",
    "item_box_balloon_sanity_dark",
    "enemy_sanity_dark",


    "enabled_acts_chaotix",
    "starting_character_chaotix",

    "obj_sanity_chaotix",
    "ring_sanity_chaotix",
    "hint_ring_sanity_chaotix",
    "item_box_balloon_sanity_chaotix",
    "enemy_sanity_chaotix",

    "difficulty",
    "badnik_bounce",
    "collis_abuse",
    "hover_frame",
    "parkour",
    "fly_deplete_boost",
    "fly_ground_bounce",
    "hammer_hover_reset",
    "belly_flop_chain",
]



def check_options(options: SonicHeroesOptions) -> None:
    if options.badnik_bounce == BadnikBounce.option_true and options.hover_frame == HoverFrame.option_disabled:
        raise OptionError(f"Badnik Bounce requires hover frames to be enabled")


