from collections import Counter
from unittest.mock import Mock

import pytest

from .ingest import (CsvFileIngest, DocxFileIngest, FileExtensionNotAllowed,
                     Ingestor, PdfFileIngest, TxtFileIngest)
from .quote_model import QuoteMode


class TestTxtFileIngest:
    def test_parses_txt_file_and_returns_quotes(self) -> None:
        actual_quotes = TxtFileIngest.parse(
            "./_data/DogQuotes/DogQuotesTXT.txt"
        )
        assert Counter(actual_quotes) == Counter(
            [
                QuoteMode(author="Bork", line="To bork or not to bork"),
                QuoteMode(author="Stinky", line="He who smelt it..."),
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
                QuoteMode(author="Skittle", line="Chase the mailman"),
                QuoteMode(
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
                QuoteMode(author="Rex", line="Bark like no one’s listening"),
                QuoteMode(author="Chewy", line="RAWRGWAWGGR"),
                QuoteMode(
                    author="Peanut", line="Life is like peanut butter: crunchy"
                ),
                QuoteMode(author="Tiny", line="Channel your inner husky"),
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
                QuoteMode(author="Fluffles", line="Treat yo self"),
                QuoteMode(
                    author="Forrest Pup", line="Life is like a box of treats"
                ),
                QuoteMode(
                    author="Bark Twain",
                    line="It's the size of the fight in the dog",
                ),
            ]
        )

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            PdfFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.txt")
