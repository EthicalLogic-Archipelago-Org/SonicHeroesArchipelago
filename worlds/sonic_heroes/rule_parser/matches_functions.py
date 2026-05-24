"""
Functions used by matches (thanks circular dependencies)
"""
import dataclasses
import enum
from typing import Any

from ..constants.enemies import SonicHeroesEnemyBase


def get_str_to_create(obj: Any, print_steps: bool = False) -> str:  # pyright: ignore[reportAny, reportExplicitAny]
    """
    returns a string with the class name and all fields
    useful for the parser to generate Python code to initialize a dataclass instance
    """
    _result: str = f"{obj.__class__.__name__}("  # pyright: ignore[reportAny]
    args_str_list: list[str] = []
    if dataclasses.is_dataclass(obj):  # pyright: ignore[reportAny]
        for field_name, field_value in obj.__dict__.items():  # pyright: ignore[reportAny]
            if dataclasses.is_dataclass(field_value):  # pyright: ignore[reportAny]
                args_str_list.append(f"{field_name}={get_str_to_create(obj=field_value, print_steps=print_steps)}")
            else:
                field_tuple = dataclasses.fields(obj)
                field_obj: dataclasses.Field[Any] = [field for field in field_tuple if field.name == field_name][0]  # pyright: ignore[reportExplicitAny]

                if field_obj.default is not dataclasses.MISSING:
                    if field_value == field_obj.default:  # pyright: ignore[reportAny]
                        continue
                if field_obj.default_factory is not dataclasses.MISSING:
                    if field_value == field_obj.default_factory:
                        continue

                if issubclass(field_value.__class__, enum.Enum):  # pyright: ignore[reportAny]
                    args_str_list.append(f"{field_name}={field_value.__class__.__name__}.{field_value.name}")  # pyright: ignore[reportAny]
                elif isinstance(field_value, str):
                    args_str_list.append(f"{field_name}=\"{field_value}\"")
                else:
                    args_str_list.append(f"{field_name}={field_value}")
        _result += ", ".join(args_str_list)
        _result += ")"
        return _result
    else:
        raise ValueError(f"Obj: {obj}, type: {obj.__class__.__name__} is not dataclass.")  # pyright: ignore[reportAny]


def get_func_str(func_name: str, params: dict[str, str | int | bool | enum.Enum | SonicHeroesEnemyBase]) -> str:
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

        if issubclass(params[name].__class__, SonicHeroesEnemyBase):
            # noinspection PyUnresolvedReferences
            _result += f"{name}={get_str_to_create(obj=params[name])}"
        elif issubclass(params[name].__class__, enum.Enum):
            # noinspection PyUnresolvedReferences
            _result += f"{name}={params[name].__class__.__name__}.{params[name].name}"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        elif isinstance(params[name], str):
            _result += f"{name}=\"{params[name]}\""
        else:
            _result += f"{name}={params[name]}"

    _result += ")"
    return _result



