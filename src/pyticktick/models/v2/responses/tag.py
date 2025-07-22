"""Response for a batch tag `POST` request via the V2 API.

!!! warning "Unofficial API"
    These models are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

from pydantic import Field

from pyticktick.models.v2.models import BaseModelV2
from pyticktick.models.v2.types import ETag, TagName


class BatchTagRespV2(BaseModelV2):
    """Model for the response of a batch tag request via the V2 API.

    Since tags do not have an `id` field, the `id2etag` and `id2error` fields return
    the `name` field as the key instead. Otherwise, the structure is the same as the
    `BatchRespV2` model.
    """

    # known fields
    id2error: dict[TagName, ETag] = Field(
        validation_alias="id2error",
        description="Tag name to error message mapping",
    )
    id2etag: dict[TagName, ETag] = Field(
        validation_alias="id2etag",
        description="Tag name to ETag mapping of objects that were successfully created / updated",
    )

    @property
    def ids(self) -> list[str]:
        """List of all the IDs in the response."""
        return list(self.id2etag)

    @property
    def etags(self) -> list[str]:
        """List of all the ETags in the response."""
        return list(self.id2etag.values())
