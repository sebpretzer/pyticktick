"""Response models for project related endpoints in TickTick API v1."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from pyticktick.models.v1.responses.task import TaskRespV1


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
    color: str | None = Field(default=None, description="Project color, eg. #F18181")
    sort_order: int = Field(
        validation_alias="sortOrder",
        description="Order value",
    )
    closed: bool | None = Field(default=None, description="Project closed")
    group_id: str | None = Field(
        default=None,
        validation_alias="groupId",
        description="Project group identifier",
    )
    view_mode: Literal["list", "kanban", "timeline"] | None = Field(
        default=None,
        validation_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )
    permission: Literal["read", "write", "comment"] | None = Field(
        default=None,
        description='"read", "write" or "comment"',
    )
    kind: Literal["TASK", "NOTE"] | None = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )


class ColumnV1(BaseModel):
    """Model for a response with column information in the V1 API.

    This model is used to represent a column in the V1 API. It is used in the
    `ProjectDataRespV1` model to represent columns under a project. It maps directly to
    the [column](https://developer.ticktick.com/docs#/openapi?id=column) definition in
    the V1 API docs.

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


class ProjectRespV1(RootModel[ProjectV1]):
    """Model for a response from the `GET /project/{project_id}` endpoint in the V1 API.

    This model is used to represent a single project in the V1 API. It corresponds to
    the the [`GET /project/{project_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-project-by-id)
    V1 endpoint.
    """

    root: ProjectV1 = Field(description="The project info")


class ProjectsRespV1(RootModel[list[ProjectV1]]):
    """Model for a response from the `GET /project` endpoint in the V1 API.

    This model is used to represent a list of projects in the V1 API. It corresponds to
    the [`GET /project`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-user-project)
    V1 endpoint.
    """

    root: list[ProjectV1] = Field(description="")


class ProjectDataRespV1(BaseModel):
    """Model for a response with more detailed project information in the V1 API.

    This model is used to represent a project in the V1 API with more detailed
    information. It includes the project itself, the tasks under the project, and the
    columns, if any. It is used in the `GET /project/{project_id}/data` endpoint. It
    maps directly to the [project data](https://developer.ticktick.com/docs#/openapi?id=projectdata)
    definition in the V1 API docs.
    """

    model_config = ConfigDict(extra="ignore")

    project: ProjectV1 = Field(description="Project info")
    tasks: list[TaskRespV1] = Field(description="Undone tasks under project")
    columns: list[ColumnV1] = Field(description="Columns under project")
