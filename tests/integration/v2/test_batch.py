from datetime import datetime

import pytest
from pydantic import TypeAdapter

from pyticktick.models.v2 import Color, GetBatchV2, TimeZoneName
from pyticktick.models.v2.models import ProjectV2, TaskV2


@pytest.mark.order(3)
@pytest.mark.dependency(
    name="get_batch_v2",
    scope="session",
    depends=[
        "create_project_group_v2",
        "create_project_v2",
        "create_tag_v2",
        "create_task_v2",
        "set_and_unset_task_parent_v2",
    ],
)
def test_get_batch_v2(  # noqa: PLR0912, PLR0915
    generate_object_id,
    delete_project_groups,
    delete_projects,
    delete_tags,
    client,
):
    project_group_data = [
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_GROUP_A",
        },
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_GROUP_B",
        },
    ]

    project_data = [
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_PROJECT_A",
            "group_id": project_group_data[0]["id"],
            "color": "#ff0000",
            "kind": "TASK",
        },
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_PROJECT_B",
            "group_id": project_group_data[0]["id"],
            "color": "rgb(255, 255, 0)",  # #ffff00
            "kind": "NOTE",
        },
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_PROJECT_C",
            "group_id": project_group_data[1]["id"],
            "color": "Blue",  # #0000ff
        },
        {
            "id": generate_object_id(),
            "name": "test_get_batch_v2_PROJECT_D",
        },
    ]

    tag_data = [
        {
            "label": "test_get_batch_v2_TAG_A",
            "name": "test_get_batch_v2_tag_a",  # should be auto-generated normally
            "color": "#ff0000",
        },
        {
            "label": "test_get_batch_v2_TAG_B",
            "name": "test_get_batch_v2_tag_b",  # should be auto-generated normally
            "color": "rgb(255, 255, 0)",  # #ffff00
        },
        {
            "label": "test_get_batch_v2_TAG_C",
            "name": "test_get_batch_v2_tag_c",  # should be auto-generated normally
        },
    ]

    task_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_A",
            "project_id": project_data[0]["id"],
            "tags": [tag_data[0]["name"]],
            "desc": "description for test_get_batch_v2_TASK_A",
            "start_date": "2022-01-01T00:00:00.000Z",
            "due_date": "2022-01-03T00:00:00.000Z",
            "modified_time": "2022-01-01T12:00:00.000Z",
            "time_zone": "Asia/Shanghai",
            "repeat_flag": "RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=SU;BYDAY=MO,TU,WE,TH,FR",
            "priority": 1,
            "sort_order": 0,
            "status": 0,
            "is_all_day": False,
            "is_floating": False,
            "kind": "CHECKLIST",
            "items": [
                {
                    "id": generate_object_id(),
                    "title": "test_get_batch_v2_task_A_ITEM_A",
                    "is_all_day": False,
                    "sort_order": 0,
                    "time_zone": "America/New_York",
                    "status": 0,
                },
                {
                    "id": generate_object_id(),
                    "title": "test_get_batch_v2_task_A_ITEM_B",
                    "is_all_day": True,
                    "sort_order": 1,
                    "time_zone": "America/Chicago",
                    "status": 1,
                },
            ],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_B",
            "project_id": project_data[1]["id"],
            "tags": [tag_data[0]["name"], tag_data[1]["name"]],
            "content": "content for test_get_batch_v2_TASK_B",
            "start_date": "2022-01-02T00:00:00.000Z",
            "due_date": "2022-01-04T00:00:00.000Z",
            "modified_time": "2022-01-02T12:00:00.000Z",
            "time_zone": "Africa/Abidjan",
            "repeat_flag": "RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND",
            "priority": 3,
            "sort_order": 1,
            "status": 0,
            "is_all_day": True,
            "is_floating": True,
            "kind": "NOTE",
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_C",
            "project_id": project_data[2]["id"],
            "tags": [tag_data[0]["name"], tag_data[1]["name"], tag_data[2]["name"]],
            "content": "content for test_get_batch_v2_TASK_C",
            "start_date": "2022-01-03T00:00:00.000Z",
            "time_zone": "Africa/Accra",
            "repeat_flag": "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=1;TT_WORKDAY=1",
            "priority": 5,
            "sort_order": 2,
            "status": 0,
            "is_all_day": False,
            "is_floating": True,
            "kind": "NOTE",
            "reminders": [
                {
                    "id": generate_object_id(),
                    "trigger": "TRIGGER:P0DT9H0M0S",
                },
                {
                    "id": generate_object_id(),
                    "trigger": "TRIGGER:-P6DT15H0M0S",
                },
            ],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_D",
            "project_id": project_data[3]["id"],
            "content": "content for test_get_batch_v2_TASK_D",
            "start_date": "2022-01-04T00:00:00.000Z",
            "time_zone": "Africa/Accra",
            "repeat_flag": "RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND",
            "priority": 0,
            "sort_order": 3,
            "status": 0,
            "is_all_day": True,
            "is_floating": False,
            "kind": "NOTE",
            "reminders": [
                {
                    "id": generate_object_id(),
                    "trigger": "TRIGGER:-PT30M",
                },
                {
                    "id": generate_object_id(),
                    "trigger": "TRIGGER:-PT0S",
                },
            ],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_E",  # will have subtasks
            "project_id": project_data[0]["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_F",
            "project_id": project_data[1]["id"],
            "tags": [tag_data[2]["name"]],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_G",
            "project_id": project_data[2]["id"],
            "tags": [tag_data[1]["name"]],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_TASK_H",
            "project_id": project_data[3]["id"],
            "tags": [tag_data[0]["name"]],
        },
    ]

    subtask_task_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_SUBTASK_A",
            "project_id": project_data[0]["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_SUBTASK_B",
            "project_id": project_data[0]["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_SUBTASK_C",
            "project_id": project_data[0]["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_get_batch_v2_SUBTASK_D",
            "project_id": project_data[0]["id"],
        },
    ]

    subtask_data = [
        {
            "parent_id": task_data[4]["id"],
            "task_id": t["id"],
            "project_id": t["project_id"],
        }
        for t in subtask_task_data
    ]

    delete_project_groups([d["name"] for d in project_group_data])
    delete_projects([d["name"] for d in project_data])
    delete_tags([d["label"] for d in tag_data])

    _resp = client.post_project_group_v2({"add": project_group_data})
    assert set(_resp.ids) == {d["id"] for d in project_group_data}

    _resp = client.post_project_v2({"add": project_data})
    assert set(_resp.ids) == {d["id"] for d in project_data}

    _resp = client.post_tag_v2({"add": tag_data})
    assert set(_resp.ids) == {d["name"] for d in tag_data}

    _resp = client.post_task_v2({"add": task_data})
    assert set(_resp.ids) == {d["id"] for d in task_data}

    _resp = client.post_task_v2({"add": subtask_task_data})
    assert set(_resp.ids) == {d["id"] for d in subtask_task_data}

    _resp = client.post_task_parent_v2(subtask_data)
    assert {d["task_id"] for d in subtask_data} <= set(_resp.ids)

    resp = client.get_batch_v2()
    assert resp is not None
    assert isinstance(resp, GetBatchV2)

    g = None
    for data in project_group_data:
        assert isinstance(resp.project_groups, list)
        assert any(data["id"] == g.id for g in resp.project_groups)
        for g in resp.project_groups:
            if g.id == data["id"]:
                break
        assert g is not None
        assert data["id"] == g.id
        assert data["name"] == g.name

    for data in project_data:
        assert any(data["id"] == p.id for p in resp.project_profiles)
        for g in resp.project_profiles:
            if g.id == data["id"]:
                break
        assert isinstance(g, ProjectV2)
        assert data["name"] == g.name
        if "group_id" in data:
            assert data["group_id"] == g.group_id
        if "color" in data:
            assert TypeAdapter(Color).validate_python(data["color"]) == g.color
        if "kind" in data:
            assert data["kind"] == g.kind

    for data in tag_data:
        t = None
        assert any(data["name"] == t.name for t in resp.tags)
        for t in resp.tags:
            if t.name == data["name"]:
                break
        assert t is not None
        assert t.name == data["name"]
        assert data["label"] == t.label
        if "color" in data:
            assert TypeAdapter(Color).validate_python(data["color"]) == t.color

    t = None
    for data in task_data + subtask_task_data:
        assert any(data["id"] == t.id for t in resp.sync_task_bean.update)
        for t in resp.sync_task_bean.update:
            if t.id == data["id"]:
                break
        assert t is not None
        assert isinstance(t, TaskV2)
        assert data["id"] == t.id
        assert data["title"] == t.title
        assert data["project_id"] == t.project_id
        if "tags" in data:
            assert set(data["tags"]) == set(t.tags)
        if "desc" in data:
            assert data["desc"] == t.desc
        if "content" in data:
            assert data["content"] == t.content
        if "time_zone" in data:
            assert (
                TypeAdapter(TimeZoneName).validate_python(data["time_zone"])
                == t.time_zone
            )
        if "start_date" in data:
            # cannot compare directly due to timezone differences
            assert isinstance(t.modified_time, datetime)
        if "due_date" in data:
            # cannot compare directly due to timezone differences
            assert isinstance(t.modified_time, datetime)
        if "modified_time" in data:
            # cannot compare directly due to timezone differences
            assert isinstance(t.modified_time, datetime)
        if "repeat_flag" in data:
            assert data["repeat_flag"] == t.repeat_flag
        if "priority" in data:
            assert data["priority"] == t.priority
        if "status" in data:
            assert data["status"] == t.status
        if "is_all_day" in data:
            assert data["is_all_day"] == t.is_all_day
        if "is_floating" in data:
            assert data["is_floating"] == t.is_floating
        if "kind" in data:
            assert data["kind"] == t.kind
        if "items" in data:
            assert len(data["items"]) == len(t.items)
            for item_data in data["items"]:
                i = None
                assert any(item_data["id"] == i.id for i in t.items)
                for i in t.items:
                    if i.id == item_data["id"]:
                        break
                assert i is not None
                assert item_data["title"] == i.title
                if "is_all_day" in item_data and data["is_all_day"] is None:
                    assert item_data["is_all_day"] == i.is_all_day
                if "time_zone" in item_data and data["time_zone"] is None:
                    assert item_data["time_zone"] == i.time_zone
                if "status" in item_data:
                    assert item_data["status"] == i.status
        if "reminders" in data:
            assert isinstance(t.reminders, list)
            assert len(data["reminders"]) == len(t.reminders)
            for reminder_data in data["reminders"]:
                r = None
                assert any(reminder_data["id"] == r.id for r in t.reminders)
                for r in t.reminders:
                    if r.id == reminder_data["id"]:
                        break
                assert r is not None
                assert reminder_data["id"] == r.id
                assert reminder_data["trigger"] == r.trigger

            if t.reminder is not None:
                assert any(t.reminder == r.trigger for r in t.reminders)

    for data in subtask_data:
        assert any(data["task_id"] == t.id for t in resp.sync_task_bean.update)
        for t in resp.sync_task_bean.update:
            if t.id == data["task_id"]:
                break
        assert t is not None
        assert data["parent_id"] == t.parent_id
        assert data["project_id"] == t.project_id

    delete_project_groups([d["name"] for d in project_group_data])
    delete_projects([d["name"] for d in project_data])
    delete_tags([d["label"] for d in tag_data])
