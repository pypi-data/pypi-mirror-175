# doomsday-trainer

A simple program for exercising the ability to calculate the day of week for
a given date (Gregorian calendar).

The name is taken from the
[Doomsday rule](https://en.wikipedia.org/wiki/Doomsday_rule) - an algorithm
devised by [John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in
1973 for this specific purpose.

## Dependencies

- Python 3.7+

- [Poetry](https://python-poetry.org/) for dependency management and packaging.

- [tox](https://pypi.org/project/tox/) for testing.

## Installation

### From source (using Poetry)

```
git clone https://github.com/cbernander/doomsday-trainer.git
cd doomsday-trainer
poetry build
pip install dist/doomsday_trainer-*.whl
```

## Usage

```
usage: doomsday-trainer [-h] [--start-year START_YEAR] [--end-year END_YEAR]

optional arguments:
  -h, --help            show this help message and exit
  --start-year START_YEAR
                        Start year
  --end-year END_YEAR   End year
```
