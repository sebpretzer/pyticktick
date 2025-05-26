"""Parameters for creating and updating projects via the V1 API."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from pyticktick.models.v2.types import Color


class CreateProjectV1(BaseModel):
    """Model for creating a project via the V1 API.

    This model is used to create a project via the V1 API. It directly maps to the
    [create project](https://developer.ticktick.com/docs#/openapi?id=create-project)
    documentation in the API docs.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="name of the project")
    color: Optional[Color] = Field(
        default=None,
        description="color of project, eg. '#F18181'",
    )
    sort_order: Optional[int] = Field(
        default=None,
        serialization_alias="sortOrder",
        description="sort order value of the project",
    )
    view_mode: Optional[Literal["list", "kanban", "timeline"]] = Field(
        default=None,
        serialization_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )
    kind: Optional[Literal["TASK", "NOTE"]] = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )


class UpdateProjectV1(BaseModel):
    """Model for updating a project via the V1 API.

    This model is used to update a project via the V1 API. It directly maps to the
    [update project](https://developer.ticktick.com/docs#/openapi?id=update-project)
    documentation in the API docs.
    """

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, description="name of the project")
    color: Optional[Color] = Field(
        default=None,
        description="color of project, eg. '#F18181'",
    )
    sort_order: Optional[int] = Field(
        default=None,
        serialization_alias="sortOrder",
        description="sort order value of the project",
    )
    view_mode: Optional[Literal["list", "kanban", "timeline"]] = Field(
        default=None,
        serialization_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )
    kind: Optional[Literal["TASK", "NOTE"]] = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )
