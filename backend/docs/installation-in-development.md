# Setup

Installation (via `pip`) for development

### How to

You can use `setup.py`'s `develop` mode to view the package in "editable" mode.

```
pip install -e .
```

If you wish to try and interface with the package as a site-package during development, you may wish to force the reinstall of said package.

```
pip install --upgrade --force-reinstall .
```

The backend is exposed as a Python package named `phantomboreas`.
