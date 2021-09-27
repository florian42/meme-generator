#!/bin/bash

black .
isort .
pytest
pydocstyle app.py meme.py ./QuoteEngine/__init__.py ./QuoteEngine/ingest.py ./QuoteEngine/quote_model.py
flake8 .
mypy .
