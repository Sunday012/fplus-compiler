# F+ Language Specification

## 1. Version

F+ version 1.0.

## 2. File extension

F+ source files use the `.fp` extension.

Example:

```text
hello.fp
```

## 3. Description

F+ is a small, statically typed programming language that compiles to
x86-64 assembly.

The F+ compiler is implemented in Python. The generated assembly is
assembled and linked into a native executable.

## 4. Version 1 features

F+ version 1 supports:

- Integer values
- Boolean values
- Variable declarations
- Variable assignments
- Arithmetic expressions
- Parenthesized expressions
- Printing values
- Static type checking through type inference

F+ version 1 does not yet support:

- `if` and `else`
- Comparison operators
- Loops
- Functions
- Strings
- Lists or arrays
- User-defined types
- Explicit type annotations

These features would be added in later versions.

## 5. Example program

```fplus
let x = 10;
let y = x + 5;
let passed = true;

print(y);
print(passed);

x = 20;
print(x);
```

Expected output:

```text
15
true
20
```

## 6. Reserved keywords

The following words have special meanings in F+ and cannot be used as
identifiers:

- `let`
- `print`
- `true`
- `false`

This is invalid:

```fplus
let print = 10;
```

It is invalid because `print` is a reserved keyword.

## 7. Tokens and symbols

### Keywords

| Token | Text |
|---|---|
| `LET` | `let` |
| `PRINT` | `print` |
| `TRUE` | `true` |
| `FALSE` | `false` |

### Operators

| Token | Symbol | Meaning |
|---|---|---|
| `EQUAL` | `=` | Assignment |
| `PLUS` | `+` | Addition |
| `MINUS` | `-` | Subtraction |
| `STAR` | `*` | Multiplication |
| `SLASH` | `/` | Integer division |

### Punctuation

| Token | Symbol | Meaning |
|---|---|---|
| `LPAREN` | `(` | Left parenthesis |
| `RPAREN` | `)` | Right parenthesis |
| `SEMICOLON` | `;` | Statement terminator |

### Other tokens

| Token | Description | Examples |
|---|---|---|
| `IDENTIFIER` | The name of a variable | `x`, `age`, `total2` |
| `INTEGER` | A whole-number literal | `0`, `19`, `250` |
| `EOF` | The end of the source file | — |

## 8. Lexical rules

### 8.1 Identifiers

An identifier must:

1. Begin with an uppercase or lowercase letter.
2. Contain only letters and digits after the first character.
3. Not be one of the reserved keywords.
4. Be treated as case-sensitive.

Valid identifiers:

```text
x
age
student2
totalAmount
Value1
```

Invalid identifiers:

```text
2student
student_name
total-price
```

The identifiers below are different because F+ is case-sensitive:

```text
total
Total
TOTAL
```

The regular-expression pattern for an identifier is:

```regex
[A-Za-z][A-Za-z0-9]*
```

### 8.2 Integer literals

An integer literal contains one or more digits.

Valid integer literals:

```text
0
7
19
250
```

Invalid integer literals:

```text
five
10.5
```

The regular-expression pattern for an integer literal is:

```regex
[0-9]+
```

F+ integers are signed 64-bit integers. Integer literals themselves contain
digits only. Negative values can be produced through subtraction.

### 8.3 Whitespace

Spaces, tabs and line breaks may appear between tokens. Whitespace separates
tokens but does not otherwise affect the program's meaning.

For example, these declarations have the same meaning:

```fplus
let x = 10;
```

```fplus
let     x
=
10
;
```

## 9. Syntax rules

1. An F+ program consists of zero or more statements.

2. Every statement must end with a semicolon (`;`).

3. A variable must be declared using `let` before it can be used.

4. A variable declaration has this form:

   ```fplus
   let variableName = expression;
   ```

5. An assignment to an existing variable has this form:

   ```fplus
   variableName = expression;
   ```

6. A value is printed using:

   ```fplus
   print(expression);
   ```

