from compiler.ir import IROp, IRProgram, Quadruple


class CodeGenerationError(Exception):
    pass


class CodeGenerator:
    STRING_PREFIX = "string:"

    def generate(self, program: IRProgram) -> str:
        variables = self._collect_variables(program)
        string_literals = self._collect_string_literals(program)
        self.string_labels = {
            value: f"string_{index}"
            for index, value in enumerate(string_literals)
        }
        lines: list[str] = []

        lines.extend(
            [
                "default rel",
                "",
                "section .data",
                '    format_int db "%ld", 10, 0',
                '    format_bool db "%s", 10, 0',
                '    format_string db "%s", 10, 0',
                '    true_text db "true", 0',
                '    false_text db "false", 0',
            ]
        )

        for value, label in self.string_labels.items():
            encoded = ", ".join(str(byte) for byte in value.encode("utf-8"))
            data = f"{encoded}, 0" if encoded else "0"
            lines.append(f"    {label} db {data}")

        lines.extend(["", "section .bss"])

        for variable in sorted(variables):
            lines.append(f"    {self._label(variable)} resq 1")

        lines.extend(
            [
                "",
                "section .text",
                "    global main",
                "    extern printf",
                "",
                "main:",
                "    push rbp",
                "    mov rbp, rsp",
                "",
            ]
        )

        for instruction in program.instructions:
            lines.extend(self._generate_instruction(instruction))
            lines.append("")

        lines.extend(
            [
                "    xor eax, eax",
                "    leave",
                "    ret",
                "",
                "section .note.GNU-stack noalloc noexec nowrite progbits",
            ]
        )

        return "\n".join(lines)

    def _generate_instruction(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        if instruction.operator == IROp.ASSIGN:
            return self._generate_assignment(instruction)

        if instruction.operator in {
            IROp.ADD,
            IROp.SUBTRACT,
            IROp.MULTIPLY,
            IROp.DIVIDE,
        }:
            return self._generate_arithmetic(instruction)

        if instruction.operator == IROp.PRINT_INT:
            return self._generate_print_int(instruction)

        if instruction.operator == IROp.PRINT_BOOL:
            return self._generate_print_bool(instruction)

        if instruction.operator == IROp.PRINT_STRING:
            return self._generate_print_string(instruction)

        raise CodeGenerationError(
            f"Unsupported IR operation: {instruction.operator.name}"
        )

    def _generate_assignment(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        if instruction.result is None:
            raise CodeGenerationError(
                "Assignment requires a result"
            )

        lines = self._load_operand(
            instruction.argument1,
            register="rax",
        )

        lines.append(
            f"    mov [rel {self._label(instruction.result)}], rax"
        )

        return lines

    def _generate_arithmetic(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        if instruction.argument2 is None:
            raise CodeGenerationError(
                "Arithmetic operation requires two operands"
            )

        if instruction.result is None:
            raise CodeGenerationError(
                "Arithmetic operation requires a result"
            )

        lines = self._load_operand(
            instruction.argument1,
            register="rax",
        )

        if instruction.operator == IROp.DIVIDE:
            lines.append("    cqo")
            lines.extend(
                self._load_operand(
                    instruction.argument2,
                    register="rcx",
                )
            )
            lines.append("    idiv rcx")
        else:
            right = self._assembly_operand(instruction.argument2)

            operation_map = {
                IROp.ADD: "add",
                IROp.SUBTRACT: "sub",
                IROp.MULTIPLY: "imul",
            }

            operation = operation_map[instruction.operator]
            lines.append(f"    {operation} rax, {right}")

        lines.append(
            f"    mov [rel {self._label(instruction.result)}], rax"
        )

        return lines

    def _generate_print_int(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        lines = self._load_operand(
            instruction.argument1,
            register="rsi",
        )

        lines.extend(
            [
                "    lea rdi, [rel format_int]",
                "    xor eax, eax",
                "    call printf",
            ]
        )

        return lines

    def _generate_print_bool(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        lines = self._load_operand(
            instruction.argument1,
            register="rax",
        )

        label_number = id(instruction)
        false_label = f".bool_false_{label_number}"
        ready_label = f".bool_ready_{label_number}"

        lines.extend(
            [
                "    cmp rax, 0",
                f"    je {false_label}",
                "    lea rsi, [rel true_text]",
                f"    jmp {ready_label}",
                f"{false_label}:",
                "    lea rsi, [rel false_text]",
                f"{ready_label}:",
                "    lea rdi, [rel format_bool]",
                "    xor eax, eax",
                "    call printf",
            ]
        )

        return lines

    def _generate_print_string(
        self,
        instruction: Quadruple,
    ) -> list[str]:
        lines = self._load_operand(
            instruction.argument1,
            register="rsi",
        )
        lines.extend(
            [
                "    lea rdi, [rel format_string]",
                "    xor eax, eax",
                "    call printf",
            ]
        )
        return lines

    def _load_operand(
        self,
        operand: str,
        register: str,
    ) -> list[str]:
        if self._is_integer(operand):
            return [f"    mov {register}, {operand}"]

        if self._is_string_literal(operand):
            value = operand[len(self.STRING_PREFIX):]
            return [
                f"    lea {register}, [rel {self.string_labels[value]}]"
            ]

        return [
            f"    mov {register}, [rel {self._label(operand)}]"
        ]

    def _assembly_operand(self, operand: str) -> str:
        if self._is_integer(operand):
            return operand

        return f"[rel {self._label(operand)}]"

    def _collect_variables(self, program: IRProgram) -> set[str]:
        variables: set[str] = set()

        for instruction in program.instructions:
            if (
                instruction.result is not None
                and not self._is_integer(instruction.result)
                and not self._is_string_literal(instruction.result)
            ):
                variables.add(instruction.result)

            if (
                not self._is_integer(instruction.argument1)
                and not self._is_string_literal(instruction.argument1)
            ):
                variables.add(instruction.argument1)

            if (
                instruction.argument2 is not None
                and not self._is_integer(instruction.argument2)
                and not self._is_string_literal(instruction.argument2)
            ):
                variables.add(instruction.argument2)

        return variables

    def _collect_string_literals(self, program: IRProgram) -> list[str]:
        literals: list[str] = []

        for instruction in program.instructions:
            for operand in (
                instruction.argument1,
                instruction.argument2,
            ):
                if operand is not None and self._is_string_literal(operand):
                    value = operand[len(self.STRING_PREFIX):]
                    if value not in literals:
                        literals.append(value)

        return literals

    def _label(self, name: str) -> str:
        return f"fplus_{name}"

    def _is_integer(self, value: str) -> bool:
        if value.startswith("-"):
            return value[1:].isdigit()

        return value.isdigit()

    def _is_string_literal(self, value: str) -> bool:
        return value.startswith(self.STRING_PREFIX)
