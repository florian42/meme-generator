"""Module Ingest specifies all Ingest classes."""
import csv
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List

import docx

from .quote_model import Quote


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
    def parse(cls, path: str) -> List[Quote]:
        """Parse a file to a list of quotes."""
        pass

    @classmethod
    def raise_if_invalid_file_type(cls, path: str):
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
    ) -> List[Quote]:
        """Parse a txt file.

        It strips bad characters except '...'.
        """
        quotes: List[Quote] = []

        cls.raise_if_invalid_file_type(path)
        with open(path, mode="r") as file:
            for line in file:
                if "-" in line:
                    quote, author = (
                        line.strip(character_to_remove)
                        .replace('"', "")
                        .split(" - ")
                    )
                    quotes.append(Quote(author, quote))
        return quotes


class CsvFileIngest(IngestInterface):
    """Ingest a csv file."""

    allowed_extensions = [".csv"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a csv file."""
        cls.raise_if_invalid_file_type(path)
        with open(path, "r") as file:
            return [
                Quote(row["author"], row["body"])
                for row in csv.DictReader(file)
            ]


class DocxFileIngest(IngestInterface):
    """Ingest a docx file."""

    allowed_extensions = [".docx"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a docx file."""
        cls.raise_if_invalid_file_type(path)
        quotes = []
        for paragraph in docx.Document(path).paragraphs:
            if paragraph.text != "":
                parsed_paragraph = paragraph.text.split(" - ")
                quotes.append(
                    Quote(parsed_paragraph[1], parsed_paragraph[0].strip('"'))
                )

        return quotes


class PdfFileIngest(IngestInterface):
    """Ingest a pdf file."""

    allowed_extensions = [".pdf"]
    temporary_text_file_path = "temp.txt"
    pdf_cli_tool = "pdftotext"

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a pdf file."""
        cls.raise_if_invalid_file_type(path)
        subprocess.run(
            [cls.pdf_cli_tool, "-layout", path, cls.temporary_text_file_path],
            capture_output=True,
            check=True,
        )
        return TxtFileIngest.parse(cls.temporary_text_file_path, '"\n')


class FileExtensionNotAllowed(Exception):
    """Throw when the file extension is not supported."""

    pass
