import pytest

from crossandra.common import *
from crossandra.rule import *


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("''", ("''", 2)),  # EMPTY STRING
        ("'test'", ("'test'", 6)),  # NORMAL STRING
        ("'''", ("''", 2)),  # STRING CONTAINING QUOTE
        ("test", NOT_APPLIED),  # NO QUOTE
        ("test'", NOT_APPLIED),  # NO STARTING QUOTE
        ("'test", NOT_APPLIED),  # NO ENDING QUOTE
        ("\\'test'", NOT_APPLIED),  # ESCAPED STARTING QUOTE
        ("'test\\'", NOT_APPLIED),  # ESCAPED ENDING QUOTE
    ],
)
def test_SINGLE_QUOTED_STRING(string, result):
    assert SINGLE_QUOTED_STRING.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ('""', ('""', 2)),  # EMPTY STRING
        ('"test"', ('"test"', 6)),  # NORMAL STRING
        ('"""', ('""', 2)),  # STRING CONTAINING QUOTE
        ("test", NOT_APPLIED),  # NO QUOTE
        ('test"', NOT_APPLIED),  # NO STARTING QUOTE
        ('"test', NOT_APPLIED),  # NO ENDING QUOTE
        ('\\"test"', NOT_APPLIED),  # ESCAPED STARTING QUOTE
        ('"test\\"', NOT_APPLIED),  # ESCAPED ENDING QUOTE
    ],
)
def test_DOUBLE_QUOTED_STRING(string, result):
    assert DOUBLE_QUOTED_STRING.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("''", NOT_APPLIED),  # EMPTY CHAR
        ("'t'", ("'t'", 3)),  # NORMAL CHAR
        ("'''", ("'''", 3)),  # SINGLE QUOTE CHAR
        ("t", NOT_APPLIED),  # NO QUOTE
        ("t'", NOT_APPLIED),  # NO STARTING QUOTE
        ("'t", NOT_APPLIED),  # NO ENDING QUOTE
        ("\\'t'", NOT_APPLIED),  # ESCAPED STARTING QUOTE
        ("'t\\'", NOT_APPLIED),  # ESCAPED ENDING QUOTE
    ],
)
def test_CHAR(string, result):
    assert CHAR.apply(string) == result
