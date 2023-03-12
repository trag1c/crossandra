import pytest

from crossandra.common import *
from crossandra.rule import *


@pytest.mark.parametrize(
    ["string", "result"],
    [
        ("''", ("''", 2)),  # EMPTY STRING
        ("'test'", ("'test'", 6)),  # NORMAL STRING
        ("test", NOT_APPLIED),  # NO QUOTE
        ("test'", NOT_APPLIED),  # NO START QUOTE
        ("'test", NOT_APPLIED),  # NO END QUOTE
    ],
)
def test_SINGLE_QUOTED_STRING(string, result):
    assert SINGLE_QUOTED_STRING.apply(string) == result
