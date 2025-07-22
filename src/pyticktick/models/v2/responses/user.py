"""Pydantic models for user-related data returned by the TickTick API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from pydantic import (
    UUID4,
    EmailStr,
    Field,
    RootModel,
    ValidationInfo,
    field_validator,
)

from pyticktick.models.v2.models import BaseModelV2


class UserSignOnWithTOTPV2(BaseModelV2):
    """Model for the response of a sign-on request via the V2 API with TOTP.

    This model is used when the user has enabled two-factor authentication (2FA) via
    TOTP (Time-based One-Time Password).
    """

    auth_id: str = Field(
        validation_alias="authId",
        description="The authentication ID used for the sign-on request.",
    )
    expire_time: int = Field(
        validation_alias="expireTime",
        description="The expiration time of the authentication ID in seconds since the epoch.",
    )


class UserSignOnV2(BaseModelV2):
    """Model for the response of a sign-on request via the V2 API.

    The most important field is `token`, which is used for authentication during a
    session.
    """

    # known fields
    inbox_id: str = Field(
        validation_alias="inboxId",
        description="The user's inbox ID.",
    )
    token: str = Field(
        description="The user's authentication token that is used for short-term authentication.",
    )
    user_id: str = Field(validation_alias="userId", description="The user's ID.")
    username: EmailStr = Field(description="The user's email address.")

    # unknown fields
    active_team_user: bool = Field(validation_alias="activeTeamUser")
    ds: bool
    free_trial: bool = Field(validation_alias="freeTrial")
    freq: str | None = None
    grace_period: bool | None = Field(default=None, validation_alias="gracePeriod")
    need_subscribe: bool = Field(validation_alias="needSubscribe")
    pro: bool
    pro_end_date: str = Field(validation_alias="proEndDate")
    pro_start_date: str | None = Field(default=None, validation_alias="proStartDate")
    subscribe_freq: str | None = Field(
        default=None,
        validation_alias="subscribeFreq",
    )
    subscribe_type: str | None = Field(
        default=None,
        validation_alias="subscribeType",
    )
    team_pro: bool = Field(validation_alias="teamPro")
    team_user: bool = Field(validation_alias="teamUser")
    user_code: UUID4 = Field(validation_alias="userCode")


class UserProfileV2(BaseModelV2):
    """Model containing the user's profile information."""

    etimestamp: Any
    username: EmailStr
    site_domain: str = Field(validation_alias="siteDomain")
    created_campaign: str | None = Field(validation_alias="createdCampaign")
    created_device_info: Any = Field(validation_alias="createdDeviceInfo")
    filled_password: bool = Field(validation_alias="filledPassword")
    account_domain: Any = Field(validation_alias="accountDomain")
    extenal_id: Any = Field(validation_alias="extenalId")  # yes, it's a typo
    email: Any
    verified_email: bool = Field(validation_alias="verifiedEmail")
    faked_email: bool = Field(validation_alias="fakedEmail")
    phone: Any
    name: str | None = None
    given_name: Any = Field(validation_alias="givenName")
    family_name: Any = Field(validation_alias="familyName")
    link: Any
    picture: str
    gender: Any
    locale: str
    user_code: UUID4 = Field(validation_alias="userCode")
    ver_code: Any = Field(validation_alias="verCode")
    ver_key: Any = Field(validation_alias="verKey")
    external_id: Any = Field(validation_alias="externalId")
    phone_without_country_code: Any = Field(validation_alias="phoneWithoutCountryCode")
    display_name: str = Field(validation_alias="displayName")


class UserStatusV2(BaseModelV2):
    """Model for the response of a user status request via the V2 API.

    This user "status" is mainly about the user's subscription status, rather than
    their current activity on TickTick.
    """

    user_id: str = Field(validation_alias="userId", description="The user's ID.")
    user_code: UUID4 = Field(validation_alias="userCode")
    username: EmailStr = Field(description="The user's email address.")
    team_pro: bool = Field(validation_alias="teamPro")
    pro_start_date: str | None = Field(
        default=None,
        validation_alias="proStartDate",
        description="The date when the user started their premium subscription.",
    )
    pro_end_date: str = Field(
        validation_alias="proEndDate",
        description="The date when the user's premium subscription is slated to end.",
    )
    subscribe_type: str | None = Field(
        default=None,
        validation_alias="subscribeType",
    )
    subscribe_freq: str | None = Field(
        default=None,
        validation_alias="subscribeFreq",
    )
    need_subscribe: bool = Field(validation_alias="needSubscribe")
    freq: str | None = None
    inbox_id: str = Field(
        validation_alias="inboxId",
        description="The user's inbox ID.",
    )
    team_user: bool = Field(validation_alias="teamUser")
    active_team_user: bool = Field(validation_alias="activeTeamUser")
    free_trial: bool = Field(validation_alias="freeTrial")
    pro: bool = Field(
        description="Whether or not a user has subscribed to the premium plan.",
    )
    ds: bool
    time_stamp: int = Field(
        validation_alias="timeStamp",
        description="Timestamp of the last update.",
    )
    grace_period: bool | None = Field(default=None, validation_alias="gracePeriod")


