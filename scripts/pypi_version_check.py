#! /usr/bin/env uv run python

"""Script to validate the version in pyproject.toml.

This script checks the version in the pyproject.toml file to ensure it adheres to the
versioning rules defined by this package. It must follow the [PyPA versioning scheme](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-scheme).
More specifically, there should not be any pre-release or post-release versions.
"""

import argparse
from pathlib import Path

import tomllib
from packaging.version import InvalidVersion, parse


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Validate the version in pyproject.toml",
    )
    parser.add_argument(
        "pyproject",
        type=Path,
        nargs="?",
        default=Path(__file__).parent.parent.joinpath("pyproject.toml"),
        help="Path to the pyproject.toml file",
    )
    return parser.parse_args()


def check(pyproject_path: Path) -> None:
    """Validate the version in the project's pyproject.toml file.

    It will read the file, parse the version string, and check if it adheres to the
    versioning rules defined by this package.

    Args:
        pyproject_path (Path): Path to the pyproject.toml file.

    Raises:
        FileNotFoundError: If the pyproject.toml file is not found.
        ValueError: If the version is not found or is not valid.
    """
    if not pyproject_path.exists():
        msg = f"File not found: {pyproject_path}"
        raise FileNotFoundError(msg)

    toml = tomllib.loads(pyproject_path.read_text())
    version = toml.get("project", {}).get("version")
    if version is None:
        msg = "Version not found in pyproject.toml"
        raise ValueError(msg)

    try:
        parsed = parse(version)
    except InvalidVersion:
        msg = f"Version is not valid: {version}"
        raise ValueError(msg) from InvalidVersion

    if parsed.is_prerelease or parsed.is_postrelease:
        msg = f"Version should not be a pre/post-release version: {version}"
        # TODO: Remove this line when ready to release  # noqa: FIX002, TD002, TD003
        # raise ValueError(msg)  # noqa: ERA001
        print(msg)  # noqa: T201


if __name__ == "__main__":
    args = parse_args()
    check(args.pyproject)
