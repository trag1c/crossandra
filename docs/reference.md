## `Crossandra`
```py
class Crossandra(
    token_source: type[Enum] = Empty,
    *,
    convert_crlf: bool = True,
    ignore_whitespace: bool = False,
    ignored_characters: str = "",
    rules: list[Rule[Any] | RuleGroup] | None = None,
    suppress_unknown: bool = False,
)
```
The core class representing a `Crossandra` tokenizer. Takes the following
arguments:

* `token_source`: an enum containing all possible tokens (defaults to an empty
  enum)
* `convert_crlf`: whether `\r\n` should be converted to `\n` before tokenization
* `ignored_characters`: a string of characters to ignore (defaults to `""`)
* `ignore_whitespace`: whether spaces, tabs, newlines etc. should be ignored
  (defaults to `False`)
* `suppress_unknown`: whether unknown-token errors should be suppressed
  (defaults to `False`)
* `rules`: a list of additional rules to use

The enum takes priority over the rule list.  
The rules are prioritized in the order they appear in the list (descending).

Token enums can allow a tuple of values as aliases:
```py
class MarkdownStyle(Enum):
    BOLD = "**"
    ITALIC = ("_", "*")
    UNDERLINE = "__"
    STRIKETHROUGH = "~~"
    CODE = ("`", "``")


print(
    *Crossandra(MarkdownStyle, ignore_whitespace=True).tokenize("* ** _ __"),
    sep="\n"
)
# <MarkdownStyle.ITALIC: ('*', '_')>
# <MarkdownStyle.BOLD: '**'>
# <MarkdownStyle.ITALIC: ('*', '_')>
# <MarkdownStyle.UNDERLINE: '__'>
```

### `Crossandra.tokenize`
```py
def tokenize(self, code: str) -> list[Enum | Any]
```
Tokenizes the input string. Returns a list of tokens.

### `Crossandra.tokenize_lines`
```py
def tokenize_lines(self, code: str) -> list[list[Enum | Any]]
```
Tokenizes the input string line by line. Returns a nested list of tokens, where
each inner list corresponds to a consecutive line of the input string.
Equivalent to `[foo.tokenize(line) for line in source.splitlines()]`.

### Fast Mode
When all tokens are of length 1 and there are no additional rules, Crossandra
will use a simpler tokenization method (the so called Fast Mode).

!!! example
    Tokenizing noisy Brainfuck code (`BrainfuckToken` taken from
    [examples](examples.md#brainfuck))

    *(tested on MacBook Air M1 (256/16) with pure Python wheels)*
    ```py
    # Setup
    from random import choices
    from string import punctuation

    program = "".join(choices(punctuation, k=...))
    tokenizer = Crossandra(Brainfuck, suppress_unknown=True)
    ```

    log10(k) | Default | Fast Mode | Speedup
    ---      | ---:    | ---:      | ---:
    1        | 40µs    | 20µs      | 100%
    2        | 160µs   | 30µs      | 433%
    3        | 1.5ms   | 130µs     | 1,054%
    4        | 14ms    | 900µs     | 1,456%
    5        | 290ms   | 9ms       | 3,122%


## Rules and rule groups

### `Rule`
```py
class Rule[T](
    pattern: Pattern[str] | str,
    converter: Callable[[str], T] | None = None,
    *,
    flags: RegexFlag | int = 0,
    ignore: bool = False,
)
```
Used for defining custom rules. `pattern` is a regex pattern to match (`flags`
can be supplied). A `converter` can be supplied and will be called with the
matched substring as the argument (defaults to `None`, returning the matched
string directly). When `ignore` is `True`, the matched substring will be
excluded from the output.

`Rule` objects are hashable and comparable and can be ORed (`|`) for grouping
with other `Rule`s and `RuleGroup`s.

#### `Rule.apply`
```py
def apply(self, target: str) -> tuple[T | str | Ignored, int] | NotApplied
```
Checks if `target` matches the Rule's pattern. If it does, returns a tuple with

* if `ignore=True`: the `Ignored` sentinel
* if `converter=None`: the matched substring
* otherwise: the result of calling the Rule's converter on the matched substring

and the length of the matched substring. If it doesn't, returns the `NotApplied`
sentinel.

### `RuleGroup`
```py
class RuleGroup(rules: tuple[Rule[Any], ...])
```
Used for storing multiple Rules in one object. `RuleGroup`s can be constructed
by passing in a tuple of rules or by ORing (`|`) two or more `Rule`s, and they
can be ORed with other `RuleGroup`s or `Rule`s themselves. `RuleGroup`s are
hashable and iterable.

#### `RuleGroup.apply`
```py
def apply(self, target: str) -> tuple[Any | str | Ignored, int] | NotApplied
```
Applies the rules in the group to the target string. Returns the result of the
first rule that matches, or `NotApplied` if none do.


## Common patterns

The `common` submodule is a collection of commonly used patterns.

### Rules
* CHAR (e.g. `'h'`)
* LETTER (e.g. `m`)
* WORD (e.g. `ball`)
* SINGLE_QUOTED_STRING (e.g. `'nice fish'`)
* DOUBLE_QUOTED_STRING (e.g. `"hello there"`)
* C_NAME (e.g. `crossandra_rocks`)
* NEWLINE (`\r\n` or `\n`)
* DIGIT (e.g. `7`)
* HEXDIGIT (e.g. `c`)
* DECIMAL (e.g. `3.14`)
* INT (e.g. `2137`)
* SIGNED_INT (e.g. `-1`)
* FLOAT (e.g. `1e3`)
* SIGNED_FLOAT (e.g. `+4.3`)

### Rule groups
* STRING (`SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING`)
* NUMBER (`INT | FLOAT`)
* SIGNED_NUMBER (`SIGNED_INT | SIGNED_FLOAT`)
* ANY_INT (`INT | SIGNED_INT`)
* ANY_FLOAT (`FLOAT | SIGNED_FLOAT`)
* ANY_NUMBER (`NUMBER | SIGNED_NUMBER`)
