from .rule import Rule, RuleGroup

_digit = r"[0-9]"
_int = r"[0-9]+"
_decimal = rf"{_int}\.{_int}?|\.{_int}"
_hexdigit = r"[0-9A-Fa-f]"
_letter = r"[A-Za-z]"
_string_base = r".*?(?<!\\)(\\\\)*?"

SINGLE_QUOTED_STRING: Rule[str] = Rule(rf"'{_string_base}'")
DOUBLE_QUOTED_STRING: Rule[str] = Rule(rf'"{_string_base}"')
STRING: RuleGroup = SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING
CHAR: Rule[str] = Rule(r"'.'")
LETTER: Rule[str] = Rule(_letter)
WORD: Rule[str] = Rule(rf"{_letter}+")
DIGIT: Rule[int] = Rule(_digit, int)
INT: Rule[int] = Rule(_int, int)
SIGNED_INT: Rule[int] = Rule(r"[+\-]" + _int, int)
DECIMAL: Rule[float] = Rule(_decimal, float)
HEXDIGIT: Rule[int] = Rule(_hexdigit, lambda n: int(n, 16))
C_NAME: Rule[str] = Rule(rf"(?:_|{_letter})(?:_|{_letter}|{_digit})*")
NEWLINE: Rule[str] = Rule(r"\n")

_exp = rf"[eE]{SIGNED_INT.pattern}"
_float = rf"{_int}{_exp}|{_decimal}{_exp}?"
FLOAT: Rule[float] = Rule(_float, float)
SIGNED_FLOAT: Rule[float] = Rule(r"[+\-" + _float, float)
NUMBER: RuleGroup = INT | FLOAT
SIGNED_NUMBER: RuleGroup = SIGNED_INT | SIGNED_FLOAT
