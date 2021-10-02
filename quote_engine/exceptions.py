"""Module that specifies exceptions that occur for ingests.

classes:
FileExtensionNotAllowedError -- Throw when the file extension is not allowed.
UnsupportedFileTypeError -- Throw when the file extension is not supported.
"""


class FileExtensionNotAllowedError(Exception):
    """Throw when the file extension is not allowed."""

    pass


class UnsupportedFileTypeError(Exception):
    """Throw when the file extension is not supported.

    This happens when the strategy for finding a file
    ingest class is exhausted.
    """

    pass
