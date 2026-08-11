"""
Constants related to Stages
"""
from __future__ import annotations
import dataclasses
import enum
from typing import override, TYPE_CHECKING, Self
from unittest import case

from .char_ability import Team

if TYPE_CHECKING:
    from .loc_region import SonicHeroesConnectionData, SonicHeroesRegionData


class EnabledTeamActs(enum.IntFlag):
    NONE = 0
    SONIC_ACT_A = 1 << 0
    SONIC_ACT_B = 1 << 1
    DARK_ACT_A = 1 << 2
    DARK_ACT_B = 1 << 3
    ROSE_ACT_A = 1 << 4
    ROSE_ACT_B = 1 << 5
    CHAOTIX_ACT_A = 1 << 6
    CHAOTIX_ACT_B = 1 << 7
    SUPER_HARD_MODE = 1 << 8


class Act(enum.IntFlag):
    NONE = 0
    ACT_A = 1
    ACT_B = 2
    BOTH_ACTS = ACT_A | ACT_B


    def get_act_str(self) -> str:
        if self is Act.BOTH_ACTS:
            return "Both Acts"
        if self is Act.ACT_A:
            return "Act A"
        if self is Act.ACT_B:
            return "Act B"
        return "No Acts"


    def is_an_act_enabled(self) -> bool:
        return self is not Act.NONE

    def get_slot_data_int(self) -> int:
        match self:
            case Act.BOTH_ACTS:
                return 2
            case Act.ACT_A | Act.ACT_B:
                return 1
            case Act.NONE:
                return 0
        return 0


class StageRegion(enum.StrEnum):
    ALL_REGIONS = "All Regions"
    OCEAN_REGION = "Ocean Region"
    HOT_PLANT_REGION = "HotPlant Region"
    CASINO_REGION = "Casino Region"
    TRAIN_REGION = "Train Region"
    BIG_PLANT_REGION = "BigPlant Region"
    GHOST_REGION = "Ghost Region"
    SKY_REGION = "Sky Region"
    SPECIAL_STAGE_REGION = "Special Stage Region"
    BOSS_REGION = "Boss Region"
    FINAL_BOSS_REGION = "Final Boss Region"


class StageType(enum.StrEnum):
    TEST_STAGE = "Test Stage"
    NORMAL_STAGE = "Normal Stage"
    BOSS_STAGE = "Boss Stage"
    FINAL_BOSS_STAGE = "Final Boss Stage"
    BONUS_STAGE = "Bonus Stage"
    EMERALD_STAGE = BONUS_STAGE

    MULTIPLAYER_BOBSLED_STAGE = "Multiplayer Bobsled Stage"
    MULTIPLAYER_ACTION_RACE = "Multiplayer Action Race"
    MULTIPLAYER_BATTLE = "Multiplayer Battle"
    MULTIPLAYER_RING_RACE = "Multiplayer Ring Race"
    MULTIPLAYER_QUICK_RACE = "Multiplayer Quick Race"
    MULTIPLAYER_EXPERT_RACE = "Multiplayer Expert Race"
    MULTIPLAYER_SPECIAL_STAGE = "Multiplayer Special Stage"


@dataclasses.dataclass(frozen=True, kw_only=True)
class _StageData:
    stage_name: str
    stage_type: StageType = StageType.TEST_STAGE
    region: StageRegion = StageRegion.ALL_REGIONS
    sort_key: str
    bonus_keys: dict[Team, int] = dataclasses.field(default_factory=lambda: {team: 0 for team in Team})
    checkpoints: dict[Team, int] = dataclasses.field(default_factory=lambda: {team: 0 for team in Team})
    chaotix_obj_sanity_checks: dict[Act, int] = dataclasses.field(default_factory=lambda: {act: 0 for act in [Act.ACT_A, Act.ACT_B]})
    chaotix_obj_sanity_str: dict[Act, str] = dataclasses.field(default_factory=lambda: {act: "NoChaotixSanityChecks" for act in [Act.ACT_A, Act.ACT_B]})
    rule_shorthand: str = "NoShorthand"


