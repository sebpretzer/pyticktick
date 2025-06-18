"""Model for getting closed tasks from the database.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GetClosedV2(BaseModel):
    """Model for getting closed tasks from the database.

    These are tasks that have been marked as completed or abandoned. They will not show
    up in the normal task list.
    """

    model_config = ConfigDict(extra="forbid")

    from_: datetime | None = Field(
        default=None,
        alias="The latest date to get tasks from",
    )
    to: datetime | None = Field(
        default=None,
        description="The earliest date to get tasks from",
    )
    status: Literal["Completed", "Abandoned"] = Field(
        description='Whether to get completed or "won\'t do" tasks',
    )
