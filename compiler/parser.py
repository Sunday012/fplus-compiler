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
from compiler.tokens import Token, TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements: list[Statement] = []

        while not self._check(TokenType.EOF):
            statements.append(self._statement())

        return Program(statements)

    def _statement(self) -> Statement:
        if self._match(TokenType.LET):
            return self._variable_declaration()

        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._check(TokenType.IDENTIFIER):
            return self._assignment()

        token = self._peek()

        raise ParserError(
            f"Expected a statement at line {token.line}, "
            f"column {token.column}; found {token.lexeme!r}"
        )

    def _variable_declaration(self) -> VariableDeclaration:
        let_token = self._previous()

        name = self._consume(
            TokenType.IDENTIFIER,
            "Expected a variable name after 'let'",
        )

        self._consume(
            TokenType.EQUAL,
            "Expected '=' after variable name",
        )

        initializer = self._expression()

        self._consume(
            TokenType.SEMICOLON,
            "Expected ';' after variable declaration",
        )

        return VariableDeclaration(
            name=name.lexeme,
            initializer=initializer,
            line=let_token.line,
            column=let_token.column,
        )

    def _assignment(self) -> Assignment:
        name = self._consume(
            TokenType.IDENTIFIER,
            "Expected a variable name",
        )

        self._consume(
            TokenType.EQUAL,
            "Expected '=' after variable name",
        )

        value = self._expression()

        self._consume(
            TokenType.SEMICOLON,
            "Expected ';' after assignment",
        )

        return Assignment(
            name=name.lexeme,
            value=value,
            line=name.line,
            column=name.column,
        )

    def _print_statement(self) -> PrintStatement:
        print_token = self._previous()

        self._consume(
            TokenType.LPAREN,
            "Expected '(' after 'print'",
        )

        expression = self._expression()

        self._consume(
            TokenType.RPAREN,
            "Expected ')' after value",
        )

        self._consume(
            TokenType.SEMICOLON,
            "Expected ';' after print statement",
        )

        return PrintStatement(
            expression=expression,
            line=print_token.line,
            column=print_token.column,
        )

    def _expression(self) -> Expression:
        expression = self._term()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._term()

            expression = BinaryExpression(
                left=expression,
                operator=operator.type,
                right=right,
                line=operator.line,
                column=operator.column,
            )

        return expression

    def _term(self) -> Expression:
        expression = self._factor()

        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self._factor()

            expression = BinaryExpression(
                left=expression,
                operator=operator.type,
                right=right,
                line=operator.line,
                column=operator.column,
            )

        return expression

    def _factor(self) -> Expression:
        if self._match(TokenType.STRING):
            token = self._previous()

            return StringLiteral(
                value=token.literal,
                line=token.line,
                column=token.column,
            )

        if self._match(TokenType.INTEGER):
            token = self._previous()

            return IntegerLiteral(
                value=token.literal,
                line=token.line,
                column=token.column,
            )

        if self._match(TokenType.TRUE):
            token = self._previous()

            return BooleanLiteral(
                value=True,
                line=token.line,
                column=token.column,
            )

        if self._match(TokenType.FALSE):
            token = self._previous()

            return BooleanLiteral(
                value=False,
                line=token.line,
                column=token.column,
            )

        if self._match(TokenType.IDENTIFIER):
            token = self._previous()

            return Identifier(
                name=token.lexeme,
                line=token.line,
                column=token.column,
            )

        if self._match(TokenType.LPAREN):
            expression = self._expression()

            self._consume(
                TokenType.RPAREN,
                "Expected ')' after expression",
            )

            return expression

        token = self._peek()

        raise ParserError(
            f"Expected an expression at line {token.line}, "
            f"column {token.column}; found {token.lexeme!r}"
        )

    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True

        return False

    def _consume(
        self,
        token_type: TokenType,
        message: str,
    ) -> Token:
        if self._check(token_type):
            return self._advance()

        token = self._peek()

        raise ParserError(
            f"{message} at line {token.line}, "
            f"column {token.column}; found {token.lexeme!r}"
        )

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1

        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]
