from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from re import RegexFlag, compile
from typing import Any, Generic, TypeVar


class Ignored:
    pass


class NotApplied:
    pass


IGNORED: Ignored = Ignored()
NOT_APPLIED: NotApplied = NotApplied()
T = TypeVar("T")


class Rule(Generic[T]):
    """
    Used for defining custom rules. `pattern` is a regex pattern to
    match (`flags` can be supplied).

    When `converter` is a callable, it will be called with the matched
    substring as the argument.
    When `True`, it will directly return the matched substring.
    When `False`, the matched substring will be excluded from output.
    """

    __slots__ = ("pattern", "converter", "flags", "_pattern")
    pattern: str
    converter: Callable[[str], T] | bool
    flags: RegexFlag | int

    def __init__(
        self,
        pattern: str,
        converter: Callable[[str], T] | bool = True,
        flags: RegexFlag | int = 0,
    ) -> None:
        self.pattern = pattern
        self.converter = converter
        self.flags = flags
        self._pattern = compile(pattern, flags)

    def __or__(self, other: Any) -> RuleGroup:
        if isinstance(other, Rule):
            return RuleGroup((self, other))
        return NotImplemented

    def apply(self, target: str) -> tuple[T | str | Ignored, int] | NotApplied:
        """
        Checks if `target` matches the Rule's pattern. If it does,
        returns a tuple with
        - if the Rule's converter is `False`: the `Ignored` sentinel
        - if the Rule's converter is `True`: the matched substring
        - otherwise: the result of calling the Rule's converter on the
            matched substring

        and the length of the matched substring. If it doesn't, returns
        the `NotApplied` sentinel.
        """
        if m := self._pattern.match(target):
            end = m.span()[1]
            matched = m[0]
            conv = self.converter
            if isinstance(conv, bool):
                if conv:
                    return matched, end
                return IGNORED, end
            return conv(matched), end
        return NOT_APPLIED


@dataclass(frozen=True)
class RuleGroup:
    """
    Used for storing multiple Rules in one object. Can be constructed
    with a tuple of rules or by ORing (`|`) two or more rules.
    """
    rules: tuple[Rule[Any], ...]

    def __iter__(self) -> Iterator[Rule[Any]]:
        yield from self.rules

    def __or__(self, other: Any) -> RuleGroup:
        if isinstance(other, RuleGroup):
            return RuleGroup((*self.rules, *other.rules))
        if isinstance(other, Rule):
            return RuleGroup((*self.rules, other))
        return NotImplemented
