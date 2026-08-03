#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""The copyright header text.

This module is the one place the text lives for every Python repository. A
repository supplies its own package identifier and nothing else. `COPYRIGHT_HEADER.md`
in the `.github` repository maps every repository to its identifier.
"""

from typing import Final


class CopyrightHeaderConstant:
    """The parts the copyright header is built from."""

    # A line comment writes each delimiter of the block comment as a bare comment
    # mark. The mark therefore opens the header, separates each line, and closes it.
    COMMENT_MARK: Final[str] = "#"

    # The package identifier is the only part that changes between repositories.
    IDENTIFIER_FIELD: Final[str] = "identifier"

    TEXT: Final[tuple[str, ...]] = (
        "This file is part of the {identifier} package.",
        "Copyright (c) 2016-present Melech Mizrachi",
        "Released under the MIT License. See LICENSE.md for details.",
    )

    # `\A` holds the header at the first byte of the file. Ruff searches the first
    # 4096 characters for the pattern, so an unanchored pattern also accepts a header
    # that sits below other content.
    ANCHOR: Final[str] = "\\A"

    # The Ruff setting that holds the pattern. `valkyrja-ruff` passes it to Ruff as a
    # `--config` override, because TOML cannot join the shared text to a per-repository
    # identifier on its own.
    NOTICE_RGX_KEY: Final[str] = "lint.flake8-copyright.notice-rgx"
