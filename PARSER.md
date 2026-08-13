ASTNode
├── Program
├── Statement
│   ├── VariableDeclaration
│   ├── Assignment
│   └── PrintStatement
└── Expression
    ├── IntegerLiteral
    ├── BooleanLiteral
    ├── Identifier
    └── BinaryExpression


Program(
    statements=[
        VariableDeclaration(
            name="x",
            initializer=BinaryExpression(
                left=IntegerLiteral(
                    value=2,
                    line=1,
                    column=9,
                ),
                operator=TokenType.PLUS,
                right=IntegerLiteral(
                    value=3,
                    line=1,
                    column=13,
                ),
                line=1,
                column=11,
            ),
            line=1,
            column=1,
        )
    ]
)