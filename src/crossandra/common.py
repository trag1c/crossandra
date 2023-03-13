from .rule import Rule, RuleGroup

_int = r"[0-9](?:[0-9_]*[0-9])?"
_string_base = r".*?(?<!\\)(\\\\)*?"

SINGLE_QUOTED_STRING: Rule[str] = Rule(rf"'{_string_base}'")
DOUBLE_QUOTED_STRING: Rule[str] = Rule(rf'"{_string_base}"')
STRING: RuleGroup = SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING
CHAR: Rule[str] = Rule(r"'(?:[^']|\\')'")
LETTER: Rule[str] = Rule(r"[A-Za-z]")
WORD: Rule[str] = Rule(r"[A-Za-z]+")
DIGIT: Rule[int] = Rule(r"\d", int)
INT: Rule[int] = Rule(_int, int)
SIGNED_INT: Rule[int] = Rule(r"[+\-]" + _int, int)
DECIMAL: Rule[float] = Rule(rf"{_int}\.(?:[0-9]+)?|\.[0-9]+", float)
HEXDIGIT: Rule[int] = Rule(r"[0-9A-Fa-f]", lambda n: int(n, 16))
C_NAME: Rule[str] = Rule(r"[_A-Za-z][_A-Za-z\d]*")
NEWLINE: Rule[str] = Rule(r"\n")

_exp = rf"(?:[eE][+\-]?{_int})"
_float = rf"{_int}{_exp}|(?:{_int}\.[0-9]*|\.[0-9]+){_exp}?"
FLOAT: Rule[float] = Rule(_float, float)
SIGNED_FLOAT: Rule[float] = Rule(rf"[+\-](?:{_float})", float)
NUMBER: RuleGroup = INT | FLOAT
SIGNED_NUMBER: RuleGroup = SIGNED_INT | SIGNED_FLOAT
