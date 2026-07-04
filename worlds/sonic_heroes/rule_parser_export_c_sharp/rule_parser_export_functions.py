"""
Functions used by the parser for exporting to C#
"""

def get_parsed_export_entry_str(entry_class_name: str, params: dict[str, str]) -> str:
    _result: str = f"new {entry_class_name}("

    for key, value in params.items():
        _result += f"{key}: {value}, "
    if _result[-2:] == ", ":
        _result = _result[:-2]

    _result += ")"
    return _result