7. Arithmetic expressions support:

   - Addition: `+`
   - Subtraction: `-`
   - Multiplication: `*`
   - Integer division: `/`

8. Multiplication and division have higher precedence than addition and
   subtraction.

   Therefore:

   ```fplus
   2 + 3 * 4
   ```

   is evaluated as:

   ```text
   2 + (3 * 4)
   ```

9. Operators at the same precedence level are evaluated from left to right.

   Therefore:

   ```fplus
   20 - 5 - 2
   ```

   is evaluated as:

   ```text
   (20 - 5) - 2
   ```

10. Parentheses can be used to change the evaluation order.

    ```fplus
    let result = (2 + 3) * 4;
    ```

11. F+ is case-sensitive.

12. Reserved keywords cannot be used as variable names.

## 10. Types

F+ version 1 has two types:

| Type | Meaning | Examples |
|---|---|---|
| `int` | A signed 64-bit integer | `0`, `19`, `250` |
| `bool` | A Boolean value | `true`, `false` |

## 11. Type inference

F+ is statically typed, but version 1 does not require programmers to write
explicit type annotations.

The compiler infers a variable's type from its initial value.

For example:

```fplus
let age = 19;
let passed = true;
```

The compiler infers:

```text
age: int
passed: bool
```

A variable keeps its inferred type throughout the program.

## 12. Type and semantic rules

1. An integer literal has the type `int`.

2. `true` and `false` have the type `bool`.

3. The arithmetic operators `+`, `-`, `*`, and `/` require two `int`
   operands.

4. An arithmetic operation produces an `int`.

5. A variable receives its type from the expression used in its declaration.

6. A variable's type cannot change after its declaration.

7. An assignment must produce the same type as the variable receiving the
   value.

8. `print` accepts both `int` and `bool` expressions.

9. A variable must be declared before it is used.

10. A variable cannot be declared more than once in the same program in
    version 1.

11. Division by zero is invalid.

## 13. Valid examples

### Integer declaration

```fplus
let age = 19;
```

### Boolean declaration

```fplus
let passed = true;
```

### Arithmetic expression

```fplus
let result = 2 + 3 * 4;
```

### Assignment

```fplus
let score = 10;
score = 20;
```

### Printing

```fplus
let total = 15;
print(total);
print(true);
```

## 14. Invalid examples

### Missing semicolon

```fplus
let x = 10
```

### Invalid identifier

```fplus
let 2student = 10;
```

### Undeclared variable

```fplus
x = 20;
```

### Duplicate declaration

```fplus
let x = 10;
let x = 20;
```

### Type-changing assignment

```fplus
let x = 10;
x = true;
```

### Invalid arithmetic operands

```fplus
let result = true + 5;
```

### Division by zero

```fplus
let result = 10 / 0;
```

## 15. BNF grammar

In the grammar below:

- `::=` means “is defined as.”
- `|` means “or.”
- `ε` represents the empty string.
- Names inside angle brackets are non-terminals.
- Values inside quotation marks are terminals written in F+ source code.

```bnf
<program> ::= <statement-list>

<statement-list> ::= <statement> <statement-list>
                   | ε

<statement> ::= <variable-declaration>
              | <assignment>
              | <print-statement>

<variable-declaration> ::= "let" <identifier> "=" <expression> ";"

<assignment> ::= <identifier> "=" <expression> ";"

<print-statement> ::= "print" "(" <expression> ")" ";"

<expression> ::= <term> <expression-tail>

<expression-tail> ::= "+" <term> <expression-tail>
                    | "-" <term> <expression-tail>
                    | ε

<term> ::= <factor> <term-tail>

<term-tail> ::= "*" <factor> <term-tail>
              | "/" <factor> <term-tail>
              | ε

<factor> ::= <number>
           | <boolean>
           | <identifier>
           | "(" <expression> ")"

<boolean> ::= "true"
            | "false"

<identifier> ::= <letter> <identifier-tail>

<identifier-tail> ::= <letter-or-digit> <identifier-tail>
                    | ε

<letter-or-digit> ::= <letter>
                    | <digit>

<letter> ::= "a" | "b" | "c" | "d" | "e" | "f"
           | "g" | "h" | "i" | "j" | "k" | "l"
           | "m" | "n" | "o" | "p" | "q" | "r"
           | "s" | "t" | "u" | "v" | "w" | "x"
           | "y" | "z"
           | "A" | "B" | "C" | "D" | "E" | "F"
           | "G" | "H" | "I" | "J" | "K" | "L"
           | "M" | "N" | "O" | "P" | "Q" | "R"
           | "S" | "T" | "U" | "V" | "W" | "X"
           | "Y" | "Z"

<digit> ::= "0" | "1" | "2" | "3" | "4"
          | "5" | "6" | "7" | "8" | "9"

<number> ::= <digit> <number-tail>

<number-tail> ::= <digit> <number-tail>
                | ε
```

