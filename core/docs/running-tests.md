# Running the Test Suite

### How to

You can use `pip` to install the project and its packages in editable mode within your `virtualenv` during development.

> If `phantomboreas` is installed as a `site-package` and you wish to test against that, you don't need to do the below.

```
pip install -e .
```

Then use `pytest` to run the test suite, located the `spec` directory.

```
py.test spec/
```

### Notes

- The `pytest-dbfixtures` plugin expects the Redis server to reside in `/usr/bin/redis-server`. You may need to use a symlink to your actual executable path.
- We use two of Redis' default 16 databases; index `0` for actual usage and index `1` for tests.
