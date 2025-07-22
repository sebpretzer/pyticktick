import pytest
from pydantic import ValidationError

from pyticktick.models.v2 import BaseModelV2, TagV2


def test_inherited_models_are_strict():
    base = BaseModelV2()
    assert base.model_config.get("extra") == "forbid"

    data = {
        "etag": "abcd1234",
        "label": "TestTag",
        "name": "test_tag",
        "raw_name": "test_tag",
        "sort_order": 1,
        "type": 1,
    }

    tag = TagV2.model_validate(data)
    assert tag.model_config.get("extra") == "forbid"

    with pytest.raises(ValidationError, match="1 validation error"):
        TagV2.model_validate({**data, "extra_field": "value"})
