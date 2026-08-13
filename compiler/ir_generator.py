from compiler.ast_nodes import (
    Assignment,
    BinaryExpression,
    BooleanLiteral,
    Expression,
    Identifier,
    IntegerLiteral,
    PrintStatement,
    Program,
    Statement,
    VariableDeclaration,
)
from compiler.ir import IROp, IRProgram, Quadruple
from compiler.tokens import TokenType
from compiler.semantic import FPlusType


class IRGenerationError(Exception):
    pass


class IRGenerator:
    def __init__(self) -> None:
        self.instructions: list[Quadruple] = []
        self.temporary_count = 0
        self.variable_types: dict[str, FPlusType] = {}

    def generate(self, program: Program) -> IRProgram:
        self.instructions = []
        self.temporary_count = 0
        self.variable_types = {}

        for statement in program.statements:
            self._generate_statement(statement)

        return IRProgram(self.instructions.copy())

    def _generate_statement(self, statement: Statement) -> None:
        if isinstance(statement, VariableDeclaration):
            variable_type = self._infer_expression_type(statement.initializer)
            self.variable_types[statement.name] = variable_type
            value = self._generate_expression(statement.initializer)

            self._emit(
                IROp.ASSIGN,
                argument1=value,
                argument2=None,
                result=statement.name,
            )
            return

        if isinstance(statement, Assignment):
            value = self._generate_expression(statement.value)

            self._emit(
                IROp.ASSIGN,
                argument1=value,
                argument2=None,
                result=statement.name,
            )
            return

        if isinstance(statement, PrintStatement):
            expression_type = self._infer_expression_type(
                statement.expression
            )
            value = self._generate_expression(statement.expression)

            if expression_type == FPlusType.INT:
                print_operator = IROp.PRINT_INT
            else:
                print_operator = IROp.PRINT_BOOL

            self._emit(
                print_operator,
                argument1=value,
                argument2=None,
                result=None,
            )
            return

        raise IRGenerationError(
            f"Unsupported statement: {type(statement).__name__}"
        )

    def _infer_expression_type(
        self,
        expression: Expression,
    ) -> FPlusType:
        if isinstance(expression, IntegerLiteral):
            return FPlusType.INT

        if isinstance(expression, BooleanLiteral):
            return FPlusType.BOOL

        if isinstance(expression, Identifier):
            variable_type = self.variable_types.get(expression.name)

            if variable_type is None:
                raise IRGenerationError(
                    f"Unknown variable type for {expression.name!r}"
                )

            return variable_type

        if isinstance(expression, BinaryExpression):
            return FPlusType.INT

        raise IRGenerationError(
            f"Cannot determine type of "
            f"{type(expression).__name__}"
    )

    def _generate_expression(self, expression: Expression) -> str:
        if isinstance(expression, IntegerLiteral):
            return str(expression.value)

        if isinstance(expression, BooleanLiteral):
            return "1" if expression.value else "0"

        if isinstance(expression, Identifier):
            return expression.name

        if isinstance(expression, BinaryExpression):
            return self._generate_binary_expression(expression)

        raise IRGenerationError(
            f"Unsupported expression: {type(expression).__name__}"
        )

    def _generate_binary_expression(
        self,
        expression: BinaryExpression,
    ) -> str:
        left = self._generate_expression(expression.left)
        right = self._generate_expression(expression.right)

        operator_map = {
            TokenType.PLUS: IROp.ADD,
            TokenType.MINUS: IROp.SUBTRACT,
            TokenType.STAR: IROp.MULTIPLY,
            TokenType.SLASH: IROp.DIVIDE,
        }

        operator = operator_map.get(expression.operator)

        if operator is None:
            raise IRGenerationError(
                f"Unsupported operator: {expression.operator.name}"
            )

        temporary = self._new_temporary()

        self._emit(
            operator,
            argument1=left,
            argument2=right,
            result=temporary,
        )

        return temporary

    def _new_temporary(self) -> str:
        self.temporary_count += 1
        return f"t{self.temporary_count}"

    def _emit(
        self,
        operator: IROp,
        argument1: str,
        argument2: str | None,
        result: str | None,
    ) -> None:
        self.instructions.append(
            Quadruple(
                operator=operator,
                argument1=argument1,
                argument2=argument2,
                result=result,
            )
        )