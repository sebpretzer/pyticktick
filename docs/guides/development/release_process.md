# Release Process

Releasing a new version of the project involves a few steps to ensure that the code is ready for release. The release process itself is automated through GitHub Actions, assuming the requirements are met.

## Update the Version

The package version in [`pyproject.toml` in the `main` branch](https://github.com/sebpretzer/pyticktick/blob/main/pyproject.toml) must be a higher version than the last release of [pyticktick](https://pypi.org/project/pyticktick/). To update the version, you can manually update the `version` field in the `pyproject.toml` file, or run `uv version <new_version>`.

### Versioning Scheme

`pyticktick` follows the [PyPA versioning scheme](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-scheme), which is derived from [Semantic Versioning](https://semver.org/). The version number is composed of three parts: `MAJOR.MINOR.PATCH`, where:

> 1. `MAJOR` version when you make incompatible API changes
> 1. `MINOR` version when you add functionality in a backward compatible manner
> 1. `PATCH` version when you make backward compatible bug fixes

No pre-release or post-release tags are used in the version number.

## Update the Changelog

The changelog is tracked in the [`CHANGELOG.md` file](https://github.com/sebpretzer/pyticktick/blob/main/docs/CHANGELOG.md). The changelog must be manually updated, with the format:

```markdown title="docs/CHANGELOG.md"
...
## MAJOR.MINOR.PATCH

- Words describing the changes ([#123]((https://github.com/sebpretzer/pyticktick/pull/123)))

## MAJOR.MINOR.PATCH-1
...
```

The relevant section of the changelog is extracted by the GitHub Action as part of the release.

## Trigger the Release

To trigger the release, you need to go to the [publish workflow](https://github.com/sebpretzer/pyticktick/actions/workflows/publish.yaml). Select `Run workflow` from the `main` branch.

Wait for the workflow to finish. The workflow will automatically:

1. Build the package
1. Create a new release on GitHub
1. Upload the package to PyPI
