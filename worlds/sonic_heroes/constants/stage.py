"""
Constants related to Stages
"""
from __future__ import annotations
import dataclasses
import enum
from typing import override, TYPE_CHECKING

from .char_ability import Team

if TYPE_CHECKING:
    from .loc_region import SonicHeroesConnectionData, SonicHeroesRegionData


class Act(enum.StrEnum):
    ACT_1 = "Act 1"
    ACT_2 = "Act 2"

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


# level/stage
class Stage(enum.Enum):
    # TEST_LEVEL = "Test Level"
    SEASIDE_HILL = \
        (
            "Seaside Hill",
            StageType.NORMAL_STAGE,
            StageRegion.OCEAN_REGION,
            {
                # bonus keys
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 2,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0
            },
            {
                #checkpoints
                Team.ANY_TEAM: 0,
                Team.SONIC: 5,
                Team.DARK: 4,
                Team.ROSE: 2,
                Team.CHAOTIX: 4,
                Team.SUPER_HARD_MODE: 4
            },
            {
                # chaotix objsanity checks
                Act.ACT_1: 5,
                Act.ACT_2: 10,
            },
            {
                # chaotix objsanity str
                Act.ACT_1: "Hermit Crabs Collected",
                Act.ACT_2: "Hermit Crabs Collected",
            },
            "SH"
        )
    OCEAN_PALACE = \
        (
            "Ocean Palace",
            StageType.NORMAL_STAGE,
            StageRegion.OCEAN_REGION,
            {
                # bonus keys
                Team.ANY_TEAM: 0,
                Team.SONIC: 3,
                Team.DARK: 3,
                Team.ROSE: 3,
                Team.CHAOTIX: 3,
                Team.SUPER_HARD_MODE: 0
            },
            {
                # checkpoints
                Team.ANY_TEAM: 0,
                Team.SONIC: 4,
                Team.DARK: 5,
                Team.ROSE: 2,
                Team.CHAOTIX: 2,
                Team.SUPER_HARD_MODE: 5
            },
            {
                # chaotix objsanity checks
                Act.ACT_1: 0,
                Act.ACT_2: 0,
            },
            {
                # chaotix objsanity str
                Act.ACT_1: "",
                Act.ACT_2: "",
            },
            "OP"
        )

    SEASIDE_HILL_BONUS_STAGE = \
        (
            "Seaside Hill Bonus Stage",
            StageType.BONUS_STAGE,
            StageRegion.SPECIAL_STAGE_REGION,
            {
                # bonus keys
                team: 0 for team in Team
            },
            {
                # checkpoints
                team: 0 for team in Team
            },
            {
                # chaotix objsanity checks
                Act.ACT_1: 0,
                Act.ACT_2: 0,
            },
            {
                # chaotix objsanity str
                Act.ACT_1: "",
                Act.ACT_2: "",
            },
        )

    def __init__(self, stage_name: str, stage_type: StageType, region: StageRegion, bonus_keys: dict[Team, int], checkpoints: dict[Team, int], chaotix_obj_sanity_checks: dict[Act, int], chaotix_obj_sanity_str: dict[Act, str], rule_shorthand: str = "NA") -> None:
        self.stage_name: str = stage_name
        self.stage_type: StageType = stage_type
        self.region: StageRegion = region
        self.bonus_keys: dict[Team, int] = bonus_keys
        self.checkpoints: dict[Team, int] = checkpoints
        self.chaotix_obj_sanity_checks: dict[Act, int] = chaotix_obj_sanity_checks
        self.chaotix_obj_sanity_str: dict[Act, str] = chaotix_obj_sanity_str
        self.rule_shorthand: str = rule_shorthand


    @override
    def __str__(self) -> str:
        return self.stage_name

    @override
    def __repr__(self) -> str:
        return self.stage_name




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