class Stage(enum.Enum):
    TEST_LEVEL = _StageData \
    (
        stage_name="TEST_LEVEL",
        sort_key="99",
    )
    SEASIDE_HILL = _StageData \
    (
        stage_name="Seaside Hill",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.OCEAN_REGION,
        sort_key="00",
        bonus_keys=\
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 2,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints=\
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 5,
                Team.DARK: 4,
                Team.ROSE: 2,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 4,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 10,
                Act.ACT_B: 20,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Hermit Crabs Collected",
                Act.ACT_B: "Hermit Crabs Collected",
            },
        rule_shorthand="SH"
    )
    OCEAN_PALACE = _StageData \
    (
        stage_name="Ocean Palace",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.OCEAN_REGION,
        sort_key="01",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 4,
                Team.ROSE: 2,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 5,
            },
        rule_shorthand="OP"
    )
    GRAND_METROPOLIS = _StageData \
    (
        stage_name="Grand Metropolis",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.HOT_PLANT_REGION,
        sort_key="03",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 2,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 4,
                Team.ROSE: 3,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 4,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 85,
                Act.ACT_B: 85,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Enemies Killed",
                Act.ACT_B: "Enemies Killed",
            },
        rule_shorthand="GM"
    )
    POWER_PLANT = _StageData \
    (
        stage_name="Power Plant",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.HOT_PLANT_REGION,
        sort_key="04",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 4,
                Team.ROSE: 2,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 4,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 3,
                Act.ACT_B: 5,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Gold Turtles Killed",
                Act.ACT_B: "Gold Turtles Killed",
            },
        rule_shorthand="PP"
    )
    CASINO_PARK = _StageData \
    (
        stage_name="Casino Park",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.CASINO_REGION,
        sort_key="06",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 1,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 3,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 200,
                Act.ACT_B: 500,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Rings Collected",
                Act.ACT_B: "Rings Collected",
            },
        rule_shorthand="CP"
    )
    BINGO_HIGHWAY = _StageData \
    (
        stage_name="Bingo Highway",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.CASINO_REGION,
        sort_key="07",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 4,
                Team.ROSE: 3,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 4,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 10,
                Act.ACT_B: 20,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Casino Chips Collected",
                Act.ACT_B: "Casino Chips Collected",
            },
        rule_shorthand="BH"
    )
    RAIL_CANYON = _StageData \
    (
        stage_name="Rail Canyon",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.TRAIN_REGION,
        sort_key="09",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 6,
                Team.DARK: 6,
                Team.ROSE: 4,
                Team.CHAOTIX: 5,
                Team.SUPER_HARD_MODE: 6,
            },
        rule_shorthand="RC"
    )
    BULLET_STATION = _StageData \
    (
        stage_name="Bullet Station",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.TRAIN_REGION,
        sort_key="10",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 5,
                Team.ROSE: 2,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 4,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 30,
                Act.ACT_B: 50,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Capsules Destroyed",
                Act.ACT_B: "Capsules Destroyed",
            },
        rule_shorthand="BS"
    )
    FROG_FOREST = _StageData \
    (
        stage_name="Frog Forest",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.BIG_PLANT_REGION,
        sort_key="12",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 2,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 3,
            },
        rule_shorthand="Frog"
    )
    LOST_JUNGLE = _StageData \
    (
        stage_name="Lost Jungle",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.BIG_PLANT_REGION,
        sort_key="13",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 5,
                Team.DARK: 5,
                Team.ROSE: 2,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 5,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 10,
                Act.ACT_B: 20,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Chao Saved",
                Act.ACT_B: "Chao Saved",
            },
        rule_shorthand="LJ"
    )
    HANG_CASTLE = _StageData \
    (
        stage_name="Hang Castle",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.GHOST_REGION,
        sort_key="15",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 2,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 3,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 10,
                Act.ACT_B: 10,
            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Keys Collected",
                Act.ACT_B: "Keys Collected",
            },
        rule_shorthand="HC"
    )
    MYSTIC_MANSION = _StageData \
    (
        stage_name="Mystic Mansion",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.GHOST_REGION,
        sort_key="16",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 4,
                Team.ROSE: 2,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 5,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 60,
                Act.ACT_B: 46,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Red Torches Extinguished",
                Act.ACT_B: "Blue Torches Extinguished",
            },
        rule_shorthand="MM"
    )
    EGG_FLEET = _StageData \
    (
        stage_name="Egg Fleet",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.SKY_REGION,
        sort_key="18",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 5,
                Team.DARK: 5,
                Team.ROSE: 3,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 5,
            },
        rule_shorthand="EF"
    )
    FINAL_FORTRESS = _StageData \
    (
        stage_name="Final Fortress",
        stage_type=StageType.NORMAL_STAGE,
        region=StageRegion.SKY_REGION,
        sort_key="19",
        bonus_keys= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0,
            },
        checkpoints= \
            {
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 2,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 3,
            },
        chaotix_obj_sanity_checks=\
            {
                Act.ACT_A: 5,
                Act.ACT_B: 10,

            },
        chaotix_obj_sanity_str=\
            {
                Act.ACT_A: "Keys Collected",
                Act.ACT_B: "Keys Collected",
            },
        rule_shorthand="Final"
    )
    EGG_HAWK = _StageData \
    (
        stage_name="Egg Hawk",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="02",
    )
    TEAM_FIGHT_1 = _StageData \
    (
        stage_name="Team Fight 1",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="05",
    )
    ROBOT_CARNIVAL = _StageData \
    (
        stage_name="Robot Carnival",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="08",
    )
    EGG_ALBATROSS = _StageData \
    (
        stage_name="Egg Albatross",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="11",
    )
    TEAM_FIGHT_2 = _StageData \
    (
        stage_name="Team Fight 2",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="14",
    )
    ROBOT_STORM = _StageData \
    (
        stage_name="Robot Storm",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="17",
    )
    EGG_EMPEROR = _StageData \
    (
        stage_name="Egg Emperor",
        stage_type=StageType.BOSS_STAGE,
        region=StageRegion.BOSS_REGION,
        sort_key="20",
    )
    METAL_MADNESS = _StageData \
    (
        stage_name="Metal Madness",
        stage_type=StageType.FINAL_BOSS_STAGE,
        region=StageRegion.FINAL_BOSS_REGION,
        sort_key="21",
    )
    METAL_OVERLORD = _StageData \
    (
        stage_name="Metal Overlord",
        stage_type=StageType.FINAL_BOSS_STAGE,
        region=StageRegion.FINAL_BOSS_REGION,
        sort_key="22",
    )
    SEA_GATE = _StageData \
    (
        stage_name="Sea Gate",
        stage_type=StageType.FINAL_BOSS_STAGE,
        region=StageRegion.FINAL_BOSS_REGION,
        sort_key="23",
    )

    SEASIDE_BOBSLED_COURSE = _StageData \
    (
        stage_name="Seaside Bobsled Course",
        stage_type=StageType.MULTIPLAYER_BOBSLED_STAGE,
        sort_key="24",
    )
    CITY_BOBSLED_COURSE = _StageData \
    (
        stage_name="City Bobsled Course",
        stage_type=StageType.MULTIPLAYER_BOBSLED_STAGE,
        sort_key="25",
    )
    CASINO_BOBSLED_COURSE = _StageData \
    (
        stage_name="Casino Bobsled Course",
        stage_type=StageType.MULTIPLAYER_BOBSLED_STAGE,
        sort_key="26",
    )

    SEASIDE_HILL_BONUS_STAGE = _StageData \
    (
        stage_name="Seaside Hill Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="27",
    )
    GRAND_METROPOLIS_BONUS_STAGE = _StageData \
    (
        stage_name="Grand Metropolis Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="28",
    )
    CASINO_PARK_BONUS_STAGE = _StageData \
    (
        stage_name="Casino Park Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="29",
    )
    RAIL_CANYON_BONUS_STAGE = _StageData \
    (
        stage_name="Rail Canyon Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="30",
    )
    FROG_FOREST_BONUS_STAGE = _StageData \
    (
        stage_name="Frog Forest Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="31",
    )
    HANG_CASTLE_BONUS_STAGE = _StageData \
    (
        stage_name="Hang Castle Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="32",
    )
    EGG_FLEET_BONUS_STAGE = _StageData \
    (
        stage_name="Egg Fleet Bonus Stage",
        stage_type=StageType.BONUS_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="33",
    )

    CHAOTIX_RAIL_CANYON = RAIL_CANYON # <- alias here

    SEASIDE_HILL_ACTION_RACE = _StageData \
    (
        stage_name="Seaside Hill Action Race",
        stage_type=StageType.MULTIPLAYER_ACTION_RACE,
        sort_key="34",
    )
    GRAND_METROPOLIS_ACTION_RACE = _StageData \
    (
        stage_name="Grand Metropolis Action Race",
        stage_type=StageType.MULTIPLAYER_ACTION_RACE,
        sort_key="35",
    )
    BINGO_HIGHWAY_ACTION_RACE = _StageData \
    (
        stage_name="Bingo Highway Action Race",
        stage_type=StageType.MULTIPLAYER_ACTION_RACE,
        sort_key="36",
    )

    CITY_TOP_BATTLE = _StageData \
    (
        stage_name="City Top Battle",
        stage_type=StageType.MULTIPLAYER_BATTLE,
        sort_key="37",
    )
    CASINO_RING_BATTLE = _StageData \
    (
        stage_name="Casino Ring Battle",
        stage_type=StageType.MULTIPLAYER_BATTLE,
        sort_key="38",
    )
    TURTLE_SHELL_BATTLE = _StageData \
    (
        stage_name="Turtle Shell Battle",
        stage_type=StageType.MULTIPLAYER_BATTLE,
        sort_key="39",
    )

    EGG_TREAT_RING_RACE = _StageData \
    (
        stage_name="Egg Treat Ring Race",
        stage_type=StageType.MULTIPLAYER_RING_RACE,
        sort_key="40",
    )
    PINBALL_MATCH_RING_RACE = _StageData \
    (
        stage_name="Pinball Match Ring Race",
        stage_type=StageType.MULTIPLAYER_RING_RACE,
        sort_key="41",
    )
    HOT_ELEVATOR_RING_RACE = _StageData \
    (
        stage_name="Hot Elevator Ring Race",
        stage_type=StageType.MULTIPLAYER_RING_RACE,
        sort_key="42",
    )
    ROAD_ROCK_QUICK_RACE = _StageData \
    (
        stage_name="Road Rock Quick Race",
        stage_type=StageType.MULTIPLAYER_QUICK_RACE,
        sort_key="43",
    )
    MAD_EXPRESS_QUICK_RACE = _StageData \
    (
        stage_name="Mad Express Quick Race",
        stage_type=StageType.MULTIPLAYER_QUICK_RACE,
        sort_key="44",
    )
    TERROR_HALL_QUICK_RACE = _StageData \
    (
        stage_name="Terror Hall Quick Race",
        stage_type=StageType.MULTIPLAYER_QUICK_RACE,
        sort_key="45",
    )
    RAIL_CANYON_EXPERT_RACE = _StageData \
    (
        stage_name="Rail Canyon Expert Race",
        stage_type=StageType.MULTIPLAYER_EXPERT_RACE,
        sort_key="46",
    )
    FROG_FOREST_EXPERT_RACE = _StageData \
    (
        stage_name="Frog Forest Expert Race",
        stage_type=StageType.MULTIPLAYER_EXPERT_RACE,
        sort_key="47",
    )
    EGG_FLEET_EXPERT_RACE = _StageData \
    (
        stage_name="Egg Fleet Expert Race",
        stage_type=StageType.MULTIPLAYER_EXPERT_RACE,
        sort_key="48",
    )

    OCEAN_PALACE_EMERALD_STAGE = _StageData \
    (
        stage_name="Ocean Palace Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="49",
    )
    POWER_PLANT_EMERALD_STAGE = _StageData \
    (
        stage_name="Power Plant Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="50",
    )
    BINGO_HIGHWAY_EMERALD_STAGE = _StageData \
    (
        stage_name="Bingo Highway Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="51",
    )
    BULLET_STATION_EMERALD_STAGE = _StageData \
    (
        stage_name="Bullet Station Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="52",
    )
    LOST_JUNGLE_EMERALD_STAGE = _StageData \
    (
        stage_name="Lost Jungle Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="53",
    )
    MYSTIC_MANSION_EMERALD_STAGE = _StageData \
    (
        stage_name="Mystic Mansion Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="54",
    )
    FINAL_FORTRESS_EMERALD_STAGE = _StageData \
    (
        stage_name="Final Fortress Emerald Stage",
        stage_type=StageType.EMERALD_STAGE,
        region=StageRegion.SPECIAL_STAGE_REGION,
        sort_key="55",
    )
    SPECIAL_STAGE_1_MULTIPLAYER = _StageData \
    (
        stage_name="Special Stage 1 Multiplayer",
        stage_type=StageType.MULTIPLAYER_SPECIAL_STAGE,
        sort_key="56",
    )
    SPECIAL_STAGE_2_MULTIPLAYER = _StageData \
    (
        stage_name="Special Stage 2 Multiplayer",
        stage_type=StageType.MULTIPLAYER_SPECIAL_STAGE,
        sort_key="57",
    )
    SPECIAL_STAGE_3_MULTIPLAYER = _StageData \
    (
        stage_name="Special Stage 3 Multiplayer",
        stage_type=StageType.MULTIPLAYER_SPECIAL_STAGE,
        sort_key="58",
    )

    def __new__(cls, data: _StageData) -> Self:
        obj = object.__new__(cls)
        obj._value_ = data
        return obj

    def __init__(self, data: _StageData) -> None:
        self.stage_name: str = data.stage_name
        self.stage_type: StageType = data.stage_type
        self.region: StageRegion = data.region
        self.sort_key: str = data.sort_key
        self.bonus_keys: dict[Team, int] = data.bonus_keys
        self.checkpoints: dict[Team, int] = data.checkpoints
        self.chaotix_obj_sanity_checks: dict[Act, int] = data.chaotix_obj_sanity_checks
        self.chaotix_obj_sanity_str: dict[Act, str] = data.chaotix_obj_sanity_str
        self.rule_shorthand: str = data.rule_shorthand

    @override
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}.{self.name}: \"{self.stage_name}\">"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def match_stage_name(cls, stage_name: str) -> Stage:
        for stage in cls:
            if stage.stage_name == stage_name:
                return stage
        raise ValueError(f"Stage {stage_name} is not a valid stage name")

    @classmethod
    def get_stages_of_type(cls, stage_type: StageType) -> list[Stage]:
        return [stage for stage in cls if stage.stage_type is stage_type]


    @classmethod
    def get_stage_to_bonus_stage(cls) -> dict[Stage, Stage]:
        return \
        {
            cls.SEASIDE_HILL: cls.SEASIDE_HILL_BONUS_STAGE,
            cls.OCEAN_PALACE: cls.OCEAN_PALACE_EMERALD_STAGE,
            cls.GRAND_METROPOLIS: cls.GRAND_METROPOLIS_BONUS_STAGE,
            cls.POWER_PLANT: cls.POWER_PLANT_EMERALD_STAGE,
            cls.CASINO_PARK: cls.CASINO_PARK_BONUS_STAGE,
            cls.BINGO_HIGHWAY: cls.BINGO_HIGHWAY_EMERALD_STAGE,
            cls.RAIL_CANYON: cls.RAIL_CANYON_BONUS_STAGE,
            cls.BULLET_STATION: cls.BULLET_STATION_EMERALD_STAGE,
            cls.FROG_FOREST: cls.FROG_FOREST_BONUS_STAGE,
            cls.LOST_JUNGLE: cls.LOST_JUNGLE_EMERALD_STAGE,
            cls.HANG_CASTLE: cls.HANG_CASTLE_BONUS_STAGE,
            cls.MYSTIC_MANSION: cls.MYSTIC_MANSION_EMERALD_STAGE,
            cls.EGG_FLEET: cls.EGG_FLEET_BONUS_STAGE,
            cls.FINAL_FORTRESS: cls.FINAL_FORTRESS_EMERALD_STAGE,
        }


