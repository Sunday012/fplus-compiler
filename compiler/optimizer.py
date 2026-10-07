from compiler.ir import IROp, IRProgram, Quadruple


class OptimizationError(Exception):
    pass


class Optimizer:
    def optimize(self, program: IRProgram) -> IRProgram:
        constants: dict[str, int] = {}
        optimized: list[Quadruple] = []

        for instruction in program.instructions:
            if instruction.operator in {
                IROp.ADD,
                IROp.SUBTRACT,
                IROp.MULTIPLY,
                IROp.DIVIDE,
            }:
                self._optimize_arithmetic(
                    instruction,
                    constants,
                    optimized,
                )
                continue

            if instruction.operator == IROp.ASSIGN:
                self._optimize_assignment(
                    instruction,
                    constants,
                    optimized,
                )
                continue

            if instruction.operator in {
                IROp.PRINT,
                IROp.PRINT_INT,
                IROp.PRINT_BOOL,
                IROp.PRINT_STRING,
            }:
                self._optimize_print(
                    instruction,
                    constants,
                    optimized,
                )
                continue

            optimized.append(instruction)

        return IRProgram(optimized)

    def _optimize_arithmetic(
        self,
        instruction: Quadruple,
        constants: dict[str, int],
        optimized: list[Quadruple],
    ) -> None:
        left = self._resolve(instruction.argument1, constants)

        if instruction.argument2 is None:
            raise OptimizationError(
                "Arithmetic instruction requires two operands"
            )

        right = self._resolve(instruction.argument2, constants)

        if self._is_integer(left) and self._is_integer(right):
            result = self._calculate(
                instruction.operator,
                int(left),
                int(right),
            )

            if instruction.result is not None:
                constants[instruction.result] = result

            return

        if instruction.result is not None:
            constants.pop(instruction.result, None)

        optimized.append(
            Quadruple(
                instruction.operator,
                left,
                right,
                instruction.result,
            )
        )

    def _optimize_assignment(
        self,
        instruction: Quadruple,
        constants: dict[str, int],
        optimized: list[Quadruple],
    ) -> None:
        value = self._resolve(
            instruction.argument1,
            constants,
        )

        if instruction.result is None:
            raise OptimizationError(
                "Assignment requires a result"
            )

        if self._is_integer(value):
            constants[instruction.result] = int(value)
        else:
            constants.pop(instruction.result, None)

        optimized.append(
            Quadruple(
                IROp.ASSIGN,
                value,
                None,
                instruction.result,
            )
        )

    def _optimize_print(
        self,
        instruction: Quadruple,
        constants: dict[str, int],
        optimized: list[Quadruple],
    ) -> None:
        value = self._resolve(
            instruction.argument1,
            constants,
        )

        optimized.append(
            Quadruple(
                instruction.operator,
                value,
                None,
                None,
            )
        )

    def _resolve(
        self,
        operand: str,
        constants: dict[str, int],
    ) -> str:
        if operand in constants:
            return str(constants[operand])

        return operand

    def _is_integer(self, value: str) -> bool:
        if value.startswith("-"):
            return value[1:].isdigit()

        return value.isdigit()

    def _calculate(
        self,
        operator: IROp,
        left: int,
        right: int,
    ) -> int:
        if operator == IROp.ADD:
            return left + right

        if operator == IROp.SUBTRACT:
            return left - right

        if operator == IROp.MULTIPLY:
            return left * right

        if operator == IROp.DIVIDE:
            if right == 0:
                raise OptimizationError("Division by zero")

            return self._truncate_division(left, right)

        raise OptimizationError(
            f"Unsupported arithmetic operator: {operator.name}"
        )

    def _truncate_division(self, left: int, right: int) -> int:
        quotient = abs(left) // abs(right)

        if (left < 0) != (right < 0):
            return -quotient

        return quotient
