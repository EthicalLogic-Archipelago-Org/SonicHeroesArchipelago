"""
Helper Functions used by APWorld
"""
from unittest import case

from rule_builder.rules import Rule, True_

from .constants.apworld import RULE_CACHING_ENABLED_ATTR
from .constants.items_events import OBJ_SANITY_EVENT_ITEM, PLAYABLE, SPAWN_POSITION
from .constants.char_ability import Ability, Character, Team
from .constants.stage import EnabledTeamActs, Stage, Act
from .constants.stage_objs import StageObj
from .world_base import SonicHeroesWorldBase

def get_correct_ability_item_name(world: SonicHeroesWorldBase, team: Team, ability: Ability) -> str:
    """Gets the correct ability item name from the Character"""
    return f"{team} {ability.ability_name}"

def get_stage_obj_item_name(team: Team, stage_obj: StageObj) -> str:
    """Gets the correct stage item name from the Stage Object"""
    return f"{team.value} {stage_obj.value}" if team is not Team.ANY_TEAM else stage_obj.value


def get_playable_char_item_name(character: Character) -> str:  # (world: SonicHeroesWorldBase, character: Character) -> str:
    """Gets the playable character item name from the Character"""
    return f"{PLAYABLE} {character.char_name}"

def get_spawn_position_item_name(team: Team, stage: Stage, checkpoint: int) -> str:
    return f"{stage.stage_name} {team.value} Checkpoint {checkpoint} {SPAWN_POSITION}" if checkpoint > 0 else f"{stage.stage_name} {team.value} Start of Level {SPAWN_POSITION}"

def get_all_characters_for_team(world: SonicHeroesWorldBase, team: Team) -> list[Character]:
    """Gets all characters for the Team"""
    return [Character.SHADOW, Character.ROUGE, Character.OMEGA]


def get_abilities_for_char(world: SonicHeroesWorldBase, character: Character) -> list[Ability]:
    """
    Gets all leveling relevant abilities for the character (Does NOT include JUMP)
    """
    return character.get_abilities(world=world)


def get_abilities_for_team(world: SonicHeroesWorldBase, team: Team) -> list[Ability]:
    """
    Gets all leveling relevant abilities for the Team (Does NOT include JUMP)
    """
    return [ability for char in get_all_characters_for_team(world=world, team=team) for ability in get_abilities_for_char(world=world, character=char)]


def get_all_ability_items_for_team_and_stage(world: SonicHeroesWorldBase, team: Team, stage: Stage) -> list[str]:
    """Gets all leveling relevant ability item names for the Team (Does NOT include JUMP)"""
    return [get_correct_ability_item_name(world=world, team=team, ability=ability) for ability in get_abilities_for_team(world=world, team=team)]


def get_characters_in_team_with_ability(world: SonicHeroesWorldBase, team: Team, ability: Ability) -> list[Character]:
    return [char for char in get_all_characters_for_team(world=world, team=team) if ability in get_abilities_for_char(world=world, character=char) or ability == Ability.JUMP]


def is_rule_caching_enabled(world: SonicHeroesWorldBase) -> bool:
    return False
    # return getattr(world, RULE_CACHING_ENABLED_ATTR, False)

def get_default_true_rule() -> Rule[SonicHeroesWorldBase]:
    return True_[SonicHeroesWorldBase]()


def get_obj_sanity_event_item_name(team: Team, stage: Stage, act: Act) -> str:
    return f"{team} {stage.stage_name} {act.get_act_str()} {OBJ_SANITY_EVENT_ITEM}"


def is_this_team_enabled(world: SonicHeroesWorldBase, team: Team) -> bool:
    if team is Team.ANY_TEAM:
        return False
    return is_this_act_enabled(world=world, team=team, act=Act.ACT_A) or is_this_act_enabled(world=world, team=team, act=Act.ACT_B)


def is_this_act_enabled(world: SonicHeroesWorldBase, team: Team, act: Act) -> bool:
    if act is Act.NONE:
        raise ValueError(f"Checking for {act.get_act_str()} in is_this_act_enabled")

    match team:
        case Team.ANY_TEAM:
            raise ValueError(f"Checking for {team} in is_this_act_enabled")
        case Team.SONIC:
            match act:
                case Act.BOTH_ACTS:
                    return EnabledTeamActs.SONIC_ACT_A in world.enabled_team_acts_flag and EnabledTeamActs.SONIC_ACT_B in world.enabled_team_acts_flag
                case Act.ACT_A | Act.ACT_B:
                    return EnabledTeamActs.SONIC_ACT_A in world.enabled_team_acts_flag or EnabledTeamActs.SONIC_ACT_B in world.enabled_team_acts_flag

        case Team.DARK:
            match act:
                case Act.BOTH_ACTS:
                    return EnabledTeamActs.DARK_ACT_A in world.enabled_team_acts_flag and EnabledTeamActs.DARK_ACT_B in world.enabled_team_acts_flag
                case Act.ACT_A | Act.ACT_B:
                    return EnabledTeamActs.DARK_ACT_A in world.enabled_team_acts_flag or EnabledTeamActs.DARK_ACT_B in world.enabled_team_acts_flag

        case Team.ROSE:
            match act:
                case Act.BOTH_ACTS:
                    return EnabledTeamActs.ROSE_ACT_A in world.enabled_team_acts_flag and EnabledTeamActs.ROSE_ACT_B in world.enabled_team_acts_flag
                case Act.ACT_A | Act.ACT_B:
                    return EnabledTeamActs.ROSE_ACT_A in world.enabled_team_acts_flag or EnabledTeamActs.ROSE_ACT_B in world.enabled_team_acts_flag

        case Team.CHAOTIX:
            match act:
                case Act.BOTH_ACTS:
                    return EnabledTeamActs.CHAOTIX_ACT_A in world.enabled_team_acts_flag and EnabledTeamActs.CHAOTIX_ACT_B in world.enabled_team_acts_flag
                case Act.ACT_A | Act.ACT_B:
                    return EnabledTeamActs.CHAOTIX_ACT_A in world.enabled_team_acts_flag or EnabledTeamActs.CHAOTIX_ACT_B in world.enabled_team_acts_flag


        case Team.SUPER_HARD_MODE:
            match act:
                case Act.BOTH_ACTS:
                    raise ValueError(f"Checking for {act.get_act_str()} for Team {team} in is_this_act_enabled")
                case Act.ACT_A | Act.ACT_B:
                    return EnabledTeamActs.SUPER_HARD_MODE in world.enabled_team_acts_flag