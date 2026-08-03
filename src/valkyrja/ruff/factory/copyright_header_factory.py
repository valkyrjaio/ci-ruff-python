#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Builds the copyright header, and the Ruff pattern that enforces it."""

import re

from valkyrja.ruff.constant.copyright_header_constant import CopyrightHeaderConstant
from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException


class CopyrightHeaderFactory:
    """Renders the copyright header from a package identifier."""

    @staticmethod
    def validate_identifier(identifier: str) -> None:
        """Raise when the identifier is not a package name.

        Warning: a caller that passes the assembled header where the name belongs
        builds `This file is part of the <whole header> package.` The header text and
        the identifier are separate values, and this guard keeps them separate.
        """
        if not identifier.strip():
            raise RuffInvalidIdentifierException(
                "The package identifier is empty. COPYRIGHT_HEADER.md in the .github "
                "repository maps every repository to its own identifier."
            )

        if "\n" in identifier:
            raise RuffInvalidIdentifierException(
                "The package identifier holds more than one line, so it is the header "
                "text rather than a package name. Pass a name such as 'Valkyrja Ruff'."
            )

    @staticmethod
    def get_lines(identifier: str) -> tuple[str, ...]:
        """Return the header as the seven lines a Python file carries."""
        CopyrightHeaderFactory.validate_identifier(identifier)

        mark = CopyrightHeaderConstant.COMMENT_MARK
        lines = [mark]

        for text in CopyrightHeaderConstant.TEXT:
            lines.append(f"{mark} {text.format(**{CopyrightHeaderConstant.IDENTIFIER_FIELD: identifier})}")
            lines.append(mark)

        return tuple(lines)

    @staticmethod
    def get_header(identifier: str) -> str:
        """Return the header as the text a file opens with."""
        return "".join(f"{line}\n" for line in CopyrightHeaderFactory.get_lines(identifier))

    @staticmethod
    def get_notice_regex(identifier: str) -> str:
        """Return the anchored pattern that Ruff `CPY001` matches the header with."""
        lines = CopyrightHeaderFactory.get_lines(identifier)

        return CopyrightHeaderConstant.ANCHOR + "\n".join(re.escape(line) for line in lines)

    @staticmethod
    def get_toml_string(value: str) -> str:
        """Return the value as a TOML basic string.

        The pattern holds a backslash, a newline, and a double quote, and each one
        ends the value early when it is written as it stands.
        """
        escaped = [
            {'"': '\\"', "\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"}.get(character, character)
            for character in value
        ]

        return '"' + "".join(escaped) + '"'

    @staticmethod
    def get_ruff_config_override(identifier: str) -> str:
        """Return the `--config` argument that gives Ruff the pattern.

        TOML holds no interpolation, so a shared configuration file cannot join the
        shared text to a per-repository identifier. Ruff reads a `KEY = VALUE` pair on
        the command line, and that pair takes precedence over every configuration file,
        so the two are joined at the moment the tool runs.
        """
        regex = CopyrightHeaderFactory.get_notice_regex(identifier)

        return f"{CopyrightHeaderConstant.NOTICE_RGX_KEY} = {CopyrightHeaderFactory.get_toml_string(regex)}"
