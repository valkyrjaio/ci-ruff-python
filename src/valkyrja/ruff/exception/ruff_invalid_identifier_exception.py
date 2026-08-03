#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""The exception a bad package identifier raises."""


class RuffInvalidIdentifierException(ValueError):
    """The package identifier is not a name this package can build a header from.

    The abstract bases that `THROWABLES.md` describes arrive with the Python
    framework repository. This exception extends the native base until then.
    """
