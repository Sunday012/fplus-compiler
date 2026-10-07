from compiler.codegen import CodeGenerator
from compiler.ir import IROp, IRProgram, Quadruple


def test_generates_utf8_string_data_and_print() -> None:
    program = IRProgram(
        [
            Quadruple(
                IROp.ASSIGN,
                "string:héllo",
                None,
                "greeting",
            ),
            Quadruple(
                IROp.PRINT_STRING,
                "greeting",
                None,
                None,
            ),
        ]
    )

    assembly = CodeGenerator().generate(program)

    assert "string_0 db 104, 195, 169, 108, 108, 111, 0" in assembly
    assert "lea rax, [rel string_0]" in assembly
    assert "mov [rel fplus_greeting], rax" in assembly
    assert "lea rdi, [rel format_string]" in assembly


def test_empty_string_has_a_null_terminator() -> None:
    program = IRProgram(
        [Quadruple(IROp.PRINT_STRING, "string:", None, None)]
    )

    assembly = CodeGenerator().generate(program)

    assert "string_0 db 0" in assembly
