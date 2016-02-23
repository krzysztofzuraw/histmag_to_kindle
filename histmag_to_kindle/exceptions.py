"""Histmag to kindle exception module."""


class GenerateMobiError(Exception):
    """Exception wrapper around kindlegen binary."""

    pass


class ImproperlyConfigured(Exception):
    """Raised when there is some configuration variable missing."""

    pass
