"""Model for getting closed tasks from the database.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import Field, field_serializer

from pyticktick.models.v2.models import BaseModelV2


class GetClosedV2(BaseModelV2):
    """Model for getting closed tasks from the database.

    These are tasks that have been marked as completed or abandoned. They will not show
    up in the normal task list.
    """

    from_: datetime | None = Field(
        default=None,
        description="The earliest date to get tasks from",
    )
    to: datetime | None = Field(
        default=None,
        description="The latest date to get tasks from",
    )
    status: Literal["Completed", "Abandoned"] = Field(
        description='Whether to get completed or "won\'t do" tasks',
    )

    @field_serializer("from_", "to")
    def _serialize_dt(self, dt: datetime | None, _info: Any) -> str | None:
        if dt is None:
            return None
        return dt.replace(tzinfo=None).isoformat(sep=" ", timespec="seconds")
