# Authenticate Client via Python

For our V1 authentication requirements, assume our client id is `7p3Hw9YMqnfxaIvKc4` and our client secret is `Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!`. Let's also assume we have a token of `a5b2c3a7-9385-47e4-80b8-a445f842e403` and an expires at `1781373801`.

??? question "How do I get my client id and secret?"

    Please refer to the [Register a V1 App](./../../ticktick_api/register_v1_app.md) guide to learn how to obtain your client id and secret.

??? question "How do I get my token?"

    Please refer to the [Generate a V1 Token](./../../ticktick_api/generate_v1_token.md) guide to learn how to obtain your token.

For our V2 authentication requirements, assume our username is `computer_wiz_02@python.org` and our password is `password123`.

=== "V1 Only"

    ```python
    from pyticktick import Client

    client = Client(
        v1_client_id="7p3Hw9YMqnfxaIvKc4",
        v1_client_secret="Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!",
        v1_token={
            "value": "a5b2c3a7-9385-47e4-80b8-a445f842e403",
            "expiration": 1781373801,
        },
    )
    ```

    !!! warning "No V2 Access"

        This client will not be able to use V2 functions without authenticating with V2
        credentials.

=== "V2 Only"

    ```python
    from pyticktick import Client

    client = Client(
        v2_username="computer_wiz_02@python.org",
        v2_password="password123",
    )
    ```

    !!! warning "No V1 Access"

        This client will not be able to use V1 functions without authenticating with V1
        credentials.

=== "Both V1 and V2"

    ```python
    from pyticktick import Client

    client = Client(
        v1_client_id="7p3Hw9YMqnfxaIvKc4",
        v1_client_secret="Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!",
        v1_token={
            "value": "a5b2c3a7-9385-47e4-80b8-a445f842e403",
            "expiration": 1781373801,
        },
        v2_username="computer_wiz_02@python.org",
        v2_password="password123",
    )
    ```
