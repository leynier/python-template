# Python Template

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Test](https://github.com/leynier/python-template/workflows/CI/badge.svg)](https://github.com/leynier/python-template/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/leynier/python-template/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/python-template)
[![DeepSource](https://deepsource.io/gh/leynier/python-template.svg/?label=active+issues)](https://deepsource.io/gh/leynier/python-template/?ref=repository-badge)
[![Version](https://img.shields.io/pypi/v/python-template?color=%2334D058&label=Version)](https://pypi.org/project/python-template)
[![Last commit](https://img.shields.io/github/last-commit/leynier/python-template.svg?style=flat)](https://github.com/leynier/python-template/commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/python-template)](https://github.com/leynier/python-template/commits)
[![Github Stars](https://img.shields.io/github/stars/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template/stargazers)
[![Github Forks](https://img.shields.io/github/forks/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template/network/members)
[![Github Watchers](https://img.shields.io/github/watchers/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/python-template)](https://leynier.github.io/python-template)
[![GitHub contributors](https://img.shields.io/github/contributors/leynier/python-template)](https://github.com/leynier/python-template/graphs/contributors)

Python template with CI/CD ready for production

## Branches

- [main](https://github.com/leynier/python-template): For packages, console applications and / or command line interfaces implemented with Python
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
