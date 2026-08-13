import pytest

from compiler.ast_nodes import (
    Assignment,
    BinaryExpression,
    BooleanLiteral,
    Identifier,
    IntegerLiteral,
    PrintStatement,
    VariableDeclaration,
)
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserError
from compiler.tokens import TokenType


def parse(source: str):
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()


def test_variable_declaration() -> None:
    program = parse("let score = 42;")

    assert len(program.statements) == 1

    statement = program.statements[0]

    assert isinstance(statement, VariableDeclaration)
    assert statement.name == "score"
    assert isinstance(statement.initializer, IntegerLiteral)
    assert statement.initializer.value == 42


def test_assignment() -> None:
    program = parse("score = 20;")
    statement = program.statements[0]

    assert isinstance(statement, Assignment)
    assert statement.name == "score"
    assert isinstance(statement.value, IntegerLiteral)
    assert statement.value.value == 20


def test_print_statement() -> None:
    program = parse("print(score);")
    statement = program.statements[0]

    assert isinstance(statement, PrintStatement)
    assert isinstance(statement.expression, Identifier)
    assert statement.expression.name == "score"


def test_multiplication_has_higher_precedence() -> None:
    program = parse("let x = 2 + 3 * 4;")
    declaration = program.statements[0]

    assert isinstance(declaration, VariableDeclaration)

    addition = declaration.initializer
    assert isinstance(addition, BinaryExpression)
    assert addition.operator == TokenType.PLUS
    assert isinstance(addition.left, IntegerLiteral)
    assert addition.left.value == 2

    multiplication = addition.right
    assert isinstance(multiplication, BinaryExpression)
    assert multiplication.operator == TokenType.STAR
    assert isinstance(multiplication.left, IntegerLiteral)
    assert multiplication.left.value == 3
    assert isinstance(multiplication.right, IntegerLiteral)
    assert multiplication.right.value == 4


def test_parentheses_change_precedence() -> None:
    program = parse("let x = (2 + 3) * 4;")
    declaration = program.statements[0]

    assert isinstance(declaration, VariableDeclaration)

    multiplication = declaration.initializer
    assert isinstance(multiplication, BinaryExpression)
    assert multiplication.operator == TokenType.STAR

    addition = multiplication.left
    assert isinstance(addition, BinaryExpression)
    assert addition.operator == TokenType.PLUS

    assert isinstance(multiplication.right, IntegerLiteral)
    assert multiplication.right.value == 4


def test_operators_are_left_associative() -> None:
    program = parse("let x = 20 - 5 - 2;")
    declaration = program.statements[0]

    assert isinstance(declaration, VariableDeclaration)

    outer_subtraction = declaration.initializer
    assert isinstance(outer_subtraction, BinaryExpression)
    assert outer_subtraction.operator == TokenType.MINUS

    inner_subtraction = outer_subtraction.left
    assert isinstance(inner_subtraction, BinaryExpression)
    assert inner_subtraction.operator == TokenType.MINUS

    assert isinstance(inner_subtraction.left, IntegerLiteral)
    assert inner_subtraction.left.value == 20

    assert isinstance(inner_subtraction.right, IntegerLiteral)
    assert inner_subtraction.right.value == 5

    assert isinstance(outer_subtraction.right, IntegerLiteral)
    assert outer_subtraction.right.value == 2


def test_boolean_literals() -> None:
    program = parse(
        "let passed = true; "
        "let failed = false;"
    )

    first = program.statements[0]
    second = program.statements[1]

    assert isinstance(first, VariableDeclaration)
    assert isinstance(first.initializer, BooleanLiteral)
    assert first.initializer.value is True

    assert isinstance(second, VariableDeclaration)
    assert isinstance(second.initializer, BooleanLiteral)
    assert second.initializer.value is False


def test_missing_semicolon_is_rejected() -> None:
    with pytest.raises(
        ParserError,
        match=r"Expected ';' after variable declaration",
    ):
        parse("let x = 10")


def test_missing_closing_parenthesis_is_rejected() -> None:
    with pytest.raises(
        ParserError,
        match=r"Expected '\)' after expression",
    ):
        parse("let x = (2 + 3;")


def test_invalid_print_syntax_is_rejected() -> None:
    with pytest.raises(
        ParserError,
        match=r"Expected '\(' after 'print'",
    ):
        parse("print 10;")


def test_missing_operand_is_rejected() -> None:
    with pytest.raises(
        ParserError,
        match=r"Expected an expression",
    ):
        parse("let x = 2 + ;")