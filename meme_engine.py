"""Loads, resizes and adds a caption to an image."""
import uuid
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

DEFAULT_FONT = "OpenSans-Medium.ttf"


class MemeGenerator:
    """Generates a Meme through the `make_meme` method."""

    def __init__(self, output_dir: Optional[str] = None):
        """Initialize MemeGenerator with optional output dir.

        The default output dir is `temp` relative to where
         `meme.py` is executed.
        """
        self._temporary_folder = (
            str(Path(output_dir).parent) if output_dir else "./temp"
        )

    def make_meme(
        self, img_path: str, text: str, author: str, width: int = 500
    ) -> str:
        """Create a meme and returns the path to the generated image."""
        image = Image.open(img_path)
        ratio = width / float(image.size[0])
        height = int(ratio * float(image.size[1]))
        resized_image = image.resize((width, height), Image.NEAREST)

        draw = ImageDraw.Draw(resized_image)
        font = ImageFont.truetype(DEFAULT_FONT, size=44)
        draw.text((40, 40), f'"{text}" - {author}', fill="white", font=font)

        output_path = Path(f"{self._temporary_folder}/{uuid.uuid4()}.jpg")
        resized_image.save(output_path)
        return str(output_path)