## 16. Compiler target

The F+ compiler translates `.fp` source files into x86-64 assembly.

The complete compilation process is:

```text
F+ source code
    ↓
Lexer
    ↓
Parser and abstract syntax tree
    ↓
Semantic analysis and type checking
    ↓
Intermediate-code generation
    ↓
Optimisation
    ↓
x86-64 assembly generation
    ↓
NASM assembler
    ↓
Object code
    ↓
Linker
    ↓
Native executable
```


## 17. Grammar verification

Expression 1: 5

<expression>
⇒ <term> <expression-tail>
⇒ <factor> <term-tail> <expression-tail>
⇒ <number> <term-tail> <expression-tail>
⇒ <digit> <number-tail> <term-tail> <expression-tail>
⇒ "5" <number-tail> <term-tail> <expression-tail>
⇒ "5" ε <term-tail> <expression-tail>
⇒ "5" ε ε <expression-tail>
⇒ "5" ε ε ε
⇒ 5

parse tree

expression
├── term
│   ├── factor
│   │   └── number
│   │       ├── digit: 5
│   │       └── number-tail: ε
│   └── term-tail: ε
└── expression-tail: ε


Expression 2: 2 + 3

<expression>
⇒ <term> <expression-tail>
⇒ <factor> <term-tail> <expression-tail>
⇒ <number> ε <expression-tail>
⇒ 2 <expression-tail>
⇒ 2 "+" <term> <expression-tail>
⇒ 2 "+" <factor> <term-tail> <expression-tail>
⇒ 2 "+" <number> ε <expression-tail>
⇒ 2 "+" 3 ε
⇒ 2 + 3

parse tree

expression
├── term
│   ├── factor
│   │   └── number: 2
│   └── term-tail: ε
└── expression-tail
    ├── +
    ├── term
    │   ├── factor
    │   │   └── number: 3
    │   └── term-tail: ε
    └── expression-tail: ε


Expression 3: (2 + 3) * 4

<expression>
⇒ <term> <expression-tail>
⇒ <factor> <term-tail> <expression-tail>
⇒ "(" <expression> ")" <term-tail> <expression-tail>
⇒ "(" 2 + 3 ")" <term-tail> <expression-tail>
⇒ "(" 2 + 3 ")" "*" <factor> <term-tail> <expression-tail>
⇒ "(" 2 + 3 ")" "*" <number> <term-tail> <expression-tail>
⇒ "(" 2 + 3 ")" "*" 4 ε ε
⇒ (2 + 3) * 4

parse tree

expression
├── term
│   ├── factor
│   │   ├── (
│   │   ├── expression
│   │   │   ├── term
│   │   │   │   └── factor
│   │   │   │       └── number: 2
│   │   │   └── expression-tail
│   │   │       ├── +
│   │   │       ├── term
│   │   │       │   └── factor
│   │   │       │       └── number: 3
│   │   │       └── expression-tail: ε
│   │   └── )
│   └── term-tail
│       ├── *
│       ├── factor
│       │   └── number: 4
│       └── term-tail: ε
└── expression-tail: ε