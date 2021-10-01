"""Main entrypoint for interfacing with meme-generator via cli."""
import argparse
import os
import random
from pathlib import Path
from typing import Optional

from meme_engine import MemeGenerator
from quote_engine.ingest import Ingestor, UnsupportedFileTypeError
from quote_engine.quote_model import QuoteModel

MAXIMUM_QUOTE_LENGTH = 11


def generate_meme(
    body: Optional[str],
    author: str,
    path: Optional[str] = None,
) -> str:
    """Generate a meme given an path and a quote.

    arguments:
        path -- path to image that will be used as meme background
        body -- quote to write on image
        author -- author of quote
    """
    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    elif author is None:
        raise AuthorRequiredError("Author Required if Body is Used")
    else:
        quote = QuoteModel(author, body)

    meme = MemeGenerator(str(Path(path).parent) if path else None)
    path = meme.make_meme(img, quote.line, quote.author)

    return path


class AuthorRequiredError(Exception):
    """Raise if an author needs to be specified."""

    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Meme.")
    parser.add_argument("-path", type=str, help="path to an image file")
    parser.add_argument(
        "-body", type=str, help="quote body to add to the image"
    )
    parser.add_argument(
        "-author",
        type=str,
        help="quote author to add to the image",
    )

    args = parser.parse_args()
    try:
        if path := generate_meme(args.body, args.author, args.path):
            print(path)
    except IsADirectoryError:
        print("You must specify the path to an image file!")
    except UnsupportedFileTypeError as error:
        print(error)
    except AuthorRequiredError:
        print("You need to specify an Author if you use the -body option.")
    except Exception as error:
        print(f"Got an unexpected error: {error}")
