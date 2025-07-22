"""Response for a batch task parent `POST` request via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from pydantic import Field

from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import ETag, ObjectId


class BatchTaskParentRespValueV2(BaseModelV2):
    """Model for the nested values of a batch task parent response via the V2 API."""

    id: ObjectId
    parent_id: ObjectId | None = Field(default=None, validation_alias="parentId")
    child_ids: list[ObjectId] | None = Field(
        default=None,
        validation_alias="childIds",
    )
    etag: ETag


class BatchTaskParentRespV2(BaseModelV2):
    """Model for the response of a batch task parent request via the V2 API.

    The `id2etag` and `id2error` fields return the `objectId` field as the key like
    the `BatchRespV2` model. Unlike the `BatchRespV2` model, the values provided are
    more complex and informative than just an `ETag`.
    """

    # known fields
    id2error: dict[ObjectId, str] = Field(
        validation_alias="id2error",
        description="Mapping of tasks that failed to be updated",
    )
    id2etag: dict[ObjectId, BatchTaskParentRespValueV2] = Field(
        validation_alias="id2etag",
        description="Mapping of tasks that were successfully updated",
    )

    @property
    def ids(self) -> list[str]:
        """List of all the IDs in the response."""
        return list(self.id2etag)

    @property
    def etags(self) -> list[str]:
        """List of all the ETags in the response."""
        return [v.etag for v in self.id2etag.values()]
