import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from compiler.codegen import CodeGenerationError, CodeGenerator
from compiler.ir_generator import IRGenerationError, IRGenerator
from compiler.lexer import Lexer, LexerError
from compiler.optimizer import OptimizationError, Optimizer
from compiler.parser import Parser, ParserError
from compiler.semantic import SemanticAnalyzer, SemanticError


def compile_file(
    source_path: Path,
    output_path: Path,
    optimize: bool = True,
) -> None:
    source = source_path.read_text(encoding="utf-8")

    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(program)

    ir_program = IRGenerator().generate(program)

    if optimize:
        ir_program = Optimizer().optimize(ir_program)

    assembly = CodeGenerator().generate(ir_program)

    with tempfile.TemporaryDirectory(
        prefix="fplus-"
    ) as temporary_directory:
        build_directory = Path(temporary_directory)
        assembly_path = build_directory / "output.asm"
        object_path = build_directory / "output.o"

        assembly_path.write_text(
            assembly,
            encoding="utf-8",
        )

        subprocess.run(
            [
                "nasm",
                "-f",
                "elf64",
                str(assembly_path),
                "-o",
                str(object_path),
            ],
            check=True,
        )

        subprocess.run(
            [
                "gcc",
                "-no-pie",
                str(object_path),
                "-o",
                str(output_path),
            ],
            check=True,
        )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fplus",
        description=(
            "Compile an F+ source file into a native "
            "x86-64 Linux executable."
        ),
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Path to the F+ source file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path for the generated executable.",
    )

    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Disable intermediate-code optimisation.",
    )

    return parser


def main() -> int:
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()

    source_path: Path = arguments.source

    if not source_path.exists():
        print(
            f"fplus: source file not found: {source_path}",
            file=sys.stderr,
        )
        return 1

    if not source_path.is_file():
        print(
            f"fplus: source path is not a file: {source_path}",
            file=sys.stderr,
        )
        return 1

    if source_path.suffix != ".fp":
        print(
            "fplus: source file must use the .fp extension",
            file=sys.stderr,
        )
        return 1

    output_path: Path

    if arguments.output is not None:
        output_path = arguments.output
    else:
        output_path = source_path.with_suffix("")

    try:
        compile_file(
            source_path,
            output_path,
            optimize=not arguments.no_optimize,
        )
    except (
        LexerError,
        ParserError,
        SemanticError,
        IRGenerationError,
        OptimizationError,
        CodeGenerationError,
    ) as error:
        print(f"fplus: {error}", file=sys.stderr)
        return 1
    except FileNotFoundError as error:
        print(
            f"fplus: required tool not found: {error.filename}",
            file=sys.stderr,
        )
        return 1
    except subprocess.CalledProcessError as error:
        print(
            f"fplus: build tool failed with exit code "
            f"{error.returncode}",
            file=sys.stderr,
        )
        return 1

    print(f"Compiled {source_path} → {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())