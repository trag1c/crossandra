"""A collection of commonly used Rules."""
from .rule import Rule, RuleGroup

_int = r"[0-9](?:[0-9_]*[0-9])?"
_string_base = r".*?(?<!\\)(\\\\)*?"
_exp = rf"(?:[eE][+\-]?{_int})"
_float = rf"{_int}{_exp}|(?:{_int}\.[0-9]*|\.[0-9]+){_exp}?"


def int_(string: str, *, base: int = 10) -> int:
    return int(string.replace("_", ""), base)


def float_(string: str) -> float:
    return float(string.replace("_", ""))


CHAR: Rule[str] = Rule(r"'(?:[^']|\\')'")
"""A single character enclosed in single quotes (e.g. `'h'`)."""
SINGLE_QUOTED_STRING: Rule[str] = Rule(rf"'{_string_base}'")
"""A string enclosed in single quotes (e.g. `'nice fish'`)."""
DOUBLE_QUOTED_STRING: Rule[str] = Rule(rf'"{_string_base}"')
"""A string enclosed in double quotes (e.g. `"hello there"`)."""
LETTER: Rule[str] = Rule(r"[A-Za-z]")
"""An English letter (e.g. `m`). Case insensitive."""
WORD: Rule[str] = Rule(r"[A-Za-z]+")
"""An English word (e.g. `ball`). Case insensitive."""
C_NAME: Rule[str] = Rule(r"[_A-Za-z][_A-Za-z\d]*")
"""
A C-like variable name (e.g. `crossandra_rocks`). Can consist of English
letters, digits, and underscores. Cannot start with a digit.
"""
NEWLINE: Rule[str] = Rule(r"\r?\n")
r"""
A newline character (`\n`, `\r\n` is converted to `\n` before
tokenization).
"""

DIGIT: Rule[int] = Rule(r"\d", int)
"""A single digit (e.g. `7`)."""
HEXDIGIT: Rule[int] = Rule(r"[0-9A-Fa-f]", lambda n: int_(n, base=16))
"""A single hexadecimal digit (e.g. `c`). Case insensitive."""
INT: Rule[int] = Rule(_int, int_)
"""An integer (e.g. `2_137`). Underscores can be used as separators."""
SIGNED_INT: Rule[int] = Rule(r"[+\-]" + _int, int_)
"""
A signed integer (e.g. `-1`).
Underscores can be used as separators.
"""

DECIMAL: Rule[float] = Rule(rf"{_int}\.(?:[0-9]+)?|\.[0-9]+", float_)
"""A decimal value (e.g. `3.14`)."""
FLOAT: Rule[float] = Rule(_float, float_)
"""A floating point value (e.g. `1e3`)."""
SIGNED_FLOAT: Rule[float] = Rule(rf"[+\-](?:{_float})", float_)
"""A signed floating point value (e.g. `+4.3`)."""

STRING: RuleGroup = SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING
"""A string enclosed in either single or double quotes."""
NUMBER: RuleGroup = INT | FLOAT
"""A number (either an integer or a floating point value)."""
SIGNED_NUMBER: RuleGroup = SIGNED_INT | SIGNED_FLOAT
"""A signed number (either an integer or a floating point value)."""
