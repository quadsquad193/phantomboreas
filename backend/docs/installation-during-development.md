# Installation

## Installation (via `pip`) during development

### How to

You can use `setup.py`'s `develop` mode to view the package in "editable" mode while working in the `backend` directory.

```
pip install -e .
```

If you wish to try and interface with the package as a site-package during development, you may wish to force the reinstall of said package.

```
pip install --upgrade --force-reinstall .
```

Each backend service is exposed as a Python package named `phantomboreas.<service>`. For example, you might use...

```
import phantomboreas.openalprservice
from phantomboreas import droneservice
from phantomboreas.db import models
# etc...
```
