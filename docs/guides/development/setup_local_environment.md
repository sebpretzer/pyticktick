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

It will also install [prek](https://prek.j178.dev/) hooks to ensure code quality. CI runs the same hooks but does not push fixes, so if you skip them with `--no-verify` during commit, run `make lint` and commit its fixes before opening a pull request.
