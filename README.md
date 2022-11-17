# Crossandra
Crossandra is a simple tokenizer operating on enums with a decent amount of configuration.

## Installation
Crossandra is available on PyPI and can be installed with pip, or any other Python package manager:
```sh
$ pip install crossandra
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead)

## License
Crossandra is licensed under the MIT License.

## Reference
### `Crossandra`
```py
Crossandra(
    token_source: type[Enum] = Empty,
    *,
    ignore_whitespace: bool = False,
    ignored_characters: str = "",
    suppress_unknown: bool = False,
    rules: list[Rule | RuleGroup] | None = None
)
```
- `token_source`: an enum containing all possible tokens (defaults to an empty enum)
- `ignore_whitespace`: whether spaces, tabs, newlines etc. should be ignored
- `ignored_characters`: characters to skip during tokenization
- `suppress_unknown`: whether unknown tokens should continue without throwing an error
- `rules`: a list of additional rules to use

The enum takes priority over the rule list.

---

When all tokens are of length 1 and there are no additional rules, Crossandra will use a simpler tokenization method (the so called Fast Mode).

> **Example:** Tokenizing noisy Brainfuck code *(tested on MacBook Air M1 (256/16))*

```py
# Setup
from random import choices
from string import punctuation

program = "".join(choices(punctuation, k=...))
```

k      | Default  | Fast Mode | Speedup
:---:  | :---:    | :---:     | :---:
10     | 0.00004s | 0.00002s  | 2x
100    | 0.00016s | 0.00003s  | 5.3x
1000   | 0.0015s  | 0.00013s  | 11.5x
10000  | 0.014s   | 0.0009s   | 15.6x
100000 | 0.29s    | 0.009s    | 32.2x


### `Rule`
```py
Rule[T](
    pattern: str,
    converter: Callable[[str], T] | bool = True,
    flags: RegexFlag | int = 0
)
```
Used for defining custom rules. `pattern` is a regex pattern to match (`flags` can be supplied).  
When `converter` is a callable, it's used on the matched substring.  
When `converter` is `True`, it will directly return the matched substring.  
When `converter` is `False`, it will not include the matched substring in the token list.

### `RuleGroup`
```py
RuleGroup(rules: tuple[Rule[Any], ...])
```
Used for storing multiple Rules in one object. Can be constructed by ORing two or more Rules.

### `common`
The `common` submodule is a collection of commonly used patterns.

Rules:
- CHAR (e.g. `'h'`)
- LETTER (e.g. `m`)
- WORD (e.g. `ball`)
- SINGLE_QUOTED_STRING (e.g. `'nice fish'`)
- DOUBLE_QUOTED_STRING (e.g. `"hello there"`)
- C_NAME (e.g. `crossandra_rocks`)
- NEWLINE (`\n`; `\r\n` is converted to `\n` before tokenization)
- DIGIT (e.g. `7`)
- HEXDIGIT (e.g. `c`)
- DECIMAL (e.g. `3.14`)
- INT (e.g. `2137`)
- SIGNED_INT (e.g. `-1`)
- FLOAT (e.g. `1e3`)
- SIGNED_FLOAT (e.g. `+4.3`)

RuleGroups:
- STRING (`SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING`)
- NUMBER (`INT | FLOAT`)
- SIGNED_NUMBER (`SIGNED_INT | SIGNED_FLOAT`)


## Examples
```py
from enum import Enum
from crossandra import Crossandra

class Brainfuck(Enum):
    ADD = "+"
    SUB = "-"
    LEFT = "<"
    RIGHT = ">"
    READ = ","
    WRITE = "."
    BEGIN_LOOP = "["
    END_LOOP = "]"

bf = Crossandra(Brainfuck, suppress_unknown=True)
print(*bf.tokenize("cat program: ,[.,]"), sep="\n")
# Brainfuck.READ
# Brainfuck.BEGIN_LOOP
# Brainfuck.WRITE
# Brainfuck.READ
# Brainfuck.END_LOOP
```
```py
from crossandra import Crossandra, Rule, common

def hex2rgb(hex_color: str) -> tuple[int, int, int]:
    r, g, b = (int(hex_color[i:i+2], 16) for i in range(1, 6, 2))
    return r, g, b

t = Crossandra(
    ignore_whitespace=True,
    rules=[
        Rule(r"#[0-9a-fA-F]+", hex2rgb),
        common.WORD
    ]
)

text = "My favorite color is #facade"
print(t.tokenize(text))
# ['My', 'favorite', 'color', 'is', (250, 202, 222)]
```
```py
# Supporting Samarium's numbers and arithmetic operators
from enum import Enum
from crossandra import Crossandra, Rule

def sm_int(string: str) -> int:
    return int(string.replace("/", "1").replace("\\", "0"), 2)

class Op(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "++"
    DIV = "--"
    POW = "+++"
    MOD = "---"

sm = Crossandra(
    Op,
    ignore_whitespace=True,
    rules=[Rule(r"(?:\\|/)+", sm_int)]
)

print(*sm.tokenize(r"//\ ++ /\\/ --- /\/\/ - ///"))
# 6 Op.MUL 9 Op.MOD 21 Op.SUB 7
```