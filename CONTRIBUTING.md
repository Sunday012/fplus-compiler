# Contributing to F+

Thank you for helping improve F+. Bug reports, language-design discussions,
documentation improvements, tests, and code contributions are all welcome.

## Before You Start

For a bug or small improvement, open an issue or submit a pull request. For a
new language feature or a change to existing syntax or semantics, open a
feature request first so the design can be discussed before implementation.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all project spaces.

## Development Setup

F+ requires Python 3.10 or newer. Native compilation also requires NASM and
GCC.

```bash
git clone https://github.com/Sunday012/fplus-compiler.git
cd fplus-compiler
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

On Debian or Ubuntu, install the native build tools with:

```bash
sudo apt install nasm gcc
```

## Making a Change

1. Fork the repository and create a focused branch from `main`.
2. Keep the change small enough to review and avoid unrelated formatting.
3. Add or update tests for behavior changes.
4. Update the README and language documentation when syntax or semantics
   change.
5. Run the complete test suite.

```bash
python -m pytest
```

For compiler pipeline or code-generation changes, also compile and run an
example program:

```bash
python main.py examples/hello.fp -o /tmp/fplus-hello
/tmp/fplus-hello
```

The compiler pipeline is organized as follows:

1. `compiler/lexer.py` creates tokens.
2. `compiler/parser.py` builds the abstract syntax tree.
3. `compiler/semantic.py` checks types and program validity.
4. `compiler/ir_generator.py` produces intermediate representation.
5. `compiler/optimizer.py` optimizes the IR.
6. `compiler/codegen.py` emits x86-64 NASM assembly.

Changes to a language feature commonly need matching updates across several
of these stages.

## Pull Requests

In your pull request:

- Explain the problem and the chosen solution.
- Link the relevant issue when one exists.
- Describe how you tested the change.
- Include documentation updates for user-visible behavior.
- Keep generated executables, object files, assembly output, virtual
  environments, and editor files out of the commit.

All automated checks should pass before the pull request is merged. A
maintainer may request changes or additional tests during review.

## Reporting Bugs

Use the bug report template and include a minimal F+ program that reproduces
the problem when possible. Include the expected result, actual result, Python
version, operating system, and the full compiler error output.

Please do not report security vulnerabilities in a public issue. Instead,
contact the repository owner privately through their GitHub profile.
