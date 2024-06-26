from __future__ import annotations

from dataclasses import dataclass
from re import Pattern, RegexFlag, compile
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .exceptions import CrossandraValueError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


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

    A `converter` can be supplied and will be called with the matched substring as the
    argument (defaults to None, returning the matched string directly).
    When `ignore` is True, the matched substring will be excluded from output.
    """

    __slots__ = (
        "__compiled_pattern",
        "__converter",
        "__flags",
        "__ignore",
        "__pattern",
    )

    def __init__(
        self,
        pattern: Pattern[str] | str,
        converter: Callable[[str], T] | None = None,
        *,
        flags: RegexFlag | int = 0,
        ignore: bool = False,
    ) -> None:
        if ignore and converter:
            msg = "cannot use a converter when ignore=True"
            raise CrossandraValueError(msg)
        self.__ignore = ignore
        pattern_str = pattern.pattern if isinstance(pattern, Pattern) else pattern
        self.__pattern = pattern_str
        self.__compiled_pattern = compile(pattern_str, flags)
        self.__converter = converter
        self.__flags = flags

    def __hash__(self) -> int:
        return hash((self.pattern, self.ignore or self.converter, self.flags))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rule):
            return hash(self) == hash(other)
        return NotImplemented

    @property
    def converter(self) -> Callable[[str], T] | None:
        return self.__converter

    @property
    def flags(self) -> RegexFlag | int:
        return self.__flags

    @property
    def ignore(self) -> bool:
        return self.__ignore

    @property
    def pattern(self) -> str:
        return self.__pattern

    def __or__(self, other: object) -> RuleGroup:
        if isinstance(other, Rule):
            return RuleGroup((self, other))
        if isinstance(other, RuleGroup):
            return RuleGroup((self, *other.rules))
        return NotImplemented

    def apply(self, target: str) -> tuple[T | str | Ignored, int] | NotApplied:
        """
        Checks if `target` matches the Rule's pattern. If it does,
        returns a tuple with
        - if ignore=True: the `Ignored` sentinel
        - if converter=None: the matched substring
        - otherwise: the result of calling the Rule's converter on the matched substring

        and the length of the matched substring. If it doesn't, returns
        the `NotApplied` sentinel.
        """
        if m := self.__compiled_pattern.match(target):
            end = m.span()[1]
            if self.__ignore:
                return IGNORED, end
            matched = m[0]
            conv = self.__converter
            if conv is None:
                return matched, end
            return conv(matched), end
        return NOT_APPLIED


@dataclass(frozen=True)
class RuleGroup:
    """
    Used for storing multiple Rules in one object. Can be constructed
    by passing in a tuple of rules or by ORing (`|`) two or more rules.
    """

    rules: tuple[Rule[Any], ...]

    def apply(self, target: str) -> tuple[Any | str | Ignored, int] | NotApplied:
        """
        Applies the rules in the group to the target string. Returns the
        result of the first rule that matches, or `NotApplied` if none do.
        """
        for rule in self.rules:
            if (result := rule.apply(target)) is not NOT_APPLIED:
                return result
        return NOT_APPLIED

    def __iter__(self) -> Iterator[Rule[Any]]:
        yield from self.rules

    def __or__(self, other: object) -> RuleGroup:
        if isinstance(other, RuleGroup):
            return RuleGroup((*self.rules, *other.rules))
        if isinstance(other, Rule):
            return RuleGroup((*self.rules, other))
        return NotImplemented
