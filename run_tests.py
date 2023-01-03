import subprocess

def run():
    """
    Run all unittests. Equivalent to run: `tox`.
    Tox will run tests for all different Python versions.
    """
    subprocess.run('tox')