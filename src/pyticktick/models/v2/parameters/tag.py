"""Parameters for creating and update tags via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from pyticktick.models.pydantic import Color
from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import TagLabel, TagName


class CreateTagV2(BaseModelV2):
    """Model for creating a tag via the V2 API.

    This model is used to create a tag via the V2 API. This is not currently documented
    or supported in the official API docs. This is used in the `PostBatchTagV2` model.
    """

    # required fields
    label: TagLabel = Field(description="Name of the tag to create")

    # optional fields
    color: Color | None = Field(
        default=None,
        description="Color of the tag, eg. '#F18181'",
    )
    name: TagName | None = Field(
        default=None,
        description="Name of the tag to create",
    )
    parent: str | None = Field(default=None, description="Name of the parent tag")
    sort_type: Literal["project", "title", "tag"] = Field(
        default="project",
        serialization_alias="sortType",
        description="Sort type when displaying by selected tag",
    )

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")

    @model_validator(mode="after")
    def _validate_name(self) -> CreateTagV2:
        if self.name is None:
            self.name = self.label
        self.name = self.name.lower()
        return self


class UpdateTagV2(BaseModelV2):
    """Model for updating a tag via the V2 API.

    This model is used to update a tag via the V2 API. This is not currently documented
    or supported in the official API docs. This is used in the `PostBatchTagV2` model.
    """

    # required fields
    label: TagLabel = Field(description="Name of the tag to update")

    # optional fields
    color: Color | None = Field(
        default=None,
        description="Color of the tag, eg. '#F18181'",
    )
    name: TagName | None = Field(
        default=None,
        description="Stand-in for the identifier of the tag, by default will be the tag label, but lowercase, it is recommended to not specify this field",
    )
    parent: str | None = Field(default=None, description="Name of the parent tag")
    raw_name: TagName | None = Field(
        default=None,
        serialization_alias="rawName",
        description="Original name of the tag, used to identify it",
    )
    sort_type: Literal["project", "title", "tag"] = Field(
        default="project",
        serialization_alias="sortType",
        description="Sort type when displaying by selected tag",
    )

    # unknown fields
    sort_order: int | None = Field(default=None, serialization_alias="sortOrder")

    @model_validator(mode="after")
    def _validate_name(self) -> UpdateTagV2:
        if self.name is None:
            self.name = self.label
        if self.raw_name is None:
            self.raw_name = self.label
        self.name = self.name.lower()
        self.raw_name = self.raw_name.lower()
        return self


class PostBatchTagV2(BaseModelV2):
    """Model for batch tag operations via the V2 API.

    This model is used to batch create, and update tags in bulk against the V2 API
    endpoint `POST /batch/tag`.

    !!! note
        While batch operations usually support adding, updating, and deleting, this
        endpoint only supports adding and updating tags. Deleting tags supported
        separately.
    """

    # optional fields
    add: list[CreateTagV2] = Field(default=[], description="List of tags to add")
    update: list[UpdateTagV2] = Field(default=[], description="List of tags to update")


class RenameTagV2(BaseModelV2):
    """Model for renaming a tag via the V2 API.

    This model is used to rename a tag via the V2 API endpoint `PUT /tag/rename`. This
    is not currently documented or supported in the official API docs.
    """

    # required fields
    name: TagName = Field(description="Identifier of the tag to rename")
    new_name: TagLabel = Field(
        description="New name for the tag",
        serialization_alias="newName",
    )


class DeleteTagV2(BaseModelV2):
    """Model for deleting a tag via the V2 API.

    This model is used to delete a tag against the V2 API endpoint `DELETE /tag`. This
    is not currently documented or supported in the official API docs.
    """

    # required fields
    name: str = Field(description="Identifier of the tag to delete")
