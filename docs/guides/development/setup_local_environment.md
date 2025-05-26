# Setting Up the Local Environment

First, clone the [repo](https://github.com/sebpretzer/pyticktick). Then, we can install the dependencies.

## Install `uv` (optional)

This package uses `uv` to manage the virtual environment and dependencies. If you already have `uv` installed, you can skip this step.

To install `uv`, run the following command:

```bash
make install-uv
```

You can also install it using their [installation guide](https://docs.astral.sh/uv/getting-started/installation/) if you prefer.

## Install Dependencies

To install the dependencies, run the following command:

```bash
make install
```

This will install all the dependencies needed to run the code, scripts, tests, and build the documentation.

It will also install [pre-commit hooks](https://pre-commit.com/) to ensure code quality. These hooks will run automatically as part of CI, so if you do not want to use them during development, you can disable them by [running `--no-verify` during commit](https://pre-commit.com/#temporarily-disabling-hooks).
