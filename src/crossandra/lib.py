from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import Any, Union

from result import Err, Ok, Result

from .rule import Ignored, NotApplied, Rule, RuleGroup


def invert_enum(enum: type[Enum]) -> dict[str, Enum]:
    return {v.value: v for v in enum.__members__.values()}


Tree = dict[str, Union[Enum, "Tree"]]


def generate_tree(inp: Iterable[tuple[str, Enum]]) -> Tree:
    inp = sorted(inp, key=lambda v: len(v[0]), reverse=True)
    result: Tree = {}
    for k, v in inp:
        curr = result
        for c in k[:-1]:
            _curr = curr.setdefault(c, {})
            assert isinstance(_curr, dict)
            curr = _curr
        k = k[-1]
        if (dct := curr.get(k)):
            assert isinstance(dct, dict)
            dct[""] = v
        else:
            curr[k] = v
    return result


class Empty(Enum):
    pass


class CrossandraError(Exception):
    pass


class Crossandra:
    __slots__ = (
        "__rules",
        "__fast",
        "__ignored",
        "__keys",
        "__maxlen",
        "__suppress",
        "__tokens",
        "__tree",
    )

    def __init__(
        self,
        token_source: type[Enum] = Empty,
        *,
        ignore_whitespace: bool = False,
        ignored_characters: str = "",
        suppress_unknown: bool = False,
        rules: list[Rule[Any] | RuleGroup] | None = None,
    ) -> None:
        self.__rules: list[Rule[Any]] = []
        for r in rules or []:
            if isinstance(r, RuleGroup):
                self.__rules.extend(r)
            else:
                self.__rules.append(r)
        self.__tokens = invert_enum(token_source)
        self.__fast = all(len(k) == 1 for k in self.__tokens) and not rules
        self.__ignored = " \f\t\v\r\n" * ignore_whitespace + ignored_characters
        self.__keys = sorted(self.__tokens, key=len, reverse=True)
        self.__maxlen = max(map(len, self.__keys or ["1"]))
        self.__suppress = suppress_unknown
        self.__tree = generate_tree(self.__tokens.items())

    def tokenize(self, code: str) -> list[Enum | Any]:
        code = code.replace("\r\n", "\n") + " " * (" " in self.__ignored)

        if self.__fast:
            toks = self.__tokenize_fast(code)
            if toks.is_ok():
                return toks.unwrap()
            raise CrossandraError(f"invalid token: {toks.unwrap_err()!r}")

        tokens: list[Enum | Any] = []
        maxlen = self.__maxlen
        ignored = self.__ignored
        t_append = tokens.append
        while code := code.lstrip(ignored):
            token, length = self.__handle(code[:maxlen])
            if token.is_ok():
                t_append(token.unwrap())
                code = code[length:]
                continue
            for rule in self.__rules:
                tok = rule.apply(code)
                if not isinstance(tok, NotApplied):
                    token_, length = tok
                    if not isinstance(token_, Ignored):
                        t_append(token_)
                    code = code[length:]
                    break
            else:
                if not self.__suppress:
                    raise CrossandraError(f"invalid token: {token.unwrap_err()!r}")
                code = code[1:]

        return tokens

    def tokenize_lines(self, code: str) -> list[list[Enum]]:
        return list(map(self.tokenize, code.splitlines()))

    def __handle(self, string: str) -> tuple[Result[Enum, str], int]:
        tree = self.__tree
        for i, v in enumerate(string):
            c = tree.get(v)
            if c is None:
                if "" not in tree:
                    break
                c = tree[""]
                assert isinstance(c, Enum)
                return Ok(c), i
            if isinstance(c, Enum):
                return Ok(c), i + 1
            tree = c
        return Err(string[0]), 0

    def __tokenize_fast(self, code: str) -> Result[list[Enum], str]:
        tokens: list[Enum] = []
        append = tokens.append
        ignored = self.__ignored
        suppress = self.__suppress
        source = self.__tokens
        for char in code:
            if char in ignored:
                continue
            if (t := source.get(char)) is None:
                if suppress:
                    continue
                return Err(char)
            append(t)
        return Ok(tokens)
