#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Holds this repository's own Ruff configuration to the canonical header text.

Ruff reads `notice-rgx` from a TOML file, and TOML holds no interpolation, so the
file carries the pattern in full. The text therefore appears twice: once in
`CopyrightHeaderConstant`, and once in the configuration Ruff reads.

Warning: without this test, a change to the canonical text leaves the
configuration behind, and nothing reports it. Ruff keeps demanding the old text,
and the gate fails on every file with no indication of the cause. This test names
the cause.

A repository that consumes this package generates the same value instead:

    valkyrja-ruff-header --print-ruff-config
"""

import re
import tomllib
from pathlib import Path

from valkyrja.ruff.factory.copyright_header_factory import CopyrightHeaderFactory
from valkyrja.ruff.factory.identifier_factory import IdentifierFactory

ROOT = Path(__file__).resolve().parents[2]
RUFF_CONFIG_PATH = ROOT / ".github" / "ci" / "ruff" / "pyproject.toml"


def get_notice_regex() -> str:
    config = tomllib.loads(RUFF_CONFIG_PATH.read_text(encoding="utf-8"))
    notice_rgx = config["tool"]["ruff"]["lint"]["flake8-copyright"]["notice-rgx"]

    assert isinstance(notice_rgx, str)

    return notice_rgx


def test_the_ruff_pattern_is_the_one_the_factory_builds() -> None:
    identifier = IdentifierFactory.get_from_config(ROOT)

    assert get_notice_regex() == CopyrightHeaderFactory.get_notice_regex(identifier)


def test_the_ruff_pattern_matches_this_repository_s_own_files() -> None:
    # The pattern is only correct if it accepts the files it governs.
    identifier = IdentifierFactory.get_from_config(ROOT)
    pattern = re.compile(get_notice_regex())
    sources = sorted((ROOT / "src").rglob("*.py"))

    assert sources

    for path in sources:
        assert pattern.search(path.read_text(encoding="utf-8")), f"{path} does not match notice-rgx"

    assert CopyrightHeaderFactory.get_header(identifier) in sources[0].read_text(encoding="utf-8")
