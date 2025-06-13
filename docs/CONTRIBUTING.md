# Contributing

There are several ways to contribute to `pyticktick`, based on your level of commitment. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Opening an Issue

For any of the following issue types, you can open a [new issue](https://github.com/sebpretzer/pyticktick/issues/new/choose) and follow along with the corresponding template.

### Reporting a Bug

You can report a bug by using the [bug report template](https://github.com/sebpretzer/pyticktick/issues/new?template=bug.yaml) on the `pyticktick` repository. Please make sure to do the following:

1. Check that there is no existing issue for the bug you are reporting
1. Ensure the bug is reproducible, and you have provided a minimal code example, following [this guide](https://matthewrocklin.com/minimal-bug-reports)
1. Provide any applicable logs

### Feature Request

You can request a feature by using the [feature request template](https://github.com/sebpretzer/pyticktick/issues/new?template=feature.yaml) on the `pyticktick` repository. Please make sure to do the following:

1. Check that there is no existing issue for the feature you are requesting
1. Ensure the feature is not already implemented in the latest version of `pyticktick`, or in the repository codebase
1. Provide any example code or pseudocode to help demonstrate the feature
1. Provide the endpoint, and any relevant parameters / responses (if applicable)

### Documentation Improvement

You can request to improve the documentation by using the [documentation improvement template](https://github.com/sebpretzer/pyticktick/issues/new?template=documentation.yaml) on the `pyticktick` repository. Please make sure to do the following:

1. Check that there is no existing issue for the documentation improvement you are requesting
1. Provide a link to the relevant documentation page (if applicable)

## Contributing to the Documentation

In order to contribute to the documentation, please go through the [issue tracker](https://github.com/sebpretzer/pyticktick/issues?q=is%3Aissue%20state%3Aopen%20label%3Adocumentation) to find an issue that you can work on. If you don't find an issue, you can [create a new one](https://github.com/sebpretzer/pyticktick/issues/new?template=documentation.yaml).

Fork the repository and create a new branch for your changes. When you have the forked repository on your workspace, you can [set up your local environment](guides/development/setup_local_environment.md) and [run the documentation server locally](guides/development/running_the_documentation_server_locally.md).

This documentation attempts to follow the approach of [Diátaxis](https://diataxis.fr/). Please ensure that you bucket your changes into the appropriate section of the documentation, depending on the question you are answering. You may find that your documentation changes can be split into multiple buckets.

When you are ready to submit your changes, you can [open a pull request](#opening-a-pull-request).

## Contributing to the Codebase

In order to contribute to the codebase, please go through the [issue tracker](https://github.com/sebpretzer/pyticktick/issues?q=is%3Aissue%20state%3Aopen+label%3Abug%2Cenhancement) to find an issue that you can work on. If you don't find an issue, you can [create a bug report](https://github.com/sebpretzer/pyticktick/issues/new?template=bug.yaml) or [feature request](https://github.com/sebpretzer/pyticktick/issues/new?template=feature.yaml).

Fork the repository and create a new branch for your changes. When you have the forked repository on your workspace, you can [set up your local environment](guides/development/setup_local_environment.md). You should try your best to follow the [codebase conventions](explanations/code_conventions.md) when making your changes. Once you are done editing, it's time to [test your changes locally](guides/development/running_tests_locally.md).

Once all tests pass on your machine, you can [open a pull request](#opening-a-pull-request).

## Opening a Pull Request

To open a pull request, you can follow [GitHub's guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork). Please adhere to the following guidelines:

- Title
    - Do not use the auto-generated title, re-word your title to be more descriptive
    - Keep it concise and clear
- Description
    - [Link to the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) you were addressing
    - Add any relevant context to your pull request to help reviewers understand the changes you made
- Make sure your branch is [rebased](https://docs.github.com/en/get-started/using-git/about-git-rebase) against the latest commit of the `main` branch.
- Make sure all tests have already passed on your machine.
