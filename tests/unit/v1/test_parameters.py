from urllib.parse import urlencode

from pyticktick.models.v1 import OAuthAuthorizeURLV1, OAuthTokenURLV1
from pyticktick.models.v2.types import HttpUrl


def test_settings_create_authorize_url(test_v1_client_id):
    model = OAuthAuthorizeURLV1(client_id=test_v1_client_id)
    expected = f"https://ticktick.com/oauth/authorize?client_id={test_v1_client_id}&scope=tasks%3Aread+tasks%3Awrite&state=None&response_type=code"

    assert model.model_dump(by_alias=True) == expected


def test_settings_create_token_url(test_v1_client_id, test_v1_client_secret):
    test_code = "test_code"
    test_oauth_redirect_url = "http://test_redirect_url.com/"

    model = OAuthTokenURLV1(
        client_id=test_v1_client_id,
        client_secret=test_v1_client_secret,
        code=test_code,
        oauth_redirect_url=HttpUrl(url=test_oauth_redirect_url),
    )

    _oauth_url = urlencode({"redirect_uri": test_oauth_redirect_url})
    expected = f"https://ticktick.com/oauth/token?client_id={test_v1_client_id}&client_secret={test_v1_client_secret}&code={test_code}&grant_type=authorization_code&scope=tasks%3Aread+tasks%3Awrite&{_oauth_url}"

    assert model.model_dump(by_alias=True) == expected
