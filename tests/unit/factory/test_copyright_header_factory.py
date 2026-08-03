#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for CopyrightHeaderFactory."""

import re

import pytest

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException
from valkyrja.ruff.factory.copyright_header_factory import CopyrightHeaderFactory

IDENTIFIER = "Valkyrja Ruff"

# The header a file carries, written out in full. A test that builds the expected
# value from the same constants the code reads asserts nothing, so this is literal.
EXPECTED_HEADER = """\
#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#
"""


def test_get_lines_returns_seven_lines() -> None:
    assert len(CopyrightHeaderFactory.get_lines(IDENTIFIER)) == 7


def test_get_lines_opens_and_closes_with_a_bare_comment_mark() -> None:
    lines = CopyrightHeaderFactory.get_lines(IDENTIFIER)

    assert lines[0] == "#"
    assert lines[-1] == "#"


def test_get_header_returns_the_header_text() -> None:
    assert CopyrightHeaderFactory.get_header(IDENTIFIER) == EXPECTED_HEADER


def test_get_header_names_the_identifier() -> None:
    assert "part of the Valkyrja Ruff package." in CopyrightHeaderFactory.get_header(IDENTIFIER)


def test_get_notice_regex_matches_the_header_it_builds() -> None:
    regex = CopyrightHeaderFactory.get_notice_regex(IDENTIFIER)

    assert re.search(regex, EXPECTED_HEADER)


def test_get_notice_regex_is_anchored_to_the_first_byte() -> None:
    regex = CopyrightHeaderFactory.get_notice_regex(IDENTIFIER)

    assert not re.search(regex, "# a leading comment\n" + EXPECTED_HEADER)


def test_get_notice_regex_rejects_another_identifier() -> None:
    regex = CopyrightHeaderFactory.get_notice_regex("Project Template")

    assert not re.search(regex, EXPECTED_HEADER)


def test_get_notice_regex_escapes_the_period() -> None:
    regex = CopyrightHeaderFactory.get_notice_regex(IDENTIFIER)
    # A period that is not escaped matches any character, so a wrong character passes.
    wrong = EXPECTED_HEADER.replace("LICENSE.md", "LICENSEXmd")

    assert not re.search(regex, wrong)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("plain", '"plain"'),
        ('a "quote"', '"a \\"quote\\""'),
        ("a\\backslash", '"a\\\\backslash"'),
        ("a\nnewline", '"a\\nnewline"'),
        ("a\rreturn", '"a\\rreturn"'),
        ("a\ttab", '"a\\ttab"'),
    ],
)
def test_get_toml_string_escapes_each_character(value: str, expected: str) -> None:
    assert CopyrightHeaderFactory.get_toml_string(value) == expected


def test_get_ruff_config_override_is_a_key_value_pair() -> None:
    override = CopyrightHeaderFactory.get_ruff_config_override(IDENTIFIER)

    assert override.startswith('lint.flake8-copyright.notice-rgx = "')
    assert override.endswith('"')


def test_get_ruff_config_override_holds_no_raw_newline() -> None:
    # A raw newline ends the TOML value early, so Ruff reads a truncated pattern.
    assert "\n" not in CopyrightHeaderFactory.get_ruff_config_override(IDENTIFIER)


def test_validate_identifier_accepts_a_package_name() -> None:
    assert CopyrightHeaderFactory.validate_identifier(IDENTIFIER) is None


@pytest.mark.parametrize("identifier", ["", "   ", "\t", "\n"])
def test_validate_identifier_rejects_an_empty_identifier(identifier: str) -> None:
    with pytest.raises(RuffInvalidIdentifierException, match="empty"):
        CopyrightHeaderFactory.validate_identifier(identifier)


def test_validate_identifier_rejects_the_assembled_header() -> None:
    # The trap: a caller passes the header where the package name belongs.
    with pytest.raises(RuffInvalidIdentifierException, match="more than one line"):
        CopyrightHeaderFactory.validate_identifier(EXPECTED_HEADER)


def test_get_lines_rejects_the_assembled_header() -> None:
    # Every entry point validates, not only the validator.
    with pytest.raises(RuffInvalidIdentifierException):
        CopyrightHeaderFactory.get_lines(EXPECTED_HEADER)


def test_get_notice_regex_holds_the_identifier_as_plain_text() -> None:
    # `_create-repo.yml` renames a new repository by replacing the package name as
    # literal text. `re.escape` also escapes a space, which hid the name from that
    # replacement and left every new repository matching `Project Template`.
    regex = CopyrightHeaderFactory.get_notice_regex(IDENTIFIER)

    assert f"the {IDENTIFIER} package" in regex


def test_get_notice_regex_does_not_escape_a_space_or_a_number_sign() -> None:
    regex = CopyrightHeaderFactory.get_notice_regex(IDENTIFIER)

    assert "\\ " not in regex
    assert "\\#" not in regex


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("plain text", "plain text"),
        ("a.period", "a\\.period"),
        ("(c)", "\\(c\\)"),
        ("2016-present", "2016-present"),
        ("# comment", "# comment"),
        ("a+b*c?", "a\\+b\\*c\\?"),
        ("[]{}|^$", "\\[\\]\\{\\}\\|\\^\\$"),
    ],
)
def test_get_escaped_escapes_only_a_metacharacter(text: str, expected: str) -> None:
    assert CopyrightHeaderFactory.get_escaped(text) == expected
