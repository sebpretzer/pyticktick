from pyticktick.models.v2 import BaseModelV2, TagV2


def test_inherited_models_are_strict():
    base = BaseModelV2()
    assert base.model_config.get("extra") == "forbid"

    tag = TagV2(
        etag="abcd1234",
        label="TestTag",
        name="test_tag",
        raw_name="test_tag",
        sort_order=1,
        type=1,
    )
    assert tag.model_config.get("extra") == "forbid"
