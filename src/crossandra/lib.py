from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import Any, Dict, Union, cast

from result import Err, Ok, Result

from .exceptions import CrossandraTokenizationError
from .rule import Ignored, NotApplied, Rule, RuleGroup


def invert_enum(enum: type[Enum]) -> dict[str, Enum]:
    out = {}
    for v in enum.__members__.values():
        if isinstance(v.value, tuple):
            for i in v.value:
                out[i] = v
        else:
            out[v.value] = v
    return out


Tree = Dict[str, Union[Enum, "Tree"]]


def empty_handler(string: str) -> tuple[Result[Enum, str], int]:
    return Err(string[0]), 1


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
        if dct := curr.get(k):
            assert isinstance(dct, dict)
            dct[""] = v
        else:
            curr[k] = v
    return result


class Empty(Enum):
    """An empty enum. Used by Crossandra if no enum is supplied."""


class Crossandra:
    """
    A Crossandra tokenizer. Takes the following arguments:
    - `token_source`: an enum containing all possible tokens (defaults
      to an empty enum)
    - `convert_crlf`: whether `\\r\\n` should be converted to `\\n` before tokenization
    - `ignored_characters`: a string of characters to ignore (defaults to "")
    - `ignore_whitespace`: whether spaces, tabs, newlines etc. should
      be ignored (defaults to False)
    - `suppress_unknown`: whether unknown token errors should be suppressed
      (defaults to False)
    - `rules`: a list of additional rules to use

    The enum takes priority over the rule list.\\
    The list of rules is ordered by priority (descending).
    """

    __slots__ = (
        "__rules",
        "__conv_crlf",
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
        convert_crlf: bool = True,
        ignore_whitespace: bool = False,
        ignored_characters: str = "",
        rules: list[Rule[Any] | RuleGroup] | None = None,
        suppress_unknown: bool = False,
    ) -> None:
        self.__rules: list[Rule[Any]] = []
        for r in rules or []:
            if isinstance(r, RuleGroup):
                self.__rules.extend(r)
            else:
                self.__rules.append(r)
        self.__conv_crlf = convert_crlf
        self.__tokens = invert_enum(token_source)
        self.__fast = all(len(k) == 1 for k in self.__tokens) and not rules
        self.__ignored = " \f\t\v\r\n" * ignore_whitespace + ignored_characters
        self.__keys = sorted(self.__tokens, key=len, reverse=True)
        self.__maxlen = max(map(len, self.__keys or ["1"]))
        self.__suppress = suppress_unknown
        self.__tree = generate_tree(self.__tokens.items())

    def tokenize(self, code: str) -> list[Enum | Any]:
        """
        Tokenizes the input string. Returns a list of tokens.
        """
        if self.__conv_crlf:
            code = code.replace("\r\n", "\n")
        if " " in self.__ignored:
            code += " "

        if self.__fast:
            toks = self.__tokenize_fast(code)
            if toks.is_ok():
                return toks.unwrap()
            raise CrossandraTokenizationError(f"invalid token: {toks.unwrap_err()!r}")

        tokens: list[Enum | Any] = []
        maxlen = self.__maxlen
        ignored = self.__ignored
        t_append = tokens.append
        handle = self.__handle if self.__tokens else empty_handler
        while code := code.lstrip(ignored):
            token, length = handle(code[:maxlen])
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
                    raise CrossandraTokenizationError(
                        f"invalid token: {token.unwrap_err()!r}"
                    )
                code = code[1:]

        return tokens

    def tokenize_lines(self, code: str) -> list[list[Enum | Any]]:
        """
        Tokenizes the input string line by line. Returns a nested list
        of tokens, where each inner list corresponds to a consecutive
        line of the input string. Equivalent to
        `[foo.tokenize(line) for line in source.splitlines()]`.
        """
        return list(map(self.tokenize, code.splitlines()))

    def __handle(self, string: str) -> tuple[Result[Enum, str], int]:
        tree = self.__tree
        break_path: tuple[Enum, int] | None = None

        for i, v in enumerate(string):
            if "" in tree:
                break_path = (cast(Enum, tree[""]), i)

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

        if break_path:
            return Ok(break_path[0]), break_path[1]

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
