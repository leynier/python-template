# Python Template

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Last commit](https://img.shields.io/github/last-commit/leynier/python-template.svg?style=flat)](https://github.com/leynier/python-template/commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/python-template)](https://github.com/leynier/python-template/commits)
[![Github Stars](https://img.shields.io/github/stars/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template/stargazers)
[![Github Forks](https://img.shields.io/github/forks/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template/network/members)
[![Github Watchers](https://img.shields.io/github/watchers/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/python-template)](https://leynier.github.io/python-template)
[![GitHub contributors](https://img.shields.io/github/contributors/leynier/python-template)](https://github.com/leynier/python-template/graphs/contributors)

Python template with CI/CD ready for production

## Branches

- [main](https://github.com/leynier/python-template): For libraries and/or console applications
- [typer](https://github.com/leynier/python-template): Command line interfaces implemented with [Typer](https://typer.tiangolo.com)
- [fastapi](https://github.com/leynier/python-template/tree/fastapi): For web applications implemented with [FastAPI](https://fastapi.tiangolo.com)

## Features

### Main Features

- Management of dependencies with [Poetry](https://python-poetry.org)
- Generation of documentation based on Markdown with [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material)
- Automatic check of the pythonic style with [flake8](https://flake8.pycqa.org), [black](https://black.readthedocs.io) and [isort](https://pycqa.github.io/isort)
- Automatic code checking with [pytest](https://pytest.org)
- Automatic code report with [codecov](https://codecov.io)
- Automatic code reviews with [deepsource](https://deepsource.io)
- Automatic publish to [GitHub Releases](https://docs.github.com/es/free-pro-team@latest/github/administering-a-repository/releasing-projects-on-github)
- Automatic publish to [PyPI](https://pypi.org)
- Automatic dependency update check with [dependabot](https://github.com/dependabot)

### FastAPI Features

- Configuration for deploy on [Heroku](https://www.heroku.com)
- Configuration for deploy with [Docker](https://www.docker.com)

> All of the above via [GitHub Actions](https://github.com/features/actions) and [GitHub Pages](https://pages.github.com)

## Tutorial

### Install `cookiecutter` ([Official Instructions](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter))

At the command line:

```bash
python3 -m pip install --user cookiecutter
```

Or, if you do not have pip:

```bash
easy_install --user cookiecutter
```

Though, `pip` is recommended.

Or, if you are using `conda`, first add `conda-forge` to your channels:

```bash
conda config --add channels conda-forge
```

Once the `conda-forge` channel has been enabled, cookiecutter can be installed with:

```bash
conda install cookiecutter
```

#### Alternate installations

**Homebrew (Mac OS X only):**

```bash
brew install cookiecutter
```

**Pipx (Linux, OSX and Windows):**

```bash
pipx install cookiecutter
```

**Debian/Ubuntu:**  

```bash
sudo apt-get install cookiecutter
```

#### Upgrading from `0.6.4` to `0.7.0` or greater

First, read [History](https://cookiecutter.readthedocs.io/en/latest/HISTORY.html) in detail. There are a lot of major changes. The big ones are:

Cookiecutter no longer deletes the cloned repo after generating a project.

Cloned repos are saved into `~/.cookiecutters/`.

You can optionally create a `~/.cookiecutterrc` config file.

Upgrade **Cookiecutter** either with `easy_install`:

```bash
easy_install --upgrade cookiecutter
```

Or with pip:

```bash
python3 -m pip install --upgrade cookiecutter
```

### Usage

Then, after you have installed `cookiecutter`, execute the following command in the terminal of your choice:

```bash
cookiecutter gh:leynier/python-template --checkout <branch>
```

Where `<branch>` can be `main`, `fastapi`, `typer`, etc.

#### Example using FastAPI template

```bash
cookiecutter gh:leynier/python-template --checkout fastapi
```

## License

This project is collaborative and open source under the [MIT license](LICENSE). Contributions are super appreciated.
