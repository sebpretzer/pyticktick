"""Response models for task related endpoints in TickTick API v1."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ItemV1(BaseModel):
    """Model for a response with checklist item information in the V1 API.

    This model is used to represent a checklist item in the V1 API. It is used in the
    `TaskRespV1` model to represent checklist items of a task. It maps directly to the [checklistitem](https://developer.ticktick.com/docs#/openapi?id=checklistitem)
    definition in the V1 API docs.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Subtask identifier")
    title: str = Field(description="Subtask title")
    status: bool = Field(
        description="The completion status of checklist item. Normal: 0, Completed: 1",
    )
    completed_time: str | None = Field(
        default=None,
        validation_alias="completedTime",
        description="Subtask completed time in `yyyy-MM-dd'T'HH:mm:ssZ`",
    )
    is_all_day: bool = Field(
        validation_alias="isAllDay",
        description="All day",
    )
    sort_order: int = Field(
        validation_alias="sortOrder",
        description="Subtask sort order",
    )
    start_date: str | None = Field(
        default=None,
        validation_alias="startDate",
        description="Subtask start date time in `yyyy-MM-dd'T'HH:mm:ssZ`",
    )
    time_zone: str = Field(
        validation_alias="timeZone",
        description="Subtask timezone. Example: 'America/Los_Angeles'",
    )

    @field_validator("status", mode="before")
    @classmethod
    def _status_from_int(cls, v: int) -> bool:
        if v == 0:
            return False
        if v == 1:
            return True
        msg = "Invalid `status`, expected 0 or 1"
        raise ValueError(msg)


class TaskRespV1(BaseModel):
    """Model for a response with task information in the V1 API.

    This model is used to represent a task in the V1 API. It is used in a few different
    endpoints, including `GET /project/{project_id}/task/{task_id}`, `POST /task`, and
    `POST /task/{task_id}`. It maps directly to the [task](https://developer.ticktick.com/docs#/openapi?id=task-1)
    definition in the V1 API docs.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Project identifier")
    project_id: str = Field(
        validation_alias="projectId",
        description="Task project id",
    )
    title: str = Field(description="Task title")
    is_all_day: bool = Field(
        validation_alias="isAllDay",
        description="All day",
    )
    completed_time: str | None = Field(
        default=None,
        validation_alias="completedTime",
        description="Task completed time in `yyyy-MM-dd'T'HH:mm:ssZ`",
    )
    content: str | None = Field(default=None, description="Task content")
    desc: str | None = Field(
        default=None,
        description="Task description of checklist",
    )
    due_date: str | None = Field(
        default=None,
        validation_alias="dueDate",
        description="Task due date time in `yyyy-MM-dd'T'HH:mm:ssZ`",
    )
    items: list[ItemV1] | None = Field(
        default=None,
        description="Subtasks of Task",
    )
    priority: Literal[0, 1, 3, 5] = Field(
        description="Task priority. None:0, Low:1, Medium:3, High:5",
    )
    reminders: list[str] | None = Field(
        default=None,
        description="List of reminder triggers. Example: ['TRIGGER:P0DT9H0M0S', 'TRIGGER:PT0S']",
    )
    repeat_flag: str | None = Field(
        default=None,
        validation_alias="repeatFlag",
        description="Recurring rules of task. Example: 'RRULE:FREQ=DAILY;INTERVAL=1'",
    )
    sort_order: int = Field(
        validation_alias="sortOrder",
        description="Task sort order",
    )
    start_date: str | None = Field(
        default=None,
        validation_alias="startDate",
        description="Start date time in `yyyy-MM-dd'T'HH:mm:ssZ`",
    )
    status: bool = Field(
        description="Task completion status. Normal: 0, Completed: 2",
    )
    time_zone: str = Field(
        validation_alias="timeZone",
        description="Task timezone. Example: 'America/Los_Angeles'",
    )

    @field_validator("status", mode="before")
    @classmethod
    def _status_from_int(cls, v: int) -> bool:
        if v == 0:
            return False
        if v == 2:  # noqa: PLR2004
            return True
        msg = "Invalid `status`, expected 0 or 2"
        raise ValueError(msg)
