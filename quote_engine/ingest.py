"""Module Ingest specifies all Ingest classes."""
import csv
import os
from abc import ABC, abstractmethod
from typing import List

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


class TxtFileIngest(IngestInterface):
    """Ingest a txt file."""

    allowed_extensions = [".txt"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a txt file.

        It strips bad characters except '...'.
        """
        quotes: List[Quote] = []

        if not cls.can_ingest(path):
            raise FileExtensionNotAllowed(
                (
                    f"Can only open files of type {cls.allowed_extensions},"
                    f"got {path}"
                )
            )
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file:
                quote, author = line.strip("\n\ufeff").split(" - ")
                quotes.append(Quote(author, quote))
        return quotes


class CsvFileIngest(IngestInterface):
    """Ingest a csv file."""

    allowed_extensions = [".csv"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a csv file."""
        if not cls.can_ingest(path):
            raise FileExtensionNotAllowed(
                (
                    f"Can only open files of type {cls.allowed_extensions},"
                    f"got {path}"
                )
            )
        with open(path, "r") as file:
            return [
                Quote(row["author"], row["body"])
                for row in csv.DictReader(file)
            ]


class FileExtensionNotAllowed(Exception):
    """Throw when the file extensions is not supported."""

    pass
