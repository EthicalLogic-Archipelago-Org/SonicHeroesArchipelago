"""
Custom Rule Builder Rules
"""
from __future__ import annotations
import dataclasses
from math import ceil
from typing import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import HasAll, HasAny, HasFromListUnique, Rule, WrapperRule, Has, True_, False_, CanReachRegion


from ..constants.apworld import SONIC_HEROES
from ..constants.char_ability import Ability, Character, Team, Formation
from ..constants.enemies import E2000, Cameron, EggFlapper, EggHammer, EnemyType, Falco, Klagen, Rhino, SonicHeroesEnemyBase, EggPawn
from ..constants.items_events import OBJ_SANITY_EVENT_ITEM, UT_GLITCH_ITEM, DARK_OBJ_SANITY_AMOUNT, ROSE_OBJ_SANITY_AMOUNT
from ..constants.stage import Act, Stage, StageType
from ..constants.stage_objs import StageObj
from ..helper_functions import get_abilities_for_char, get_abilities_for_team, get_all_characters_for_team, get_correct_ability_item_name, get_playable_char_item_name, is_rule_caching_enabled, get_characters_in_team_with_ability, is_this_act_enabled
from ..rule_builder.functions_stage_obj import has_stage_obj_rule
from ..world_base import SonicHeroesWorldBase


