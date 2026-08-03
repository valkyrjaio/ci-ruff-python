#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for CopyrightHeaderConstant.

The text these tests assert is the text every Valkyrja Python repository carries.
A change here changes every repository, so each value is asserted literally.
"""

from valkyrja.ruff.constant.copyright_header_constant import CopyrightHeaderConstant


def test_text_holds_the_three_lines() -> None:
    assert CopyrightHeaderConstant.TEXT == (
        "This file is part of the {identifier} package.",
        "Copyright (c) 2016-present Melech Mizrachi",
        "Released under the MIT License. See LICENSE.md for details.",
    )


def test_the_year_is_2016() -> None:
    # The first commit in valkyrja-php dates to October 2016. Every repository uses
    # that year, because each port is a translation of the same work.
    assert "2016-present" in CopyrightHeaderConstant.TEXT[1]


def test_only_the_first_line_names_the_package() -> None:
    naming = [text for text in CopyrightHeaderConstant.TEXT if CopyrightHeaderConstant.IDENTIFIER_FIELD in text]

    assert naming == [CopyrightHeaderConstant.TEXT[0]]


def test_comment_mark_is_the_number_sign() -> None:
    assert CopyrightHeaderConstant.COMMENT_MARK == "#"


def test_anchor_holds_the_header_at_the_first_byte() -> None:
    assert CopyrightHeaderConstant.ANCHOR == "\\A"


def test_notice_rgx_key_names_the_ruff_setting() -> None:
    assert CopyrightHeaderConstant.NOTICE_RGX_KEY == "lint.flake8-copyright.notice-rgx"
