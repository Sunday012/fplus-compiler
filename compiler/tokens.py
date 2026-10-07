from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()

    # Literals and identifiers
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()

    # Operators
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()

    # End of input
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: int | bool | str | None
    line: int
    column: int


KEYWORDS: dict[str, TokenType] = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}
