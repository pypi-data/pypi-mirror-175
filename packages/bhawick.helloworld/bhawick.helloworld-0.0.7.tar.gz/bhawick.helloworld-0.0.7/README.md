# Hello World

This is an example project demonstrating how to publish a python module to PyPI.

## Installation

Run the following to install:

```python
pip install bhawick.helloworld
```

## Usage

```python
from helloworld import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")
```

## Useful References

[Build & test Python -- github docs](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)
[MyPy Typehints cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
[MyPy example .ini file](https://mypy.readthedocs.io/en/stable/config_file.html#examples)
[Cannot find implementation or library stub](https://mypy.readthedocs.io/en/stable/running_mypy.html#cannot-find-implementation-or-library-stub)
[black formatter just needs the directory name to work](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#output-verbosity)
[setup.py cheatsheet](http://turbo87.github.io/setup.py/)
[specifying python versions on tox](https://stackoverflow.com/questions/63180349/error-py37-interpreternotfound-python3-7-when-running-tox-from-github)
[asking pipenv to install dev dependencies](https://github.com/pypa/pipenv/issues/1083)
[installing pipenv](https://pipenv.pypa.io/en/latest/install/#installing-packages-for-your-project)
[PEP 423 naming convetions for projects](https://peps.python.org/pep-0423/#use-a-single-name)
[hitchhiker's guide to packaging and saving the universe](https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html)
[real python project inspiration](https://github.com/olavolav/uniplot/blob/master/.github/workflows/unit_tests.yml)

