"""A collection of commonly used Rules."""
from .rule import Rule, RuleGroup

_int = r"[0-9](?:[0-9_]*[0-9])?"
_string_base = r".*?(?<!\\)(\\\\)*?"


def int_(string: str, *, base: int = 10) -> int:
    return int(string.replace("_", ""), base)


def float_(string: str) -> float:
    return float(string.replace("_", ""))


SINGLE_QUOTED_STRING: Rule[str] = Rule(rf"'{_string_base}'")
DOUBLE_QUOTED_STRING: Rule[str] = Rule(rf'"{_string_base}"')
STRING: RuleGroup = SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING
CHAR: Rule[str] = Rule(r"'(?:[^']|\\')'")
LETTER: Rule[str] = Rule(r"[A-Za-z]")
WORD: Rule[str] = Rule(r"[A-Za-z]+")
DIGIT: Rule[int] = Rule(r"\d", int)
INT: Rule[int] = Rule(_int, int_)
SIGNED_INT: Rule[int] = Rule(r"[+\-]" + _int, int_)
DECIMAL: Rule[float] = Rule(rf"{_int}\.(?:[0-9]+)?|\.[0-9]+", float_)
HEXDIGIT: Rule[int] = Rule(r"[0-9A-Fa-f]", lambda n: int_(n, base=16))
C_NAME: Rule[str] = Rule(r"[_A-Za-z][_A-Za-z\d]*")
NEWLINE: Rule[str] = Rule(r"\n")

_exp = rf"(?:[eE][+\-]?{_int})"
_float = rf"{_int}{_exp}|(?:{_int}\.[0-9]*|\.[0-9]+){_exp}?"
FLOAT: Rule[float] = Rule(_float, float_)
SIGNED_FLOAT: Rule[float] = Rule(rf"[+\-](?:{_float})", float_)
NUMBER: RuleGroup = INT | FLOAT
SIGNED_NUMBER: RuleGroup = SIGNED_INT | SIGNED_FLOAT
