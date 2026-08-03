#
# This file is part of the Valkyrja Ruff package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for RuffInvalidIdentifierException."""

from valkyrja.ruff.exception.ruff_invalid_identifier_exception import RuffInvalidIdentifierException


def test_it_is_a_value_error() -> None:
    # THROWABLES.md maps the invalid-argument exception onto the native ValueError.
    assert issubclass(RuffInvalidIdentifierException, ValueError)


def test_it_carries_its_message() -> None:
    exception = RuffInvalidIdentifierException("the message")

    assert str(exception) == "the message"
