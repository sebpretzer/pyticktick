#! /usr/bin/env uv run python

"""Script to check the changelog for missing version or missing description."""

import argparse
import re
from importlib.metadata import version
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Check the changelog for missing version or missing description.",
    )
    parser.add_argument(
        "changelog",
        type=Path,
        nargs="?",
        default=Path(__file__).parents[2].joinpath("docs/CHANGELOG.md"),
        help="Path to the CHANGELOG.md file",
    )
    return parser.parse_args()


def check(changelog_path: Path) -> None:
    """Check the changelog for basic formatting and content.

    Rules checked:
    - The file must exist.
    - The file must start with a title "# Changelog".
    - The current `pyticktick` version must be present in the format "## X.Y.Z".
    - The current version should be at the top of the changelog.
    - The current version should have a description.

    Args:
        changelog_path (Path): Path to the CHANGELOG.md file.

    Raises:
        FileNotFoundError: If the changelog file does not exist.
        ValueError: If the changelog does not match any of the expected conditions.
    """
    if not changelog_path.exists():
        msg = f"File not found: {changelog_path}"
        raise FileNotFoundError(msg)

    changelog = changelog_path.read_text()
    regex = r"^(?P<title># Changelog)\n+## (?P<version>[0-9]+\.[0-9]+\.[0-9]+)\n+(?P<description>[\S\s]+)##"  # noqa: E501
    match = re.match(regex, changelog)
    if match is None:
        msg = "Changelog does not match the expected format, regex failed to match."
        raise ValueError(msg)

    if (ptt_ver := version("pyticktick")) != (chnglg_ver := match.group("version")):
        msg = f"Version in changelog ({chnglg_ver}) does not match the version of pyticktick ({ptt_ver})."  # noqa: E501
        raise ValueError(msg)

    if len(match.group("description").strip()) == 0:
        msg = "Changelog entry is missing a description."
        raise ValueError(msg)


if __name__ == "__main__":
    args = parse_args()
    check(args.changelog)
