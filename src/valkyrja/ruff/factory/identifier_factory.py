#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Reads the package identifier that a repository declares."""

import re
from pathlib import Path

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException

# The copyright header check reads the same file, so the repository declares its
# name once and both mechanisms agree. COPYRIGHT_HEADER.md maps every repository
# to its own identifier.
CONFIG_PATH = Path(".github/ci/copyright-header/config")

IDENTIFIER_PATTERN = re.compile(r"^IDENTIFIER='([^']*)'$", re.MULTILINE)


class IdentifierFactory:
    """Renders the package identifier from the repository's own configuration."""

    @staticmethod
    def get_from_config(root: Path) -> str:
        """Return the identifier that the copyright header config declares."""
        path = root / CONFIG_PATH

        if not path.is_file():
            raise RuffInvalidIdentifierException(
                f"No copyright header config at {path}. The file sets IDENTIFIER, and "
                "COPYRIGHT_HEADER.md in the .github repository maps every repository to its own."
            )

        match = IDENTIFIER_PATTERN.search(path.read_text(encoding="utf-8"))

        if match is None:
            raise RuffInvalidIdentifierException(
                f"{path} sets no IDENTIFIER. The value is a package name in single quotes, on a line of its own."
            )

        return match.group(1)
