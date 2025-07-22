"""Responses for batch requests in the V2 API.

This module holds both the response for general `POST` batch requests and the response
for `GET` batch requests.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from pyticktick.models.v2.models import (
    BaseModelV2,
    ProjectGroupV2,
    ProjectV2,
    TagV2,
    TaskV2,
)
from pyticktick.models.v2.types import ETag, ObjectId


class BatchRespV2(BaseModelV2):
    """Model for the response of a generic batch request via the V2 API.

    !!! warning
        This model is a best guess at the structure of the response. It is not clear
        whether the `id2etag` and `id2error` fields are from MongoDB, but they seem to
        fit the pattern.
    """

    # known fields
    id2error: dict[ObjectId, str] = Field(
        validation_alias="id2error",
        description="Mapping of objects that failed to be created / updated",
    )
    id2etag: dict[ObjectId, ETag] = Field(
        validation_alias="id2etag",
        description="ID to ETag mapping of objects that were successfully created / updated",
    )

    @property
    def ids(self) -> list[str]:
        """List of all the IDs in the response."""
        return list(self.id2etag)

    @property
    def etags(self) -> list[str]:
        """List of all the ETags in the response."""
        return list(self.id2etag.values())

    @model_validator(mode="after")
    def _exceeded_quota(self) -> BatchRespV2:
        if self.id2error:
            for id_, error in self.id2error.items():
                if error == "EXCEED_QUOTA":
                    msg = (
                        f"Exceeded quota for object `{id_}`, please check your account."
                    )
                    raise ValueError(msg)
        return self


class SyncTaskBeanV2(BaseModelV2):
    """Model for all the tasks in a batch response via the V2 API.

    This model is used to represent all the tasks in a batch response from the V2 API.
    It lends itself to being used as parameters for a update request, but we do not have
    a complete understanding of how. For now, the `update` field is the most important,
    as it contains all the active tasks for the user.
    """

    # known fields
    update: list[TaskV2] = Field(
        description="List of all active tasks for the user",
    )

    # unknown fields
    add: list[Any]
    delete: list[Any]
    empty: bool
    tag_update: list[Any] = Field(validation_alias="tagUpdate")


class SyncTaskOrderBeanV2(BaseModelV2):
    """Unknown model for the V2 API."""

    # unknown fields
    task_order_by_date: dict[str, Any] = Field(validation_alias="taskOrderByDate")
    task_order_by_priority: dict[str, Any] = Field(
        validation_alias="taskOrderByPriority",
    )
    task_order_by_project: dict[str, Any] = Field(validation_alias="taskOrderByProject")


class SyncOrderBeanV3V2(BaseModelV2):
    """Unknown model for the V2 API."""

    # unknown fields
    order_by_type: dict[str, Any] = Field(validation_alias="orderByType")


class GetBatchV2(BaseModelV2):
    """Model for the response of a batch object status request via the V2 API.

    This model appears to be used like an [entity bean](https://en.wikipedia.org/wiki/Entity_Bean)
    for TickTick apps to take advantage of. It keeps track of the state of the user's
    projects, tasks, etc. We do not have a complete understanding of the structure of
    this model, nor do we have an understanding of how to use this model to
    publish changes to the user's account. This model is currently intended for
    reading the user's state.
    """

    # known fields
    inbox_id: str = Field(
        validation_alias="inboxId",
        description="ID of the inbox project, a special kind of project",
    )
    project_groups: list[ProjectGroupV2] | None = Field(
        validation_alias="projectGroups",
        description="List of all active project groups",
    )
    project_profiles: list[ProjectV2] = Field(
        validation_alias="projectProfiles",
        description="List of all active projects, excluding the inbox",
    )
    sync_task_bean: SyncTaskBeanV2 = Field(
        validation_alias="syncTaskBean",
        description="List of all active tasks",
    )
    tags: list[TagV2] = Field(description="List of all task tags")

    # unknown fields
    check_point: int = Field(validation_alias="checkPoint")
    checks: None
    filters: list[dict[str, Any]] | None
    sync_order_bean: dict[str, Any] = Field(validation_alias="syncOrderBean")
    sync_order_bean_v3: SyncOrderBeanV3V2 = Field(validation_alias="syncOrderBeanV3")
    sync_task_order_bean: SyncTaskOrderBeanV2 = Field(
        validation_alias="syncTaskOrderBean",
    )
    remind_changes: list[Any] = Field(validation_alias="remindChanges")
