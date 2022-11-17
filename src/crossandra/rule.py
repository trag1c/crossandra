from __future__ import annotations

from dataclasses import dataclass
from re import compile, RegexFlag
from typing import Any, Callable, Generic, Iterator, TypeVar


T = TypeVar("T")


@dataclass
class Rule(Generic[T]):
    pattern: str
    converter: Callable[[str], T] | None = None
    flags: RegexFlag | int = 0

    def __post_init__(self) -> None:
        self._pattern = compile(self.pattern, self.flags)

    def __or__(self, other: Any) -> RuleGroup:
        if isinstance(other, Rule):
            return RuleGroup((self, other))
        return NotImplemented

    def apply(self, target: str) -> tuple[T | str, int] | None:
        if m := self._pattern.match(target):
            end = m.span()[1]
            matched = m[0]
            if self.converter:
                return self.converter(matched), end
            return matched, end
        return None


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
