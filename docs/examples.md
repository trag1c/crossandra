## Brainfuck
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
## Word tokenization with HEX2RGB conversion
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
## Supporting [Samarium]'s numbers and arithmetic operators
```py
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

[Samarium]: https://github.com/samarium-lang/samarium
