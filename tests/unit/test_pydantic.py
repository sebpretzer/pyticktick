import pytest
from pydantic import ValidationError

from pyticktick.models.v2 import PostBatchTaskV2
from pyticktick.pydantic import update_model_config


def test_update_model_config_nested():
    dict_ = {
        "add": [
            {
                "project_id": "123456789012345678901234",
                "title": "dummy task",
                "kind": "CHECKLIST",
                "items": [{"title": "item 1", "extra_nested_nested_field": "value"}],
                "extra_nested_field": "value",
            },
        ],
        "update": [
            {
                "id": "987654321098765432109876",
                "project_id": "123456789012345678901234",
                "title": "dummy task 2",
                "kind": "TEXT",
                "reminders": [
                    {
                        "id": "102938475610293847568493",
                        "trigger": "RRULE:FREQ=WEEKLY;INTERVAL=1",
                        "extra_extra_nested_field": "value",
                    },
                ],
                "extra_nested_field": "value",
            },
        ],
        "delete": [
            {
                "project_id": "123456789012345678901234",
                "task_id": "123456789012345678901234",
                "extra_nested_field": "value",
            },
        ],
        "extra_field": "value",
    }

    with pytest.raises(ValidationError, match="6 validation errors"):
        PostBatchTaskV2.model_validate(dict_)

    update_model_config(PostBatchTaskV2, extra="allow")

    data = PostBatchTaskV2.model_validate(dict_)
    assert isinstance(data, PostBatchTaskV2)
    assert data.extra_field == "value"  # pyright: ignore[reportAttributeAccessIssue]
    assert data.add[0].extra_nested_field == "value"  # pyright: ignore[reportAttributeAccessIssue]
    assert data.add[0].items[0].extra_nested_nested_field == "value"  # pyright: ignore[reportOptionalSubscript,reportAttributeAccessIssue]
    assert data.update[0].extra_nested_field == "value"  # pyright: ignore[reportAttributeAccessIssue]
    assert data.update[0].reminders[0].extra_extra_nested_field == "value"  # pyright: ignore[reportOptionalSubscript,reportAttributeAccessIssue]
    assert data.delete[0].extra_nested_field == "value"  # pyright: ignore[reportAttributeAccessIssue]
