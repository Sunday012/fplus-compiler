from dataclasses import dataclass
from enum import Enum, auto


class IROp(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    ASSIGN = auto()
    PRINT = auto()
    PRINT_INT = auto()
    PRINT_BOOL = auto()

@dataclass(frozen=True)
class Quadruple:
    operator: IROp
    argument1: str
    argument2: str | None
    result: str | None


@dataclass(frozen=True)
class IRProgram:
    instructions: list[Quadruple]