# STAGE_TO_BONUS_STAGE: dict[Stage, Stage] = \
# {
#     Stage.SEASIDE_HILL: Stage.SEASIDE_HILL_BONUS_STAGE,
#     Stage.OCEAN_PALACE: Stage.OCEAN_PALACE_EMERALD_STAGE,
#     Stage.GRAND_METROPOLIS: Stage.GRAND_METROPOLIS_BONUS_STAGE,
#     Stage.POWER_PLANT: Stage.POWER_PLANT_EMERALD_STAGE,
#     Stage.CASINO_PARK: Stage.CASINO_PARK_BONUS_STAGE,
#     Stage.BINGO_HIGHWAY: Stage.BINGO_HIGHWAY_EMERALD_STAGE,
#     Stage.RAIL_CANYON: Stage.RAIL_CANYON_BONUS_STAGE,
#     Stage.BULLET_STATION: Stage.BULLET_STATION_EMERALD_STAGE,
#     Stage.FROG_FOREST: Stage.FROG_FOREST_BONUS_STAGE,
#     Stage.LOST_JUNGLE: Stage.LOST_JUNGLE_EMERALD_STAGE,
#     Stage.HANG_CASTLE: Stage.HANG_CASTLE_BONUS_STAGE,
#     Stage.MYSTIC_MANSION: Stage.MYSTIC_MANSION_EMERALD_STAGE,
#     Stage.EGG_FLEET: Stage.EGG_FLEET_BONUS_STAGE,
#     Stage.FINAL_FORTRESS: Stage.FINAL_FORTRESS_EMERALD_STAGE,
# }


