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
from valkyrja.ruff.factory.copyright_header_factory import CopyrightHeaderFactory
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
    parser.add_argument(
        "--print-ruff-config",
        action="store_true",
        help="print the Ruff `--config` override that carries the header pattern, and write nothing",
    )

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
        # Warning: test for `None`, never for a false value. An empty `--identifier`
        # is a value the caller gave, and `or` would replace it with the config value
        # instead of reporting it.
        identifier = IdentifierFactory.get_from_config(root) if arguments.identifier is None else arguments.identifier
        # Warning: validate before the loop, never inside it. A run that matches no
        # Python file never enters the loop, so a bad identifier would go unreported
        # and the command would report success.
        CopyrightHeaderFactory.validate_identifier(identifier)
    except RuffInvalidIdentifierException as exception:
        print(f"error: {exception}")

        return EXIT_ERROR

    if arguments.print_ruff_config:
        print(CopyrightHeaderFactory.get_ruff_config_override(identifier))

        return EXIT_OK

    changed: list[Path] = []

    for path in get_python_files(root, arguments.paths):
        source = path.read_text(encoding="utf-8")
        rendered = PythonSourceFactory.get_source_with_header(source, identifier)

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
