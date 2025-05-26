import pytest

from pyticktick.models.v2 import BatchRespV2


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="create_task_v2",
    scope="session",
    depends=["create_project_v2"],
)
def test_create_task_v2(generate_object_id, delete_projects, client, get_batch):
    project_data = {"id": generate_object_id(), "name": "test_create_task_v2_PROJECT"}

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    data = [
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_A",
            "project_id": project_data["id"],
            "desc": "description for test_create_task_v2_task_A",
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
                    "title": "test_create_task_v2_task_A_ITEM_A",
                    "is_all_day": False,
                    "sort_order": 0,
                    "time_zone": "America/New_York",
                    "status": 0,
                },
                {
                    "id": generate_object_id(),
                    "title": "test_create_task_v2_task_A_ITEM_B",
                    "is_all_day": True,
                    "sort_order": 1,
                    "time_zone": "America/Chicago",
                    "status": 1,
                },
            ],
            "modified_time": "2022-01-01T12:00:00.000Z",
            "kind": "CHECKLIST",
            "status": 0,
            "is_floating": False,
        },
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_B",
            "project_id": project_data["id"],
            "content": "content for test_create_task_v2_task_B",
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
            "status": 0,
            "is_floating": True,
        },
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_C",
            "project_id": project_data["id"],
            "content": "content for test_create_task_v2_task_C",
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
            "status": 0,
            "is_floating": False,
        },
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_D",
            "project_id": project_data["id"],
            "content": "content for test_create_task_v2_task_D",
            "is_all_day": True,
            "start_date": "2022-05-01T00:00:00.000Z",
            "due_date": "2022-05-03T00:00:00.000Z",
            "time_zone": "America/New_York",
            "repeat_flag": "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=-1;TT_WORKDAY=-1",
            "priority": 0,
            "sort_order": 3,
            "modified_time": "2022-05-01T12:00:00.000Z",
            "kind": "NOTE",
            "status": 0,
            "is_floating": True,
        },
    ]

    expected_tasks = []
    for d in data:
        _expected = {
            "id": d["id"],
            "projectId": project_data["id"],
            "title": d["title"],
            "timeZone": d["time_zone"],
            "isFloating": d["is_floating"],
            "isAllDay": d["is_all_day"],
            "repeatFlag": d["repeat_flag"],
            "priority": d["priority"],
            "status": d["status"],
            "kind": d["kind"],
        }
        if "desc" in d:
            _expected["desc"] = d["desc"]
        if "content" in d:
            _expected["content"] = d["content"]

    # Warning: Cannot currently test times, as the API returns different times than the
    # ones sent in the request. This is due to the API converting the times to UTC.

    resp = client.post_task_v2({"add": data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in data}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in expected_tasks:
        assert any(task.items() <= t.items() for t in batch_tasks), (
            f"Task '{task['title']}' not found in batch"
        )

    expected_task_0_items = [
        {
            "id": item["id"],
            "title": item["title"],
            "sortOrder": item["sort_order"],
            "isAllDay": item["is_all_day"],
            "timeZone": item["time_zone"],
            "status": item["status"],
        }
        for item in data[0]["items"]
    ]
    for task in batch_tasks:
        if task["title"] == data[0]["title"]:
            for item in expected_task_0_items:
                assert any(item.items() <= i.items() for i in task["items"]), (
                    f"Item '{item['title']}' not found in task '{task['title']}'"
                )

    expected_task_1_reminders = [
        {"id": reminder["id"], "trigger": reminder["trigger"]}
        for reminder in data[1]["reminders"]
    ]
    expected_task_2_reminders = [
        {"id": reminder["id"], "trigger": reminder["trigger"]}
        for reminder in data[2]["reminders"]
    ]
    for task in batch_tasks:
        if task["title"] == data[1]["title"]:
            for reminder in expected_task_1_reminders:
                assert any(reminder.items() <= r.items() for r in task["reminders"]), (
                    f"'{reminder['trigger']}' not found in task '{task['title']}'"
                )
        if task["title"] == data[2]["title"]:
            for reminder in expected_task_2_reminders:
                assert any(reminder.items() <= r.items() for r in task["reminders"]), (
                    f"'{reminder['trigger']}' not found in task '{task['title']}'"
                )

    delete_projects([project_data["name"]])


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="update_task_v2",
    scope="session",
    depends=["create_project_v2", "create_task_v2"],
)
def test_update_task_v2(generate_object_id, delete_projects, client, get_batch):
    project_data = {"id": generate_object_id(), "name": "test_update_task_v2_PROJECT"}

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    initial_data = [
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_A",
            "project_id": project_data["id"],
            "desc": "description for test_create_task_v2_task_A",
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
                    "title": "test_create_task_v2_task_A_ITEM_A",
                    "is_all_day": False,
                    "sort_order": 0,
                    "time_zone": "America/New_York",
                    "status": 0,
                },
            ],
            "modified_time": "2022-01-01T12:00:00.000Z",
            "kind": "CHECKLIST",
            "status": 0,
            "is_floating": False,
        },
        {
            "id": generate_object_id(),
            "title": "test_create_task_v2_TASK_B",
            "project_id": project_data["id"],
            "content": "content for test_create_task_v2_task_B",
            "is_all_day": True,
            "start_date": "2023-01-01T00:00:00.000Z",
            "due_date": "2023-01-03T00:00:00.000Z",
            "time_zone": "Africa/Cairo",
            "reminders": [
                {
                    "id": generate_object_id(),
                    "trigger": "TRIGGER:P0DT9H0M0S",
                },
            ],
            "repeat_flag": "RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND",
            "priority": 3,
            "sort_order": 1,
            "modified_time": "2023-01-01T12:00:00.000Z",
            "kind": "NOTE",
            "status": 0,
            "is_floating": True,
        },
    ]

    updated_data = [
        {
            "id": initial_data[0]["id"],
            "project_id": project_data["id"],
            "title": "test_update_task_v2_TASK_A_updated",
            "is_all_day": initial_data[1]["is_all_day"],
            "time_zone": initial_data[1]["time_zone"],
            "reminders": initial_data[1]["reminders"],
            "repeat_flag": initial_data[1]["repeat_flag"],
            "priority": initial_data[1]["priority"],
            "items": None,
            "kind": initial_data[1]["kind"],
            "status": 0,
            "is_floating": initial_data[1]["is_floating"],
        },
        {
            "id": initial_data[1]["id"],
            "project_id": project_data["id"],
            "title": "test_update_task_v2_TASK_B_updated",
            "is_all_day": initial_data[0]["is_all_day"],
            "time_zone": initial_data[0]["time_zone"],
            "reminders": None,
            "repeat_flag": initial_data[0]["repeat_flag"],
            "priority": initial_data[0]["priority"],
            "items": initial_data[0]["items"],
            "kind": initial_data[0]["kind"],
            "status": 0,
            "is_floating": initial_data[0]["is_floating"],
        },
    ]

    expected_tasks = []
    for d in updated_data:
        _expected = {
            "id": d["id"],
            "projectId": project_data["id"],
            "title": d["title"],
            "timeZone": d["time_zone"],
            "isFloating": d["is_floating"],
            "isAllDay": d["is_all_day"],
            "repeatFlag": d["repeat_flag"],
            "priority": d["priority"],
            "status": d["status"],
            "kind": d["kind"],
        }
        if "desc" in d:
            _expected["desc"] = d["desc"]
        if "content" in d:
            _expected["content"] = d["content"]

    _resp = client.post_task_v2({"add": initial_data})
    assert set(_resp.ids) == {d["id"] for d in initial_data}

    resp = client.post_task_v2({"update": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in initial_data}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in expected_tasks:
        assert any(task.items() <= t.items() for t in batch_tasks), (
            f"Task '{task['title']}' not found in batch"
        )

    delete_projects([project_data["name"]])


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="test_complete_and_wont_do_v2",
    scope="session",
    depends=["create_task_v2", "update_task_v2"],
)
def test_complete_and_wont_do_v2(
    generate_object_id,
    delete_projects,
    client,
    get_batch,
    get_task_v2,
):
    project_data = {
        "id": generate_object_id(),
        "name": "test_complete_and_wont_do_v2_PROJECT",
    }

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    initial_data = [
        {
            "id": generate_object_id(),
            "title": "test_complete_and_wont_do_v2_TO_COMPLETE_TASK",
            "project_id": project_data["id"],
            "status": 0,
        },
        {
            "id": generate_object_id(),
            "title": "test_complete_and_wont_do_v2_TO_WONT_DO_TASK",
            "project_id": project_data["id"],
            "status": 0,
        },
        {
            "id": generate_object_id(),
            "title": "test_complete_and_wont_do_v2_ALSO_TO_COMPLETE_TASK",
            "project_id": project_data["id"],
            "status": 0,
        },
    ]

    updated_data = [
        {
            "id": initial_data[0]["id"],
            "project_id": project_data["id"],
            "title": initial_data[0]["title"],
            "status": 2,
        },
        {
            "id": initial_data[1]["id"],
            "project_id": project_data["id"],
            "title": initial_data[1]["title"],
            "status": -1,
        },
        {
            "id": initial_data[2]["id"],
            "project_id": project_data["id"],
            "title": initial_data[2]["title"],
            "status": 1,
        },
    ]

    expected_tasks = [
        {
            "id": d["id"],
            "projectId": project_data["id"],
            "title": d["title"],
            "status": d["status"],
        }
        for d in updated_data
    ]

    _resp = client.post_task_v2({"add": initial_data})
    assert set(_resp.ids) == {d["id"] for d in initial_data}

    resp = client.post_task_v2({"update": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in initial_data}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in expected_tasks:
        assert not any(t["id"] == task["id"] for t in batch_tasks)
        _resp = get_task_v2(project_data["id"], task["id"])
        assert task.items() <= _resp.items()

    delete_projects([project_data["name"]])


@pytest.mark.order(1)
@pytest.mark.dependency(scope="session", depends=["create_task_v2", "update_task_v2"])
def test_delete_task_v2(generate_object_id, delete_projects, client, get_batch):
    project_data = {
        "id": generate_object_id(),
        "name": "test_complete_and_wont_do_v2_PROJECT",
    }

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})

    initial_data = [
        {
            "id": generate_object_id(),
            "title": "test_delete_task_v2_TASK_A",
            "project_id": project_data["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_delete_task_v2_TASK_B",
            "project_id": project_data["id"],
        },
    ]

    updated_data = [
        {"task_id": d["id"], "project_id": project_data["id"]} for d in initial_data
    ]

    _resp = client.post_task_v2({"add": initial_data})
    assert set(_resp.ids) == {d["id"] for d in initial_data}

    resp = client.post_task_v2({"delete": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert len(resp.ids) == 0

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in updated_data:
        assert not any(t["id"] == task["task_id"] for t in batch_tasks)

    delete_projects([project_data["name"]])
