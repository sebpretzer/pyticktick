from datetime import datetime

import pytest
from pydantic import TypeAdapter

from pyticktick.models.v2 import ClosedRespV2, TimeZoneName


@pytest.mark.order(2)
@pytest.mark.dependency(
    name="test_get_project_all_completed_v2",
    scope="session",
    depends=["create_project_v2", "create_task_v2", "test_complete_and_wont_do_v2"],
)
def test_get_project_all_completed_v2(generate_object_id, delete_projects, client):  # noqa: PLR0912, PLR0915
    project_data = {
        "name": "test_get_project_all_completed_v2",
        "id": generate_object_id(),
    }

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    completed_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_A",
            "project_id": project_data["id"],
            "desc": "description for test_get_project_all_completed_v2_task_A",
            "is_all_day": False,
            "start_date": "2022-01-01T00:00:00.000Z",
            "due_date": "2022-01-03T00:00:00.000Z",
            "time_zone": "Asia/Shanghai",
            "repeat_flag": "RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=SU;BYDAY=MO,TU,WE,TH,FR",
            "priority": 1,
            "sort_order": 0,
            "items": [
                {
                    "id": generate_object_id(),
                    "title": "test_get_project_all_completed_v2_task_A_ITEM_A",
                    "is_all_day": False,
                    "sort_order": 0,
                    "time_zone": "America/New_York",
                    "status": 2,
                },
                {
                    "id": generate_object_id(),
                    "title": "test_get_project_all_completed_v2_task_A_ITEM_B",
                    "is_all_day": True,
                    "sort_order": 1,
                    "time_zone": "America/Chicago",
                    "status": 2,
                },
            ],
            "modified_time": "2022-01-01T12:00:00.000Z",
            "kind": "CHECKLIST",
            "status": 2,
            "is_floating": False,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_B",
            "project_id": project_data["id"],
            "content": "content for test_get_project_all_completed_v2_task_B",
            "is_all_day": True,
            "start_date": "2023-01-01T00:00:00.000Z",
            "due_date": "2023-01-03T00:00:00.000Z",
            "time_zone": "Africa/Cairo",
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
            "repeat_flag": "RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND",
            "priority": 3,
            "sort_order": 1,
            "modified_time": "2023-01-01T12:00:00.000Z",
            "kind": "NOTE",
            "status": 2,
            "is_floating": True,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_C",
            "project_id": project_data["id"],
            "content": "content for test_get_project_all_completed_v2_task_C",
            "is_all_day": False,
            "start_date": "2023-02-01T00:00:00.000Z",
            "due_date": "2023-02-03T00:00:00.000Z",
            "time_zone": "Africa/Bangui",
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
            "repeat_flag": "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=1;TT_WORKDAY=1",
            "priority": 5,
            "sort_order": 2,
            "modified_time": "2023-02-01T12:00:00.000Z",
            "kind": "TEXT",
            "status": 2,
            "is_floating": False,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_D",
            "project_id": project_data["id"],
            "content": "content for test_get_project_all_completed_v2_task_D",
            "is_all_day": True,
            "start_date": "2022-05-01T00:00:00.000Z",
            "due_date": "2022-05-03T00:00:00.000Z",
            "time_zone": "America/New_York",
            "repeat_flag": "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=-1;TT_WORKDAY=-1",
            "priority": 0,
            "sort_order": 3,
            "modified_time": "2022-05-01T12:00:00.000Z",
            "kind": "NOTE",
            "status": 2,
            "is_floating": True,
        },
    ]

    not_completed_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_E",
            "project_id": project_data["id"],
            "status": 0,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_completed_v2_TASK_F",
            "project_id": project_data["id"],
            "status": -1,
        },
    ]

    task_data = completed_data + not_completed_data

    _resp = client.post_task_v2({"add": task_data})
    assert set(_resp.ids) == {d["id"] for d in task_data}

    resp = client.get_project_all_closed_v2({"status": "Completed"})
    assert resp is not None
    assert isinstance(resp, ClosedRespV2)
    t = None
    for data in completed_data:
        assert any(t.id == data["id"] for t in resp.root)
        for t in resp.root:
            if t.id == data["id"]:
                break
        assert t is not None
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
            i = None
            for item_data in data["items"]:
                assert any(item_data["id"] == i.id for i in t.items)
                for i in t.items:
                    if i.id == item_data["id"]:
                        break
                assert i is not None
                assert item_data["id"] == i.id
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

    for data in not_completed_data:
        assert not any(t.id == data["id"] for t in resp.root)

    delete_projects([project_data["name"]])


@pytest.mark.order(2)
@pytest.mark.dependency(
    scope="session",
    depends=[
        "create_project_v2",
        "create_task_v2",
        "test_complete_and_wont_do_v2",
        "test_get_project_all_completed_v2",
    ],
)
def test_get_project_all_wont_do_v2(generate_object_id, delete_projects, client):
    project_data = {
        "name": "test_get_project_all_wont_do_v2",
        "id": generate_object_id(),
    }

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    wont_do_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_wont_do_v2_TASK_A",
            "project_id": project_data["id"],
            "status": -1,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_wont_do_v2_TASK_B",
            "project_id": project_data["id"],
            "status": -1,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_wont_do_v2_TASK_C",
            "project_id": project_data["id"],
            "status": -1,
        },
    ]

    not_wont_do_data = [
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_wont_do_v2_TASK_D",
            "project_id": project_data["id"],
            "status": 0,
        },
        {
            "id": generate_object_id(),
            "title": "test_get_project_all_wont_do_v2_TASK_E",
            "project_id": project_data["id"],
            "status": 2,
        },
    ]

    task_data = wont_do_data + not_wont_do_data

    _resp = client.post_task_v2({"add": task_data})
    assert set(_resp.ids) == {d["id"] for d in task_data}

    resp = client.get_project_all_closed_v2({"status": "Abandoned"})
    assert resp is not None
    assert isinstance(resp, ClosedRespV2)
    t = None
    for data in wont_do_data:
        assert any(t.id == data["id"] for t in resp.root)
        for t in resp.root:
            if t.id == data["id"]:
                break
        assert t is not None
        assert data["id"] == t.id
        assert data["title"] == t.title
        assert data["project_id"] == t.project_id
        assert data["status"] == t.status

    for data in not_wont_do_data:
        assert not any(t.id == data["id"] for t in resp.root)

    delete_projects([project_data["name"]])
