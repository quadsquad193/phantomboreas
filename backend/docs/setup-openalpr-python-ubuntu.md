# Setup

## Setting up OpenALPR and its Python bindings on *Ubuntu 14.04 LTS*

### Notes

We recommend building OpenALPR from source instead of installing it from Aptitude. The Python bindings from the most current repository may not be compatible with older releases.

If OpenALPR is already installed (without Python bindings) using `apt-get`, please `remove` the packages.

This setup guide will install the OpenALPR libraries globally to a `/usr` installation and create a global Python package. Be sure your Python `virtualenv` is created with `--system-site-packages` to allow the use of the Python bindings.

### Dependencies

```
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install liblog4cplus-dev libcurl3-dev
```

### Build and install OpenALPR

```
git clone https://github.com/openalpr/openalpr.git

cd openalpr/src
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

make
sudo make install
```

### Set up Python bindings

```
cd ../bindings/python
source make.sh
```

You can then run `python test.py <image>` to verify the installation.
