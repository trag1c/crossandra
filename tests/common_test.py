import pytest

from crossandra.common import *
from crossandra.rule import *


# ESC = ESCAPED
# UC = UPPERCASE
# LC = LOWERCASE
# POS = POSITIVE
# NEG = NEGATIVE
# USCORE = UNDERSCORD


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("'test'", ("'test'", 6)),  # CLASSIC
        ("'''", ("''", 2)),  # STRING CONTAINING QUOTE
        ("test", NOT_APPLIED),  # NO QUOTE
        ("test'", NOT_APPLIED),  # NO STARTING QUOTE
        ("'test", NOT_APPLIED),  # NO ENDING QUOTE
        ("\\'test'", NOT_APPLIED),  # ESC STARTING QUOTE
        ("'test\\'", NOT_APPLIED),  # ESC ENDING QUOTE
        ("''", ("''", 2)),  # EMPTY
    ],
)
def test_SINGLE_QUOTED_STRING(string, result):
    assert SINGLE_QUOTED_STRING.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ('"test"', ('"test"', 6)),  # CLASSIC
        ('"""', ('""', 2)),  # STRING CONTAINING QUOTE
        ("test", NOT_APPLIED),  # NO QUOTE
        ('test"', NOT_APPLIED),  # NO STARTING QUOTE
        ('"test', NOT_APPLIED),  # NO ENDING QUOTE
        ('\\"test"', NOT_APPLIED),  # ESC STARTING QUOTE
        ('"test\\"', NOT_APPLIED),  # ESC ENDING QUOTE
        ('""', ('""', 2)),  # EMPTY
    ],
)
def test_DOUBLE_QUOTED_STRING(string, result):
    assert DOUBLE_QUOTED_STRING.apply(string) == result


