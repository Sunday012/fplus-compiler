# F+ Compiler

F+ is a small, statically typed programming language that compiles to native
x86-64 Linux executables. The compiler is written in Python and currently
supports a compact language core: variables, assignment, integer arithmetic,
boolean and string values, printing, semantic checks, IR generation,
optimization, and assembly code generation.

## Example

```fplus
let x = 2 + 3 * 4;
let passed = true;
let greeting = "Hello, F+!";

print(x);
print(passed);
print(greeting);
```

Expected output:

```text
14
true
Hello, F+!
```

## Language Features

F+ version 1 supports:

- Integer, boolean, and UTF-8 string values
- Variable declarations with `let`
- Variable assignment
- Arithmetic expressions with `+`, `-`, `*`, and `/`
- Parenthesized expressions
- `print(...)` statements
- String escapes for newlines (`\n`), tabs (`\t`), carriage returns (`\r`),
  quotes (`\"`), and backslashes (`\\`)
- Static type checking through type inference
- Constant folding optimization
- Native executable output through NASM and GCC

F+ does not yet support conditionals, loops, functions, arrays, user-defined
types, string concatenation, or explicit type annotations.

String literals use double quotes and can be stored, reassigned, and printed:

```fplus
let message = "first line\nsecond line";
message = "She said: \"Hello!\"";
print(message);
```

Strings are a distinct static type. Arithmetic operators remain restricted to
integers, so an expression such as `"hello" + 1` is rejected during semantic
analysis.

## Requirements

- Python 3.10 or newer
- `nasm`
- `gcc`
- `pytest` for running the test suite

Install the Python test dependency with:

```bash
python3 -m pip install -r requirements-dev.txt
```

On Debian or Ubuntu, the native build tools can be installed with:

```bash
sudo apt install nasm gcc
```

## Usage

Compile an F+ source file:

```bash
python3 main.py examples/hello.fp
```

By default, the output executable is written next to the source file without
the `.fp` extension. For `examples/hello.fp`, that produces `examples/hello`.

Run the executable:

```bash
./examples/hello
```

Choose a custom output path:

```bash
python3 main.py examples/hello.fp -o hello
```

Disable optimization:

```bash
python3 main.py examples/hello.fp --no-optimize
```

## Development

Run the tests with:

```bash
pytest
```

The compiler pipeline is:

1. Lex source text into tokens
2. Parse tokens into an abstract syntax tree
3. Run semantic analysis and type inference
4. Generate intermediate representation
5. Optimize the intermediate representation
6. Generate x86-64 assembly
7. Assemble and link a native executable

## Project Layout

```text
compiler/
  lexer.py          Tokenizes F+ source code
  parser.py         Builds the AST
  semantic.py       Performs semantic checks and type inference
  ir_generator.py   Converts AST nodes to intermediate representation
  optimizer.py      Optimizes IR instructions
  codegen.py        Emits x86-64 assembly
examples/
  hello.fp          Example F+ program
  strings.fp        String literals and escape sequences
tests/
  test_*.py         Unit tests for compiler stages
main.py             Command-line compiler entry point
```

## Documentation

- [LANGUAGE.md](LANGUAGE.md) describes the F+ language syntax and semantics.
- [LEXER.md](LEXER.md) documents lexer patterns and DFA tables.
- [PARSER.md](PARSER.md) sketches the AST structure and parser output.

## License

This project is licensed under the terms in [LICENSE](LICENSE).
