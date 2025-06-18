"""Parameters for creating and updating tasks via the V1 API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CreateItemV1(BaseModel):
    """Model for creating a checklist item via the V1 API.

    This model is used to create a checklist item via the V1 API. It directly maps to
    the 'items' field in the [create task](https://developer.ticktick.com/docs#/openapi?id=create-task)
    documentation. It is used in the `CreateTaskV1` model.
    """

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, description="Subtask title")
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="All day",
    )
    sort_order: int | None = Field(
        default=None,
        serialization_alias="sortOrder",
        description="The order of checklist item",
    )
    time_zone: str | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="The time zone in which the Start time is specified",
    )
    status: bool | None = Field(
        default=None,
        description="The completion status of checklist item",
    )
    completed_time: str | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )


class CreateTaskV1(BaseModel):
    """Model for creating a task via the V1 API.

    This model is used to create a task via the V1 API. It directly maps to the
    [create task](https://developer.ticktick.com/docs#/openapi?id=create-task)
    documentation in the API docs.
    """

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, description="Task id")
    title: str = Field(description="Task title")
    project_id: str = Field(
        serialization_alias="projectId",
        description="Task project id. (Note: This is missing in the API docs)",
    )
    content: str | None = Field(default=None, description="Task content")
    desc: str | None = Field(
        default=None,
        description="Task description of checklist",
    )
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="All day",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    due_date: str | None = Field(
        default=None,
        serialization_alias="dueDate",
        description="Due date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    time_zone: str | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="The time zone in which the time is specified",
    )
    reminders: list[str] | None = Field(
        default=None,
        description="Lists of reminders specific to the task",
    )
    repeat_flag: str | None = Field(
        default=None,
        serialization_alias="repeatFlag",
        description="Recurring rules of task",
    )
    priority: Literal[0, 1, 3, 5] | None = Field(
        default=None,
        description="The priority of task, default is '0'",
    )
    sort_order: int | None = Field(
        default=None,
        serialization_alias="sortOrder",
        description="The order of task",
    )
    items: list[CreateItemV1] | None = Field(
        default=None,
        description="The list of checklist items to create",
    )


class UpdateItemV1(BaseModel):
    """Model for updating a checklist item via the V1 API.

    This model is used to update a checklist item via the V1 API. It directly maps to
    the 'items' field in the [update task](https://developer.ticktick.com/docs#/openapi?id=update-task)
    documentation. It is used in the `UpdateTaskV1` model.
    """

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, description="Subtask title")
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="All day",
    )
    sort_order: int | None = Field(
        default=None,
        serialization_alias="sortOrder",
        description="The order of checklist item",
    )
    time_zone: str | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="The time zone in which the Start time is specified",
    )
    status: bool | None = Field(
        default=None,
        description="The completion status of checklist item",
    )
    completed_time: str | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )


class UpdateTaskV1(BaseModel):
    """Model for updating a task via the V1 API.

    This model is used to updating a task via the V1 API. It directly maps to the
    [update task](https://developer.ticktick.com/docs#/openapi?id=update-task)
    documentation in the API docs.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Task id")
    project_id: str = Field(
        serialization_alias="projectId",
        description="Task project id",
    )
    title: str | None = Field(default=None, description="Task title")
    content: str | None = Field(default=None, description="Task content")
    desc: str | None = Field(
        default=None,
        description="Task description of checklist",
    )
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="All day",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    due_date: str | None = Field(
        default=None,
        serialization_alias="dueDate",
        description="Due date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    time_zone: str | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="The time zone in which the time is specified",
    )
    reminders: list[str] | None = Field(
        default=None,
        description="Lists of reminders specific to the task",
    )
    repeat_flag: str | None = Field(
        default=None,
        serialization_alias="repeatFlag",
        description="Recurring rules of task",
    )
    priority: Literal[0, 1, 3, 5] | None = Field(
        default=None,
        description="The priority of task, default is '0'",
    )
    sort_order: int | None = Field(
        default=None,
        serialization_alias="sortOrder",
        description="The order of task",
    )
    items: list[UpdateItemV1] | None = Field(
        default=None,
        description="The list of checklist items to update",
    )
