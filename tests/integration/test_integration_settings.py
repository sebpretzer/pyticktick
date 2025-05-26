from time import time
from uuid import UUID

import pytest

from pyticktick import Settings
from pyticktick.settings import TokenV1


@pytest.mark.local
def test_authenticate_v1(client):
    _client_id = client.v1_client_id
    _client_secret = client.v1_client_secret.get_secret_value()

    settings = Settings(v1_client_id=_client_id, v1_client_secret=_client_secret)

    assert settings.v1_client_id == _client_id
    assert settings.v1_client_secret.get_secret_value() == _client_secret
    assert settings.v1_token is not None
    assert isinstance(settings.v1_token, TokenV1)
    assert settings.v1_token.value is not None
    assert isinstance(settings.v1_token.value, UUID)
    assert settings.v1_token.expiration is not None
    assert settings.v1_token.expiration > int(time())

    assert settings.v1_token != client.v1_token


def test_initialize_api_v2(client):
    _username = client.v2_username
    _password = client.v2_password.get_secret_value()

    settings = Settings(v2_username=_username, v2_password=_password)

    assert settings.v2_username == _username
    assert settings.v2_password.get_secret_value() == _password
    assert settings.v2_token is not None
    assert isinstance(settings.v2_token, str)

    assert settings.v2_token != client.v2_token
