from compiler.ir import IROp, Quadruple
from compiler.ir_generator import IRGenerator
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer


def generate_ir(source: str) -> list[Quadruple]:
    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()

    SemanticAnalyzer().analyze(program)

    return IRGenerator().generate(program).instructions


def test_integer_declaration() -> None:
    instructions = generate_ir("let x = 10;")

    assert instructions == [
        Quadruple(
            operator=IROp.ASSIGN,
            argument1="10",
            argument2=None,
            result="x",
        ),
    ]


def test_boolean_declarations() -> None:
    instructions = generate_ir(
        """
        let passed = true;
        let failed = false;
        """
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "1", None, "passed"),
        Quadruple(IROp.ASSIGN, "0", None, "failed"),
    ]


def test_string_declaration_and_print() -> None:
    instructions = generate_ir(
        'let greeting = "hello"; print(greeting); print("world");'
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "string:hello", None, "greeting"),
        Quadruple(IROp.PRINT_STRING, "greeting", None, None),
        Quadruple(IROp.PRINT_STRING, "string:world", None, None),
    ]


def test_operator_precedence() -> None:
    instructions = generate_ir("let x = 2 + 3 * 4;")

    assert instructions == [
        Quadruple(IROp.MULTIPLY, "3", "4", "t1"),
        Quadruple(IROp.ADD, "2", "t1", "t2"),
        Quadruple(IROp.ASSIGN, "t2", None, "x"),
    ]


def test_parentheses_change_generation_order() -> None:
    instructions = generate_ir("let x = (2 + 3) * 4;")

    assert instructions == [
        Quadruple(IROp.ADD, "2", "3", "t1"),
        Quadruple(IROp.MULTIPLY, "t1", "4", "t2"),
        Quadruple(IROp.ASSIGN, "t2", None, "x"),
    ]


def test_assignment() -> None:
    instructions = generate_ir(
        """
        let x = 10;
        x = x - 1;
        """
    )

    assert instructions == [
        Quadruple(IROp.ASSIGN, "10", None, "x"),
        Quadruple(IROp.SUBTRACT, "x", "1", "t1"),
        Quadruple(IROp.ASSIGN, "t1", None, "x"),
    ]


def test_all_arithmetic_operators() -> None:
    instructions = generate_ir(
        "let x = 20 + 5 - 3 * 2 / 1;"
    )

    assert instructions == [
        Quadruple(IROp.ADD, "20", "5", "t1"),
        Quadruple(IROp.MULTIPLY, "3", "2", "t2"),
        Quadruple(IROp.DIVIDE, "t2", "1", "t3"),
        Quadruple(IROp.SUBTRACT, "t1", "t3", "t4"),
        Quadruple(IROp.ASSIGN, "t4", None, "x"),
    ]


def test_print_expression() -> None:
    instructions = generate_ir("print(2 + 3);")

    assert instructions == [
        Quadruple(IROp.ADD, "2", "3", "t1"),
        Quadruple(IROp.PRINT_INT, "t1", None, None),
    ]


def test_temporary_numbers_restart_per_generation() -> None:
    generator = IRGenerator()

    first_program = Parser(
        Lexer("print(1 + 2);").scan_tokens()
    ).parse()

    second_program = Parser(
        Lexer("print(3 + 4);").scan_tokens()
    ).parse()

    first = generator.generate(first_program)
    second = generator.generate(second_program)

    assert first.instructions[0].result == "t1"
    assert second.instructions[0].result == "t1"
