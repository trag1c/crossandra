# Crossandra
Crossandra is a fast and simple tokenization library for Python operating on
enums and regular expressions, with a decent amount of configuration.

## Installation
Crossandra is available on PyPI and can be installed with pip, or any other
Python package manager:
```sh
$ pip install crossandra
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip`
instead)

## [Documentation]

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
        Rule(r"#[0-9a-fA-F]{6}", hex2rgb),
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
    rules=[Rule(r"[\\/]+", sm_int)]
)

print(*sm.tokenize(r"//\ ++ /\\/ --- /\/\/ - ///"))
# 6 Op.MUL 9 Op.MOD 21 Op.SUB 7
```

## Contributing

Contributions are welcome!

Please open an issue before submitting a pull request (unless it's a minor
change like fixing a typo).

To get started:
1. Clone your fork of the project.
2. Set up the project with `just install` (uses [uv]).
3. After you're done, run `just check` to check your changes.

> [!note]
> If you don't want to use [`just`][just], simply look up the recipes
> in the project's [`justfile`][justfile].

## License
Crossandra is licensed under the MIT License.

If you have any questions, or would like to get in touch, join my
[Discord server]!

[Documentation]: https://github.com/trag1c/crossandra/wiki/The-Crossandra-class
[Discord server]: https://discord.gg/C8QE5tVQEq
[just]: https://github.com/casey/just
[justfile]: https://github.com/trag1c/crossandra/blob/main/justfile
[uv]: https://github.com/astral-sh/uv