# test_STRING <=> test_SINGLE_QUOTED_STRING and test_DOUBLE_QUOTED_STRING


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("'t'", ("'t'", 3)),  # CLASSIC
        ("'''", ("'''", 3)),  # SINGLE QUOTE CHAR
        ("t", NOT_APPLIED),  # NO QUOTE
        ("t'", NOT_APPLIED),  # NO STARTING QUOTE
        ("'t", NOT_APPLIED),  # NO ENDING QUOTE
        ("\\'t'", NOT_APPLIED),  # ESC STARTING QUOTE
        ("'t\\'", NOT_APPLIED),  # ESC ENDING QUOTE
        ("''", NOT_APPLIED),  # EMPTY
    ],
)
def test_CHAR(string, result):
    assert CHAR.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("A", ("A", 1)),  # UC LETTER
        ("a", ("a", 1)),  # LC LETTER
        ("!", NOT_APPLIED),  # ASCII CHAR BETWEEN UC AND LC
        ("@", NOT_APPLIED),  # ASCII CHAR BEFORE UC
        ("|", NOT_APPLIED),  # ASCII CHAR AFTER LC
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_LETTER(string, result):
    assert LETTER.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("word", ("word", 4)),  # CLASSIC
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_WORD(string, result):
    assert WORD.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("0", (0, 1)),  # CLASSIC
        ("/", NOT_APPLIED),  # CHAR BEFORE DIGITS IN ASCII TABLE
        (":", NOT_APPLIED),  # CHAR AFTER DIGITS IN ASCII TABLE
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_DIGIT(string, result):
    assert DIGIT.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("69", (69, 2)),  # CLASSIC
        ("069", (69, 3)),  # LEADING ZERO
        ("1_000_000", NOT_APPLIED),  # USCORE SEPARATOR  [INCORRECTLY FAILING]
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_INT(string, result):
    assert INT.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("+69", (69, 3)),  # POS INT
        ("-69", (-69, 3)),  # NEG INT
        ("69", NOT_APPLIED),  # NOT SIGNED
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_SIGNED_INT(string, result):
    assert SIGNED_INT.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("3.14", (3.14, 4)),  # CLASSIC
        ("3.0", (3.0, 3)),  # POST-COMMA TRAILING ZERO
        ("69.42", (69.42, 5)),  # N-DIGIT INT BASE
        ("0.92", (0.92, 4)),  # ZERO-DIGIT
        (".92", (0.92, 3)),  # IMPLICIT ZERO-DIGIT
        ("3.", (3.0, 2)),  # IMPLICIT POST-COMMA ZERO
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_DECIMAL(string, result):
    assert DECIMAL.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("3", (3, 1)),  # CLASSIC: DIGIT
        ("D", (13, 1)),  # CLASSIC: UC LETTER
        ("a", (10, 1)),  # CLASSIC: LC LETTER
        ("g", NOT_APPLIED),  # INVALID HEX VALUE
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_HEXDIGIT(string, result):
    assert HEXDIGIT.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("W", ("W", 1)),  # ONE LETTER
        ("_", ("_", 1)),  # ONE USCORE
        ("word", ("word", 4)),  # ONE WORD
        ("two_words", ("two_words", 9)),  # TWO WORDS, USCORE SEP
        ("_word", ("_word", 5)),  # 'PRIVATE' ONE WORD
        ("_two_words", ("_two_words", 10)),  # 'PRIVATE' TWO WORDS, USCORE SEP
        ("0word", NOT_APPLIED),  # LEADING DIGIT
        ("word0", ("word0", 5)),  # TRAILING DIGIT
        ("_0word", ("_0word", 6)),  # 'PRIVATE' LEADING DIGIT
        ("_word0", ("_word0", 6)),  # 'PRIVATE' TRAILING DIGIT
        ("0", NOT_APPLIED),  # SINGLE DIGIT
        ("69420", NOT_APPLIED),  # N-DIGITS
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_C_NAME(string, result):
    assert C_NAME.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("\n", ("\n", 1)),  # LF NEWLINE
        ("\r\n", NOT_APPLIED),  # CRLF NEWLINE
        ("\r", NOT_APPLIED),  # CR NEWLINE
        ("\\n", NOT_APPLIED),  # ESC LF NEWLINE
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_NEWLINE(string, result):
    assert NEWLINE.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("1e3", (1_000.0, 3)),  # INT, LC E, INT
        ("1e+3", (1_000.0, 4)),  # INT, E, POS INT
        ("1e-3", (0.001, 4)),  # INT, E, NEG INT
        ("1E3", (1_000.0, 3)),  # INT, UC E, INT
        ("1.0e3", (1_000.0, 5)),  # DECIMAL, E, INT
        ("1.0e+3", (1_000.0, 6)),  # DECIMAL, E, POS INT
        ("1.0e-3", (0.001, 6)),  # DECIMAL, E, NEG INT
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_FLOAT(string, result):
    assert FLOAT.apply(string) == result


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("+1e3", (1_000.0, 4)),  # POS INT, E, INT [INCORRECTLY FAILING]
        ("-1e3", (-1_000.0, 4)),  # NEG INT, E, INT [INCORRECTLY FAILING]
        ("+1e+3", (1_000.0, 5)),  # POS INT, E, POS INT
        ("+1e-3", (0.001, 5)),  # POS INT, E, NEG INT
        ("+1.0e3", (1_000.0, 6)),  # POS DECIMAL, E, INT [INCORRECTLY FAILING]
        ("-1.0e3", (-1_000.0, 6)),  # NEG DECIMAL, E, INT [INCORRECTLY FAILING]
        ("+1.0e+3", (1_000.0, 7)),  # POS DECIMAL, E, POS INT [INCORRECTLY FAILING]
        ("+1.0e-3", (0.001, 7)),  # POS DECIMAL, E, NEG INT [INCORRECTLY FAILING]
        ("", NOT_APPLIED),  # EMPTY
    ],
)
def test_SIGNED_FLOAT(string, result):
    assert SIGNED_FLOAT.apply(string) == result


# test_NUMBER <=> test_INT and test_FLOAT

# test_SIGNED_NUMBER <=> test_SIGNED_INT and test_SIGNED_FLOAT
