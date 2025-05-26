"""Pydantic response models for the OAuth2 flow in the V1 API."""

from __future__ import annotations

from typing import Literal

from pydantic import UUID4, BaseModel, ConfigDict, Field


class OAuthTokenV1(BaseModel):
    """Response of the POST request in the [third step](https://developer.ticktick.com/docs#/openapi?id=third-step) of the OAuth2 flow."""  # noqa: W505

    model_config = ConfigDict(extra="ignore")

    access_token: UUID4 = Field(description="OAuth2 access token for the V1 API.")
    expires_in: int = Field(
        description="Access token expiration time in seconds from the time of issue. Usually lasts 6 months.",
    )
    token_type: Literal["bearer"] = Field(
        default="bearer",
        description="Fixed value 'bearer'.",
    )
    scope: Literal["tasks:read tasks:write"] = Field(
        default="tasks:read tasks:write",
        description="Spaces-separated permissions for the generated token. The currently available scopes are 'tasks:write' and 'tasks:read'. Default is 'tasks:read tasks:write'.",
    )
