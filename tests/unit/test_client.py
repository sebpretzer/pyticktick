from pyticktick import Client
from pyticktick.settings import TokenV1


def test_client(
    test_v1_client_id,
    test_v1_client_secret,
    test_v1_token_value,
    test_v1_token_expiration,
    test_v2_username,
    test_v2_password,
    test_v2_token,
) -> Client:
    return Client(
        v1_client_id=test_v1_client_id,
        v1_client_secret=test_v1_client_secret,
        v1_token=TokenV1(
            value=test_v1_token_value,
            expiration=test_v1_token_expiration,
        ),
        v2_username=test_v2_username,
        v2_password=test_v2_password,
        v2_token=test_v2_token,
    )
