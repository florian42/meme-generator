from typing import List

class Document:
    def __init__(self, path: str) -> None: ...
    @property
    def paragraphs(self) -> List[Paragraph]: ...

class Paragraph:
    text: str
