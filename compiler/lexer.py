from compiler.tokens import KEYWORDS, Token, TokenType


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []

        self.start = 0
        self.current = 0

        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column

            self._scan_token()

        self.tokens.append(
            Token(
                TokenType.EOF,
                "",
                None,
                self.line,
                self.column,
            )
        )

        return self.tokens

    def _scan_token(self) -> None:
        character = self._advance()

        single_character_tokens = {
            "=": TokenType.EQUAL,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ";": TokenType.SEMICOLON,
        }

        if character in single_character_tokens:
            self._add_token(single_character_tokens[character])
            return

        if character in " \t\r\n":
            self._scan_whitespace()
            return

        if character.isdigit():
            self._scan_integer()
            return

        if character.isalpha():
            self._scan_identifier()
            return

        raise LexerError(
            f"Unexpected character {character!r} "
            f"at line {self.start_line}, column {self.start_column}"
        )

    def _scan_whitespace(self) -> None:
        while self._peek() in " \t\r\n":
            self._advance()

    def _scan_integer(self) -> None:
        while self._peek().isdigit():
            self._advance()

        lexeme = self.source[self.start:self.current]
        self._add_token(TokenType.INTEGER, int(lexeme))

    def _scan_identifier(self) -> None:
        while self._peek().isalnum():
            self._advance()

        lexeme = self.source[self.start:self.current]
        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)

        literal = None
        if token_type == TokenType.TRUE:
            literal = True
        elif token_type == TokenType.FALSE:
            literal = False

        self._add_token(token_type, literal)

    def _add_token(
        self,
        token_type: TokenType,
        literal: int | bool | None = None,
    ) -> None:
        lexeme = self.source[self.start:self.current]

        self.tokens.append(
            Token(
                token_type,
                lexeme,
                literal,
                self.start_line,
                self.start_column,
            )
        )

    def _advance(self) -> str:
        character = self.source[self.current]
        self.current += 1

        if character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return character

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"

        return self.source[self.current]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
