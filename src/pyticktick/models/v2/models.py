"""Pydantic models for the general TickTick objects of the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from pyticktick.models.pydantic import Color
from pyticktick.models.v2.types import (
    ETag,
    ICalTrigger,
    InboxId,
    Kind,
    ObjectId,
    Priority,
    Progress,
    RepeatFrom,
    SortOptions,
    Status,
    TagLabel,
    TagName,
    TimeZoneName,
    TTRRule,
)


class BaseModelV2(BaseModel):
    """Base model for all pydantic models of the TickTick V2 API.

    This model is used to provide a common configuration for all models in the V2 API.

    It sets the `extra` configuration to `forbid`, which means that extra data is not
    permitted in the model, and a `pydantic.ValidationError` will be raised if this is
    the case. See [`pydantic.config.ConfigDict.extra`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra)
    for more information.

    It also sets both [`validate_by_name`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_by_name)
    and [`validate_by_alias`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_by_alias)
    to `True`, which means that field names will be validated by their name _or_ alias.
    This is useful for compatibility with the V2 API, while still allowing for
    instantiation in Python with field names.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )

    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        """Convert empty strings to None.

        TickTick API responses sometimes conflates `None` and empty strings for
        optional fields. This validator ensures that empty strings are converted to
        `None`, which then allows for more consistent handling of the data within the
        library.

        Args:
            v (Any): The value to validate.

        Returns:
            Any: The input value if it is not an empty string, otherwise `None`.
        """
        if isinstance(v, str) and len(v) == 0:
            return None
        return v


class SortOptionV2(BaseModelV2):
    """Model for the sort options of tasks within a project in the V2 API."""

    # known fields
    group_by: SortOptions = Field(
        validation_alias="groupBy",
        description="How tasks are grouped within a project",
    )
    order_by: SortOptions = Field(
        validation_alias="orderBy",
        description="How tasks are ordered within a project",
    )


class ProjectTimelineV2(BaseModelV2):
    """Unknown model for the V2 API."""

    # unknown fields
    range: str | None
    sort_type: str | None = Field(validation_alias="sortType")
    sort_option: SortOptionV2 = Field(validation_alias="sortOption")


