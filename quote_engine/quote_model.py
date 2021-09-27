"""Module QuoteModel contains a dataclass that represents quotes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    """Class Quote represents quotes from authors.

    A quote can only contain one line and one author.
    """

    author: str
    line: str
