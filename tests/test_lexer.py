import pytest

from compiler.lexer import Lexer, LexerError
from compiler.tokens import TokenType


def test_scan_program() -> None:
    source = "let x = 42;\nprint(x + 8);\ntrue false"

    tokens = Lexer(source).scan_tokens()

    assert [token.type for token in tokens] == [
        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.PRINT,
        TokenType.LPAREN,
        TokenType.IDENTIFIER,
        TokenType.PLUS,
        TokenType.INTEGER,
        TokenType.RPAREN,
        TokenType.SEMICOLON,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.EOF,
    ]

    assert tokens[3].lexeme == "42"
    assert tokens[3].literal == 42
    assert tokens[12].literal is True
    assert tokens[13].literal is False


def test_scan_identifiers() -> None:
    tokens = Lexer("name user1 temp").scan_tokens()

    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]

    assert [token.lexeme for token in tokens[:-1]] == [
        "name",
        "user1",
        "temp",
    ]


def test_scan_integers() -> None:
    tokens = Lexer("0 7 12345").scan_tokens()

    assert [token.type for token in tokens] == [
        TokenType.INTEGER,
        TokenType.INTEGER,
        TokenType.INTEGER,
        TokenType.EOF,
    ]

    assert [token.literal for token in tokens[:-1]] == [
        0,
        7,
        12345,
    ]


def test_scan_string_with_escapes() -> None:
    tokens = Lexer(r'"hello\n\t\"world\"\\"').scan_tokens()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].lexeme == r'"hello\n\t\"world\"\\"'
    assert tokens[0].literal == 'hello\n\t"world"\\'


def test_unterminated_string_is_rejected() -> None:
    with pytest.raises(
        LexerError,
        match=r"Unterminated string at line 1, column 1",
    ):
        Lexer('"hello').scan_tokens()


def test_unknown_string_escape_is_rejected() -> None:
    with pytest.raises(
        LexerError,
        match=r"Unknown escape sequence \\q",
    ):
        Lexer(r'"hello\q"').scan_tokens()


def test_scan_fixed_tokens() -> None:
    tokens = Lexer("= + - * / ( ) ;").scan_tokens()

    assert [token.type for token in tokens] == [
        TokenType.EQUAL,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]


def test_keywords_are_not_identifiers() -> None:
    tokens = Lexer(
        "let print true false letter printer"
    ).scan_tokens()

    assert [token.type for token in tokens] == [
        TokenType.LET,
        TokenType.PRINT,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]


def test_line_and_column_tracking() -> None:
    tokens = Lexer("let x = 10;\nprint(x);").scan_tokens()

    let_token = tokens[0]
    print_token = tokens[5]

    assert let_token.line == 1
    assert let_token.column == 1

    assert print_token.type == TokenType.PRINT
    assert print_token.line == 2
    assert print_token.column == 1


def test_invalid_character() -> None:
    with pytest.raises(
        LexerError,
        match=r"Unexpected character '@' at line 1, column 9",
    ):
        Lexer("let x = @;").scan_tokens()


def test_underscore_is_rejected() -> None:
    with pytest.raises(
        LexerError,
        match=r"Unexpected character '_'",
    ):
        Lexer("let user_name = 10;").scan_tokens()
