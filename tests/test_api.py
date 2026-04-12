from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING, Any

import pytest

from crossandra import (
    Crossandra,
    CrossandraTokenizationError,
    CrossandraValueError,
    Rule,
    RuleGroup,
    common,
)
from crossandra.lib import invert_enum
from crossandra.rule import IGNORED, NOT_APPLIED

if TYPE_CHECKING:
    from tests.test_common import RuleResult


@pytest.mark.parametrize(
    ("convert_crlf", "result"),
    [
        (True, ["a", "\n", "b", "\n", "c"]),
        (False, ["a", "\n", "b", "\r\n", "c"]),
    ],
)
def test_convert_crlf(convert_crlf: bool, result: list[str]) -> None:
    assert (
        Crossandra(
            rules=[common.LETTER, common.NEWLINE], convert_crlf=convert_crlf
        ).tokenize("a\nb\r\nc")
        == result
    )


@pytest.mark.parametrize(
    ("ignored", "result"),
    [
        ("", list("abbadeff")),
        ("ae", list("bbdff")),
        ("abdef", []),
        ("abdf", ["e"]),
        ("aaaaa", list("bbdeff")),
        ("fg", list("abbade")),
    ],
)
def test_ignored_characters(ignored: str, result: list[str]) -> None:
    assert (
        Crossandra(rules=[common.LETTER], ignored_characters=ignored).tokenize(
            "abbadeff"
        )
        == result
    )


def test_ignore_whitespace_error() -> None:
    with pytest.raises(CrossandraTokenizationError):
        Crossandra(rules=[common.LETTER]).tokenize("a b")


def test_ignore_whitespace() -> None:
    assert Crossandra(rules=[common.LETTER], ignore_whitespace=True).tokenize(
        "a b\nc\rde"
    ) == ["a", "b", "c", "d", "e"]


def test_suppress_unknown_error() -> None:
    with pytest.raises(CrossandraTokenizationError):
        Crossandra().tokenize("a")


@pytest.mark.parametrize(
    ("string", "result"),
    [
        ("1", []),
        ("hello there", ["hello", "there"]),
        ("hello1", ["hello"]),
        ("", []),
        ("$%&^", []),
        ("hi.123-world", ["hi", "world"]),
        (
            "Mr. John Smith Jr. was born in the U.S.A.",
            ["Mr", "John", "Smith", "Jr", "was", "born", "in", "the", "U", "S", "A"],
        ),
    ],
)
def test_suppress_unknown(string: str, result: list[str]) -> None:
    assert (
        Crossandra(suppress_unknown=True, rules=[common.WORD]).tokenize(string)
        == result
    )


@pytest.mark.parametrize(
    ("string", "result"),
    [
        ("1", []),
        ("hello there", [(0, "hello"), (6, "there")]),
        ("hello1", [(0, "hello")]),
        ("", []),
        ("$%&^", []),
        ("hi.123-world", [(0, "hi"), (7, "world")]),
        (
            "Mr. John Smith Jr. was born in the U.S.A.",
            [
                (0, "Mr"),
                (4, "John"),
                (9, "Smith"),
                (15, "Jr"),
                (19, "was"),
                (23, "born"),
                (28, "in"),
                (31, "the"),
                (35, "U"),
                (37, "S"),
                (39, "A"),
            ],
        ),
    ],
)
def test_suppress_unknown_with_positions(
    string: str, result: list[tuple[int, str]]
) -> None:
    assert (
        Crossandra(suppress_unknown=True, rules=[common.WORD]).tokenize(
            string, with_positions=True
        )
        == result
    )


class BrainfuckToken(Enum):
    ADD = "+"
    SUB = "-"
    LEFT = "<"
    RIGHT = ">"
    READ = ","
    WRITE = "."
    BEGIN_LOOP = "["
    END_LOOP = "]"


