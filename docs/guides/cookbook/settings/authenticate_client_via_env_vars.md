# Authenticate Client via Env Vars

For our V1 authentication requirements, assume our client id is `7p3Hw9YMqnfxaIvKc4` and our client secret is `Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!`. Let's also assume we have a token of `a5b2c3a7-9385-47e4-80b8-a445f842e403` and an expires at `1781373801`.

??? question "How do I get my client id and secret?"

    Please refer to the [Register a V1 App](./../../ticktick_api/register_v1_app.md) guide to learn how to obtain your client id and secret.

??? question "How do I get my token?"

    Please refer to the [Generate a V1 Token](./../../ticktick_api/generate_v1_token.md) guide to learn how to obtain your token.

For our V2 authentication requirements, assume our username is `computer_wiz_02@python.org` and our password is `password123`.

=== "V1 Only"

    First, export the following environment variables:

    ```bash
    export TICKTICK_API_V1_CLIENT_ID=7p3Hw9YMqnfxaIvKc4
    export TICKTICK_API_V1_CLIENT_SECRET=Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!
    export TICKTICK_API_V1_TOKEN_VALUE=a5b2c3a7-9385-47e4-80b8-a445f842e403
    export TICKTICK_API_V1_TOKEN_EXPIRATION=1781373801
    ```

    Then, you can create the client like this:

    ```python
    from pyticktick import Client

    client = Client()
    ```

    !!! warning "No V2 Access"

        This client will not be able to use V2 functions without authenticating with V2
        credentials.

=== "V2 Only"

    First, export the following environment variables:

    ```bash
    export TICKTICK_API_V2_USERNAME=computer_wiz_02@python.org
    export TICKTICK_API_V2_PASSWORD=password123
    ```

    Then, you can create the client like this:

    ```python
    from pyticktick import Client

    client = Client()
    ```

    !!! warning "No V1 Access"

        This client will not be able to use V1 functions without authenticating with V1
        credentials.

=== "Both V1 and V2"

    First, export the following environment variables:

    ```bash
    export TICKTICK_API_V1_CLIENT_ID=7p3Hw9YMqnfxaIvKc4
    export TICKTICK_API_V1_CLIENT_SECRET=Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!
    export TICKTICK_API_V1_TOKEN_VALUE=a5b2c3a7-9385-47e4-80b8-a445f842e403
    export TICKTICK_API_V1_TOKEN_EXPIRATION=1781373801
    export TICKTICK_API_V2_USERNAME=computer_wiz_02@python.org
    export TICKTICK_API_V2_PASSWORD=password123
    ```

    Then, you can create the client like this:

    ```python
    from pyticktick import Client

    client = Client()
    ```

To see more on env file support, please refer to [Pydantic Settings' Dotenv (.env) support](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support).
