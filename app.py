"""Module sets up a web server using flask as interface for meme generator."""
import os
import random
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import uuid4

import requests
from flask import Flask, abort, render_template, request

from meme_engine import MemeGenerator
from quote_engine.ingest import Ingestor
from quote_engine.quote_model import QuoteModel

app = Flask(__name__)

meme = MemeGenerator("./static")


def setup() -> Tuple[List[QuoteModel], List[str]]:
    """Load all resources."""
    quotes = []
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"
    imgs = []  # images within the images images_path directory
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand() -> str:
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.line, quote.author)
    print(meme)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form() -> str:
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post() -> str:
    """Create a user defined meme."""
    body: Optional[str] = request.form.get("body")
    author: Optional[str] = request.form.get("author")
    image_url = request.form.get("image_url")
    if image_url and body and author:
        tmp = f"./tmp/{uuid4()}.png"
        temp_dir = Path(tmp).parent
        if not temp_dir.exists():
            os.mkdir(temp_dir)
        try:
            response = requests.get(image_url, allow_redirects=True)
            with open(tmp, "wb") as file:
                file.write(response.content)
            path = meme.make_meme(
                tmp,
                text=body,
                author=author,
            )
            os.remove(tmp)
            return render_template("meme.html", path=path)
        except Exception:
            abort(500)
    else:
        abort(400, "You need to specify an image, a text and an author.")


if __name__ == "__main__":
    app.run()
