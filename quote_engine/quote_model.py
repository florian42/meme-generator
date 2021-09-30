"""Module QuoteModel contains a dataclass that represents quotes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuoteModel:
    """Class QuoteModel represents quotes from authors.

    A quote can only contain one line and one author.
    """

    author: str
    line: str

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f'"{self.line}" - {self.author}'
