from __future__ import annotations

from dataclasses import dataclass

from compiler.tokens import TokenType


class ASTNode:
    pass


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


@dataclass(frozen=True)
class Program(ASTNode):
    statements: list[Statement]


@dataclass(frozen=True)
class VariableDeclaration(Statement):
    name: str
    initializer: Expression
    line: int
    column: int


@dataclass(frozen=True)
class Assignment(Statement):
    name: str
    value: Expression
    line: int
    column: int


@dataclass(frozen=True)
class PrintStatement(Statement):
    expression: Expression
    line: int
    column: int


@dataclass(frozen=True)
class IntegerLiteral(Expression):
    value: int
    line: int
    column: int


@dataclass(frozen=True)
class BooleanLiteral(Expression):
    value: bool
    line: int
    column: int


@dataclass(frozen=True)
class Identifier(Expression):
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression
    line: int
    column: int