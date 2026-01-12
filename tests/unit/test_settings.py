import json
from time import time
from uuid import UUID, uuid4

import pytest
from pydantic import SecretStr, ValidationError

from pyticktick import Settings
from pyticktick.settings import TokenV1, V2XDevice

pytestmark = pytest.mark.filterwarnings("ignore:Unable to initialize")


@pytest.fixture()
def test_settings(
    test_v1_client_id,
    test_v1_client_secret,
    test_v1_token_value,
    test_v1_token_expiration,
    test_v2_username,
    test_v2_password,
    test_v2_token,
) -> Settings:
    return Settings(
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


def test_settings__parse_url_params():
    url = "http://127.0.0.1:8080/?code=ABCDEF&state=None&tester=test"
    assert Settings._parse_url_params(url) == {
        "code": "ABCDEF",
        "state": "None",
        "tester": "test",
    }


@pytest.mark.filterwarnings("ignore:`token` will expire in less than 7 days")
@pytest.mark.parametrize("test_expiration_days", [1, 5, 30])
def test_v1_token_initialize(
    test_v1_token_value,
    test_expiration_days,
    test_v1_token_expiration_days,
):
    test_expiration = test_v1_token_expiration_days(test_expiration_days)
    token = TokenV1.model_validate(
        {"value": test_v1_token_value, "expiration": test_expiration},
    )

    assert str(token.value) == test_v1_token_value
    assert token.expiration == test_expiration


@pytest.mark.parametrize(
    ("test_value", "test_expiration_days"),
    [
        (None, None),
        (None, 30),
        ("invalid", 30),
        (str(uuid4()), None),
        (str(uuid4()), -1),
    ],
)
def test_v1_token_initialize_invalid(
    test_value,
    test_expiration_days,
    test_v1_token_expiration_days,
):
    if test_expiration_days is not None:
        test_expiration = test_v1_token_expiration_days(test_expiration_days)
    else:
        test_expiration = None

    with pytest.raises(ValidationError):
        TokenV1(value=test_value, expiration=test_expiration)  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]


def test_v1_token_expiration():
    with pytest.warns(UserWarning, match="`token` will expire in less than 7 days"):
        TokenV1._validate_expiration(int(time()) + 1)

    with pytest.raises(ValueError, match="`token` has expired"):
        TokenV1._validate_expiration(int(time()) - 1)


@pytest.mark.filterwarnings("ignore:Cannot signon to v2")
@pytest.mark.parametrize("from_env", [True, False])
@pytest.mark.parametrize("test_base_url", [None, "http://test_base_url.com/"])
@pytest.mark.parametrize(
    "test_oauth_redirect_url",
    [None, "http://test_redirect_url.com/"],
)
def test_v1_settings_initialize(
    monkeypatch,
    test_v1_client_id,
    test_v1_client_secret,
    test_v1_token_value,
    test_base_url,
    test_oauth_redirect_url,
    from_env,
    test_v1_token_expiration_days,
):
    if from_env:
        monkeypatch.setenv("PYTICKTICK_V1_CLIENT_ID", test_v1_client_id)
        monkeypatch.setenv("PYTICKTICK_V1_CLIENT_SECRET", test_v1_client_secret)
        monkeypatch.setenv("PYTICKTICK_V1_TOKEN_VALUE", test_v1_token_value)
        monkeypatch.setenv(
            "PYTICKTICK_V1_TOKEN_EXPIRATION",
            str(test_v1_token_expiration_days(30)),
        )
        if test_base_url is not None:
            monkeypatch.setenv("PYTICKTICK_V1_BASE_URL", test_base_url)
        if test_oauth_redirect_url is not None:
            monkeypatch.setenv(
                "PYTICKTICK_V1_OAUTH_REDIRECT_URL",
                test_oauth_redirect_url,
            )
        settings = Settings()

    else:
        kwargs = {
            "v1_client_id": test_v1_client_id,
            "v1_client_secret": test_v1_client_secret,
            "v1_token": {
                "value": test_v1_token_value,
                "expiration": test_v1_token_expiration_days(30),
            },
        }
        if test_base_url is not None:
            kwargs["v1_base_url"] = test_base_url
        if test_oauth_redirect_url is not None:
            kwargs["v1_oauth_redirect_url"] = test_oauth_redirect_url
        settings = Settings.model_validate(kwargs)

    assert settings.v1_client_id == test_v1_client_id
    assert isinstance(settings.v1_client_secret, SecretStr)
    assert settings.v1_client_secret.get_secret_value() == test_v1_client_secret
    assert isinstance(settings.v1_token, TokenV1)
    assert settings.v1_token.value == UUID(test_v1_token_value)


@pytest.mark.filterwarnings("ignore:Cannot signon to v1")
@pytest.mark.parametrize("from_env", [True, False])
@pytest.mark.parametrize("test_base_url", [None, "http://test_base_url.com/"])
def test_v2_settings_initialize(
    monkeypatch,
    test_v2_username,
    test_v2_password,
    test_v2_token,
    from_env,
    test_base_url,
):
    if from_env:
        monkeypatch.setenv("PYTICKTICK_V2_USERNAME", test_v2_username)
        monkeypatch.setenv("PYTICKTICK_V2_PASSWORD", test_v2_password)
        monkeypatch.setenv("PYTICKTICK_V2_TOKEN", test_v2_token)
        if test_base_url is not None:
            monkeypatch.setenv("PYTICKTICK_V2_BASE_URL", test_base_url)
        settings = Settings()

    else:
        kwargs = {
            "v2_username": test_v2_username,
            "v2_password": test_v2_password,
            "v2_token": test_v2_token,
        }
        if test_base_url is not None:
            kwargs["v2_base_url"] = test_base_url
        settings = Settings.model_validate(kwargs)

    assert settings.v2_username == test_v2_username
    assert isinstance(settings.v2_password, SecretStr)
    assert settings.v2_password.get_secret_value() == test_v2_password
    assert settings.v2_token == test_v2_token


