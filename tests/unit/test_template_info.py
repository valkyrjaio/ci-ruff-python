#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for TemplateInfo.

The release workflow rewrites both constants. Each test asserts a format and never
an exact value.
"""

import re

from valkyrja.template.constant.template_info import TemplateInfo

# The MAJOR.MINOR.PATCH format that the release workflow writes.
VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+")

# The `Month D YYYY HH:MM:SS MST` format that the release workflow writes with
# `date '+%B %-d %Y %T MST'`.
VERSION_BUILD_DATE_TIME_PATTERN = re.compile(r"[A-Z][a-z]+ \d{1,2} \d{4} \d{2}:\d{2}:\d{2} MST")


def test_version_has_the_version_format() -> None:
    assert VERSION_PATTERN.fullmatch(TemplateInfo.VERSION)


def test_version_build_date_time_has_the_build_date_time_format() -> None:
    assert VERSION_BUILD_DATE_TIME_PATTERN.fullmatch(TemplateInfo.VERSION_BUILD_DATE_TIME)