@dataclasses.dataclass(kw_only=True)
class SonicHeroesMacroRule(WrapperRule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """
    Combines multiple rules into a single name and description
    Main AP Repo PR# 5972
    """
    name: str
    description: str = "Description Here"

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        if rule := world.rule_macros.get(self.name):
            return rule
        rule = self.Resolved(  # pyright: ignore[reportAny]
            self.child.resolve(world),
            self.name,
            self.description,
            player=world.player,
            caching_enabled=is_rule_caching_enabled(world)
        )
        world.rule_macros[self.name] = rule
        return rule  # pyright: ignore[reportAny]

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str
        description: str

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [{"type": "color", "color": "green" if self(state) else "salmon", "text": str(self)}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name


@dataclasses.dataclass(kw_only=True)
class HasFormationCharForTeam(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Checks if you have the Character Item for the Formation and Team"""
    team: Team
    formation: Formation

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_all_characters_for_team(world=world, team=self.team):
            if char.formation == self.formation:
                rule |= Has(item_name=get_playable_char_item_name(character=char))
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasFormationCharWithLevelForTeam(HasFormationCharForTeam, game=SONIC_HEROES):
    stage: Stage
    level: int

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_all_characters_for_team(world=world, team=self.team):
            if char.formation == self.formation:
                rule |= Has(item_name=get_playable_char_item_name(character=char)) & self._has_level_for_character(world=world, character=char)
        return rule.resolve(world=world)

    def _has_level_for_character(self, world: SonicHeroesWorldBase, character: Character) -> Rule[SonicHeroesWorldBase]:
        ability_item_list: list[str] = [get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=ability) for ability in get_abilities_for_char(world=world, character=character)]
        # has x abilities from char
        match self.level:
            case 0:
                return True_[SonicHeroesWorldBase]()
            case 1:
                return HasFromListUnique(*ability_item_list, count=1)
            case 2:
                return HasFromListUnique(*ability_item_list, count=ceil(len(ability_item_list) / 2))
            case 3:
                return HasFromListUnique(*ability_item_list, count=len(ability_item_list))
            case _:
                return False_[SonicHeroesWorldBase]()


@dataclasses.dataclass(kw_only=True)
class HasFlyingAnd1MoreChar(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    team: Team

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return self._has_flying_and_1_more_chars(world=world).resolve(world=world)

    def _has_flying_and_1_more_chars(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        has_flying_and_1_more_chars_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        char_list: list[Character] = get_all_characters_for_team(world=world, team=self.team)
        for char in char_list:
            if char.formation is not Formation.FLYING:
                continue
            has_1_more_char_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()

            for other_char in char_list:
                if char is other_char:
                    continue
                has_1_more_char_rule |= Has(item_name=get_playable_char_item_name(character=other_char))

            has_flying_and_1_more_chars_rule |= (Has(item_name=get_playable_char_item_name(character=char)) & has_1_more_char_rule)

        return has_flying_and_1_more_chars_rule


@dataclasses.dataclass(kw_only=True)
class HasTallChar(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    team: Team

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return self._has_tall_character(world=world).resolve(world=world)

    def _has_tall_character(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        has_tall_power_char: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        char_list: list[Character] = get_all_characters_for_team(world=world, team=self.team)

        if Character.OMEGA in char_list:
            has_tall_power_char |= SonicHeroesMacroRule(child=Has(item_name=get_playable_char_item_name(character=Character.OMEGA)), name=f"Tall Power Char: ({Character.OMEGA.char_name})")
        if Character.BIG in char_list:
            has_tall_power_char |= SonicHeroesMacroRule(child=Has(item_name=get_playable_char_item_name(character=Character.BIG)), name=f"Tall Power Char: ({Character.BIG.char_name})")
        if Character.VECTOR in char_list:
            has_tall_power_char |= SonicHeroesMacroRule(child=Has(item_name=get_playable_char_item_name(character=Character.VECTOR)), name=f"Tall Power Char: ({Character.VECTOR.char_name})")
        return has_tall_power_char


@dataclasses.dataclass(kw_only=True)
class HasAll3Char(HasTallChar, game=SONIC_HEROES):

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return self._has_all_3_chars(world=world).resolve(world=world)

    def _has_all_3_chars(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        has_all_3: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
        char_list: list[Character] = get_all_characters_for_team(world=world, team=self.team)
        for char in char_list:
            has_all_3 &= Has(item_name=get_playable_char_item_name(character=char))
        return has_all_3


@dataclasses.dataclass(kw_only=True)
class HasFullFlyingStackWithTallChar(HasAll3Char, game=SONIC_HEROES):

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return (self._has_flying_char(world=world) & self._has_tall_character(world=world) & self._has_all_3_chars(world=world)).resolve(world=world)


    def _has_flying_char(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        has_flying_char: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        char_list: list[Character] = get_all_characters_for_team(world=world, team=self.team)
        for char in char_list:
            if char.formation == Formation.FLYING:
                has_flying_char |= Has(item_name=get_playable_char_item_name(character=char))
        return has_flying_char


@dataclasses.dataclass(kw_only=True)
class CanAutoPowerAttack(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """
    Checks for having the power char and a second char for the auto attack feature
    """
    team: Team
    stage: Stage
    need_speed_lvl_3: bool

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_all_characters_for_team(world=world, team=self.team):
            if char.formation == Formation.POWER:
                temp_rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_playable_char_item_name(character=char))
                if self.need_speed_lvl_3:
                    temp_rule &= HasFormationCharWithLevelForTeam(team=self.team, stage=self.stage, formation=Formation.SPEED, level=3)
                else:
                    has_other_char_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
                    for other_char in get_all_characters_for_team(world=world, team=self.team):
                        if other_char != char:
                            has_other_char_rule |= Has(item_name=get_playable_char_item_name(character=other_char))
                    temp_rule &= has_other_char_rule
                rule |= temp_rule
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasAbilityItem(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """
    Checks for having the ability item for the Team and Stage and having a character that has the ability (Jump matches all)
    """
    ability: Ability
    team: Team
    stage: Stage

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = HasAny(*[get_playable_char_item_name(character=char) for char in get_characters_in_team_with_ability(world=world, team=self.team, ability=self.ability)])
        rule &= Has(item_name=get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=self.ability))
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasAbilityItemLevel(HasAbilityItem, game=SONIC_HEROES):
    """
    Checks for having the ability item for the Team and Stage and having a character that has the ability
    Also checks for the character's other abilities for the required level
    """
    level: int

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=self.ability))
        rule &= self._has_char_level_with_ability_rule(world=world)
        return rule.resolve(world=world)

    def _has_char_level_with_ability_rule(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        combined_char_level_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_characters_in_team_with_ability(world=world, team=self.team, ability=self.ability):
            # has char
            char_level_rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_playable_char_item_name(character=char))
            ability_item_list: list[str] = [get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=ability) for ability in get_abilities_for_char(world=world, character=char)]
            #has x abilities from char
            match self.level:
                case 0:
                    char_level_rule &= True_[SonicHeroesWorldBase]()
                case 1:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=1)
                case 2:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=ceil(len(ability_item_list) / 2))
                case 3:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=len(ability_item_list))
                case _:
                    char_level_rule &= False_[SonicHeroesWorldBase]()
            combined_char_level_rule |= char_level_rule
        return combined_char_level_rule


@dataclasses.dataclass(init=False, kw_only=True)
class HasComboHeight(HasAbilityItemLevel, game=SONIC_HEROES):
    """
    Checks for having the Combo Finisher item for the Team and Stage and having a character that has the ability
    MAKE SURE TO ALSO CHECK FOR POWER ATTACK (in the macro rule)
    """
    def __init__(self, team: Team, stage: Stage) -> None:
        super().__init__(team=team, stage=stage, ability=Ability.COMBO_FINISHER, level=0)


    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=self.ability))
        rule &= self._has_knuckles_or_super_hard_knuckles_rule(world=world)
        return rule.resolve(world=world)

    def _has_knuckles_or_super_hard_knuckles_rule(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        char_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        char_list: list[Character] = get_characters_in_team_with_ability(world=world, team=self.team, ability=self.ability)
        if Character.KNUCKLES in char_list:
            char_rule |= Has(item_name=get_playable_char_item_name(character=Character.KNUCKLES))
        if Character.SUPER_HARD_MODE_KNUCKLES in char_list:
            char_rule |= Has(item_name=get_playable_char_item_name(character=Character.SUPER_HARD_MODE_KNUCKLES))
        return char_rule


@dataclasses.dataclass(kw_only=True)
class HasAbilityItemLevelOtherChars(HasAbilityItemLevel, game=SONIC_HEROES):
    """
    Checks for having the ability item for the Team and Stage and having a character that has the ability
    Also checks for the character's other abilities for the required level
    Also checks for having other characters in addition to the leader
    """
    num_other_chars: int

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=self.ability))
        rule &= self._has_other_chars_rule(world=world)
        return rule.resolve(world=world)

    def _has_other_chars_rule(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        combined_char_level_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_characters_in_team_with_ability(world=world, team=self.team, ability=self.ability):
            # has char
            char_level_rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_playable_char_item_name(character=char))
            ability_item_list: list[str] = [get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=ability) for ability in get_abilities_for_char(world=world, character=char)]
            #has x abilities from char
            match self.level:
                case 0:
                    char_level_rule &= True_[SonicHeroesWorldBase]()
                case 1:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=1)
                case 2:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=ceil(len(ability_item_list) / 2))
                case 3:
                    char_level_rule &= HasFromListUnique(*ability_item_list, count=len(ability_item_list))
                case _:
                    char_level_rule &= False_[SonicHeroesWorldBase]()
            # has other chars
            other_chars: list[str] = [get_playable_char_item_name(character=other_char) for other_char in get_all_characters_for_team(world=world, team=self.team) if other_char != char]
            match self.num_other_chars:
                case 0:
                    char_level_rule &= True_[SonicHeroesWorldBase]()
                case 1:
                    char_level_rule &= HasFromListUnique(*other_chars, count=1)
                case 2:
                    char_level_rule &= HasFromListUnique(*other_chars, count=2)
                case _:
                    char_level_rule &= False_[SonicHeroesWorldBase]()

            combined_char_level_rule |= char_level_rule
        return combined_char_level_rule


@dataclasses.dataclass(kw_only=True)
class CanTeamBlast(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Rule for Team Blast, needs Team and Stage"""
    team: Team
    stage: Stage

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        combined_ability_rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()
        combined_ability_rule &= HasAll(*[get_playable_char_item_name(character=char) for char in get_all_characters_for_team(world=world, team=self.team)])
        combined_ability_rule &= HasAll(*[get_correct_ability_item_name(world=world, team=self.team, stage=self.stage, ability=ability) for ability in get_abilities_for_team(world=world, team=self.team)])
        return SonicHeroesMacroRule(child=combined_ability_rule, name=f"Team Blast in {self.stage.stage_name} as Team: {self.team}", description="Team Blast Description Here").resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanGoalStage(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Rule for Goaling stage"""
    team: Team
    stage: Stage

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()

        if self.stage.stage_type is StageType.NORMAL_STAGE:
            match self.team:
                case Team.SONIC:
                    rule = self._can_goal_sonic_stage(world=world)
                case Team.DARK:
                    rule = self._can_goal_dark_stage(world=world)
                case Team.ROSE:
                    rule = self._can_goal_rose_stage(world=world)
                case Team.CHAOTIX:
                    rule = self._can_goal_chaotix_stage(world=world)
                case Team.SUPER_HARD_MODE:
                    rule = self._can_goal_super_hard_mode_stage(world=world)
                case _:
                    raise ValueError(f"Wrong Team in CanGoalStage: {self.team} for {self.stage.stage_name}")
        # else:
        #     raise ValueError(f"Wrong StageType in CanGoalStage: {self.stage.stage_name}")

        return SonicHeroesMacroRule(child=rule, name=f"Get Goal {self.stage.stage_name} as Team: {self.team}").resolve(world=world)


    def _can_reach_goal_vanilla(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        return CanReachRegion(region_name=f"{self.stage.stage_name} {self.team} Goal") & has_stage_obj_rule(stage_obj=StageObj.GOAL_RING)

    def _can_goal_sonic_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        if self.stage is Stage.EGG_FLEET:
            # sonic egg fleet does not have a goal ring
            return CanReachRegion(region_name=f"{self.stage.stage_name} {self.team} Goal")
        return self._can_reach_goal_vanilla(world=world)

    def _can_goal_dark_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_1):
            rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_2):
            rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=DARK_OBJ_SANITY_AMOUNT)
        return rule

    def _can_goal_rose_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_1):
            rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_2):
            rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=ROSE_OBJ_SANITY_AMOUNT)
        return rule

    def _can_goal_chaotix_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        # TODO fix for stealth levels
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_1):
            if self.stage.chaotix_obj_sanity_checks[Act.ACT_1] > 0:
                rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=self.stage.chaotix_obj_sanity_checks[Act.ACT_1])
            else:
                rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_2):
            if self.stage.chaotix_obj_sanity_checks[Act.ACT_2] > 0:
                rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}",count=self.stage.chaotix_obj_sanity_checks[Act.ACT_2])
            else:
                rule |= self._can_reach_goal_vanilla(world=world)
        return rule

    def _can_goal_super_hard_mode_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        return self._can_reach_goal_vanilla(world=world)


@dataclasses.dataclass(kw_only=True)
class CanGetEmerald(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Rule for getting emerald in emerald stage. Already assumes access to level"""
    stage: Stage

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        has_speed_char: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for team in world.enabled_teams:  # pyright: ignore[reportAny]
            has_speed_char |= HasFormationCharForTeam(team=team, formation=Formation.SPEED)  # pyright: ignore[reportAny]
        return SonicHeroesMacroRule(child=has_stage_obj_rule(stage_obj=StageObj.SPECIAL_STAGE_ORBS) & has_speed_char, name=f"Get Chaos Emerald in {self.stage.stage_name}").resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class TrickRule(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    option_filter: OptionFilter

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return self.Resolved(
            in_logic=self.option_filter.check(world.options),
            trick_filter=str(self.option_filter),
            glitch_item_name=UT_GLITCH_ITEM,
            player=world.player,
            caching_enabled=is_rule_caching_enabled(world=world)
        )  # pyright: ignore[reportAny]

    # @override
    # def __str__(self) -> str:
    #     return self.trick_filter

    class Resolved(Rule.Resolved):
        in_logic: bool
        trick_filter: str
        glitch_item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(item=self.glitch_item_name, player=self.player)

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return \
                [
                    {
                        "type": "color",
                        "color": "green" if self.in_logic else "yellow",
                        "text": str(self),
                    }
                ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            # if state is None:
            #     return str(self)
            return str(self)

        @override
        def __str__(self) -> str:
            return f"{'LogicTrick' if self.in_logic else 'OutOfLogic'}[{self.trick_filter}]"


@dataclasses.dataclass(kw_only=True)
class HasEnemyItem(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Do you have the enemy spawned into the level?"""
    team: Team
    stage: Stage
    enemy: SonicHeroesEnemyBase

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        if isinstance(self.enemy, EggFlapper):
            return self._has_egg_flapper_spawned(world=world)
        if isinstance(self.enemy, EggPawn):
            return self._has_egg_pawn_spawned(world=world)
        if isinstance(self.enemy, Klagen):
            return self._has_klagen_spawned(world=world)
        if isinstance(self.enemy, Falco):
            return self._has_falco_spawned(world=world)
        if isinstance(self.enemy, EggHammer):
            return self._has_egg_hammer_spawned(world=world)
        if isinstance(self.enemy, Cameron):
            return self._has_cameron_spawned(world=world)
        if isinstance(self.enemy, Rhino):
            return self._has_rhino_spawned(world=world)
        if isinstance(self.enemy, E2000):
            return self._has_e2000_spawned(world=world)
        return Has(item_name=self.enemy.enemy_type).resolve(world=world)

    def _has_egg_flapper_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.EGG_FLAPPER).resolve(world=world)
    def _has_egg_pawn_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.EGG_PAWN).resolve(world=world)
    def _has_klagen_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.KLAGEN).resolve(world=world)
    def _has_falco_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.FALCO).resolve(world=world)
    def _has_egg_hammer_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.EGG_HAMMER).resolve(world=world)
    def _has_cameron_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.CAMERON).resolve(world=world)
    def _has_rhino_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.RHINO).resolve(world=world)
    def _has_egg_bishop_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.EGG_BISHOP).resolve(world=world)
    def _has_e2000_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=EnemyType.E2000).resolve(world=world)
