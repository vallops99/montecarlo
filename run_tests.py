import os

def run():
    """
    Run all unittests. Equivalent to run:
    `pytest --cov --cov-report html --cov-report term-missing
    --cov-fail-under 95`.
    """
    os.system(
        'pytest \
        --cov \
        --cov-report html \
        --cov-report term-missing \
        --cov-fail-under 95 \
        --capture=tee-sys \
        --show-capture=all'
    )