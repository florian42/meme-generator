import os
from collections import Counter

import pytest

from .ingest import (CsvFileIngest, DocxFileIngest, FileExtensionNotAllowed,
                     PdfFileIngest, TxtFileIngest)
from .quote_model import QuoteModel


class TestTxtFileIngest:
    def test_parses_txt_file_and_returns_quotes(self) -> None:
        actual_quotes = TxtFileIngest.parse(
            "./_data/DogQuotes/DogQuotesTXT.txt"
        )
        assert Counter(actual_quotes) == Counter(
            [
                QuoteModel(author="Bork", line="To bork or not to bork"),
                QuoteModel(author="Stinky", line="He who smelt it..."),
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
                QuoteModel(author="Skittle", line="Chase the mailman"),
                QuoteModel(
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
                QuoteModel(author="Rex", line="Bark like no one’s listening"),
                QuoteModel(author="Chewy", line="RAWRGWAWGGR"),
                QuoteModel(
                    author="Peanut", line="Life is like peanut butter: crunchy"
                ),
                QuoteModel(author="Tiny", line="Channel your inner husky"),
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
                QuoteModel(author="Fluffles", line="Treat yo self"),
                QuoteModel(
                    author="Forrest Pup", line="Life is like a box of treats"
                ),
                QuoteModel(
                    author="Bark Twain",
                    line="It's the size of the fight in the dog",
                ),
            ]
        )
        assert os.path.isfile(PdfFileIngest.temporary_text_file_path) is False

    def test_does_not_open_other_files(self) -> None:
        with pytest.raises(FileExtensionNotAllowed):
            PdfFileIngest.parse("../_data/DogQuotes/DogQuotesTXT.txt")
