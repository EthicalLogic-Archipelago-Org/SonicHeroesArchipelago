"""
The World For Universal Tracker
"""
import re
from math import floor, log10
from typing import override, Any, ClassVar

from BaseClasses import CollectionState, MultiWorld
from NetUtils import JSONMessagePart
from Options import Option
from Utils import get_intended_text, get_fuzzy_results  # pyright: ignore[reportUnknownVariableType]

from ..location_generation import FULL_LOCATION_DICT
from ..rule_builder.custom_rules import SonicHeroesMacroRule
from ..rule_parser.functions_parser import get_parsed_data_module_for_team_stage

from ..constants.apworld import RE_GEN_PASSTHROUGH_ATTR
from ..constants.char_ability import Team
from ..constants.items_events import UT_GLITCH_ITEM, OBJ_SANITY
from ..constants.loc_region import LocationType, SonicHeroesLocationData
from ..constants.stage import Act, EnabledTeamActs, Stage
from ..world_base import SonicHeroesWorldBase


class SonicHeroesUTWorld(SonicHeroesWorldBase):
    ut_can_gen_without_yaml: ClassVar[bool] = True
    glitches_item_name: ClassVar[str] = UT_GLITCH_ITEM
    is_ut_gen: bool = False

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)
        self.enabled_team_acts_flag: EnabledTeamActs = EnabledTeamActs.NONE
        self.enabled_sanity_acts: dict[Team, dict[LocationType, Act]] = {team: {loc_type: Act.NONE for loc_type in LocationType.get_sanity_types()} for team in Team}
        """Dict of Team to Sanity Type to Act Flag"""

        # Obj Sanity cares about Act
        # every other sanity cares about group vs full


    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        return slot_data


    @override
    def generate_early(self) -> None:
        #do UT stuff here
        self.handle_ut_gen()
        super().generate_early()
        pass


    def custom_ut_sort(self, region_label: str, location_label: str) -> str | int:
        # make a bitfield
        # team most significant             (AnyTeam, Sonic, Dark, Rose, Chaotix)
        # stage                             (SH -> Final)
        # region (order through level)      can be several hundred
        # type (ObjSanity, Act Goal)        (regular, ObjSanity, Goal)
        # first group second group
        # left center right

        # could be string
        # NOT HEXA!!!
        # 0 (Any Team) 00 (SH) 3 (EggPawnSanity) 0059 (Region) 0 (First Group) 2 (Right)
        # 0003005902
        _result: str = ""

        # get team and Stage
        team: Team = Team.ANY_TEAM
        stage: Stage = Stage.TEST_LEVEL

        for temp_stage in Stage:
            if location_label.startswith(temp_stage.stage_name):
                stage = temp_stage
                # break # cant break as Seaside Hill Bonus Stage exists (would match SH)

        if stage is Stage.TEST_LEVEL:
            raise ValueError(f"No Valid Stage in Location: {location_label} ::: Region: {region_label}")

        temp_location_label: str = location_label.removeprefix(f"{stage.stage_name} ")

        for temp_team in Team:
            if temp_team is Team.ANY_TEAM:
                continue
            if temp_location_label.startswith(temp_team):
                team = temp_team

        # handle Ring locations (end with Ring 1) (or Ring Group)
        ring_individual_pattern: re.Pattern[str] = re.compile(r"(Ring \d+)$")
        ring_group_pattern: re.Pattern[str] = re.compile(r"(Ring Group)$")

        if re.match(ring_individual_pattern, temp_location_label) is not None:
            temp_location_label = re.sub(ring_individual_pattern, location_label)  # pyright: ignore[reportCallIssue]

        elif re.match(ring_group_pattern, temp_location_label) is not None:
            temp_location_label = re.sub(ring_group_pattern, location_label)  # pyright: ignore[reportCallIssue]

        else:
            temp_location_label = location_label


        location_list: list[SonicHeroesLocationData] = [loc_data for loc_data in FULL_LOCATION_DICT[stage][team] if loc_data.name == temp_location_label]

        if len(location_list) != 1:
            raise ValueError(f"Problem Matching Location: {location_label} For Team: {team.value} and Stage: {stage.stage_name}. Matched: {location_list}")
        location_data: SonicHeroesLocationData = location_list[0]


        # get region
        region_to_index: dict[str, int] = \
        {
            region.region_name: index for index, region in enumerate(get_parsed_data_module_for_team_stage(team=team, stage=stage).regions)  # pyright: ignore[reportAny]
        }
        #force ObjSanity to last (but before goal)
        region_to_index[f"{stage.stage_name} {team.value} {OBJ_SANITY}"] = region_to_index[f"{stage.stage_name} {team.value} Goal"]
        region_to_index[f"{stage.stage_name} {team.value} Goal"] += 1


        # start sorting here
        # Team most significant
        match team:
            case Team.SONIC:
                _result += "0"
            case Team.DARK:
                _result += "1"
            case Team.ROSE:
                _result += "2"
            case Team.CHAOTIX:
                _result += "3"
            case Team.SUPER_HARD_MODE:
                _result += "4"
            case Team.ANY_TEAM:
                _result += "9"

        # then Stage
        _result += stage.sort_key

        # then region (ObjSanity and Act Goal matters here)
        num_of_digits_for_region_key: int = 1 + floor(log10(region_to_index[f"{stage.stage_name} {team.value} Goal"]))
        _result += f"{region_to_index[region_label]:0{num_of_digits_for_region_key}d}"
        # for x in range(num_of_digits_for_region_key - 1):
        #     if region_to_index[region_label] < 10 * x:
        #         _result += f"0"
        # _result += str(region_to_index[f"{stage.stage_name} {team.value} Goal"])

        # sort based on type (enemy, item box)
        _result += location_data.loc_type.sort_key

        # sort based on act
        _result += str(location_data.act)

        # sort based on left -> right
        # maybe append last digits of loc ID (this could be a clean way of handling this)
        _result += str(location_data.code)[-3:]

        return _result



    def explain_rule(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart] | None:  # pyright: ignore[reportExplicitAny, reportAny]
        if not dest_name:
            _result: list[JSONMessagePart] = [{"type": "text", "text": "Enter a macro, location, or region to get an explanation"}]
            return _result
        result, usable, confidence = self._explain_macro(macro_name=dest_name, state=state)
        if usable:
            return result

        #need to do thing here



        return None #Do Normal UT Thing


    def _explain_macro(self, macro_name: str, state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_macro_names: set[str] = set(self.rule_macros.keys())
        guess, usable, response = get_intended_text(input_text=macro_name, possible_answers=all_macro_names)
        if not usable:
            picks: list[tuple[str, int]] = get_fuzzy_results(input_word=macro_name, word_list=all_macro_names, limit=1)
            confidence: int = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        macro_name: str = guess
        macro: SonicHeroesMacroRule.Resolved = self.rule_macros[macro_name]  # pyright: ignore[reportAssignmentType]
        assert isinstance(macro, SonicHeroesMacroRule.Resolved)
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Rule Macro "},
            {"type": "color", "color": "green" if macro(state) else "salmon", "text": macro.name},
        ]
        if macro.description:
            messages.append({"type": "text", "text": f"\n{macro.description}"})
        messages.extend(
            [
                {"type": "text", "text": "\nLogic: "},
                *macro.child.explain_json(state),
            ]
        )
        return messages, True, 100



    # def explain_more(self, target_name: str, state: CollectionState) -> list[JSONMessagePart] | None:
    #     if target_name == "Do Normal UT thing":
    #         return None
    #     _result: list[JSONMessagePart] = [{"type": "text", "text": target_name}]
    #     return _result


    def handle_ut_gen(self) -> None:
        re_gen_passthrough: dict[str, dict[str, Any]] | None = getattr(self.multiworld, RE_GEN_PASSTHROUGH_ATTR, {})  # pyright: ignore[reportExplicitAny]
        if not re_gen_passthrough or not self.game in re_gen_passthrough:
            return
        self.is_ut_gen = True
        slot_data: dict[str, Any] = re_gen_passthrough[self.game]  # pyright: ignore[reportExplicitAny]

        self.enabled_team_acts_flag = EnabledTeamActs(value=slot_data["ActsAndSanities"]["EnabledActs"])

        for key, value in slot_data.get("options", {}).items():  # pyright: ignore[reportAny]
            opt: Option[SonicHeroesWorldBase] | None = getattr(self.options, key, None)  # pyright: ignore[reportAny]
            if opt is not None:
                setattr(self.options, key, opt.from_any(data=value))  # pyright: ignore[reportAny]


    #
    # def explain_rule(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart]:
    #     if not dest_name:
    #         return [{"type": "text", "text": "Enter a macro, location, region, item, or acronym to get an explanation"}]
    #     if description := ACRONYMS.get(dest_name.lower()):
    #         return [{"type": "text", "text": description}]
    #
    #     types_to_try = {
    #         "macro": self._explain_macro,
    #         "location": self._explain_location,
    #         "region": self._explain_region,
    #         "item": self._explain_item,
    #     }
    #     attempts = list(types_to_try.keys())
    #     parts = dest_name.split(maxsplit=1)
    #     if len(parts) == 2:
    #         first_word = parts[0].lower()
    #         for label in types_to_try.keys():
    #             if first_word == label:
    #                 attempts = [label]
    #                 break
    #
    #     result = []
    #     usable = False
    #     best_guess = []
    #     max_confidence = 0
    #     confidence = 0
    #     for classification in attempts:
    #         result, usable, confidence = types_to_try[classification](dest_name, state)
    #         if usable:
    #             return result
    #         if confidence > max_confidence:
    #             best_guess = result
    #             max_confidence = confidence
    #
    #     return best_guess


    # def _explain_macro(self, macro_name: str, state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
    #     all_macro_names = set(self.rule_macros.keys())
    #     guess, usable, response = get_intended_text(macro_name, all_macro_names)
    #     if not usable:
    #         picks = get_fuzzy_results(macro_name, all_macro_names, limit=1)
    #         confidence = picks[0][1]
    #         return [{"type": "text", "text": response}], False, confidence
    #
    #     macro_name = guess
    #     macro = self.rule_macros[macro_name]
    #     assert isinstance(macro, Macro.Resolved)
    #     messages: list[JSONMessagePart] = [
    #         {"type": "text", "text": "Macro "},
    #         {"type": "color", "color": "green" if macro(state) else "salmon", "text": macro.name},
    #     ]
    #     if macro.description:
    #         messages.append({"type": "text", "text": f"\n{macro.description}"})
    #     messages.extend(
    #         [
    #             {"type": "text", "text": "\nLogic: "},
    #             *macro.child.explain_json(state),
    #         ]
    #     )
    #     return messages, True, 100

