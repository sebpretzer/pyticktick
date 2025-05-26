# Running Tests Locally

??? question "Have you set up your local environment?"

    Make sure your local environment is set up by following the steps in the [Setting Up the Local Environment](setup_local_environment.md) guide.

There are two sets of tests that you can run locally: [unit tests](#running-unit-tests) and [integration tests](#running-integration-tests). They are run separately, because the integration tests take a lot longer to run, and require credentials.

## Running Unit Tests

To run the unit tests, run the following command:

```bash
make test-unit
```

This command will run the unit tests and generate a coverage report in your terminal. You can also view the coverage report in your browser by opening the html report:

```bash
open htmlcov/index.html
```

## Running Integration Tests

Before running the integration tests, you need to set up your environment variables. You can do this by creating a `.env` file in the root of the repo and adding the following environment variables:

```bash title=".env"
TICKTICK_API_V1_CLIENT_ID="YOUR_CLIENT_ID"
TICKTICK_API_V1_CLIENT_SECRET="YOUR_CLIENT_SECRET"
TICKTICK_API_V1_TOKEN_VALUE="YOUR_TOKEN_UUID"
TICKTICK_API_V1_TOKEN_EXPIRATION=1111111111
TICKTICK_API_V2_USERNAME="YOUR_USERNAME"
TICKTICK_API_V2_PASSWORD="YOUR_PASSWORD"
```

If you don't want to create a `.env` file, you can set the same environment variables in your session before running the tests.

To run the integration tests, run the following command:

```bash
make test-integration
```

This command will run the integration tests and generate a coverage report in your terminal. You can also view the coverage report in your browser by opening the html report:

```bash
open htmlcov/index.html
```
