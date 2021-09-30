"""Module to handle file ingests.

classes:
IngestInterface -- Abstract class that specifies Ingest behaviour
TxtFileIngest -- Class to ingest .txt files
CsvFileIngest -- Class to ingest .csv files using pandas
DocxFileIngest -- Class to ingest .docx files using pydocx
PdfFileIngest -- Class to ingest .pdf files by invoking xpdf from environment
Ingestor -- Class to that selected a suitable file ingest and returns
the result
FileExtensionNotAllowed -- Exception that is raised if a module tries to
ingest an unsupported file
UnsupportedFileType -- Exception that is raised when no suitable file
ingest could be selected
"""
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List

import docx
import pandas

from .quote_model import QuoteModel


class IngestInterface(ABC):
    """IngestInterface defines the interface common to all ingest modules."""

    allowed_extensions: List[str] = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return if the file extension is in 'allowed_extensions'."""
        _, file_extension = os.path.splitext(path)
        return file_extension in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file to a list of quotes."""
        pass

    @classmethod
    def raise_for_unsupported_file_type(cls, path: str) -> None:
        """Raise an exception if the file type is not supported.

        arguments:
        path -- path to file that will be ingested
        """
        if not cls.can_ingest(path):
            raise FileExtensionNotAllowed(
                (
                    f"Can only open files of type {cls.allowed_extensions},"
                    f"got {path}"
                )
            )


class TxtFileIngest(IngestInterface):
    """Ingest a txt file."""

    allowed_extensions = [".txt"]

    @classmethod
    def parse(
        cls, path: str, character_to_remove: str = "\n\ufeff"
    ) -> List[QuoteModel]:
        """Parse a txt file.

        It strips bad characters except '...'.
        """
        quotes: List[QuoteModel] = []

        cls.raise_for_unsupported_file_type(path)
        with open(path, mode="r") as file:
            for line in file:
                if "-" in line:
                    quote, author = (
                        line.strip(character_to_remove)
                        .replace('"', "")
                        .split(" - ")
                    )
                    quotes.append(QuoteModel(author, quote))
        return quotes


class CsvFileIngest(IngestInterface):
    """Ingest a csv file."""

    allowed_extensions = [".csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a csv file."""
        cls.raise_for_unsupported_file_type(path)
        return [
            QuoteModel(row["author"], row["body"])
            for index, row in pandas.read_csv(path).iterrows()
        ]


class DocxFileIngest(IngestInterface):
    """Ingest a docx file."""

    allowed_extensions = [".docx"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a docx file."""
        cls.raise_for_unsupported_file_type(path)
        quotes = []
        for paragraph in docx.Document(path).paragraphs:
            if paragraph.text != "":
                parsed_paragraph = paragraph.text.split(" - ")
                quotes.append(
                    QuoteModel(
                        parsed_paragraph[1], parsed_paragraph[0].strip('"')
                    )
                )

        return quotes


class PdfFileIngest(IngestInterface):
    """Ingest a pdf file."""

    allowed_extensions = [".pdf"]
    temporary_text_file_path = "temp.txt"
    pdf_cli_tool = "pdftotext"

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a pdf file."""
        cls.raise_for_unsupported_file_type(path)
        subprocess.run(
            [cls.pdf_cli_tool, "-layout", path, cls.temporary_text_file_path],
            capture_output=True,
            check=True,
        )
        quotes = TxtFileIngest.parse(cls.temporary_text_file_path, '"\n')
        os.remove(cls.temporary_text_file_path)
        return quotes


class Ingestor(IngestInterface):
    """Parse different file types.

    Public Methods:
    parse -- Given a path to a file parse its contents
    to a list of `QuoteModel`.
    """

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of `QuoteModel` by parsing a file."""
        if DocxFileIngest.can_ingest(path):
            return DocxFileIngest.parse(path)
        if CsvFileIngest.can_ingest(path):
            return CsvFileIngest.parse(path)
        if TxtFileIngest.can_ingest(path):
            return TxtFileIngest.parse(path)
        if PdfFileIngest.can_ingest(path):
            return PdfFileIngest.parse(path)
        raise UnsupportedFileType()


class FileExtensionNotAllowed(Exception):
    """Throw when the file extension is not allowed."""

    pass


class UnsupportedFileType(Exception):
    """Throw when the file extension is not supported.

    This happens when the strategy for finding a file
    ingest class is exhausted.
    """

    pass