def _cast_task_count_keys(root: dict[str, Any]) -> dict[date, Any]:
    if root is None or not isinstance(root, dict):
        msg = "root must be a dictionary"
        raise TypeError(msg)

    data = {}
    for k, v in root.items():
        if not isinstance(k, str):
            msg = "keys must be strings"
            raise TypeError(msg)
        data[datetime.strptime(k, "%Y%m%d").replace(tzinfo=timezone.utc).date()] = v
    return data


class ScoreByDayV2(RootModel[dict[date, int]]):
    """The user's score for each day."""

    root: dict[date, int]

    @field_validator("root", mode="before")
    @classmethod
    def _cast_keys(
        cls,
        root: dict[str, int],
        info: ValidationInfo,  # noqa: ARG003
    ) -> Any:
        return _cast_task_count_keys(root)


class TaskCountV2(BaseModelV2):
    """Model that represents the current task count for a given time period."""

    complete_count: int = Field(validation_alias="completeCount")
    not_complete_count: int = Field(validation_alias="notCompleteCount")


class TaskByDayV2(RootModel[dict[date, TaskCountV2]]):
    """The number of tasks both completed and not completed for a given day."""

    root: dict[date, TaskCountV2] = Field(
        description="The number of tasks both completed and not completed for a given day, where the key is the date.",
    )

    @field_validator("root", mode="before")
    @classmethod
    def _cast_keys(
        cls,
        root: dict[str, TaskCountV2],
        info: ValidationInfo,  # noqa: ARG003
    ) -> Any:
        return _cast_task_count_keys(root)


class TaskByWeekV2(RootModel[dict[date, TaskCountV2]]):
    """The number of tasks both completed and not completed for a given week."""

    root: dict[date, TaskCountV2] = Field(
        description="The number of tasks both completed and not completed for a given week, where the key is the first day of the week.",
    )

    @field_validator("root", mode="before")
    @classmethod
    def _cast_keys(
        cls,
        root: dict[str, TaskCountV2],
        info: ValidationInfo,  # noqa: ARG003
    ) -> Any:
        return _cast_task_count_keys(root)


class TaskByMonthV2(RootModel[dict[date, TaskCountV2]]):
    """The number of tasks both completed and not completed for a given month."""

    root: dict[date, TaskCountV2] = Field(
        description="The number of tasks both completed and not completed for a given month, where the key is the first day of the month.",
    )

    @field_validator("root", mode="before")
    @classmethod
    def _cast_keys(
        cls,
        root: dict[str, TaskCountV2],
        info: ValidationInfo,  # noqa: ARG003
    ) -> Any:
        return _cast_task_count_keys(root)


class UserStatisticsV2(BaseModelV2):
    """Model for the response of a user statistics request via the V2 API."""

    score: int
    level: int
    yesterday_completed: int = Field(validation_alias="yesterdayCompleted")
    today_completed: int = Field(validation_alias="todayCompleted")
    total_completed: int = Field(validation_alias="totalCompleted")
    score_by_day: ScoreByDayV2 = Field(validation_alias="scoreByDay")
    task_by_day: TaskByDayV2 = Field(validation_alias="taskByDay")
    task_by_week: TaskByWeekV2 = Field(validation_alias="taskByWeek")
    task_by_month: TaskByMonthV2 = Field(validation_alias="taskByMonth")
    today_pomo_count: int = Field(validation_alias="todayPomoCount")
    yesterday_pomo_count: int = Field(validation_alias="yesterdayPomoCount")
    total_pomo_count: int = Field(validation_alias="totalPomoCount")
    today_pomo_duration: int = Field(validation_alias="todayPomoDuration")
    yesterday_pomo_duration: int = Field(validation_alias="yesterdayPomoDuration")
    total_pomo_duration: int = Field(validation_alias="totalPomoDuration")
    pomo_goal: int = Field(validation_alias="pomoGoal")
    pomo_duration_goal: int = Field(validation_alias="pomoDurationGoal")
    pomo_by_day: dict[str, Any] = Field(validation_alias="pomoByDay")
    pomo_by_week: dict[str, Any] = Field(validation_alias="pomoByWeek")
    pomo_by_month: dict[str, Any] = Field(validation_alias="pomoByMonth")
