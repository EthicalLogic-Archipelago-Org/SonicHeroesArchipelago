"""
Custom Rule Builder Rules
"""
from __future__ import annotations
import dataclasses
from math import ceil
from typing import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.options import OPERATOR_STRINGS, OptionFilter
from rule_builder.rules import AtLeast, HasAll, HasAny, HasFromListUnique, Rule, WrapperRule, Has, True_, False_, CanReachRegion


from ..constants.apworld import SONIC_HEROES
from ..constants.char_ability import Ability, Character, Team, Formation
from ..constants.enemies import E2000, Cameron, EggFlapper, EggHammer, EnemyType, Falco, Klagen, Rhino, SonicHeroesEnemyBase, EggPawn
from ..constants.items_events import OBJ_SANITY_EVENT_ITEM, UT_GLITCH_ITEM, DARK_OBJ_SANITY_AMOUNT, \
    ROSE_OBJ_SANITY_AMOUNT, PROGRESSIVE
from ..constants.stage import Act, Stage, StageType
from ..constants.stage_objs import StageObj
from ..helper_functions import get_abilities_for_char, get_abilities_for_team, get_all_characters_for_team, \
    get_correct_ability_item_name, get_playable_char_item_name, is_rule_caching_enabled, \
    get_characters_in_team_with_ability, is_this_act_enabled, get_stage_obj_item_name
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
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state=state)

        @override
        def __str__(self) -> str:
            return self.name


@dataclasses.dataclass(kw_only=True)
class HasCharacter(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    character: Character

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return self._has_char_rule(world=world).resolve(world=world)


    def _has_char_rule(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        return Has(item_name=get_playable_char_item_name(character=self.character))


    def _get_ability_rule(self, world: SonicHeroesWorldBase, ability: Ability) -> Rule[SonicHeroesWorldBase]:
        team: Team = self.character.get_team(world=world)
        rule: Rule[SonicHeroesWorldBase] = Has(item_name=get_correct_ability_item_name(world=world, team=team, ability=ability))

        match ability:
            case Ability.HOMING_ATTACK:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.HOMING_ATTACK.ability_name}")
            case Ability.TORNADO:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.TORNADO.ability_name}")
            case Ability.TRIANGLE_JUMP:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.HOMING_ATTACK.ability_name}", count=2)
            case Ability.INVISIBILITY:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.TORNADO.ability_name}", count=2)
            # case Ability.LIGHT_ATTACK: # <- handled by function in functions_ability_char (macro)
            #     rule &= CanTeamBlast(team=team)
            case Ability.THUNDER_SHOOT:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}")
            case Ability.FLIGHT:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}", count=2)
            case Ability.DUMMY_RINGS:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}")
            case Ability.CHEESE_CANNON:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.FLIGHT.ability_name}")
            case Ability.POWER_ATTACK:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.POWER_ATTACK.ability_name}")
            case Ability.COMBO_FINISHER:
                rule |= Has(item_name=f"{PROGRESSIVE} {team.value} {Ability.POWER_ATTACK.ability_name}", count=2)
            case _:
                pass
        return rule


