"""Parameters for creating and updating project groups via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import ObjectId


class CreateProjectGroupV2(BaseModelV2):
    """Model for creating a project group via the V2 API.

    This model is used to create a project group via the V2 API. This is not currently
    documented or supported in the official API docs. This is used in the
    `PostBatchProjectGroupV2` model.
    """

    # required fields
    name: str = Field(description="Name of the project group to create")

    # optional fields
    id: ObjectId | None = Field(
        default=None,
        description="ID of the project group to create",
    )
    list_type: Literal["group"] = Field(
        default="group",
        serialization_alias="listType",
        description="Fixed value 'group'",
    )


class UpdateProjectGroupV2(BaseModelV2):
    """Model for updating a project group via the V2 API.

    This model is used to update a project group via the V2 API. This is not currently
    documented or supported in the official API docs. This is used in the
    `PostBatchProjectGroupV2` model.
    """

    # required fields
    name: str = Field(description="Name of the project group to update")
    id: ObjectId = Field(description="ID of the project group to update")

    list_type: Literal["group"] = Field(
        default="group",
        serialization_alias="listType",
        description="Fixed value 'group'",
    )


class PostBatchProjectGroupV2(BaseModelV2):
    """Model for batch project group operations via the V2 API.

    This model is used to batch create, update, and delete project groups in bulk
    against the V2 API endpoint `POST /batch/projectGroup`.
    """

    # required fields
    add: list[CreateProjectGroupV2] = Field(
        default=[],
        description="List of project groups to add",
    )
    delete: list[ObjectId] = Field(
        default=[],
        description="List of project group IDs to delete",
    )
    update: list[UpdateProjectGroupV2] = Field(
        default=[],
        description="List of project groups to update",
    )
