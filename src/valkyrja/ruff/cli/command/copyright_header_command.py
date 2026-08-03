#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""The command that puts the copyright header into every Python file."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException
from valkyrja.ruff.factory.identifier_factory import IdentifierFactory
from valkyrja.ruff.factory.python_source_factory import PythonSourceFactory

EXIT_OK = 0
EXIT_CHANGED = 1
EXIT_ERROR = 2


def get_parser() -> argparse.ArgumentParser:
    """Return the parser for this command."""
    parser = argparse.ArgumentParser(
        prog="valkyrja-ruff-header",
        description="Put the Valkyrja copyright header into every Python file.",
    )
    parser.add_argument("paths", nargs="*", default=["src", "tests"], help="the paths to read")
    parser.add_argument(
        "--check",
        action="store_true",
        help="report a file that needs the header, and write nothing",
    )
    parser.add_argument(
        "--identifier",
        default=None,
        help="the package identifier; read from the copyright header config when absent",
    )
    parser.add_argument("--root", default=".", help="the repository root")

    return parser


def get_python_files(root: Path, paths: Sequence[str]) -> list[Path]:
    """Return every Python file under the given paths, in a stable order."""
    files: list[Path] = []

    for name in paths:
        path = root / name

        if path.is_file():
            files.append(path)
            continue

        files.extend(path.rglob("*.py"))

    return sorted(set(files))


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command, and return the exit code."""
    arguments = get_parser().parse_args(argv)
    root = Path(arguments.root)

    try:
        identifier = arguments.identifier or IdentifierFactory.get_from_config(root)
    except RuffInvalidIdentifierException as exception:
        print(f"error: {exception}")

        return EXIT_ERROR

    changed: list[Path] = []

    for path in get_python_files(root, arguments.paths):
        source = path.read_text(encoding="utf-8")

        try:
            rendered = PythonSourceFactory.get_source_with_header(source, identifier)
        except RuffInvalidIdentifierException as exception:
            print(f"error: {exception}")

            return EXIT_ERROR

        if rendered == source:
            continue

        changed.append(path)

        if not arguments.check:
            path.write_text(rendered, encoding="utf-8")

    if not changed:
        print("Every Python file carries the copyright header.")

        return EXIT_OK

    verb = "needs" if arguments.check else "took"

    for path in changed:
        print(f"{path} {verb} the copyright header")

    # `--check` reports a failure so a gate can run it. A run that writes reports
    # success, because it fixed what it found.
    return EXIT_CHANGED if arguments.check else EXIT_OK
