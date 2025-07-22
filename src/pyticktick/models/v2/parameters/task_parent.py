"""Parameters for setting and unsetting parent tasks via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from typing import Union

from pydantic import Field, RootModel

from pyticktick.models.v2.models import BaseModelV2


class SetTaskParentV2(BaseModelV2):
    """Model for setting a parent task via the V2 API.

    This model is used to set a parent task via the V2 API. This is not currently
    documented or supported in the official API docs. This is used as the payload in the
    `POST /batch/taskParent` endpoint.
    """

    # required fields
    parent_id: str = Field(
        description="ID of the task to set as the parent",
        serialization_alias="parentId",
    )
    project_id: str = Field(
        description="ID of the project for both tasks",
        serialization_alias="projectId",
    )
    task_id: str = Field(
        description="ID of the task to set the parent for",
        serialization_alias="taskId",
    )


class UnSetTaskParentV2(BaseModelV2):
    """Model for unsetting a parent task via the V2 API.

    This model is used to unset a parent task via the V2 API. This is not currently
    documented or supported in the official API docs. This is used as the payload in the
    `POST /batch/taskParent` endpoint.
    """

    # required fields
    old_parent_id: str = Field(
        description="ID of the task to unset as the parent",
        serialization_alias="oldParentId",
    )
    project_id: str = Field(
        description="ID of the project for both tasks",
        serialization_alias="projectId",
    )
    task_id: str = Field(
        description="ID of the task to unset the parent for",
        serialization_alias="taskId",
    )


class PostBatchTaskParentV2(RootModel[list[Union[SetTaskParentV2, UnSetTaskParentV2]]]):
    """Model for setting and unsetting parent tasks via the V2 API.

    This model is used to set and unset parent tasks via the V2 API. This is not
    currently documented or supported in the official API docs. This is used as the
    payload in the `POST /batch/taskParent` endpoint. It can contain a list of both
    `SetTaskParentV2` and `UnSetTaskParentV2` models. The API will process the list
    and set or unset the parent tasks as needed.
    """

    # required fields
    root: list[Union[SetTaskParentV2, UnSetTaskParentV2]] = Field(
        description="List of task parent operations",
    )
