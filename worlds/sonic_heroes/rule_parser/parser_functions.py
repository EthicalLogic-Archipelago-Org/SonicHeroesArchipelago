"""
Functions used by the rule parser
"""
import enum

from worlds.sonic_heroes.constants.enemies import SonicHeroesEnemy


def get_func_str(func_name: str, params: dict[str, str | int | bool | enum.Enum | SonicHeroesEnemy]) -> str:
    if func_name == "":
        # return "True_[SonicHeroesWorldBase]()"
        return "None"
    if func_name == "NOTPOSSIBLE":
        return "False_[SonicHeroesWorldBase]()"

    _result: str = f"{func_name}("
    param_names: list[str] = list(params.keys())
    for index, name in enumerate(param_names):
        if index > 0:
            _result += ", "

        if issubclass(params[name].__class__, SonicHeroesEnemy):
            # noinspection PyUnresolvedReferences
            _result += f"{name}={params[name].get_func_str()}"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        elif issubclass(params[name].__class__, enum.Enum):
            # noinspection PyUnresolvedReferences
            _result += f"{name}={params[name].__class__.__name__}.{params[name].name}"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        elif isinstance(params[name], str):
            _result += f"{name}=\"{params[name]}\""
        else:
            _result += f"{name}={params[name]}"

    _result += ")"
    return _result