@dataclasses.dataclass(kw_only=True)
class StageData:
    regions: list[SonicHeroesRegionData] = dataclasses.field(default_factory=list)
    connections: list[SonicHeroesConnectionData] = dataclasses.field(default_factory=list)

    def get_specific_region_data(self, name: str) -> SonicHeroesRegionData | None:
        for region in self.regions:
            if region.region_name == name:
                return region
        return None

    def get_specific_connection_data(self, name: str) -> SonicHeroesConnectionData | None:
        for connection in self.connections:
            if connection.name == name:
                return connection
        return None


@dataclasses.dataclass(init=False, kw_only=True)
class AllStageData:
    team_stage_data: dict[Team, dict[Stage, StageData]]# = dataclasses.field(default_factory=dict)

    def __init__(self) -> None:
        self.team_stage_data = \
        {team: {stage: StageData() for stage in Stage} for team in Team}


    def map_data_for_team_and_stage(self, team: Team, stage: Stage) -> None:
        # TODO get data here and add it to the map
        pass

    def get_specific_region_data_for_team_and_stage(self, team: Team, stage: Stage, name: str) -> SonicHeroesRegionData | None:
        return self.team_stage_data[team][stage].get_specific_region_data(name)

    def get_specific_connection_data_for_team_and_stage(self, team: Team, stage: Stage, name: str) -> SonicHeroesConnectionData | None:
        return self.team_stage_data[team][stage].get_specific_connection_data(name)

