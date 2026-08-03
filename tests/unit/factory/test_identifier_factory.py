#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for IdentifierFactory."""

from pathlib import Path

import pytest

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException
from valkyrja.ruff.factory.identifier_factory import CONFIG_PATH, IdentifierFactory


def write_config(root: Path, body: str) -> None:
    path = root / CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_it_reads_the_identifier(tmp_path: Path) -> None:
    write_config(tmp_path, "IDENTIFIER='Valkyrja Ruff'\n")

    assert IdentifierFactory.get_from_config(tmp_path) == "Valkyrja Ruff"


def test_it_reads_the_identifier_among_other_settings(tmp_path: Path) -> None:
    write_config(tmp_path, "# a comment\nIDENTIFIER='Valkyrja PHPStan'\nEXCLUDED=(\n    '*.md'\n)\n")

    assert IdentifierFactory.get_from_config(tmp_path) == "Valkyrja PHPStan"


def test_it_reads_a_name_that_holds_a_hyphen(tmp_path: Path) -> None:
    write_config(tmp_path, "IDENTIFIER='Valkyrja golangci-lint'\n")

    assert IdentifierFactory.get_from_config(tmp_path) == "Valkyrja golangci-lint"


def test_it_reports_a_missing_config(tmp_path: Path) -> None:
    with pytest.raises(RuffInvalidIdentifierException, match="No copyright header config"):
        IdentifierFactory.get_from_config(tmp_path)


def test_it_reports_a_config_that_sets_no_identifier(tmp_path: Path) -> None:
    write_config(tmp_path, "EXCLUDED=(\n    '*.md'\n)\n")

    with pytest.raises(RuffInvalidIdentifierException, match="sets no IDENTIFIER"):
        IdentifierFactory.get_from_config(tmp_path)
