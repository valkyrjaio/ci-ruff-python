#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for PythonSourceFactory."""

import pytest

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException
from valkyrja.ruff.factory.python_source_factory import PythonSourceFactory

IDENTIFIER = "Valkyrja Ruff"

HEADER = """\
#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#
"""

OTHER_HEADER = HEADER.replace("Valkyrja Ruff", "Project Template")

FIVE_LINE_HEADER = """\
# This file is part of the Project Template package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
"""


def render(source: str) -> str:
    return PythonSourceFactory.get_source_with_header(source, IDENTIFIER)


def test_it_adds_the_header_to_a_file_that_has_none() -> None:
    assert render("X = 1\n") == HEADER + "\nX = 1\n"


def test_it_leaves_a_correct_header_alone() -> None:
    source = HEADER + "\nX = 1\n"

    assert render(source) == source


def test_it_is_stable() -> None:
    # Rendering a second time must change nothing, or a gate never goes green.
    once = render("X = 1\n")

    assert render(once) == once


def test_it_replaces_a_header_that_names_another_package() -> None:
    assert render(OTHER_HEADER + "\nX = 1\n") == HEADER + "\nX = 1\n"


def test_it_replaces_the_five_line_form() -> None:
    assert render(FIVE_LINE_HEADER + "\nX = 1\n") == HEADER + "\nX = 1\n"


def test_it_keeps_a_shebang_on_the_first_line() -> None:
    rendered = render("#!/usr/bin/env python\nX = 1\n")

    assert rendered.startswith("#!/usr/bin/env python\n")
    assert rendered == "#!/usr/bin/env python\n" + HEADER + "\nX = 1\n"


def test_it_keeps_a_coding_declaration_above_the_header() -> None:
    rendered = render("# -*- coding: utf-8 -*-\nX = 1\n")

    assert rendered == "# -*- coding: utf-8 -*-\n" + HEADER + "\nX = 1\n"


def test_it_keeps_a_shebang_and_a_coding_declaration_together() -> None:
    source = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nX = 1\n"
    rendered = render(source)

    assert rendered == "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n" + HEADER + "\nX = 1\n"


def test_it_replaces_a_wrong_header_below_a_shebang() -> None:
    rendered = render("#!/usr/bin/env python\n" + OTHER_HEADER + "\nX = 1\n")

    assert rendered == "#!/usr/bin/env python\n" + HEADER + "\nX = 1\n"


def test_it_never_eats_an_ordinary_leading_comment() -> None:
    # PHP CS Fixer replaces the first comment block, and a file whose first
    # comment explains the code loses it. This must add the header above instead.
    source = "# This comment explains the code below.\nX = 1\n"
    rendered = render(source)

    assert "This comment explains the code below." in rendered
    assert rendered == HEADER + "\n" + source


def test_it_never_eats_a_module_docstring() -> None:
    source = '"""The module docstring."""\n\nX = 1\n'

    assert render(source) == HEADER + "\n" + source


def test_it_handles_a_file_that_holds_only_a_header() -> None:
    assert render(OTHER_HEADER) == HEADER


def test_it_handles_an_empty_file() -> None:
    assert render("") == HEADER


def test_it_rejects_the_assembled_header_as_an_identifier() -> None:
    with pytest.raises(RuffInvalidIdentifierException):
        PythonSourceFactory.get_source_with_header("X = 1\n", HEADER)


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        (["X = 1"], 0),
        (["#!/usr/bin/env python", "X = 1"], 1),
        (["# -*- coding: utf-8 -*-", "X = 1"], 1),
        (["#!/usr/bin/env python", "# coding=utf-8", "X = 1"], 2),
        # PEP 263 reads a coding declaration only on the first two lines.
        (["X = 1", "Y = 2", "# coding=utf-8"], 0),
    ],
)
def test_get_preamble_length(lines: list[str], expected: int) -> None:
    assert PythonSourceFactory.get_preamble_length(lines) == expected


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        (HEADER.rstrip("\n").split("\n"), 7),
        (FIVE_LINE_HEADER.rstrip("\n").split("\n"), 5),
        # A comment block that carries neither marker is not a header.
        (["# just a comment", "X = 1"], 0),
        # One marker alone is not enough to call a block a header.
        (["# This file is part of the thing.", "X = 1"], 0),
        ([], 0),
    ],
)
def test_get_header_length(lines: list[str], expected: int) -> None:
    assert PythonSourceFactory.get_header_length(lines) == expected
