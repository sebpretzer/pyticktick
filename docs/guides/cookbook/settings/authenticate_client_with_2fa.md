# Authenticate Client with 2-Factor Authentication (2FA)

For our V1 authentication requirements, assume our client id is `7p3Hw9YMqnfxaIvKc4` and our client secret is `Qxm^^3h(7ZK994U8M%/g!YFo2VEPs*k!`. Let's also assume we have a token of `a5b2c3a7-9385-47e4-80b8-a445f842e403` and an expires at `1781373801`.

!!! note "2FA Authentication"

    2FA is only used for V2 authentication. If you are using V1, you do not need to worry about 2FA.

For our V2 authentication requirements, assume our username is `computer_wiz_02@python.org` and our password is `password123`. Let's assume that 2FA is enabled for this account, and the 2FA secret is `5SY29FY0VXU5XBEJCJH3Z4KYNQ7G915S`.

=== "V2 with 2FA"

    ```python
    from pyticktick import Client

    client = Client(
        v2_username="computer_wiz_02@python.org",
        v2_password="password123",
        v2_totp="5SY29FY0VXU5XBEJCJH3Z4KYNQ7G915S",
    )
    ```

=== "Both V1 and V2 with 2FA"

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
        v2_totp="5SY29FY0VXU5XBEJCJH3Z4KYNQ7G915S",
    )
    ```
