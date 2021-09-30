"""Main entrypoint for interfacing with meme-generator via cli."""
import argparse
import os
import random
from typing import Optional

from meme_engine import MemeGenerator
from quote_engine.ingest import Ingestor
from quote_engine.quote_model import QuoteModel


def generate_meme(
    body: str,
    author: str,
    path: Optional[str] = None,
) -> str:
    """Generate a meme given an path and a quote.

    arguments:
        path -- path to file that will be ingested
        body -- quote to write on image
        author -- author of quote
    """
    img = None
    quote = None

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
        raise Exception("Author Required if Body is Used")
    else:
        quote = QuoteModel(author, body)

    meme = MemeGenerator(path)
    path = meme.make_meme(img, quote.line, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Meme.")
    parser.add_argument("-path", type=str, help="path to an image file")
    parser.add_argument(
        "-body", type=str, help="quote body to add to the image", required=True
    )
    parser.add_argument(
        "-author",
        type=str,
        help="quote author to add to the image",
        required=True,
    )

    args = parser.parse_args()
    print(generate_meme(args.body, args.author, args.path))
