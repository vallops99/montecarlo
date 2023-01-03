# MonteCarlo simulation algorithm

## Installation
`pip install montecarlosim`

## Requirements
Python 3.10.0+
Currently working to introduce support to old version.

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