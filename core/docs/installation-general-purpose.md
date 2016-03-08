# Installation

Setting up `phantomboreas` is fairly straightforward.

To start, we must satisfy some dependencies outside of the Python project. Be sure to
- ... install [OpenALPR with Python bindings](./setup-openalpr-python-ubuntu.md)
- ... install [Redis](./setup-openalpr-python-ubuntu.md) or have a Redis server ready

Next, clone the GitHub repository and navigate to the `backend` directory.

```
git clone https://github.com/quadsquad193/Quadcopter
cd backend
```

Use `pip` to install the project to your `site-packages` or `virtualenv`.

You may need to use `--upgrade` or `--force-reinstall` for previous setups. If you are using a `virtualenv`, be sure it has access to the *global* Python bindings of the OpenALPR library.

```
pip install .
```

You're now ready to start running all the services! It's always a good idea to [run the test suite](./running-tests.md) for a sanity check. Spin up or point to a Redis server and use the package's submodules to start each service.

Each service requires particular configuration and exposes different invocation points. The Git repository has a folder named `launch` which comes with basic configuration and runnable scripts to fire up each service. You may wish to use these as examples to guide your own rollout.
