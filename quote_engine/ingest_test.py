from collections import Counter

import pytest

from .ingest import CsvFileIngest, FileExtensionNotAllowed, TxtFileIngest
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


class TestCsvFileIngest:
    def test_parses_csv_file_and_returns_quotes(self) -> None:
        actual_quotes = CsvFileIngest.parse(
            "./_data/DogQuotes/DogQuotesCSV.csv"
        )
        assert Counter(actual_quotes) == Counter(
            [
                Quote(author="Skittle", line="Chase the mailman"),
                Quote(
                    author="Mr. Paws", line="When in doubt, go shoe-shopping"
                ),
            ]
        )

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            TxtFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.pdf")
