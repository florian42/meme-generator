"""Loads, resizes and adds a caption to an image."""
import uuid
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    def __init__(self, output_dir):
        self._temporary_folder = output_dir

    def make_meme(
        self, img_path: str, text: str, author: str, width: Optional[int] = 500
    ) -> str:
        """Creates a meme and returns the path to the generated image."""

        image = Image.open(img_path)
        ratio = width / float(image.size[0])
        height = int(ratio * float(image.size[1]))
        resized_image = image.resize((width, height), Image.NEAREST)

        draw = ImageDraw.Draw(resized_image)
        draw.text((10, 30), f'"{text}" - {author}', fill="white")

        output_path = Path(f"{self._temporary_folder}/{uuid.uuid4()}")
        resized_image.save(output_path)
        return str(output_path)
