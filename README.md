# Drawlib Developer Guide

Drawlib is a pure Python drawing library designed to facilitate Illustration as Code rather than focusing solely on creating polished illustrations.

This document is intended for developers. 
If you are a Drawlib user, please refer to the official documentation.

- [Documentation](https://www.drawlib.com/docs/)


## Setting Up the Development Environment

Drawlib uses Poetry for project management. 
Check the `pyproject.toml` file for details about the environment.

Here is a list of the tools you'll need:

- Language: The oldest Drawlib-supported CPython version
- IDE: We recommend VSCode, but you can use any editor as long as you follow the formatting rules.
- Linter: ruff
- Formatter: ruff
- Type Checker: pyright
- Unit Testing: pytest, pytest-cov


### Using WSL (Windows Only)

Drawlib development heavily relies on shell scripts. 
Please use WSL on Windows.

Not only bash, but zsh might also work well.


### Python Version

Drawlib needs to support users who may not be using the latest Python version. 
Set up the oldest minor Python version supported, using the latest patch version available.

For example, if `pyproject.toml` states:

```toml
[tool.poetry.dependencies]
python = "^3.9"
matplotlib = "^3.8.3"
pygments = "^2.17.2"
```

You should use the latest patch version of Python 3.9. 
Note that while the latest 3.9 code might work on the latest Python version, the reverse is not guaranteed. 
If you are using another Python version, we recommend using `pyenv` to switch between Python versions.

```bash
$ pyenv install 3.9

$ pyenv global 3.9
$ python --version
Python 3.9.19
```

### Installing Poetry

After changing your Python version, install Poetry. 
Follow the Poetry documentation for installation.
But here is a typical install procedure.

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```

We recommend creating Poetry's virtual environment under the project.
This helps your IDE recognize and use it as the default.

You might not need any special settings to achieve this since we already created `poetry.toml` for that purpose.
However, you can configure Poetry with this command:

```bash
$ poetry config virtualenvs.in-project true --local
```

### Installing Dependencies

Drawlib development requires a clean environment that is not shared with other purposes. 
Set up the development environment with this command:

```bash
$ poetry install
```

This will install both mandatory dependencies and developer dependencies.

### Activating the Project Python Environment

If you are using a modern IDE, it will detect the virtual Python environment and use it. 
For example, in VSCode, you can choose the Python environment from the bottom right corner.

You can also activate the environment manually:

```
$ poetry shell
```

Refer to the Poetry documentation for more details.

### Configuring Auto Code Checking and Formatting

Drawlib developers must follow the same source code formatting.

Please use these tools:

- Linter: ruff
- Formatter: ruff
- Type Checker: pyright (IDE will use pylance)

Tool settings are stored in `pyproject.toml` and `pyrightconfig.json`.

VSCode settings `.vscode/*` are also provided in the project directory.


## Code Checking and Testing

Your local git repository exists on your environment, but the remote repository is shared among developers. 
You must strive to keep it clean, with no visible bugs and no visible lint/type errors.

Here are some guidelines:

- Understand the current project development status before making changes.
- Make small, frequent commits rather than large, infrequent ones.
- Before committing your code, ensure it passes lint/type checks and unit tests.
- After committing and pushing or making a pull request, GitHub Actions will start CI, running unit tests and lint/type checks.
- If it fails, fix the problems.


### Before planning change, check release plan

Drawlib does not fix old releases. 
Patches are applied to the latest version only.

If you plan to fix or add/change features, check whether the next version's branch exists. 
Patches can be applied to the latest released version and the next version. 
New features can be applied to the next version's development releases.

If you don't follow these guidelines, you may be asked to port your changes to the latest code.


### Commit Rules

Make one change per commit. 
A single commit should not contain multiple changes.

One change does not necessarily mean one file, but rather one feature or one bug fix.


### Lint check

Please fix any lint problems your IDE warns you about. 
After that, run the code format check manually using the scripts provided in `./scripts`.

- Lint check: `./scripts/check_lint.sh`
- Type check: `./scripts/check_type.sh`

Lint checks also include complexity and security checks. 
Your new code should pass all checks.

Only the main committer can disable check rules in certain situations.


### Unit Testing

Run unit tests locally before committing your code. 
Scripts are provided in the `./scripts` directory.

- `./scripts/utest_all.sh` : Runs all unit tests
- `./scripts/utest_*.sh` : Package-level unit tests

Drawlib supports multiple OS and Python versions, but you don't need to run unit tests in environments you are not using. 
CI will take care of this.


### Checking/Testing on GitHub Repository

When you push or create a pull request, CI (GitHub Actions) is triggered to run unit tests and lint checks.

These tests are run on multiple OS environments with the oldest supported Python version:

- `ubuntu-latest`
- `windows-latest`
- `macos-latest`.

If you want to test at multiple python version, please start GitHub Action manually.
The actions is named `Unit test GitHub, os:all, python:all` or something like that.


## Releasing New Major/Minor Versions

New software releases are handled manually by the primary authors. 
Here is an abstract of the procedure:

1. Create a new version branch.
2. Continue development. You can commit even if the full feature set is not yet implemented.
3. Release `m.n.0.dev<n>`, called a "Development" release.
4. When development is complete, `release m.n.1.rc<n>`, called a "Release Candidate" release.
5. Fix any problems until the software quality is satisfactory.
6. When the candidate release is judged satisfactory, release `m.n.1`.
7. Merge the development branch into main.
8. Announce the new version release.

Patch versions are developed in the main repository. 
You don't need to create a branch for patch release development.

When development of the next version `m.n+1.0` begins, patch releases m.n.* will stop being developed. 
Fixes will be applied to the next version.


### Master Version Information

Take care only of `drawlib.__init__.py` regarding version information. 
It contains the constant `LIB_VERSION`, which is referenced throughout the code. 
The version information in pyproject.toml also uses this constant.


### Publishing to PyPI

The script `./scripts/publish_pypi.sh` handles publishing new releases. 
Due to authentication restrictions, only the main author can push new versions. 

Currently, there are no plans to automate this process through CI (such as GitHub Actions and secrets).


### Manual Testing for PyPI Releases

We have CI for testing PyPI releases. 
When you publish a new version on PyPI, please run tests manually. 
To avoid releasing broken software, publish rc releases first. 
Once you confirm the rc release works fine, you can release the standard version.

On GitHub Actions, look for `Unit test PyPI, os:all, python:all` or similar. 
This will run unit tests with:

- The specified version of the PyPI repository (default is latest)
- The specified branch (where the unit tests exist)
- All supported OS
- All supported Python versions

New releases must pass all these tests. 
The CI does not run lint checks since code quality is not a concern for end-users.


### Updating PyPI Library Description

The `pyproject.toml` file points to the PyPI explanation file, currently `pypi.md`.

To update the PyPI explanation, update the markdown file. 
Note that PyPI cannot host images; images must be provided via URL.


## Links

- [Documentation](https://www.drawlib.com/docs/)
- [PyPI](https://pypi.org/project/drawlib/)
- [Code repository](https://github.com/yuichi110/drawlib)
- [Documentation repository](https://github.com/yuichi110/drawlib_docs)
- [Assets repository](https://github.com/yuichi110/drawlib_assets)
