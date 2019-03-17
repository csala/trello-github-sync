[![PyPi][pypi-img]][pypi-url]
[![Travis][travis-img]][travis-url]
[![CodeCov][codecov-img]][codecov-url]

[travis-img]: https://travis-ci.org/csala/trello-github-sync.svg?branch=master
[travis-url]: https://travis-ci.org/csala/trello-github-sync
[pypi-img]: https://img.shields.io/pypi/v/tghs.svg
[pypi-url]: https://pypi.python.org/pypi/tghs
[codecov-img]: https://codecov.io/gh/csala/trello-github-sync/branch/master/graph/badge.svg
[codecov-url]: https://codecov.io/gh/csala/trello-github-sync

# Trello Github Sync

Synchronize Github Issues, Pull Requests and Milestones as Trello cards.

- Free software: MIT license
- Source Code: https://github.com/csala/trello-github-sync
- Documentation: https://csala.github.io/trello-github-sync

## Installation

The simplest and recommended way to install Trello Github Sync is using `pip`:

```bash
pip install tghs
```

If the installation is not being done inside a virtualenv, it's recommended to use
the `--user` flag to keep the installation inside the user home folder.

```bash
pip install --user tghs
```

Alternatively, you can also clone the repository and install it from sources

```bash
git clone git://github.com/csala/trello-github-sync.git
cd trello-github-sync
make install
```

For development, you can use `make install-develop` instead in order to install all
the required dependencies for testing and code linting.

## Configuration

Once installed, the command `tghs` will be available from any terminal, but it
still needs to be configured.
