#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Puts the copyright header into Python source text.

Ruff reports a file whose header does not match `notice-rgx`, and it corrects
nothing. This module is what corrects it.
"""

import re

from valkyrja.ruff.constant.copyright_header_constant import CopyrightHeaderConstant
from valkyrja.ruff.factory.copyright_header_factory import CopyrightHeaderFactory

# A shebang names the interpreter, and it must stay on the first line.
SHEBANG_PATTERN = re.compile(r"^#![^\n]*$")

# PEP 263 lets a coding declaration sit on the first line or the second line, and
# Python reads it only there. It must therefore stay above the header too.
CODING_PATTERN = re.compile(r"^#.*coding[:=]\s*[-\w.]+")

# The two sentences that identify a block as a license header rather than as an
# ordinary comment. Both must be present.
HEADER_MARKERS = ("This file is part of the", "Released under the MIT License.")


class PythonSourceFactory:
    """Renders Python source text that carries the correct copyright header."""

    @staticmethod
    def get_preamble_length(lines: list[str]) -> int:
        """Return how many leading lines must stay above the header.

        Warning: a shebang that moves off line 1 stops working, and a coding
        declaration that moves below line 2 stops being read.
        """
        length = 0

        for index, line in enumerate(lines[:2]):
            if index == 0 and SHEBANG_PATTERN.match(line):
                length = 1
            elif CODING_PATTERN.match(line):
                length = index + 1

        return length

    @staticmethod
    def get_header_length(lines: list[str]) -> int:
        """Return the length of the license header that opens these lines.

        Return 0 when the lines do not open with one.

        Warning: never treat the first comment block as a header. A file whose
        first comment explains the code loses that comment, and the gate stays
        green because the file then carries a correct header. This reads the
        leading comment block and requires every marker in it.
        """
        length = 0

        for line in lines:
            if not line.startswith(CopyrightHeaderConstant.COMMENT_MARK):
                break

            length += 1

        block = "\n".join(lines[:length])

        if not all(marker in block for marker in HEADER_MARKERS):
            return 0

        return length

    @staticmethod
    def get_source_with_header(source: str, identifier: str) -> str:
        """Return the source text with the correct header, replacing a wrong one.

        The result is stable: rendering it a second time changes nothing.
        """
        header = CopyrightHeaderFactory.get_header(identifier)
        lines = source.split("\n")

        preamble_length = PythonSourceFactory.get_preamble_length(lines)
        preamble = lines[:preamble_length]
        remainder = lines[preamble_length:]

        # A header that is already correct is left alone, so the file keeps its
        # own spacing below it.
        if "\n".join(remainder).startswith(header):
            return source

        remainder = remainder[PythonSourceFactory.get_header_length(remainder) :]

        # One empty line separates the header from the code. A file that holds
        # only a header gets no separator, because it has nothing to separate.
        body = "\n".join(remainder).lstrip("\n")
        parts = [*preamble, header.rstrip("\n")]

        if body:
            parts.append("")
            parts.append(body)

        rendered = "\n".join(parts)

        # Every file ends with a newline, and a file that holds only a header has
        # no body to supply one.
        if not rendered.endswith("\n"):
            rendered += "\n"

        return rendered
