"""Model for the response of `GET` closed tasks via the V2 API."""

from __future__ import annotations

from pydantic import Field, RootModel

from pyticktick.models.v2.models import TaskV2


class ClosedRespV2(RootModel[list[TaskV2]]):
    """Model for the response of getting closed tasks via the V2 API.

    Closed tasks are tasks that have been marked as completed or abandoned. They will
    not show up in the normal task list.
    """

    root: list[TaskV2] = Field(description="List of all closed tasks for the user")
