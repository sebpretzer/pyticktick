import json

import pytest
from pydantic import BaseModel

from pyticktick.models.v2 import Color


@pytest.mark.parametrize(
    ("input_", "expected"),
    [
        ("#ff0000", "#ff0000"),
        ("#ffff00", "#ffff00"),
        ("#0000ff", "#0000ff"),
        ("#FF0000", "#ff0000"),
        ("#FFFF00", "#ffff00"),
        ("#0000FF", "#0000ff"),
    ],
)
def test_color(input_, expected):
    color = Color(input_)
    assert str(color) == expected


def test_color_json_serializeable():
    class TestModel(BaseModel):
        color: Color

    color_str = "#ff0000"

    model = TestModel(color=color_str)
    assert isinstance(model.color, Color)

    dict_ = model.model_dump()
    assert isinstance(dict_, dict)
    dict_to_json = json.dumps(dict_)
    assert isinstance(dict_to_json, str)

    json_ = model.model_dump_json()
    assert isinstance(json_, str)
    json_dict = json.loads(json_)
    assert isinstance(json_dict, dict)

    assert json_dict == dict_
    assert dict_to_json.replace(" ", "") == json_.replace(" ", "")
