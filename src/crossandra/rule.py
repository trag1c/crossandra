from __future__ import annotations

from dataclasses import dataclass
from re import RegexFlag, compile
from typing import Any, Callable, Generic, Iterator, TypeVar


class Ignored:
    pass


class NotApplied:
    pass


IGNORED = Ignored()
NOT_APPLIED = NotApplied()
T = TypeVar("T")


class Rule(Generic[T]):
    __slots__ = ("pattern", "converter", "flags", "_pattern")

    def __init__(self, pattern: str, converter: Callable[[str], T] | bool = True, flags: RegexFlag | int = 0) -> None:
        self.pattern = pattern
        self.converter = converter
        self.flags = flags
        self._pattern = compile(self.pattern, self.flags)

    def __or__(self, other: Any) -> RuleGroup:
        if isinstance(other, Rule):
            return RuleGroup((self, other))
        return NotImplemented

    def apply(self, target: str) -> tuple[T | str | Ignored, int] | NotApplied:
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
    rules: tuple[Rule[Any], ...]

    def __iter__(self) -> Iterator[Rule[Any]]:
        yield from self.rules

    def __or__(self, other: Any) -> RuleGroup:
        if isinstance(other, RuleGroup):
            return RuleGroup((*self.rules, *other.rules))
        if isinstance(other, Rule):
            return RuleGroup((*self.rules, other))
        return NotImplemented
