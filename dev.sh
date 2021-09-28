#!/bin/bash

black .
isort .
pytest
pydocstyle app.py meme.py ./quote_engine/__init__.py ./quote_engine/ingest.py ./quote_engine/quote_model.py
flake8 .
mypy .