class ArithmeticToken(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "**"
    MOD = "%"


AT = ArithmeticToken


def test_fast() -> None:
    assert Crossandra(BrainfuckToken).__fast


def test_not_fast_long_tokens() -> None:
    assert not Crossandra(ArithmeticToken).__fast


def test_not_fast_rules() -> None:
    assert not Crossandra(BrainfuckToken, rules=[common.NEWLINE]).__fast


def test_tokenize_fast() -> None:
    assert Crossandra(BrainfuckToken, suppress_unknown=True).tokenize(
        "cat program: ,[.,]"
    ) == [
        BrainfuckToken.READ,
        BrainfuckToken.BEGIN_LOOP,
        BrainfuckToken.WRITE,
        BrainfuckToken.READ,
        BrainfuckToken.END_LOOP,
    ]


def test_tokenize_fast_with_positions() -> None:
    assert Crossandra(BrainfuckToken, suppress_unknown=True).tokenize(
        "cat program: ,[.,]", with_positions=True
    ) == [
        (13, BrainfuckToken.READ),
        (14, BrainfuckToken.BEGIN_LOOP),
        (15, BrainfuckToken.WRITE),
        (16, BrainfuckToken.READ),
        (17, BrainfuckToken.END_LOOP),
    ]


@pytest.mark.parametrize(
    ("expression", "result"),
    [
        ("2 * 2 + 3 - 7", [2, AT.MUL, 2, AT.ADD, 3, AT.SUB, 7]),
        ("2**3", [2, AT.POW, 3]),
        ("-5", [AT.SUB, 5]),
        ("100 + -5", [100, AT.ADD, AT.SUB, 5]),
        ("4 - 2 ** 5 / 2", [4, AT.SUB, 2, AT.POW, 5, AT.DIV, 2]),
        ("10 % 3", [10, AT.MOD, 3]),
    ],
)
def test_tokenize(expression: str, result: list[Any]) -> None:
    assert (
        Crossandra(ArithmeticToken, rules=[common.INT], suppress_unknown=True).tokenize(
            expression
        )
        == result
    )


@pytest.mark.parametrize(
    ("expression", "result"),
    [
        (
            "2 * 2 + 3 - 7",
            [(0, 2), (2, AT.MUL), (4, 2), (6, AT.ADD), (8, 3), (10, AT.SUB), (12, 7)],
        ),
        ("2**3", [(0, 2), (1, AT.POW), (3, 3)]),
        ("-5", [(0, AT.SUB), (1, 5)]),
        ("100 + -5", [(0, 100), (4, AT.ADD), (6, AT.SUB), (7, 5)]),
        (
            "4 - 2 ** 5 / 2",
            [(0, 4), (2, AT.SUB), (4, 2), (6, AT.POW), (9, 5), (11, AT.DIV), (13, 2)],
        ),
        ("10 % 3", [(0, 10), (3, AT.MOD), (5, 3)]),
    ],
)
def test_tokenize_with_positions(
    expression: str, result: list[tuple[int, Any]]
) -> None:
    assert (
        Crossandra(ArithmeticToken, rules=[common.INT], suppress_unknown=True).tokenize(
            expression, with_positions=True
        )
        == result
    )


def test_rule_conflict() -> None:
    with pytest.raises(CrossandraValueError):
        Rule(r"", int, ignore=True)


def test_rule_ignore() -> None:
    assert Rule(r"\d", ignore=True).apply("1") == (IGNORED, 1)


def test_rule_not_applied() -> None:
    assert Rule(r"\d").apply("x") is NOT_APPLIED


def test_rule_converter() -> None:
    assert Rule(r"\d", int).apply("1") == (1, 1)


def test_rule() -> None:
    assert Rule(r"\d").apply("1") == ("1", 1)


@pytest.mark.parametrize(
    ("flags", "result"),
    [
        (0, NOT_APPLIED),
        (re.IGNORECASE, ("A", 1)),
        (re.IGNORECASE | re.DOTALL, ("A\nb", 3)),
    ],
)
def test_flags(flags: re.RegexFlag, result: RuleResult) -> None:
    assert Rule(r"a.?b?", flags=flags).apply("A\nb") == result


def test_rule_group() -> None:
    # type params required until Python 3.13's PEP 696 is here :')
    a, b = Rule[str]("a"), Rule[str]("b")

    x, y = a | b
    p, r = RuleGroup((a, b))

    assert (a, b) == (x, y) == (p, r)


def test_rule_properties() -> None:
    a = Rule[str]("a")
    b = Rule[str]("a")

    assert a == b
    assert a != 1
    assert isinstance(a | a | b, RuleGroup)
    assert isinstance(a | (a | b), RuleGroup)


@pytest.mark.parametrize(
    "rule_or_rulegroup",
    [
        Rule[str]("a"),
        RuleGroup((Rule[str]("a"), Rule[str]("b"))),
    ],
)
def test_rule_group_creation_fail(rule_or_rulegroup: Rule[Any] | RuleGroup) -> None:
    with pytest.raises(TypeError):
        rule_or_rulegroup | 1


def test_invert_enum_with_aliases() -> None:
    class Test(Enum):
        FOO = "1"
        BAR = ("2", "3")

    assert invert_enum(Test) == {"1": Test.FOO, "2": Test.BAR, "3": Test.BAR}


def test_tokenize_lines() -> None:
    assert Crossandra(rules=[common.WORD], ignore_whitespace=True).tokenize_lines(
        "a b\nc\rde"
    ) == [["a", "b"], ["c"], ["de"]]


def test_tokenize_lines_with_positions() -> None:
    assert Crossandra(rules=[common.WORD], ignore_whitespace=True).tokenize_lines(
        "a b\nc\rde", with_positions=True
    ) == [[(0, "a"), (2, "b")], [(0, "c")], [(0, "de")]]


def test_break_path() -> None:
    class Test(Enum):
        X = "ABC"
        Y = "A"
        Z = "B"

    assert Crossandra(Test).tokenize("ABABAABABC") == [
        Test.Y,
        Test.Z,
        Test.Y,
        Test.Z,
        Test.Y,
        Test.Y,
        Test.Z,
        Test.X,
    ]


def test_break_path_with_positions() -> None:
    class Test(Enum):
        X = "ABC"
        Y = "A"
        Z = "B"

    assert Crossandra(Test).tokenize("ABABAABABC", with_positions=True) == [
        (0, Test.Y),
        (1, Test.Z),
        (2, Test.Y),
        (3, Test.Z),
        (4, Test.Y),
        (5, Test.Y),
        (6, Test.Z),
        (7, Test.X),
    ]


def test_tokenize_fast_with_ignored() -> None:
    class Test(Enum):
        FOO = "x"
        BAR = "y"

    assert Crossandra(Test, ignored_characters="z").tokenize("xzy") == [
        Test.FOO,
        Test.BAR,
    ]


def test_tokenize_fast_with_ignored_with_positions() -> None:
    class Test(Enum):
        FOO = "x"
        BAR = "y"

    assert Crossandra(Test, ignored_characters="z").tokenize(
        "xzy", with_positions=True
    ) == [
        (0, Test.FOO),
        (2, Test.BAR),
    ]