@pytest.mark.filterwarnings("ignore:Cannot signon to v1")
@pytest.mark.parametrize("from_env", [True, False])
@pytest.mark.parametrize("user_agent", ["Mozilla/5.0 (rv:145.0) Firefox/145.0"])
@pytest.mark.parametrize(
    "v2_x_device",
    [{"platform": "web", "version": 1000, "id": "69436d1b5890154a76755e9d"}],
)
def test_v2_settings_v2_headers(
    monkeypatch,
    test_v2_username,
    test_v2_password,
    test_v2_token,
    from_env,
    user_agent,
    v2_x_device,
):
    if from_env:
        monkeypatch.setenv("PYTICKTICK_V2_USERNAME", test_v2_username)
        monkeypatch.setenv("PYTICKTICK_V2_PASSWORD", test_v2_password)
        monkeypatch.setenv("PYTICKTICK_V2_TOKEN", test_v2_token)

        monkeypatch.setenv("PYTICKTICK_V2_USER_AGENT", user_agent)
        monkeypatch.setenv("PYTICKTICK_V2_X_DEVICE_PLATFORM", v2_x_device["platform"])
        monkeypatch.setenv(
            "PYTICKTICK_V2_X_DEVICE_VERSION", str(v2_x_device["version"])
        )
        monkeypatch.setenv("PYTICKTICK_V2_X_DEVICE_ID", v2_x_device["id"])
        settings = Settings()

    else:
        settings = Settings.model_validate(
            {
                "v2_username": test_v2_username,
                "v2_password": test_v2_password,
                "v2_token": test_v2_token,
                "v2_user_agent": user_agent,
                "v2_x_device": v2_x_device,
            },
        )

    assert settings.v2_user_agent == user_agent

    assert isinstance(settings.v2_x_device, V2XDevice)
    assert settings.v2_x_device.platform == v2_x_device["platform"]
    assert settings.v2_x_device.version == v2_x_device["version"]
    assert settings.v2_x_device.id == v2_x_device["id"]

    assert isinstance(settings.v2_headers, dict)
    assert settings.v2_headers.get("User-Agent") == user_agent
    assert json.loads(settings.v2_headers.get("X-Device", "{}")) == v2_x_device


@pytest.mark.filterwarnings("ignore:Cannot signon to v1")
def test_v2_settings__get_v2_token(
    mocker,
    test_v2_username,
    test_v2_password,
    test_v2_token,
    test_v2_usersignonv2,
):
    mocker.patch(
        "pyticktick.settings.Settings.v2_signon",
        return_value=test_v2_usersignonv2,
    )
    settings = Settings(
        v2_username=test_v2_username,
        v2_password=test_v2_password,
    )
    assert settings.v2_token == test_v2_token


def test_v1_header_dict(test_settings):
    d = test_settings.v1_headers

    assert isinstance(d, dict)

    assert "Authorization" in d
    assert isinstance(d["Authorization"], str)
    assert d["Authorization"] == f"Bearer {test_settings.v1_token.value}"

    assert "Content-Type" in d
    assert isinstance(d["Content-Type"], str)
    assert d["Content-Type"] == "application/json"


def test_v2_header_dict(test_settings):
    d = test_settings.v2_headers

    assert isinstance(d, dict)

    assert "User-Agent" in d
    assert isinstance(d["User-Agent"], str)

    assert "X-Device" in d
    assert isinstance(d["X-Device"], str)
    assert isinstance(json.loads(d["X-Device"]), dict)


def test_v2_cookie_dict(test_settings):
    d = test_settings.v2_cookies

    assert isinstance(d, dict)

    assert "t" in d
    assert isinstance(d["t"], str)
    assert d["t"] == test_settings.v2_token


def test_webbrowser_cannot_open(
    test_v1_client_id,
    test_v1_client_secret,
    mocker,
):
    mocker.patch("webbrowser.open", return_value=False)
    mocker.patch("click.confirm", return_value=True)

    with pytest.raises(ValidationError):
        Settings(
            v1_client_id=test_v1_client_id,
            v1_client_secret=test_v1_client_secret,
        )


@pytest.mark.filterwarnings("ignore:Cannot signon to v1")
@pytest.mark.parametrize("from_env", [True, False])
@pytest.mark.parametrize("test_forbid_extra", [True, False, None])
def test_other_settings_initialize(
    monkeypatch,
    test_v2_username,
    test_v2_password,
    test_v2_token,
    from_env,
    test_forbid_extra,
):
    if from_env:
        monkeypatch.setenv("PYTICKTICK_V2_USERNAME", test_v2_username)
        monkeypatch.setenv("PYTICKTICK_V2_PASSWORD", test_v2_password)
        monkeypatch.setenv("PYTICKTICK_V2_TOKEN", test_v2_token)
        if test_forbid_extra is not None:
            monkeypatch.setenv(
                "PYTICKTICK_OVERRIDE_FORBID_EXTRA",
                str(test_forbid_extra),
            )
        settings = Settings()

    else:
        kwargs = {
            "v2_username": test_v2_username,
            "v2_password": test_v2_password,
            "v2_token": test_v2_token,
        }
        if test_forbid_extra is not None:
            kwargs["override_forbid_extra"] = test_forbid_extra
        settings = Settings.model_validate(kwargs)

    if test_forbid_extra is not None:
        assert settings.override_forbid_extra == test_forbid_extra
    else:
        assert not settings.override_forbid_extra
