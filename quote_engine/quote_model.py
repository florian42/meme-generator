"""Module QuoteModel contains a dataclass that represents quotes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuoteMode:
    """Class QuoteMode represents quotes from authors.

    A quote can only contain one line and one author.
    """

    author: str
    line: str

    def __str__(self):
        """Return a human-readable string representation."""
        return f'"{self.line}" - {self.author}'
