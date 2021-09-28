from collections import Counter

import pytest

from .ingest import (CsvFileIngest, DocxFileIngest, FileExtensionNotAllowed,
                     PdfFileIngest, TxtFileIngest)
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
            CsvFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.pdf")


class TestDocxFileIngest:
    def test_parses_docx_file_and_returns_quotes(self) -> None:
        actual_quotes = DocxFileIngest.parse(
            "./_data/DogQuotes/DogQuotesDOCX.docx"
        )
        assert Counter(actual_quotes) == Counter(
            [
                Quote(author="Rex", line="Bark like no one’s listening"),
                Quote(author="Chewy", line="RAWRGWAWGGR"),
                Quote(
                    author="Peanut", line="Life is like peanut butter: crunchy"
                ),
                Quote(author="Tiny", line="Channel your inner husky"),
            ]
        )

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            DocxFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.pdf")


class TestPdfFileIngest:
    def test_parses_pdf_file_and_returns_quotes(self) -> None:
        actual_quotes = PdfFileIngest.parse(
            "./_data/DogQuotes/DogQuotesPDF.pdf"
        )
        assert Counter(actual_quotes) == Counter(
            [
                Quote(author="Fluffles", line="Treat yo self"),
                Quote(
                    author="Forrest Pup", line="Life is like a box of treats"
                ),
                Quote(
                    author="Bark Twain",
                    line="It's the size of the fight in the dog",
                ),
            ]
        )

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            PdfFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.txt")
