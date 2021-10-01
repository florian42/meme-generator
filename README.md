# Meme Generator (Intermediate Python Nanodegree Project 2)

## Features
- Dynamically generate memes
- over-engineered solution to load quotes from multiple file formats
- Accepts dynamic user input through a command-line tool and a web service

## Motivation

This project is meant to showcase:

- Object-oriented thinking in Python, including abstract classes, class methods, and static methods.
- DRY (don’t repeat yourself) principles of class and method design.
- Working with modules and packages in Python.

## Set Up and Run

### Requirements
- Python 3.9.X
- [xpdf](http://www.xpdfreader.com) needs to be installed on your machine

### Set Up

1. Open a terminal in the project root
2. Run `$ python -m venv venv` to create your virtual environment
3. Run `$ pip install -r requirements.text` to install all dependencies

### Run

- You can use the cli, e.g.: `$ python meme.py -body 123 -author me`
- You can start the web app using: `$ python app.py`

## Structure

- meme.py: Main entrypoint for interfacing with meme-generator via cli. Usage: `$ python meme.py -body 123 -author me`
- meme_engine.py: Loads, resizes and adds a caption to an image. Usage:
```python
   meme = MemeGenerator(path)
   path = meme.make_meme(img, quote.line, quote.author)
```
- appy.py: sets up web app to as user interface to meme generator. Useage: `$ python app.py`
- stubs: stubs for type checking with mypy. Picked up automatically by mypy.
- quote_engine: Contains Ingest Module and QuoteModel. Usage: `Ingestor.parse("./_data/photos/dog/xander_1.jpg")`

## Dependencies

- flask: framework for creating the web application to interface with the meme generator
- mypy: used for type checking
- requests: for making http requests
- python-docx: to parse .docx files
- flake8: linting
- black: pep8 compliant formatting
- pandas: parsing csv files
- pillow: opening and editing images
- pydocstyle: linting
- pytest: write tests
- 