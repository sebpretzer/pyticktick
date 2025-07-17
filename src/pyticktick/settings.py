"""Settings for the pyticktick client.

This module contains the settings for the pyticktick client. The settings juggle the two
TickTick APIs: V1 and V2. The V1 API is the official API, and the V2 API
is an undocumented one. The settings are expected to be used in conjunction with the
`pyticktick.client.Client` class, which manages the API requests.
"""

from __future__ import annotations

import json
import warnings
import webbrowser
from time import time
from typing import Any
from urllib.parse import parse_qsl, urlparse

import click
import httpx
from loguru import logger
from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyotp import TOTP

from pyticktick.models.pydantic import HttpUrl
from pyticktick.models.v1.parameters.oauth import OAuthAuthorizeURLV1, OAuthTokenURLV1
from pyticktick.models.v1.responses.oauth import OAuthTokenV1
from pyticktick.models.v2.responses.user import UserSignOnV2, UserSignOnWithTOTPV2


class TokenV1(BaseModel):  # noqa: DOC601, DOC603
    """Model for the V1 API token.

    The token is a standard UUID4 string, which seems to [expire after about 6 months](https://github.com/lazeroffmichael/ticktick-py/blob/9ebc0c5b09c702de8a137a05dc5b8d8803f18f48/docs/index.md?plain=1#L148).
    The expiration is a Unix timestamp in seconds, which is validated to confirm that
    the token has not expired.
    """

    model_config = ConfigDict(extra="forbid")

    value: UUID4 = Field(description="The UUID4 string token")
    expiration: int = Field(
        description="The Unix timestamp in seconds when the token expires.",
    )

    @field_validator("expiration", mode="after")
    @classmethod
    def _validate_expiration(cls, v: int) -> int:
        if v < int(time()):
            msg = "`token` has expired, `expiration` time has passed"
            raise ValueError(msg)
        if v < int(time()) + 7 * 24 * 60 * 60:
            msg = "`token` will expire in less than 7 days"
            logger.warning(msg)
            warnings.warn(msg, UserWarning, stacklevel=1)
        return v