class ProjectV2(BaseModelV2):
    """Model for all the details of a project taken from the V2 API.

    This model is used to represent a single project in TickTick. It contains all the
    relevant details, such as name, color, sort order, etc. that you see in the web app.
    """

    # known fields
    color: Color | None = Field(
        default=None,
        description="Color of the project profile, eg. '#F18181'",
    )
    etag: ETag = Field(description="ETag of the project object")
    group_id: ObjectId | None = Field(
        validation_alias="groupId",
        description="ID of the project group the project is in",
    )
    id: Union[InboxId, ObjectId] = Field(description="ID of the project")
    in_all: bool = Field(
        validation_alias="inAll",
        description="Whether or not to show in Smart Lists. If False, tasks within this list won't be shown in 'All', 'Today', 'Tomorrow', 'Next 7 Days', or other smart lists, but you will still receive reminders.",
    )
    kind: Literal["TASK", "NOTE"] | None = Field(
        default=None,
        description='"TASK" or "NOTE"',
    )
    modified_time: datetime = Field(
        validation_alias="modifiedTime",
        description="Last modified time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    name: str = Field(description="Name of the project")
    sort_option: SortOptionV2 | None = Field(
        validation_alias="sortOption",
        description="How to sort the tasks in the project",
    )
    view_mode: Literal["list", "kanban", "timeline"] | None = Field(
        default=None,
        validation_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )

    # unknown fields
    barcode_need_audit: bool = Field(validation_alias="barcodeNeedAudit")
    is_owner: bool = Field(validation_alias="isOwner")
    sort_order: int = Field(validation_alias="sortOrder")
    sort_type: str | None = Field(validation_alias="sortType")
    user_count: int = Field(validation_alias="userCount")
    closed: Any
    muted: bool
    transferred: Any
    notification_options: Any = Field(validation_alias="notificationOptions")
    team_id: Any = Field(validation_alias="teamId")
    permission: Any
    timeline: ProjectTimelineV2 | None
    need_audit: bool = Field(validation_alias="needAudit")
    open_to_team: bool | None = Field(validation_alias="openToTeam")
    team_member_permission: Any = Field(validation_alias="teamMemberPermission")
    source: int
    show_type: int | None = Field(validation_alias="showType")
    reminder_type: int | None = Field(validation_alias="reminderType")


class ProjectGroupV2(BaseModelV2):
    """Model for a project group in the V2 API.

    This model is used to represent a group of projects in TickTick. It contains all the
    relevant details, such as name, color, sort order, etc. that you see in the web app.
    """

    # known fields
    etag: ETag = Field(description="ETag of the project group object")
    id: ObjectId = Field(description="ID of the project group")
    name: str = Field(description="Name of the project group")
    sort_option: SortOptionV2 | None = Field(
        validation_alias="sortOption",
        description="How to sort the tasks in the project",
    )
    view_mode: Literal["list", "kanban", "timeline"] | None = Field(
        default=None,
        validation_alias="viewMode",
        description='view mode, "list", "kanban", "timeline"',
    )

    # unknown fields
    deleted: int
    show_all: bool = Field(validation_alias="showAll")
    sort_order: int = Field(validation_alias="sortOrder")
    sort_type: str = Field(validation_alias="sortType")
    team_id: Any = Field(validation_alias="teamId")
    timeline: ProjectTimelineV2 | None
    user_id: int = Field(validation_alias="userId")


class TagV2(BaseModelV2):
    """Model for a tag in the V2 API.

    This model is used to represent a tag in TickTick. Tags are used to categorize tasks
    and make them easier to find. They can be assigned a color and a sort order.

    They do not have a unique ID, but they can be identified by their raw name.
    """

    # known fields
    color: Color | None = Field(
        default=None,
        description="Color of the tag, eg. '#F18181'",
    )
    etag: ETag = Field(description="ETag of the tag object")
    label: TagLabel = Field(description="Name of the tag, as it appears in the UI")
    name: TagName = Field(
        description="Name of the tag, similar to the label but lowercase, and not visible in the UI",
    )
    parent: TagName | None = Field(
        default=None,
        description="Name of the parent tag, if nested.",
    )
    raw_name: TagName = Field(
        validation_alias="rawName",
        description="Original name of the tag, used to identify it",
    )
    sort_option: SortOptionV2 | None = Field(
        default=None,
        validation_alias="sortOption",
        description="How to sort the tasks within the tag",
    )
    sort_type: Literal["project", "title", "tag"] = Field(
        default="project",
        validation_alias="sortType",
        description="Sort type when displaying by selected tag",
    )

    # unknown fields
    sort_order: int = Field(validation_alias="sortOrder")
    timeline: ProjectTimelineV2 | None = None
    type: int


class TaskReminderV2(BaseModelV2):
    """Model for a reminder for a task via the V2 API."""

    id: ObjectId | None = Field(default=None, description="Reminder ID")
    trigger: ICalTrigger = Field(description="Reminder trigger")


class ItemV2(BaseModelV2):
    """Model for a checklist item via the V2 API."""

    completed_time: str | None = Field(
        default=None,
        validation_alias="completedTime",
        description="Completed time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    id: ObjectId = Field(description="ID of the checklist item")
    is_all_day: bool | None = Field(
        default=None,
        validation_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    sort_order: int | None = Field(
        default=None,
        validation_alias="sortOrder",
        description="The order of checklist item",
    )
    start_date: str | None = Field(
        default=None,
        validation_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status | None = Field(
        default=None,
        description="The completion status of checklist item",
    )
    time_zone: TimeZoneName | None = Field(
        default=None,
        validation_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )
    title: str | None = Field(default=None, description="Checklist item title")

    snooze_reminder_time: Any = Field(
        default=None,
        validation_alias="snoozeReminderTime",
    )


class TaskV2(BaseModelV2):
    """Model for a task in a batch response via the V2 API."""

    child_ids: list[ObjectId] | None = Field(
        default=None,
        validation_alias="childIds",
        description="List of sub-task IDs",
    )
    completed_time: datetime | None = Field(
        default=None,
        validation_alias="completedTime",
        description="Completed time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    content: str | None = Field(
        default=None,
        description="Content of the task, used for `TEXT` or `NOTE` tasks, otherwise `desc` is used",
    )
    created_time: datetime | None = Field(
        default=None,
        validation_alias="createdTime",
        description="Created time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    desc: str | None = Field(
        default=None,
        description="Description of the task, used for `CHECKLIST` tasks, otherwise `content` is used",
    )
    due_date: datetime | None = Field(
        default=None,
        validation_alias="dueDate",
        description="Due date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    etag: ETag = Field(description="ETag of the task object")
    id: ObjectId = Field(description="ID of the task")
    is_all_day: bool | None = Field(
        default=None,
        validation_alias="isAllDay",
        description="The task is due any time on the due date, rather than at a specific time",
    )
    is_floating: bool = Field(
        validation_alias="isFloating",
        description="The task will remain at the same time regardless of time zone",
    )
    items: list[ItemV2] = Field(description="List of checklist items")
    kind: Kind = Field(
        default="TEXT",
        description='"TEXT", "NOTE", or "CHECKLIST"',
    )
    modified_time: datetime = Field(
        validation_alias="modifiedTime",
        description="Last modified time in `YYYY-MM-DD'T'HH:MM:SS.sss'+'hhmm` format",
    )
    parent_id: ObjectId | None = Field(
        default=None,
        validation_alias="parentId",
        description="ID of the parent task, if this is a subtask",
    )
    priority: Priority = Field(description="Priority of the task")
    progress: Progress | None = Field(
        default=None,
        description="Progress of a `CHECKLIST` task, should be a number between 0 and 100",
    )
    project_id: Union[InboxId, ObjectId] = Field(
        validation_alias="projectId",
        description="ID of the project the task is in",
    )
    reminder: ICalTrigger | None = Field(
        default=None,
        description="Unclear what this is, but it can sometimes be one of the reminder triggers in `reminders`",
    )
    reminders: list[TaskReminderV2] | None = Field(
        default=None,
        description="List of reminders for the task",
    )
    repeat_first_date: datetime | None = Field(
        default=None,
        validation_alias="repeatFirstDate",
        description="First date of the repeating task in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    repeat_flag: TTRRule | None = Field(
        default=None,
        validation_alias="repeatFlag",
        description="Recurring rules of task",
    )
    repeat_from: RepeatFrom | None = Field(
        default=None,
        validation_alias="repeatFrom",
        description="When to start repeating the task",
    )
    repeat_task_id: ObjectId | None = Field(
        default=None,
        validation_alias="repeatTaskId",
        description="ID of the repeating task if a duplicate is somehow (re)opened",
    )
    start_date: datetime | None = Field(
        default=None,
        validation_alias="startDate",
        description="Start date and time in `yyyy-MM-dd'T'HH:mm:ssZ` format",
    )
    status: Status = Field(description="Status of the task")
    tags: list[TagName] = Field(
        default=[],
        description="List of tag names for the task",
    )
    title: str | None = Field(description="Title of the task")
    time_zone: TimeZoneName | None = Field(
        default=None,
        validation_alias="timeZone",
        description="IANA time zone. Example: 'America/Los_Angeles'",
    )

    # unknown fields
    assignee: Any | None = None
    attachments: list[Any] = []
    annoying_alert: int | None = Field(
        default=None,
        validation_alias="annoyingAlert",
    )
    column_id: ObjectId | None = Field(default=None, validation_alias="columnId")
    comment_count: int | None = Field(default=None, validation_alias="commentCount")
    completed_user_id: int | None = Field(
        default=None,
        validation_alias="completedUserId",
    )
    creator: int
    deleted: int
    ex_date: list[Any] | None = Field(default=None, validation_alias="exDate")
    focus_summaries: list[Any] = Field(default=[], validation_alias="focusSummaries")
    img_mode: int | None = Field(default=None, validation_alias="imgMode")
    is_dirty: bool | None = Field(default=None, validation_alias="isDirty")
    local: bool | None = None
    remind_time: datetime | None = Field(default=None, validation_alias="remindTime")
    sort_order: int = Field(validation_alias="sortOrder")
