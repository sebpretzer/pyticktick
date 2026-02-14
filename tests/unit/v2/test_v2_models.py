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


@pytest.mark.parametrize(
    ("input_", "expected"),
    [("", None), (None, None), ("test", "test"), (1, 1)],
)
def test_base_model_empty_str_to_none(input_, expected):
    assert BaseModelV2.empty_str_to_none(input_) == expected


def test_override_forbid_extra_message_injector():
    class CustomModel(BaseModelV2):
        field1: str
        field2: int

    valid_data = {"field1": "value", "field2": 10}
    model = CustomModel.model_validate(valid_data)
    assert model.field1 == "value"
    assert model.field2 == 10

    invalid_data = {**valid_data, "extra_field": "not allowed"}
    match_ = r"Extra inputs are not permitted by default for `CustomModel`. Please set `override_forbid_extra` to `True` if you believe the TickTick API has diverged from the model."  # noqa: E501
    with pytest.raises(ValidationError, match=match_):
        CustomModel.model_validate(invalid_data)
