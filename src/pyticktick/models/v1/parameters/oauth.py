"""OAuth2 URL parameters for the V1 API.

This module contains the Pydantic models that generate the OAuth2 URLs for the V1 API
[authorization flow](https://developer.ticktick.com/api#/openapi?id=authorization).
"""

from __future__ import annotations

from typing import Any, Literal
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict, Field, model_serializer

from pyticktick.models.pydantic import HttpUrl


class OAuthAuthorizeURLV1(BaseModel):
    """OAuth2 authorize URL parameters for V1 API.

    Helper class to generate the OAuth2 authorize URL for the V1 API. This is the
    [first step](https://developer.ticktick.com/api#/openapi?id=first-step) in the
    OAuth2 flow.

    ???+ example
        ```python
        from pyticktick.models.v1.parameters.oauth import OAuthAuthorizeURLV1

        oauth_url = OAuthAuthorizeURLV1(client_id="your_client_id")
        print(oauth_url.model_dump())
        ```
        would print:
        ```
        https://ticktick.com/oauth/authorize?client_id=your_client_id&scope=tasks%3Aread+tasks%3Awrite&state=None&response_type=code
        ```
    """

    model_config = ConfigDict(extra="forbid")

    client_id: str = Field(
        description="V1 API App unique client id. Taken from the [Manage Apps](https://developer.ticktick.com/manage) page.",
    )
    scope: Literal["tasks:read tasks:write"] = Field(
        default="tasks:read tasks:write",
        description="Spaces-separated permissions for the generated token. The currently available scopes are 'tasks:write' and 'tasks:read'. Default is 'tasks:read tasks:write'.",
    )
    state: Any = Field(default=None, description="Passed to redirect url as is.")
    response_type: Literal["code"] = Field(
        default="code",
        description="Fixed value 'code'.",
    )
    base_url: HttpUrl = Field(
        default=HttpUrl("https://ticktick.com/oauth/authorize"),
        description="OAuth2 authorize URL.",
    )

    @model_serializer
    def ser_model(self) -> str:
        """Serialize the model to a URL string.

        Returns:
            str: The URL string.
        """
        params = {
            "client_id": self.client_id,
            "scope": self.scope,
            "state": self.state,
            "response_type": self.response_type,
        }
        return f"{self.base_url}?{urlencode(params)}"


class OAuthTokenURLV1(BaseModel):
    """OAuth2 token URL parameters for V1 API.

    Helper class to generate the OAuth2 token URL for the V1 API. This is the
    [third step](https://developer.ticktick.com/api#/openapi?id=third-step) in the
    OAuth2 flow.

    ???+ example
        ```python
        from pyticktick.models.v1.parameters.oauth import OAuthTokenURLV1

        oauth_url = OAuthTokenURLV1(
            client_id="your_client_id",
            client_secret="your_client_secret",
            code="your_code",
        )
        print(oauth_url.model_dump())
        ```
        would print:
        ```
        https://ticktick.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=your_code&grant_type=authorization_code&scope=tasks%3Aread+tasks%3Awrite&redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2F
        ```
    """

    model_config = ConfigDict(extra="forbid")

    client_id: str = Field(
        description="V1 API App unique client id. Taken from the [Manage Apps](https://developer.ticktick.com/manage) page.",
    )
    client_secret: str = Field(
        description="V1 API App unique client secret. Taken from the [Manage Apps](https://developer.ticktick.com/manage) page.",
    )
    code: str = Field(description="The code received from the OAuth2 authorize URL.")
    oauth_redirect_url: HttpUrl = Field(
        default=HttpUrl("http://127.0.0.1:8080/"),
        description="The redirect URL. Can be any URL, but should be one that does not collide with other applications.",
    )
    scope: Literal["tasks:read tasks:write"] = Field(
        default="tasks:read tasks:write",
        description="Spaces-separated permissions for the generated token. The currently available scopes are 'tasks:write' and 'tasks:read'. Default is 'tasks:read tasks:write'.",
    )
    grant_type: Literal["authorization_code"] = Field(
        default="authorization_code",
        description="Fixed value 'authorization_code'.",
    )
    base_url: HttpUrl = Field(
        default=HttpUrl("https://ticktick.com/oauth/token"),
        description="OAuth2 token URL.",
    )

    @model_serializer
    def ser_model(self) -> str:
        """Serialize the model to a URL string.

        Returns:
            str: The OAuth URL string.
        """
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "grant_type": self.grant_type,
            "scope": self.scope,
            "redirect_uri": self.oauth_redirect_url,
        }
        return f"{self.base_url}?{urlencode(params)}"
