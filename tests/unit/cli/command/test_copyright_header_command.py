#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the copyright header command."""

from pathlib import Path

import pytest

from valkyrja.ruff.cli.command.copyright_header_command import (
    EXIT_CHANGED,
    EXIT_ERROR,
    EXIT_OK,
    get_python_files,
    main,
)
from valkyrja.ruff.factory.identifier_factory import CONFIG_PATH

HEADER = """\
#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#
"""


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    config = tmp_path / CONFIG_PATH
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("IDENTIFIER='Valkyrja Ruff'\n", encoding="utf-8")
    (tmp_path / "src").mkdir()

    return tmp_path


def run(repository: Path, *arguments: str) -> int:
    return main(["--root", str(repository), *arguments])


def test_it_writes_the_header(repository: Path) -> None:
    source = repository / "src" / "thing.py"
    source.write_text("X = 1\n", encoding="utf-8")

    assert run(repository, "src") == EXIT_OK
    assert source.read_text(encoding="utf-8") == HEADER + "\nX = 1\n"


def test_it_reports_success_when_every_file_is_correct(repository: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repository / "src" / "thing.py").write_text(HEADER + "\nX = 1\n", encoding="utf-8")

    assert run(repository, "src") == EXIT_OK
    assert "Every Python file carries the copyright header." in capsys.readouterr().out


def test_check_writes_nothing_and_reports_a_failure(repository: Path) -> None:
    source = repository / "src" / "thing.py"
    source.write_text("X = 1\n", encoding="utf-8")

    assert run(repository, "src", "--check") == EXIT_CHANGED
    assert source.read_text(encoding="utf-8") == "X = 1\n"


def test_check_reports_success_when_every_file_is_correct(repository: Path) -> None:
    (repository / "src" / "thing.py").write_text(HEADER + "\nX = 1\n", encoding="utf-8")

    assert run(repository, "src", "--check") == EXIT_OK


def test_it_names_each_file_it_changed(repository: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repository / "src" / "thing.py").write_text("X = 1\n", encoding="utf-8")
    run(repository, "src")

    assert "took the copyright header" in capsys.readouterr().out


def test_check_names_each_file_that_needs_it(repository: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repository / "src" / "thing.py").write_text("X = 1\n", encoding="utf-8")
    run(repository, "src", "--check")

    assert "needs the copyright header" in capsys.readouterr().out


def test_the_identifier_argument_wins(repository: Path) -> None:
    source = repository / "src" / "thing.py"
    source.write_text("X = 1\n", encoding="utf-8")
    run(repository, "src", "--identifier", "Sindri")

    assert "part of the Sindri package." in source.read_text(encoding="utf-8")


def test_it_reports_a_missing_config(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--root", str(tmp_path), "src"]) == EXIT_ERROR
    assert "No copyright header config" in capsys.readouterr().out


def test_it_reports_an_identifier_that_is_the_whole_header(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # The trap: the caller passes the assembled header where the name belongs.
    (repository / "src" / "thing.py").write_text("X = 1\n", encoding="utf-8")

    assert run(repository, "src", "--identifier", HEADER) == EXIT_ERROR
    assert "more than one line" in capsys.readouterr().out


def test_it_takes_a_file_path(repository: Path) -> None:
    source = repository / "src" / "thing.py"
    source.write_text("X = 1\n", encoding="utf-8")

    assert run(repository, str(source)) == EXIT_OK
    assert source.read_text(encoding="utf-8").startswith(HEADER)


def test_get_python_files_reads_a_directory_and_a_file(repository: Path) -> None:
    (repository / "src" / "a.py").write_text("", encoding="utf-8")
    (repository / "src" / "nested").mkdir()
    (repository / "src" / "nested" / "b.py").write_text("", encoding="utf-8")
    (repository / "src" / "notes.txt").write_text("", encoding="utf-8")

    found = get_python_files(repository, ["src"])

    assert [path.name for path in found] == ["a.py", "b.py"]
