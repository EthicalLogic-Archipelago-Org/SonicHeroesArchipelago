import enum
from typing import Callable

from worlds.sonic_heroes.constants.char_ability import Team
from worlds.sonic_heroes.constants.stage import Stage



def get_func_str(func_name: str, params: dict[str, str | int | enum.Enum]) -> str:
    if func_name == "":
        return "True_[SonicHeroesWorldBase]()"
    if func_name == "NOTPOSSIBLE":
        return "False_[SonicHeroesWorldBase]()"

    _result: str = f"{func_name}("
    param_names: list[str] = list(params.keys())
    for index, name in enumerate(param_names):
        if index > 0:
            _result += ", "

        if issubclass(params[name].__class__, enum.Enum):
            # noinspection PyUnresolvedReferences
            _result += f"{name}={params[name].__class__.__name__}.{params[name].name}"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        elif isinstance(params[name], str):
            _result += f"{name}=\"{params[name]}\""
        else:
            _result += f"{name}={params[name]}"

    _result += ")"
    return _result




PARSER_ABILITY_MAPPING: dict[str, Callable[[Team, Stage], str]] = \
{
    "BreakThings": lambda team, stage: get_func_str(func_name="can_break_things_rule", params={"team": team, "stage": stage}),
    "BadnikBounce": lambda team, stage: get_func_str(func_name="can_badnik_bounce_rule", params={}),
}


# print(PARSER_ABILITY_MAPPING["BadnikBounce"](Team.DARK, Stage.SEASIDE_HILL))
# print(PARSER_ABILITY_MAPPING["BreakThings"](Team.DARK, Stage.SEASIDE_HILL))
# print(PARSER_ABILITY_MAPPING["BreakThings"]("Hehe", "HASET"))
# print(PARSER_ABILITY_MAPPING["BreakThings"](55, 100))