# Report to signal-spam.fr

## Install

To install signal-spam CLI, use:

    python -m pip install signal-spam


## Usage

    signal-spam BuyMyDogFood.eml


# Releasing

To push a new version of `signal-spam` on PyPI:

- Bump the `__version__` in `signalspam.py`.
- commit, tag, push commit, push tag.
- `python -m pip install --upgrade build twine`
- `python -m build`
- `python -m twine upload dist/*`
