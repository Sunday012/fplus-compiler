from enum import Enum

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
    StringLiteral,
    VariableDeclaration,
)
from compiler.tokens import TokenType


class SemanticError(Exception):
    pass


class FPlusType(Enum):
    INT = "int"
    BOOL = "bool"
    STRING = "string"


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.symbols: dict[str, FPlusType] = {}

    def analyze(self, program: Program) -> None:
        for statement in program.statements:
            self._analyze_statement(statement)

    def _analyze_statement(self, statement: Statement) -> None:
        if isinstance(statement, VariableDeclaration):
            self._analyze_variable_declaration(statement)
            return

        if isinstance(statement, Assignment):
            self._analyze_assignment(statement)
            return

        if isinstance(statement, PrintStatement):
            self._infer_expression_type(statement.expression)
            return

        raise SemanticError(
            f"Unsupported statement type: "
            f"{type(statement).__name__}"
        )

    def _analyze_variable_declaration(
        self,
        statement: VariableDeclaration,
    ) -> None:
        if statement.name in self.symbols:
            raise SemanticError(
                f"Variable {statement.name!r} is already declared "
                f"at line {statement.line}, "
                f"column {statement.column}"
            )

        initializer_type = self._infer_expression_type(
            statement.initializer
        )

        self.symbols[statement.name] = initializer_type

    def _analyze_assignment(
        self,
        statement: Assignment,
    ) -> None:
        if statement.name not in self.symbols:
            raise SemanticError(
                f"Variable {statement.name!r} is not declared "
                f"at line {statement.line}, "
                f"column {statement.column}"
            )

        variable_type = self.symbols[statement.name]
        value_type = self._infer_expression_type(statement.value)

        if variable_type != value_type:
            raise SemanticError(
                f"Cannot assign {value_type.value} to variable "
                f"{statement.name!r} of type {variable_type.value} "
                f"at line {statement.line}, "
                f"column {statement.column}"
            )

    def _infer_expression_type(
        self,
        expression: Expression,
    ) -> FPlusType:
        if isinstance(expression, IntegerLiteral):
            return FPlusType.INT

        if isinstance(expression, BooleanLiteral):
            return FPlusType.BOOL

        if isinstance(expression, StringLiteral):
            return FPlusType.STRING

        if isinstance(expression, Identifier):
            return self._infer_identifier_type(expression)

        if isinstance(expression, BinaryExpression):
            return self._infer_binary_expression_type(expression)

        raise SemanticError(
            f"Unsupported expression type: "
            f"{type(expression).__name__}"
        )

    def _infer_identifier_type(
        self,
        expression: Identifier,
    ) -> FPlusType:
        if expression.name not in self.symbols:
            raise SemanticError(
                f"Variable {expression.name!r} is not declared "
                f"at line {expression.line}, "
                f"column {expression.column}"
            )

        return self.symbols[expression.name]

    def _infer_binary_expression_type(
        self,
        expression: BinaryExpression,
    ) -> FPlusType:
        left_type = self._infer_expression_type(expression.left)
        right_type = self._infer_expression_type(expression.right)

        arithmetic_operators = {
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
        }

        if expression.operator not in arithmetic_operators:
            raise SemanticError(
                f"Unsupported binary operator "
                f"{expression.operator.name} "
                f"at line {expression.line}, "
                f"column {expression.column}"
            )

        if (
            left_type != FPlusType.INT
            or right_type != FPlusType.INT
        ):
            raise SemanticError(
                f"Operator {expression.operator.name!r} requires "
                f"int operands, but received "
                f"{left_type.value} and {right_type.value} "
                f"at line {expression.line}, "
                f"column {expression.column}"
            )

        if (
            expression.operator == TokenType.SLASH
            and isinstance(expression.right, IntegerLiteral)
            and expression.right.value == 0
        ):
            raise SemanticError(
                f"Division by zero "
                f"at line {expression.line}, "
                f"column {expression.column}"
            )

        return FPlusType.INT
