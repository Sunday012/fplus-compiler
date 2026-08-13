import pytest

from compiler.ir import IROp, IRProgram, Quadruple
from compiler.optimizer import OptimizationError, Optimizer


def optimize(*instructions: Quadruple) -> list[Quadruple]:
    program = IRProgram(list(instructions))
    return Optimizer().optimize(program).instructions


def test_constant_folding() -> None:
    instructions = optimize(
        Quadruple(IROp.MULTIPLY, "3", "4", "t1"),
        Quadruple(IROp.ADD, "2", "t1", "t2"),
        Quadruple(IROp.ASSIGN, "t2", None, "x"),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "14", None, "x"),
    ]


def test_constant_propagation() -> None:
    instructions = optimize(
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ADD, "x", "5", "t1"),
        Quadruple(IROp.ASSIGN, "t1", None, "y"),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ASSIGN, "15", None, "y"),
    ]


def test_constant_propagation_into_print() -> None:
    instructions = optimize(
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.PRINT, "x", None, None),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.PRINT, "10", None, None),
    ]


def test_constant_propagation_into_typed_prints() -> None:
    instructions = optimize(
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ASSIGN, "1", None, "flag"),
        Quadruple(IROp.PRINT_INT, "x", None, None),
        Quadruple(IROp.PRINT_BOOL, "flag", None, None),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ASSIGN, "1", None, "flag"),
        Quadruple(IROp.PRINT_INT, "10", None, None),
        Quadruple(IROp.PRINT_BOOL, "1", None, None),
    ]


def test_nonconstant_expression_is_preserved() -> None:
    instructions = optimize(
        Quadruple(IROp.ADD, "x", "5", "t1"),
    )

    assert instructions == [
        Quadruple(IROp.ADD, "x", "5", "t1"),
    ]


def test_reassignment_updates_constant() -> None:
    instructions = optimize(
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ASSIGN, "20", None, "x"),
        Quadruple(IROp.PRINT, "x", None, None),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.ASSIGN, "20", None, "x"),
        Quadruple(IROp.PRINT, "20", None, None),
    ]


def test_negative_constant_is_recognised() -> None:
    instructions = optimize(
        Quadruple(IROp.SUBTRACT, "2", "5", "t1"),
        Quadruple(IROp.MULTIPLY, "t1", "4", "t2"),
        Quadruple(IROp.ASSIGN, "t2", None, "x"),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "-12", None, "x"),
    ]


def test_signed_division_truncates_toward_zero() -> None:
    instructions = optimize(
        Quadruple(IROp.DIVIDE, "-7", "2", "t1"),
        Quadruple(IROp.ASSIGN, "t1", None, "x"),
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "-3", None, "x"),
    ]


def test_division_by_zero_is_rejected() -> None:
    with pytest.raises(
        OptimizationError,
        match=r"Division by zero",
    ):
        optimize(
            Quadruple(IROp.DIVIDE, "10", "0", "t1"),
        )


def test_generator_output_is_optimized() -> None:
    from compiler.ir_generator import IRGenerator
    from compiler.lexer import Lexer
    from compiler.parser import Parser
    from compiler.semantic import SemanticAnalyzer

    source = """
    let x = 2 + 3 * 4;
    let y = x + 5;
    print(y);
    """

    program = Parser(Lexer(source).scan_tokens()).parse()
    SemanticAnalyzer().analyze(program)

    ir = IRGenerator().generate(program)
    instructions = Optimizer().optimize(ir).instructions

    assert instructions == [
        Quadruple(IROp.ASSIGN, "14", None, "x"),
        Quadruple(IROp.ASSIGN, "19", None, "y"),
        Quadruple(IROp.PRINT_INT, "19", None, None),
    ]
