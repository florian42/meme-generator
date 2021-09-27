from collections import Counter

import pytest

from .ingest import FileExtensionNotAllowed, TxtFileIngest
from .quote_model import Quote


class TestTxtFileIngest:
    def test_parses_txt_file_and_returns_quotes(self) -> None:
        actual_quotes = TxtFileIngest.parse(
            "./_data/DogQuotes/DogQuotesTXT.txt"
        )
        assert Counter(actual_quotes) == Counter(
            [
                Quote(author="Bork", line="To bork or not to bork"),
                Quote(author="Stinky", line="He who smelt it..."),
            ]
        )

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            TxtFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.pdf")
