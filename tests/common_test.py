import pytest

from crossandra.common import *
from crossandra.rule import *


def rule_test_f(rule):
    """
    Factory to generate a test from a rule.
    """

    def decorator(func):
        def inner(string, result):
            assert rule.apply(string) == result

        return inner

    return decorator


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
@rule_test_f(SINGLE_QUOTED_STRING)
def test_SINGLE_QUOTED_STRING(string, result):
    pass


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
@rule_test_f(DOUBLE_QUOTED_STRING)
def test_DOUBLE_QUOTED_STRING(string, result):
    pass


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
@rule_test_f(CHAR)
def test_CHAR(string, result):
    pass


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("A", ("A", 1)),  # UPPERCASE LETTER
        ("a", ("a", 1)),  # LOWERCASE LETTER
        ("", NOT_APPLIED),  # EMPTY STRING
        ("!", NOT_APPLIED),  # ASCII CHAR BETWEEN UPPERCASE AND LOWERCASE
        ("@", NOT_APPLIED),  # ASCII CHAR BEFORE UPPERCASE
        ("|", NOT_APPLIED),  # ASCII CHAR AFTER LOWERCASE
    ],
)
@rule_test_f(LETTER)
def test_LETTER(string, result):
    pass


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("word", ("word", 4)),  # NORMAL WORD
        ("", NOT_APPLIED),  # EMPTY STRING
    ],
)
@rule_test_f(WORD)
def test_WORD(string, result):
    pass


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("0", (0, 1)),  # NORMAL DIGIT
        ("", NOT_APPLIED),  # EMPTY STRING
        ("/", NOT_APPLIED),  # CHAR BEFORE DIGITS IN ASCII TABLE
        (":", NOT_APPLIED),  # CHAR AFTER DIGITS IN ASCII TABLE
    ],
)
@rule_test_f(DIGIT)
def test_DIGIT(string, result):
    pass


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("69", (69, 2)),  # NORMAL INT
        ("069", (69, 3)),  # LEADING ZERO
        ("1_000_000", NOT_APPLIED),  # UNDERSCORE SEPARATOR
        ("", NOT_APPLIED),  # EMPTY STRING
    ],
)
@rule_test_f(INT)
def test_INT(string, result):
    pass


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("3.14", (3.14, 4)),  # NORMAL DECIMAL
        ("3.0", (3.0, 3)),  # POST-COMMA TRAILING ZERO
        ("69.42", (69.42, 5)),  # MULTI-DIGIT INT BASE DECIMAL
        ("0.92", (0.92, 4)),  # ZERO DIGIT DECIMAL
        (".92", (0.92, 3)),  # IMPLICIT ZERO DIGIT DECIMAL
        ("3.", NOT_APPLIED),  # IMPLICIT POST-COMMA ZERO
        ("", NOT_APPLIED),  # EMPTY STRING
    ],
)
@rule_test_f(DECIMAL)
def test_DECIMAL(string, result):
    pass
