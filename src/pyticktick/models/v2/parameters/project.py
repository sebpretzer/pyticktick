"""Parameters for creating and updating projects via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import Field

from pyticktick.models.pydantic import Color
from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import ObjectId


class CreateProjectV2(BaseModelV2):
    """Model for creating a project via the V2 API.

    This model is used to create a project via the V2 API. It mostly maps to the
    [create project](https://developer.ticktick.com/docs#/openapi?id=create-project)
    documentation in the API docs. The main differences are the addition of the `id`
    and `group_id` fields. This is used in the `PostBatchProjectV2` model.
    """

    # required fields
    name: str = Field(description="name of the project")

    # optional fields
    color: Color | None = Field(
        default=None,
        description="color of project, eg. '#F18181'",
    )
    group_id: ObjectId | None = Field(
        default=None,
        description="ID of the project group to add the project to",
        serialization_alias="groupId",
    )
    id: ObjectId | None = Field(
        default=None,
        description="ID of the project to create",
    )
    kind: Literal["TASK", "NOTE"] | None = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )
    view_mode: Literal["list", "kanban", "timeline"] | None = Field(
        default=None,
        serialization_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")


class UpdateProjectV2(BaseModelV2):
    """Model for updating a project via the V2 API.

    This model is used to update a project via the V2 API. It mostly maps to the
    [update project](https://developer.ticktick.com/docs#/openapi?id=update-project)
    documentation in the API docs. The main differences are the addition of the `id`
    and `group_id` fields. This is used in the `PostBatchProjectV2` model.
    """

    # required fields
    id: ObjectId = Field(description="ID of the project to update")
    name: str = Field(description="name of the project, must be set even on update")

    # optional fields
    color: Color | None = Field(
        default=None,
        description="color of project, eg. '#F18181'",
    )
    group_id: Union[Literal["NONE"], None, ObjectId] = Field(
        default=None,
        description='ID of the project group to move the project to, `"NONE"` to actively be ungrouped, `None` to be set to the group it was in before',
        serialization_alias="groupId",
    )
    kind: Literal["TASK", "NOTE"] | None = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )
    view_mode: Literal["list", "kanban", "timeline"] | None = Field(
        default=None,
        serialization_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")


class PostBatchProjectV2(BaseModelV2):
    """Model for batch project operations via the V2 API.

    This model is used to create, update, and delete projects in bulk against the V2 API
    endpoint `POST /batch/project`.
    """

    # optional fields
    add: list[CreateProjectV2] = Field(
        default=[],
        description="List of projects to add",
    )
    delete: list[ObjectId] = Field(
        default=[],
        description="List of project IDs to delete",
    )
    update: list[UpdateProjectV2] = Field(
        default=[],
        description="List of projects to update",
    )
