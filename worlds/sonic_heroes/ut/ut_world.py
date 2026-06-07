"""
The World For Universal Tracker
"""
from typing import override, Any, ClassVar, Optional

from BaseClasses import CollectionState, MultiWorld
from NetUtils import JSONMessagePart
from Options import Option

from ..constants.apworld import GENERATION_IS_FAKE_ATTR, RE_GEN_PASSTHROUGH_ATTR
from ..constants.char_ability import Team
from ..constants.items_events import UT_GLITCH_ITEM
from ..constants.loc_region import LocationType
from ..constants.stage import Act
from ..world_base import SonicHeroesWorldBase


class SonicHeroesUTWorld(SonicHeroesWorldBase):
    ut_can_gen_without_yaml: ClassVar[bool] = True
    glitches_item_name: ClassVar[str] = UT_GLITCH_ITEM
    is_ut_gen: bool = False

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)
        self.enabled_team_acts: dict[Team, Act] = {team: Act.NONE for team in Team}
        """Dict of Team to enabled Acts flag"""
        self.enabled_sanity_acts: dict[Team, dict[LocationType, Act]] = {team: {loc_type: Act.NONE for loc_type in LocationType.get_sanity_types()} for team in Team}
        """Dict of Team to Sanity Type to Act Flag"""


    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        return slot_data


    @override
    def generate_early(self) -> None:
        #do UT stuff here
        self.is_ut_gen = getattr(self.multiworld, GENERATION_IS_FAKE_ATTR, False)
        self.handle_ut_gen()
        super().generate_early()
        pass


    # def explain_rule(self, target_name: str, state: CollectionState) -> list[JSONMessagePart] | None:
    #     if target_name == "Do Normal UT thing":
    #         return None
    #     _result: list[JSONMessagePart] = [{"type": "text", "text": target_name}]
    #     return _result
    #
    #
    # def explain_more(self, target_name: str, state: CollectionState) -> list[JSONMessagePart] | None:
    #     if target_name == "Do Normal UT thing":
    #         return None
    #     _result: list[JSONMessagePart] = [{"type": "text", "text": target_name}]
    #     return _result


    def handle_ut_gen(self) -> None:
        re_gen_passthrough: dict[str, dict[str, Any]] | None = getattr(self.multiworld, RE_GEN_PASSTHROUGH_ATTR, {})  # pyright: ignore[reportExplicitAny]
        if not re_gen_passthrough or not self.game in re_gen_passthrough:
            return
        slot_data: dict[str, Any] = re_gen_passthrough[self.game]  # pyright: ignore[reportExplicitAny]
        #TODO pull YAML and rando stuff here

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

