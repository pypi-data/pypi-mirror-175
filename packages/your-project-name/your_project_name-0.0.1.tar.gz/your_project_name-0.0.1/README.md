# Your Project Name

<!-- begin badges -->

[![Status][status badge]][status link]
[![Python Version][python version badge]][pypi package page]
[![Package Version][pypi latest version]][pypi package page]
[![Package Downloads][pypi downloads]][pypi package page]

[![License][license]][license]<br>
[![pre-commit enabled][pre-commit badge]][pre-commit project]
[![Black codestyle][black badge]][black project]

[status badge]: https://ci.jamesveitch.xyz/api/badges/james/your-project-name/status.svg
[status link]: https://ci.jamesveitch.xyz/james/your-project-name
[python version badge]: https://img.shields.io/pypi/pyversions/your_project_name
[pypi latest version]: https://img.shields.io/pypi/v/your_project_name
[pypi package page]: https://pypi.org/project/your_project_name/
[pypi downloads]: https://img.shields.io/pypi/dm/your_project_name
[license]: https://img.shields.io/pypi/l/your_project_name
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit project]: https://pre-commit.com/
[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black project]: https://github.com/psf/black

<!-- end badges -->

Short description of your project

This project was generated with the [python-cookiecutter](https://git.jamesveitch.xyz/james/python-cookiecutter) template and, amongst other things, provides the following functionality out of the box.

- CI/CD integration with Woodpecker-CI pipelines
- Testing via Nox across multiple python versions
- PyTest integration with codecoverage, mocking and asyncio
- Linting with black and flake8
- Type checking with MyPy
- Security using bandit and safety
- Documentation via MkDocs with a material theme and autodoc
  - Live reload during development with `make docs` Makefile
  - Deployment to GitHub Pages through woodpecker pipeline using [mike](https://github.com/jimporter/mike) for version control
- Package versioning and build with Poetry
  - Deployment to both pypi (production) and test.pypi (development) through woodpecker pipelines based on branch

## 📚 Documenation

Documentation is hosted with GitHub Pages and can be found at:

- ✅ [your-project-name/stable](https://darth-veitcher.github.io/your-project-name/latest/stable) (reflecting the `Master` branch); or
- ⚠️ [your-project-name/develop](https://darth-veitcher.github.io/your-project-name/latest/develop) (for bleeding edge).

##  ⚒️ Installation

**Python Version:** This library is tested against Python >=3.7

To install the library run this command in your terminal.

```zsh
pip install your_project_name
```

## 🚀 Usage

TODO: improve documentation here

```py
>>> import your_project_name
>>> your_project_name.__version__
'0.0.1'
```
