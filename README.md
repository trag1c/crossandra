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

## License
Crossandra is licensed under the MIT License.

## [Documentation](https://github.com/trag1c/crossandra/wiki/The-Crossandra-class)

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

If you have any questions, or would like to get in touch, join my
[Discord server](https://discord.gg/C8QE5tVQEq)!
