"""Parameters for creating and updating tasks via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Union

from pydantic import Field, model_validator

from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import (
    ETag,
    ICalTrigger,
    InboxId,
    Kind,
    ObjectId,
    Priority,
    Progress,
    RepeatFrom,
    Status,
    TagName,
    TimeZoneName,
    TTRRule,
)


class CreateItemV2(BaseModelV2):
    """Model for creating a checklist item via the V2 API.

    This model is used to create a checklist item via the V2 API, but its identical to
    the `CreateItemV1` model. It directly maps to the 'items' field in the [create task](https://developer.ticktick.com/docs#/openapi?id=create-task)
    documentation. It is used in the `CreateTaskV2` model.
    """

    # optional fields
    completed_time: datetime | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    id: ObjectId | None = Field(default=None, description="Checklist item ID")
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status | None = Field(
        default=None,
        description="The completion status of checklist item",
    )
    time_zone: TimeZoneName | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )
    title: str | None = Field(default=None, description="Checklist item title")

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")


class CreateTaskReminderV2(BaseModelV2):
    """Model for creating a reminder for a task via the V2 API."""

    # required fields
    id: ObjectId | None = Field(default=None, description="Reminder ID")
    trigger: ICalTrigger = Field(description="Reminder trigger")


class CreateTaskV2(BaseModelV2):
    """Model for creating a task via the V2 API.

    This model is used to create a task via the V2 API. It mostly maps to the 'items'
    field in the [create task](https://developer.ticktick.com/docs#/openapi?id=create-task)
    documentation. The main differences are the addition of the following fields:

    - `modified_time`
    - `completed_time`
    - `completed_user_id`
    - `tags`
    - `etag`
    - `kind`
    - `status`
    - `is_floating`
    - `creator`
    - `assignee`
    - `progress`

    This is used in the `PostBatchTaskV2` model.
    """

    # required fields
    project_id: Union[InboxId, ObjectId] = Field(
        serialization_alias="projectId",
        description="Task project id. (Note: This is missing in the API docs)",
    )
    title: str = Field(description="Task title")

    # optional fields
    completed_time: datetime | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    content: str | None = Field(
        default=None,
        description="Content of the task, used for `TEXT` or `NOTE` tasks, otherwise `desc` is used",
    )
    desc: str | None = Field(
        default=None,
        description="Description of the task, used for `CHECKLIST` tasks, otherwise `content` is used",
    )
    due_date: datetime | None = Field(
        default=None,
        serialization_alias="dueDate",
        description="Due date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    etag: ETag | None = Field(default=None, description="ETag of the task")
    id: ObjectId | None = Field(default=None, description="Task id")
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    is_floating: bool | None = Field(
        default=None,
        serialization_alias="isFloating",
        description="The task will remain at the same time regardless of time zone",
    )
    items: list[CreateItemV2] | None = Field(
        default=None,
        description="The list of checklist items to create",
    )
    kind: Kind = Field(
        default="TEXT",
        description='"TEXT", "NOTE", or "CHECKLIST"',
    )
    modified_time: datetime | None = Field(
        default=None,
        serialization_alias="modifiedTime",
        description="Last modified time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    reminders: list[CreateTaskReminderV2] | None = Field(
        default=None,
        description="Lists of reminders specific to the task",
    )
    repeat_flag: TTRRule | None = Field(
        default=None,
        serialization_alias="repeatFlag",
        description="Recurring rules of task",
    )
    repeat_from: RepeatFrom | None = Field(
        default=None,
        serialization_alias="repeatFrom",
        description="When to start repeating the task",
    )
    priority: Priority | None = Field(
        default=None,
        description="The priority of task, default is '0'",
    )
    progress: Progress | None = Field(
        default=None,
        description="Progress of a `CHECKLIST` task, should be a number between 0 and 100",
    )
    start_date: datetime | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status | None = Field(default=None, description="Status of the task")
    time_zone: TimeZoneName | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )
    tags: list[TagName] = Field(default=[], description="List of tags to add")

    # unknown fields
    assignee: int | None = None
    completed_user_id: int | None = Field(
        default=None,
        serialization_alias="completedUserId",
    )
    creator: int | None = None
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")

    @model_validator(mode="after")
    def _mutually_exclusive_fields(self) -> CreateTaskV2:
        if self.kind == "CHECKLIST" and self.content is not None:
            msg = "Content is not allowed for checklist tasks"
            raise ValueError(msg)
        if self.kind != "CHECKLIST" and self.desc is not None:
            msg = "Description is not allowed for non-checklist tasks"
            raise ValueError(msg)
        return self


class UpdateItemV2(BaseModelV2):
    """Model for updating a checklist item via the V2 API.

    This model is used to update a checklist item via the V2 API, but its identical to
    the `UpdateItemV1` model. It directly maps to the 'items' field in the [update task](https://developer.ticktick.com/docs#/openapi?id=update-task)
    documentation. It is used in the `UpdateTaskV2` model.
    """

    # required fields
    id: ObjectId = Field(description="Checklist item ID")

    # optional fields
    completed_time: datetime | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status | None = Field(
        default=None,
        description="The completion status of checklist item",
    )
    time_zone: TimeZoneName | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )
    title: str | None = Field(default=None, description="Checklist item title")

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")


class UpdateTaskReminderV2(BaseModelV2):
    """Model for creating a reminder for a task via the V2 API."""

    # required fields
    id: ObjectId = Field(description="Reminder ID")
    trigger: ICalTrigger = Field(description="Reminder trigger")


class UpdateTaskV2(BaseModelV2):
    """Model for updating a task via the V2 API.

    This model is used to update a task via the V2 API. It mostly maps to the 'items'
    field in the [update task](https://developer.ticktick.com/docs#/openapi?id=update-task)
    documentation. The main differences are the addition of the following fields:

    - `modified_time`
    - `completed_time`
    - `completed_user_id`
    - `tags`
    - `etag`
    - `kind`
    - `status`
    - `is_floating`
    - `creator`
    - `assignee`
    - `progress`

    This is used in the `PostBatchTaskV2` model.
    """

    # required fields
    id: ObjectId = Field(description="Task id")
    project_id: Union[InboxId, ObjectId] = Field(
        serialization_alias="projectId",
        description="Task project id",
    )

    # optional fields
    completed_time: datetime | None = Field(
        default=None,
        serialization_alias="completedTime",
        description="Completed time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    content: str | None = Field(
        default=None,
        description="Content of the task, used for `TEXT` or `NOTE` tasks, otherwise `desc` is used",
    )
    desc: str | None = Field(
        default=None,
        description="Description of the task, used for `CHECKLIST` tasks, otherwise `content` is used",
    )
    due_date: datetime | None = Field(
        default=None,
        serialization_alias="dueDate",
        description="Due date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    etag: ETag | None = Field(default=None, description="ETag of the task")
    is_all_day: bool | None = Field(
        default=None,
        serialization_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    is_floating: bool | None = Field(
        default=None,
        serialization_alias="isFloating",
        description="The task will remain at the same time regardless of time zone",
    )
    items: list[UpdateItemV2] | None = Field(
        default=None,
        description="The list of checklist items to update",
    )
    kind: Kind = Field(
        default="TEXT",
        description='"TEXT", "NOTE", or "CHECKLIST"',
    )
    modified_time: datetime | None = Field(
        default=None,
        serialization_alias="modifiedTime",
        description="Last modified time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    repeat_flag: TTRRule | None = Field(
        default=None,
        serialization_alias="repeatFlag",
        description="Recurring rules of task",
    )
    repeat_from: RepeatFrom | None = Field(
        default=None,
        serialization_alias="repeatFrom",
        description="When to start repeating the task",
    )
    reminders: list[UpdateTaskReminderV2] | None = Field(
        default=None,
        description="Lists of reminders specific to the task",
    )
    priority: Priority | None = Field(
        default=None,
        description="The priority of task, default is '0'",
    )
    progress: Progress | None = Field(
        default=None,
        description="Progress of a `CHECKLIST` task, should be a number between 0 and 100",
    )
    start_date: datetime | None = Field(
        default=None,
        serialization_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status | None = Field(default=None, description="Status of the task")
    time_zone: TimeZoneName | None = Field(
        default=None,
        serialization_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )
    tags: list[TagName] = Field(default=[], description="List of tags to update")
    title: str | None = Field(default=None, description="Task title")

    # unknown fields
    assignee: int | None = None
    completed_user_id: int | None = Field(
        default=None,
        serialization_alias="completedUserId",
    )
    creator: int | None = None
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")

    @model_validator(mode="after")
    def _mutually_exclusive_fields(self) -> UpdateTaskV2:
        if self.kind == "CHECKLIST" and self.content is not None:
            msg = "Content is not allowed for checklist tasks"
            raise ValueError(msg)
        if self.kind != "CHECKLIST" and self.desc is not None:
            msg = "Description is not allowed for non-checklist tasks"
            raise ValueError(msg)
        return self


class DeleteTaskV2(BaseModelV2):
    """Model for deleting a task via the V2 API.

    This model is used to delete a task via the V2 API. It mostly maps to the `DELETE
    /project/{project_id}/task/{task_id}` endpoint in the API docs. Since it's used
    in a batch operation, it must be bundled in the `PostBatchTaskV2` model, rather
    than being a direct call to the API.
    """

    # required fields
    project_id: Union[InboxId, ObjectId] = Field(
        description="ID of the project the task belongs to",
        serialization_alias="projectId",
    )
    task_id: str = Field(
        description="ID of the task to delete",
        serialization_alias="taskId",
    )


class PostBatchTaskV2(BaseModelV2):
    """Model for batch task operations via the V2 API.

    This model is used to create, update, and delete tasks in bulk against the V2 API
    endpoint `POST /batch/task`.
    """

    # optional fields
    add: list[CreateTaskV2] = Field(default=[], description="List of tasks to add")
    delete: list[DeleteTaskV2] = Field(
        default=[],
        description="List of task IDs to delete",
    )
    update: list[UpdateTaskV2] = Field(
        default=[],
        description="List of tasks to update",
    )

    # unknown fields`
    add_attachments: list[Any] = Field(default=[], serialization_alias="addAttachments")
    update_attachments: list[Any] = Field(
        default=[],
        serialization_alias="updateAttachments",
    )
