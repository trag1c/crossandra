from __future__ import annotations

import re
from enum import Enum

import pytest
from crossandra import (
    Crossandra,
    common,
    CrossandraTokenizationError,
    CrossandraValueError,
    Rule,
    RuleGroup
)
from crossandra.rule import IGNORED, NOT_APPLIED


@pytest.mark.parametrize(
    ["convert_crlf", "result"],
    [
        (True, ["a", "\n", "b", "\n", "c"]),
        (False, ["a", "\n", "b", "\r\n", "c"]),
    ]
)
def test_convert_crlf(convert_crlf, result):
    assert Crossandra(
        rules=[common.LETTER, common.NEWLINE],
        convert_crlf=convert_crlf
    ).tokenize("a\nb\r\nc") == result


@pytest.mark.parametrize(
    ["ignored", "result"],
    [
        ("", list("abbadeff")),
        ("ae", list("bbdff")),
        ("abdef", []),
        ("abdf", ["e"]),
        ("aaaaa", list("bbdeff")),
        ("fg", list("abbade")),
    ]
)
def test_ignored_characters(ignored, result):
    assert Crossandra(
        rules=[common.LETTER],
        ignored_characters=ignored
    ).tokenize("abbadeff") == result


def test_ignore_whitespace_error():
    with pytest.raises(CrossandraTokenizationError):
        Crossandra(rules=[common.LETTER]).tokenize("a b")


def test_ignore_whitespace():
    assert Crossandra(
        rules=[common.LETTER],
        ignore_whitespace=True
    ).tokenize("a b\nc\rde") == ["a", "b", "c", "d", "e"]


def test_suppress_unknown_error():
    with pytest.raises(CrossandraTokenizationError):
        Crossandra().tokenize("a")


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("1", []),
        ("hello there", ["hello", "there"]),
        ("hello1", ["hello"]),
        ("", []),
        ("$%&^", []),
        ("hi.123-world", ["hi", "world"]),
        (
            "Mr. John Smith Jr. was born in the U.S.A.",
            "Mr John Smith Jr was born in the U S A".split()
        )
    ]
)
def test_suppress_unknown(string, result):
    assert Crossandra(
        suppress_unknown=True,
        rules=[common.WORD]
    ).tokenize(string) == result


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


def test_fast():
    assert Crossandra(BrainfuckToken)._Crossandra__fast  # type: ignore


def test_not_fast_long_tokens():
    assert not Crossandra(ArithmeticToken)._Crossandra__fast  # type: ignore


def test_not_fast_rules():
    assert not Crossandra(BrainfuckToken, rules=[common.NEWLINE])._Crossandra__fast  # type: ignore


def test_tokenize_fast():
    assert Crossandra(
        BrainfuckToken,
        suppress_unknown=True
    ).tokenize("cat program: ,[.,]") == [
        BrainfuckToken.READ,
        BrainfuckToken.BEGIN_LOOP,
        BrainfuckToken.WRITE,
        BrainfuckToken.READ,
        BrainfuckToken.END_LOOP
    ]


@pytest.mark.parametrize(
    ["expression", "result"],
    [
        ("2 * 2 + 3 - 7", [2, AT.MUL, 2, AT.ADD, 3, AT.SUB, 7]),
        ("2**3", [2, AT.POW, 3]),
        ("-5", [AT.SUB, 5]),
        ("100 + -5", [100, AT.ADD, AT.SUB, 5]),
        ("4 - 2 ** 5 / 2", [4, AT.SUB, 2, AT.POW, 5, AT.DIV, 2]),
        ("10 % 3", [10, AT.MOD, 3])
    ]
)
def test_tokenize(expression, result):
    assert Crossandra(
        ArithmeticToken,
        rules=[common.INT],
        suppress_unknown=True
    ).tokenize(expression) == result


def test_rule_conflict():
    with pytest.raises(CrossandraValueError):
        Rule(r"", int, ignore=True)


def test_rule_ignore():
    assert Rule(r"\d", ignore=True).apply("1") == (IGNORED, 1)


def test_rule_not_applied():
    assert Rule(r"\d").apply("x") is NOT_APPLIED


def test_rule_converter():
    assert Rule(r"\d", int).apply("1") == (1, 1)


def test_rule():
    assert Rule(r"\d").apply("1") == ("1", 1)


@pytest.mark.parametrize(
    ["flags", "result"],
    [
        (0, NOT_APPLIED),
        (re.I, ("A", 1)),
        (re.I | re.S, ("A\nb", 3))
    ]
)
def test_flags(flags, result):
    assert Rule(r"a.?b?", flags=flags).apply("A\nb") == result


def test_rule_group():
    a, b = Rule("a"), Rule("b")
    x, y = a | b
    p, r = RuleGroup((a, b))
    assert (a, b) == (x, y) == (p, r)
