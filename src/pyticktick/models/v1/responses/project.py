"""Response models for project related endpoints in TickTick API v1."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from pyticktick.models.v1.responses.task import TaskV1


class ProjectV1(BaseModel):
    """Model for a response with high-level project information in the V1 API.

    This model is used to represent a project in the V1 API. It is used in a few
    different endpoints, including `GET /project`, `GET /project/{project_id}`,
    `POST /project`, and `POST /project/{project_id}`. It maps directly to the [project](https://developer.ticktick.com/docs#/openapi?id=project-1)
    definition in the V1 API docs.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Project identifier")
    name: str = Field(description="Project name")
    color: Optional[str] = Field(default=None, description="Project color, eg. #F18181")
    sort_order: int = Field(
        validation_alias="sortOrder",
        description="Order value",
    )
    closed: Optional[bool] = Field(default=None, description="Project closed")
    group_id: Optional[str] = Field(
        default=None,
        validation_alias="groupId",
        description="Project group identifier",
    )
    view_mode: Optional[Literal["list", "kanban", "timeline"]] = Field(
        default=None,
        validation_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )
    permission: Optional[Literal["read", "write", "comment"]] = Field(
        default=None,
        description='"read", "write" or "comment"',
    )
    kind: Optional[Literal["TASK", "NOTE"]] = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )


class ColumnV1(BaseModel):
    """Model for a response with column information in the V1 API.

    This model is used to represent a column in the V1 API. It is used in the
    `ProjectDataV1` model to represent columns under a project. It maps directly to the
    [column](https://developer.ticktick.com/docs#/openapi?id=column) definition in the
    V1 API docs.

    It is useful for Kanban views of tasks.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Column identifier")
    project_id: str = Field(
        validation_alias="projectId",
        description="Project identifier",
    )
    name: str = Field(description="Column name")
    sort_order: int = Field(
        validation_alias="sortOrder",
        description="Order value",
    )


class ProjectDataV1(BaseModel):
    """Model for a response with more detailed project information in the V1 API.

    This model is used to represent a project in the V1 API with more detailed
    information. It includes the project itself, the tasks under the project, and the
    columns, if any. It is used in the `GET /project/{project_id}/data` endpoint. It
    maps directly to the [project data](https://developer.ticktick.com/docs#/openapi?id=projectdata)
    definition in the V1 API docs.
    """

    model_config = ConfigDict(extra="ignore")

    project: ProjectV1 = Field(description="Project info")
    tasks: list[TaskV1] = Field(description="Undone tasks under project")
    columns: list[ColumnV1] = Field(description="Columns under project")
