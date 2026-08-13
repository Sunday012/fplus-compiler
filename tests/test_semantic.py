import pytest

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import (
    FPlusType,
    SemanticAnalyzer,
    SemanticError,
)


def analyze(source: str) -> SemanticAnalyzer:
    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)

    return analyzer


def test_infers_variable_types() -> None:
    analyzer = analyze(
        """
        let age = 19;
        let passed = true;
        let total = age + 5;
        """
    )

    assert analyzer.symbols == {
        "age": FPlusType.INT,
        "passed": FPlusType.BOOL,
        "total": FPlusType.INT,
    }


def test_valid_assignment() -> None:
    analyzer = analyze(
        """
        let score = 10;
        score = 20;
        """
    )

    assert analyzer.symbols["score"] == FPlusType.INT


def test_print_accepts_integers_and_booleans() -> None:
    analyze(
        """
        let score = 10;
        let passed = true;

        print(score);
        print(passed);
        """
    )


def test_undeclared_assignment_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Variable 'score' is not declared",
    ):
        analyze("score = 20;")


def test_undeclared_identifier_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Variable 'score' is not declared",
    ):
        analyze("print(score);")


def test_duplicate_declaration_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Variable 'score' is already declared",
    ):
        analyze(
            """
            let score = 10;
            let score = 20;
            """
        )


def test_type_changing_assignment_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Cannot assign bool to variable 'score' of type int",
    ):
        analyze(
            """
            let score = 10;
            score = true;
            """
        )


def test_boolean_arithmetic_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"requires int operands",
    ):
        analyze(
            """
            let passed = true;
            let result = passed + 5;
            """
        )


def test_literal_division_by_zero_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Division by zero",
    ):
        analyze("let result = 10 / 0;")


def test_nested_division_by_zero_is_rejected() -> None:
    with pytest.raises(
        SemanticError,
        match=r"Division by zero",
    ):
        analyze("let result = 5 + 10 / 0;")


def test_boolean_variable_type_is_preserved() -> None:
    analyzer = analyze(
        """
        let active = true;
        active = false;
        """
    )

    assert analyzer.symbols["active"] == FPlusType.BOOL