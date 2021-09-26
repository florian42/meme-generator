#!/bin/bash

black .
isort .
pytest
pydocstyle app.py meme.py
flake8 .
mypy .