@dataclasses.dataclass(kw_only=True)
class HasLevelForCharacter(HasCharacter, game=SONIC_HEROES):
    """Checks if you have the Character Item and enough Abilities to be the level"""
    level: int = 0

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return (self._has_char_rule(world=world) & self._has_level_rule(world=world)).resolve(world=world)


    def _has_level_rule(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        ability_rules: list[Rule[SonicHeroesWorldBase]] = [self._get_ability_rule(world=world, ability=ability) for ability in self.character.get_abilities(world=world)]
        match self.level:
            case 0:
                return True_[SonicHeroesWorldBase]()
            case 1:
                return AtLeast(1, *ability_rules)
            case 2:
                return AtLeast(ceil(len(ability_rules) / 2), *ability_rules)
            case 3:
                return AtLeast(len(ability_rules), *ability_rules)
            case _:
                return False_[SonicHeroesWorldBase]()


@dataclasses.dataclass(kw_only=True)
class HasAbilityForCharacter(HasLevelForCharacter, game=SONIC_HEROES):
    """Checks if you have the Character Item and enough Abilities to be the level"""
    ability: Ability

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return (self._has_char_rule(world=world) & self._get_ability_rule(world=world, ability=self.ability) & self._has_level_rule(world=world)).resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasAllAbilitiesForCharacter(HasLevelForCharacter, game=SONIC_HEROES):
    """Checks if you have the Character Item and all Abilities except JUMP. Level is ignored"""

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = self._has_char_rule(world=world)
        for ability in self.character.get_abilities(world=world):
            rule &= self._get_ability_rule(world=world, ability=ability)
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasFormationCharForTeam(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    team: Team
    formation: Formation
    level: int = 0

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_all_characters_for_team(world=world, team=self.team):
            if char.formation is self.formation:
                rule |= HasLevelForCharacter(character=char, level=self.level)
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class HasAbilityForTeam(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """
    Checks for having the ability item for the Team and Stage and having a character that has the ability (Jump matches all)
    """
    team: Team
    ability: Ability
    level: int = 0
    num_other_chars: int = 0

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()

        for char in self._get_chars_with_ability(world=world):
            rule |= HasAbilityForCharacter(character=char, ability=self.ability, level=self.level) & self._get_other_chars_rule(world=world, character=char)

        return rule.resolve(world=world)

    def _get_chars_with_ability(self, world: SonicHeroesWorldBase) -> list[Character]:
        return [character for character in get_all_characters_for_team(world=world, team=self.team) if self.ability is Ability.JUMP or self.ability in character.get_abilities(world=world)]

    def _get_other_chars_rule(self, world: SonicHeroesWorldBase, character: Character) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        if self.num_other_chars < 1:
            return True_[SonicHeroesWorldBase]()
        if self.num_other_chars == 1:
            for char in get_all_characters_for_team(world=world, team=self.team):
                if char is character:
                    continue
                rule |= HasCharacter(character=char)
        elif self.num_other_chars == 2:
            rule |= True_[SonicHeroesWorldBase]()
            for char in get_all_characters_for_team(world=world, team=self.team):
                if char is character:
                    continue
                rule &= HasCharacter(character=char)
        else:
            raise ValueError(f"Invalid Num other Chars in HasAbilityForTeam: {self.num_other_chars}")
        return rule


@dataclasses.dataclass(init=False, kw_only=True)
class HasComboHeight(HasAbilityForTeam, game=SONIC_HEROES):
    """
    Checks for having the Combo Finisher item for the Team and Stage and having a character that has the ability
    MAKE SURE TO ALSO CHECK FOR POWER ATTACK (in the macro rule)
    """
    def __init__(self, team: Team) -> None:
        super().__init__(team=team, ability=Ability.COMBO_FINISHER, level=1, num_other_chars=0)


    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for character in get_all_characters_for_team(world=world, team=self.team):
            if character is Character.KNUCKLES:
                rule |= HasAbilityForCharacter(character=character, ability=self.ability, level=self.level)
            if character is Character.SUPER_HARD_MODE_KNUCKLES:
                rule |= HasAbilityForCharacter(character=character, ability=self.ability, level=self.level)
        return rule.resolve(world=world)


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
                has_1_more_char_rule |= HasCharacter(character=other_char)

            has_flying_and_1_more_chars_rule |= (HasCharacter(character=char) & has_1_more_char_rule)

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
            has_tall_power_char |= SonicHeroesMacroRule(child=HasCharacter(character=Character.OMEGA), name=f"Tall Power Char: ({Character.OMEGA.char_name})")
        if Character.BIG in char_list:
            has_tall_power_char |= SonicHeroesMacroRule(child=HasCharacter(character=Character.BIG), name=f"Tall Power Char: ({Character.BIG.char_name})")
        if Character.VECTOR in char_list:
            has_tall_power_char |= SonicHeroesMacroRule(child=HasCharacter(character=Character.VECTOR), name=f"Tall Power Char: ({Character.VECTOR.char_name})")
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
            has_all_3 &= HasCharacter(character=char)
        return has_all_3


@dataclasses.dataclass(kw_only=True)
class HasFullFlyingStackWithTallChar(HasAll3Char, game=SONIC_HEROES):

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return (self._has_flying_char(world=world) & self._has_tall_character(world=world) & self._has_all_3_chars(world=world)).resolve(world=world)


    def _has_flying_char(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        return HasFormationCharForTeam(team=self.team, formation=Formation.FLYING)


@dataclasses.dataclass(kw_only=True)
class CanAutoPowerAttack(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """
    Checks for having the power char and a second char for the auto attack feature
    """
    team: Team
    need_speed_lvl_3: bool

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        for char in get_all_characters_for_team(world=world, team=self.team):
            if char.formation is Formation.POWER:
                temp_rule: Rule[SonicHeroesWorldBase] = HasCharacter(character=char)
                if self.need_speed_lvl_3:
                    temp_rule &= HasFormationCharForTeam(team=self.team, formation=Formation.SPEED, level=3)
                else:
                    has_other_char_rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
                    for other_char in get_all_characters_for_team(world=world, team=self.team):
                        if other_char is not char:
                            has_other_char_rule |= HasCharacter(character=other_char)
                    temp_rule &= has_other_char_rule
                rule |= temp_rule
        return rule.resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanTeamBlast(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    """Rule for Team Blast, needs Team"""
    team: Team

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        rule: Rule[SonicHeroesWorldBase] = True_[SonicHeroesWorldBase]()

        for character in get_all_characters_for_team(world=world, team=self.team):
            rule &= HasCharacter(character=character)
            for ability in character.get_abilities(world=world):
                rule &= HasAbilityForCharacter(character=character, ability=ability)
        return rule.resolve(world=world)
        #return SonicHeroesMacroRule(child=rule, name=f"Team Blast as Team: {self.team}", description="Team Blast Description Here").resolve(world=world)


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
        return CanReachRegion(region_name=f"{self.stage.stage_name} {self.team} Goal") & has_stage_obj_rule(team=self.team, stage_obj=StageObj.GOAL_RING)

    def _can_goal_sonic_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        if self.stage is Stage.EGG_FLEET:
            # sonic egg fleet does not have a goal ring
            return CanReachRegion(region_name=f"{self.stage.stage_name} {self.team} Goal")
        return self._can_reach_goal_vanilla(world=world)

    def _can_goal_dark_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_A):
            rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_B):
            rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=DARK_OBJ_SANITY_AMOUNT)
        return rule

    def _can_goal_rose_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_A):
            rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_B):
            rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=ROSE_OBJ_SANITY_AMOUNT)
        return rule

    def _can_goal_chaotix_stage(self, world: SonicHeroesWorldBase) -> Rule[SonicHeroesWorldBase]:
        rule: Rule[SonicHeroesWorldBase] = False_[SonicHeroesWorldBase]()
        # TODO fix for stealth levels
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_A):
            if self.stage.chaotix_obj_sanity_checks[Act.ACT_A] > 0:
                rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=self.stage.chaotix_obj_sanity_checks[Act.ACT_A])
            else:
                rule |= self._can_reach_goal_vanilla(world=world)
        if is_this_act_enabled(world=world, team=self.team, act=Act.ACT_B):
            if self.stage.chaotix_obj_sanity_checks[Act.ACT_B] > 0:
                rule |= Has(item_name=f"{self.stage.stage_name} {self.team} {OBJ_SANITY_EVENT_ITEM}", count=self.stage.chaotix_obj_sanity_checks[Act.ACT_B])
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
        # TODO decide on team handling for Special Stage Stage objs
        return SonicHeroesMacroRule(child=has_stage_obj_rule(team=Team.ANY_TEAM, stage_obj=StageObj.SPECIAL_STAGE_ORBS) & has_speed_char, name=f"Get Chaos Emerald in {self.stage.stage_name}").resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class TrickRule(Rule[SonicHeroesWorldBase], game=SONIC_HEROES):
    option_filter: OptionFilter

    @override
    def _instantiate(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        _trick_filter: str = f"{self._handle_operator()}{self.option_filter.option.handle_logic_trick_explain(self.option_filter.value)}" # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]

        return self.Resolved(
            in_logic=self.option_filter.check(world.options),
            trick_filter=_trick_filter,
            glitch_item_name=UT_GLITCH_ITEM,
            player=world.player,
            caching_enabled=is_rule_caching_enabled(world=world)
        )  # pyright: ignore[reportAny]

    # @override
    # def __str__(self) -> str:
    #     return self.trick_filter

    def _handle_operator(self) -> str:
        if self.option_filter.operator in ["ne", "gt", "lt", "ge", "le"]:
            return f"{OPERATOR_STRINGS[self.option_filter.operator]} "
        return ""



    class Resolved(Rule.Resolved):
        in_logic: bool
        trick_filter: str
        glitch_item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.in_logic or state.has(item=self.glitch_item_name, player=self.player)

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
            return self.trick_filter


        # TODO handle caching here


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

        print(f"BIG ISSUE HERE with HasEnemyItem")
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)

    def _has_egg_flapper_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_egg_pawn_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_klagen_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_falco_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_egg_hammer_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_cameron_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_rhino_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_egg_bishop_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
    def _has_e2000_spawned(self, world: SonicHeroesWorldBase) -> Rule.Resolved:
        return Has(item_name=get_stage_obj_item_name(team=self.team, stage_obj=self.enemy.obj_id)).resolve(world=world)