class Settings(BaseSettings):  # noqa: DOC601, DOC603
    """Settings for the pyticktick client.

    The settings are used to sign on to the [two TickTick APIs](https://pyticktick.pretzer.io/explanations/ticktick_api/two_apis.md).
    The two APIs have two distinct sign on methods. The V1 API uses OAuth2, and is the
    official API, with [official documentation](https://developer.ticktick.com/docs#/openapi).
    The V2 API uses a username and password, is an undocumented, and not officially
    supported by TickTick.

    Each API can be signed on to independently, so a user can use one or both,
    depending on their needs. It is recommended to create and save the V1 token, as it
    requires user input to sign on, and is not easily automated.

    ???+ example "Load all settings"
        ```python
        from pyticktick import Settings

        settings = Settings(
            v1_client_id="client_id",
            v1_client_secret="client_secret",
            v1_token={
                "value": "fa371b10-8b95-442b-b4a5-11a9959d3590",
                "expiration": 1701701789,
            },
            v2_username="username",
            v2_password="password",
            override_forbid_extra=True,
        )
        ```

    ???+ example "Load only V1 API settings"
        ```python
        from pyticktick import Settings

        settings = Settings(
            v1_client_id="client_id",
            v1_client_secret="client_secret",
            v1_token={
                "value": "fa371b10-8b95-442b-b4a5-11a9959d3590",
                "expiration": 1701701789,
            },
        )
        ```

    ???+ example "Load only V2 API settings"
        ```python
        from pyticktick import Settings

        settings = Settings(
            v2_username="username",
            v2_password="password",
        )
        ```

    ???+ example "Load only V2 API settings when 2FA is enabled"
        ```python
        from pyticktick import Settings

        settings = Settings(
            v2_username="username",
            v2_password="password",
            v2_totp_secret="totp_secret",
        )
        ```

    This class is a subclass of `pydantic_settings.BaseSettings`, which allows for
    [environment variable and secret file parsing](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

    ???+ example "Load settings from environment variables"
        ```bash title=".bashrc"
        export PYTICKTICK_V1_CLIENT_ID="client_id"
        export PYTICKTICK_V1_CLIENT_SECRET="client_secret"
        export PYTICKTICK_V1_TOKEN_VALUE="fa371b10-8b95-442b-b4a5-11a9959d3590"
        export PYTICKTICK_V1_TOKEN_EXPIRATION="1701701789"
        export PYTICKTICK_V2_USERNAME="username"
        export PYTICKTICK_V2_PASSWORD="password"
        export PYTICKTICK_OVERRIDE_FORBID_EXTRA="True"
        ```

        ```python
        from pyticktick import Settings

        settings = Settings()
        ```

    ???+ example "Load settings from a secret file"
        ```bash title=".env"
        PYTICKTICK_V1_CLIENT_ID="client_id"
        PYTICKTICK_V1_CLIENT_SECRET="client_secret"
        PYTICKTICK_V1_TOKEN_VALUE="fa371b10-8b95-442b-b4a5-11a9959d3590"
        PYTICKTICK_V1_TOKEN_EXPIRATION="1701701789"
        PYTICKTICK_V2_USERNAME="username"
        PYTICKTICK_V2_PASSWORD="password"
        PYTICKTICK_OVERRIDE_FORBID_EXTRA="True"
        ```

        ```python
        from pyticktick import Settings

        settings = Settings(_env_file=".env")
        ```

    Attributes:
        v1_client_id (Optional[str]): The client ID for the V1 API.
        v1_client_secret (Optional[SecretStr]): The client secret for the V1 API.
        v1_token (Optional[TokenV1]): The OAuth2 token for the V1 API.
        v1_base_url (HttpUrl): The base URL for the V1 API. Defaults to
            `https://api.ticktick.com/open/v1/`.
        v1_oauth_redirect_url (HttpUrl): The URL to redirect to after authorization.
            Defaults to `http://127.0.0.1:8080/`.
        v2_username (Optional[EmailStr]): The username for the V2 API.
        v2_password (Optional[SecretStr]): The password for the V2 API.
        v2_totp_secret (Optional[SecretStr]): The TOTP secret for the V2 API, required
            for two-factor authentication.
        v2_token (Optional[str]): The cookie token for the V2 API.
        v2_base_url (HttpUrl): The base URL for the V2 API. Defaults to
            `https://api.ticktick.com/api/v2/`.
        override_forbid_extra (bool): Whether to override forbidding extra fields.
    """

    # NOTE: Docstring attributes are required here, as griffe_pydantic does not support
    # BaseSettings: https://github.com/mkdocstrings/griffe-pydantic/issues/27

    model_config = SettingsConfigDict(
        env_prefix="pyticktick_",
        env_nested_delimiter="_",
        extra="forbid",
    )

    v1_client_id: str | None = Field(
        default=None,
        description="The client ID for the V1 API.",
    )
    v1_client_secret: SecretStr | None = Field(
        default=None,
        description="The client secret for the V1 API.",
    )
    v1_token: TokenV1 | None = Field(
        default=None,
        description="The OAuth2 token for the V1 API.",
    )
    v1_base_url: HttpUrl = Field(
        default=HttpUrl("https://api.ticktick.com/open/v1/"),
        description="The base URL for the V1 API.",
    )
    v1_oauth_redirect_url: HttpUrl = Field(
        default=HttpUrl("http://127.0.0.1:8080/"),
        description="The URL to redirect to after authorization.",
    )

    v2_username: EmailStr | None = Field(
        default=None,
        description="The username for the V2 API.",
    )
    v2_password: SecretStr | None = Field(
        default=None,
        description="The password for the V2 API.",
    )
    v2_totp_secret: SecretStr | None = Field(
        default=None,
        description="The TOTP Secret for the V2 API, used for two-factor authentication.",  # noqa: E501
    )
    v2_token: str | None = Field(
        default=None,
        description="The cookie token for the V2 API.",
    )
    v2_base_url: HttpUrl = Field(
        default=HttpUrl("https://api.ticktick.com/api/v2/"),
        description="The base URL for the V2 API.",
    )

    override_forbid_extra: bool = Field(
        default=False,
        description="Override any API models that may be out of date and should contain new fields.",  # noqa: E501
    )

    @staticmethod
    def _parse_url_params(url: str) -> dict[str, str]:
        return dict(parse_qsl(urlparse(url).query))

    @classmethod
    def _v1_signon(
        cls,
        client_id: str,
        client_secret: str,
        oauth_redirect_url: str,
    ) -> dict[str, str]:
        url = OAuthAuthorizeURLV1(client_id=client_id).model_dump()
        if not isinstance(url, str):
            msg = f"Invalid token URL, expected a string, got {type(url)}"
            logger.error(msg)
            raise TypeError(msg)

        open_browser = click.confirm(
            f"Request URL:\n\n\t{url}\n\nOpen the browser to signon to the V1 API?",
            default=True,
        )
        if open_browser and not webbrowser.open(url):
            msg = "Cannot open the browser to signon to the V1 API"
            logger.error(msg)
            raise ValueError(msg)

        redirect_url = click.prompt("What is the URL you were redirected to?")
        data = cls._parse_url_params(redirect_url)
        if (code := data.get("code")) is None:
            msg = "No `code` found in the URL"
            logger.error(msg)
            raise ValueError(msg)

        token_url = OAuthTokenURLV1(
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            oauth_redirect_url=HttpUrl(oauth_redirect_url),
        ).model_dump()

        if not isinstance(token_url, str):
            msg = f"Invalid token URL, expected a string, got {type(token_url)}"
            logger.error(msg)
            raise TypeError(msg)

        try:
            resp = httpx.post(token_url, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if isinstance((content := e.response.content), bytes):
                content = content.decode()
            msg = f"Response [{e.response.status_code}]:\n{content}"
            logger.error(msg)
            raise ValueError(msg) from e
        return resp.json()

    @classmethod
    def v1_signon(
        cls,
        client_id: str,
        client_secret: str,
        oauth_redirect_url: str,
    ) -> OAuthTokenV1:
        """Generate an OAuth2 token for the V1 API.

        This method runs the OAuth2 sign on process for the V1 API. This is a multi-step
        process that requires user input, so its use is limited to interactive sessions.

        ???+ note "V1 OAuth2 Sign On Process"
            The multi-step process is as follows:

            1. The user is redirected to the authorization URL, where they log in, and
            authorize the application.
            2. The user is redirected to a new URL, which contains a `code` parameter.
            This URL should be copied into the console, and the code extracted.
            3. The code is exchanged for an OAuth2 token. This token is then used for
            authentication moving forward.

            You can read the official documentation [here](https://developer.ticktick.com/docs/index.html#/openapi?id=authorization).

        Args:
            client_id (str): The client ID for the application.
            client_secret (str): The client secret for the application.
            oauth_redirect_url (str): The URL to redirect to after authorization.

        Returns:
            OAuthTokenV1: The OAuth2 token response model for the V1 API.
        """
        resp = cls._v1_signon(client_id, client_secret, oauth_redirect_url)
        return OAuthTokenV1.model_validate(resp)

    @staticmethod
    def _v2_signon(
        username: str,
        password: str,
        base_url: str,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        try:
            resp = httpx.post(
                url=base_url + "/user/signon?wc=true&remember=true",
                headers=headers,
                json={
                    "username": username,
                    "password": password,
                },
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if isinstance((_content := e.response.content), bytes):
                content = _content.decode()
            else:
                content = _content
            msg = f"Response [{e.response.status_code}]:\n{content}"
            logger.error(msg)
            raise ValueError(msg) from e

        if not isinstance((_dict := resp.json()), dict):
            msg = f"Invalid response, expected `dict`, got {type(_dict)}"
            raise TypeError(msg)
        return _dict

    @staticmethod
    def _v2_mfa_verify(
        totp_secret: str,
        auth_id: str,
        base_url: str,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        try:
            resp = httpx.post(
                url=base_url + "/user/sign/mfa/code/verify",
                headers={**headers, "x-verify-id": auth_id},
                json={"code": TOTP(totp_secret).now(), "method": "app"},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if isinstance((_content := e.response.content), bytes):
                content = _content.decode()
            else:
                content = _content
            msg = f"Response [{e.response.status_code}]:\n{content}"
            logger.error(msg)
            raise ValueError(msg) from e

        if not isinstance((_dict := resp.json()), dict):
            msg = f"Invalid response, expected `dict`, got {type(_dict)}"
            raise TypeError(msg)
        return _dict

    @classmethod
    def v2_signon(
        cls,
        username: str,
        password: str,
        totp_secret: str | None,
        base_url: str,
        headers: dict[str, str],
    ) -> UserSignOnV2:
        """Generate a cookie token for the undocumented V2 API.

        This method uses a username and password to sign on to the V2 API. The sign on
        request returns a cookie token, which is then used for authentication moving
        forward. This API is undocumented and TickTick may change it at any time. This
        logic was mainly pulled [lucasvtiradentes/ticktick-api-lvt](https://github.com/lucasvtiradentes/ticktick-api-lvt):

        1. The headers and url base were taken from [here](https://github.com/lucasvtiradentes/ticktick-api-lvt/blob/2b121beacf8d93e4408e194dc7ea9b8ac9553988/src/configs.ts#L25-L26).
        2. The url route was taken from [here](https://github.com/lucasvtiradentes/ticktick-api-lvt/blob/2b121beacf8d93e4408e194dc7ea9b8ac9553988/src/routes/auth/login.ts#L6).

        Args:
            username (str): The username for the V2 API.
            password (str): The password for the V2 API.
            totp_secret (str | None): The TOTP secret for the V2 API, used for
                two-factor authentication. If the sign on request requires TOTP
                verification, this parameter must be provided. If the sign on request
                does not require TOTP verification, this parameter can be `None`.
            base_url (str): The base URL for the V2 API.
            headers (dict[str, str]): The headers dictionary for the V2 API.

        Raises:
            ValueError: If the sign on request requires TOTP verification, but no TOTP
                was provided.

        Returns:
            UserSignOnV2: The sign on response model for the V2 API.
        """
        resp = cls._v2_signon(
            username=username,
            password=password,
            base_url=base_url,
            headers=headers,
        )
        try:
            totp_resp = UserSignOnWithTOTPV2.model_validate(resp)
            if totp_secret is None:
                msg = "Sign on requires TOTP verification, but no TOTP was provided."
                logger.error(msg)
                raise ValueError(msg)
            resp = cls._v2_mfa_verify(
                totp_secret=totp_secret,
                auth_id=totp_resp.auth_id,
                base_url=base_url,
                headers=headers,
            )
        except ValidationError:
            pass

        return UserSignOnV2.model_validate(resp)

    def _check_no_settings(self) -> Settings:
        if (self.v1_client_id is None and self.v1_client_secret is None) and (
            self.v2_username is None and self.v2_password is None
        ):
            msg = "No settings provided, cannot signon to any API"
            logger.error(msg)
            raise ValueError(msg)

        return self

    def _get_v1_token(self) -> Settings:
        if self.v1_token is None:
            if self.v1_client_id is None or self.v1_client_secret is None:
                msg = (
                    "Cannot signon to v1 without `v1_client_id` and `v1_client_secret`"
                )
                logger.warning(msg)
                warnings.warn(msg, UserWarning, stacklevel=1)
            else:
                _token = self.v1_signon(
                    client_id=self.v1_client_id,
                    client_secret=self.v1_client_secret.get_secret_value(),
                    oauth_redirect_url=str(self.v1_oauth_redirect_url),
                )
                self.v1_token = TokenV1(
                    value=_token.access_token,
                    expiration=_token.expires_in + int(time()),
                )
        return self

    def _get_v2_token(self) -> Settings:
        if self.v2_token is None:
            if self.v2_username is None or self.v2_password is None:
                msg = "Cannot signon to v2 without `v2_username` and `v2_password`"
                logger.warning(msg)
                warnings.warn(msg, UserWarning, stacklevel=1)
            else:
                totp_secret = None
                if self.v2_totp_secret is not None:
                    totp_secret = self.v2_totp_secret.get_secret_value()
                self.v2_token = self.v2_signon(
                    username=self.v2_username,
                    password=self.v2_password.get_secret_value(),
                    totp_secret=totp_secret,
                    base_url=str(self.v2_base_url),
                    headers=self.v2_headers,
                ).token
        return self

    @model_validator(mode="after")
    def _validate_model(self) -> Settings:
        self._check_no_settings()
        self._get_v1_token()
        self._get_v2_token()
        return self

    @property
    def v1_headers(self) -> dict[str, str]:
        """Get the headers dictionary for the V1 API.

        Provides the headers dictionary for the V1 API. This is used to authenticate
        requests to the V1 API. The headers change as frequently as the V1 token, and
        therefore change, but rarely.

        Returns:
            dict[str, str]: The headers dictionary for the V1 API.

        Raises:
            ValueError: If the `v1_token` is not set.
        """
        if self.v1_token is None:
            msg = "Cannot get headers for v1 without `v1_token`"
            logger.error(msg)
            raise ValueError(msg)

        return {
            "Authorization": f"Bearer {self.v1_token.value}",
            "Content-Type": "application/json",
        }

    @property
    def v2_headers(self) -> dict[str, str]:
        """Get the headers dictionary for the V2 API.

        Provides the headers dictionary for the V2 API. This is used to authenticate
        requests to the V2 API. The headers are static and do not change. They were
        taken from a web browser request to the TickTick website, and are meant to mimic
        a web browser request.

        Returns:
            dict[str, str]: The headers dictionary for the V2 API.
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",  # noqa: E501
            "X-Device": json.dumps(
                {
                    "platform": "web",
                    "os": "Windows 10",
                    "device": "Firefox 117.0",
                    "name": "",
                    "version": 4576,
                    "id": "64fc9b22cbb2c305b2df7ad6",
                    "channel": "website",
                    "campaign": "",
                    "websocket": "6500a8a3bf02224e648ef8bd",
                },
            ),
        }

    @property
    def v2_cookies(self) -> dict[str, str]:
        """Get the cookies dictionary for the V2 API.

        Provides the cookies dictionary for the V2 API. This is used to authenticate
        requests to the V2 API. The cookies are only valid for the length of the client,
        and will change for each new client.

        Returns:
            dict[str, str]: The cookies dictionary for the V2 API.

        Raises:
            ValueError: If the `v2_token` is not set.
        """
        if self.v2_token is None:
            msg = "Cannot get v2 cookies without `v2_token`"
            logger.error(msg)
            raise ValueError(msg)

        return {"t": self.v2_token}
