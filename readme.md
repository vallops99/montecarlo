# MonteCarlo simulation algorithm

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build](https://img.shields.io/badge/Build-Passing-green.svg)]()

## Requirements
Python 3.10.0+
Currently working to introduce support to old version.

## Installation
`pip install montecarlosim`

## How to use it
Import the Montecarlo class, create an instance of it by passing a function that accepts a one-dimensional numpy array and return a numpy array with the same shape (you can see them as passing the X axis points and returning the relative Y axis points).<br>
If you don't have a function to use, but you want to test the library, you can use a gaussian function inside the `functions.py` file.<br>
With the newly created instance, call one of the Montecarlo simulation methods (`hit_or_miss` or `average`) and pass them: min value of X axis, max value of Y axis and number of samples.
This method will return the results (dictionary), hit_or_miss dict contains hit points and miss points also.<br/>
If you want to graphically see your results, you can use the `plot` static method of Montecarlo's class by passing it the reuslts dict of every simulation method.<br>
Example:<br/>
```python
from montecarlosim.montecarlo import Montecarlo
from montecarlosim.functions import gauss

simulation = Montecarlo(gauss)
results = simulation.hit_or_miss(-3, 3, 1000)
Montecarlo.plot(results)
```

More on Montecarlo class:<br/>
You can also decide which criteria to use for defining how to read HIT or MISS points (will affect hit_or_miss method only).
These criteria are defined inside the Criteria enum class inside CriteriaValue class inside Montecarlo class.
```python
from montecarlosim.montecarlo import Montecarlo

for criteria in Montecarlo.CriteriaValue.Criteria:
    print(criteria.value)

# By being an ENUM you can access a single criteria like that
print(Montecarlo.CriteriaValue.Criteria.MINOR.value)
```

## Getting started
- Clone the repository the way you like;
- Create a virtualenv (with pyenv and virtualenv you can run `pyenv virtualenv 3.10.0 <name_you_like>`) otherwise install poetry and run `poetry install`, it will take care of the virtualenv itself;
- Now you can lunch the tests with `poetry run tests` and it will tests all environment inside tox.ini `envlist`;
- Create a branch, do your changes, push them and open a PR.

## Repository structure
Repository configuration files are:
- `pyproject.toml`;
- `tox.ini`, tests;
- `src`, contains the actual repository code;
- `src/montecarlo.py`, contains the Montecarlo class (where magic happens);
- `src/functions.py`, contains example functions to be used with Montecarlo class;
- `src/exceptions.py`, contains custom exception that are used to better handle errors;
- `tests`, contains python tests file that is launched by tox;
- `run_tests.py`, simple function that run `subprocess.run('tox')`.