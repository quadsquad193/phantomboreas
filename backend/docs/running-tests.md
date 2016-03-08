# Setup

Running tests

### How to

Within your `virtualenv`, use `pip` to install the project and its packages in editable mode. See `setup.py` for details about which "packages" are exposed.

```
pip install -e .
```

Then, you may use `pytest` to run each services' (or packages') test suite. For example...

```
py.test openalprservice
```

Some tests require the use of Redis. Be sure to have a server running!

### Notes

- The `pytest-dbfixtures` plugin expects the Redis server to reside in `/usr/bin/redis-server`. You may need to use a symlink to your actual executable path.
- We use two of Redis' default 16 databases; index `0` for actual usage and index `1` for tests.
