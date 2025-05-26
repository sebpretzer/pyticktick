import pytest

from pyticktick.models.v2 import BatchTagRespV2


@pytest.mark.order(1)
@pytest.mark.dependency(name="create_tag_v2", scope="session")
def test_create_tag_v2(delete_tags, client, get_batch):
    data = [
        {
            "label": "test_create_tag_v2_PARENT",
            "name": "test_create_tag_v2_parent",  # should be auto-generated normally
            "color": "#ff0000",
        },
        {
            "label": "test_create_tag_v2_STANDARD",
            "name": "test_create_tag_v2_standard",  # should be auto-generated normally
            "color": "rgb(255, 255, 0)",  # #ffff00
        },
    ]

    expected_data = [
        {
            "label": "test_create_tag_v2_PARENT",
            "name": "test_create_tag_v2_parent",
            "color": "#ff0000",
        },
        {
            "label": "test_create_tag_v2_STANDARD",
            "name": "test_create_tag_v2_standard",
            "color": "#ffff00",
        },
    ]

    delete_tags([d["label"] for d in data])

    resp = client.post_tag_v2({"add": data})
    assert isinstance(resp, BatchTagRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["name"] for d in data}

    batch = get_batch()
    for tag in expected_data:
        assert any(tag.items() <= t.items() for t in batch["tags"])

    child_data = {
        "label": "test_create_tag_v2_CHILD",
        "name": "test_create_tag_v2_child",  # should be auto-generated normally
        "color": "Blue",  # #0000ff
        "parent": data[0]["name"],
    }
    expected_child_data = {
        "label": "test_create_tag_v2_CHILD",
        "name": "test_create_tag_v2_child",
        "color": "#0000ff",
        "parent": data[0]["name"],
    }

    delete_tags([child_data["label"]])

    resp = client.post_tag_v2({"add": [child_data]})
    assert resp is not None
    assert isinstance(resp, BatchTagRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {child_data["name"]}

    batch = get_batch()
    assert any(expected_child_data.items() <= t.items() for t in batch["tags"])

    delete_tags([d["label"] for d in data] + [child_data["label"]])


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="rename_tag_v2",
    scope="session",
    depends=["create_tag_v2"],
)
def test_rename_tag_v2(delete_tags, client, get_batch):
    initial_data = [
        {
            "label": "test_rename_tag_v2",
            "name": "test_rename_tag_v2",
        },
    ]

    data = {
        "name": initial_data[0]["name"],
        "new_name": "test_rename_tag_v2_RENAMED",
    }

    expected_data = [
        {
            "label": "test_rename_tag_v2_RENAMED",
            "name": "test_rename_tag_v2_renamed",
            "rawName": "test_rename_tag_v2",
        },
    ]

    delete_tags(
        [d["label"] for d in initial_data] + [d["label"] for d in expected_data],
    )

    _resp = client.post_tag_v2({"add": initial_data})
    assert set(_resp.ids) == {d["name"] for d in initial_data}

    resp = client.put_rename_tag_v2(data)
    assert resp is None

    batch = get_batch()
    for tag in expected_data:
        assert any(tag.items() <= t.items() for t in batch["tags"])

    delete_tags(
        [d["label"] for d in initial_data] + [d["label"] for d in expected_data],
    )


@pytest.mark.dependency(
    name="update_tag_v2",
    scope="session",
    depends=["create_tag_v2", "rename_tag_v2"],
)
def test_update_tag_v2(delete_tags, client, get_batch):
    initial_data = [
        {
            "label": "test_update_tag_v2_PARENT",
            "name": "test_update_tag_v2_parent",  # should be auto-generated normally
            "color": "#ff0000",
        },
        {
            "label": "test_update_tag_v2_STANDARD",
            "name": "test_update_tag_v2_standard",  # should be auto-generated normally
            "color": "rgb(255, 255, 0)",  # #ffff00
        },
    ]

    updated_data = [
        {
            "label": "test_update_tag_v2_PARENT_updated",
            "name": "test_update_tag_v2_parent_updated",  # should be auto-generated normally # noqa: E501
            "raw_name": "test_update_tag_v2_parent",
            "color": "Blue",  # #0000ff
        },
        {
            "label": "test_update_tag_v2_STANDARD_now_a_child",
            "name": "test_update_tag_v2_standard_now_a_child",  # should be auto-generated normally  # noqa: E501
            "raw_name": "test_update_tag_v2_standard",
            "color": "#0000ff",
            "parent": "test_update_tag_v2_parent_updated",
        },
    ]

    expected_data = [
        {
            "label": "test_update_tag_v2_PARENT_updated",
            "name": "test_update_tag_v2_parent_updated",
            "rawName": "test_update_tag_v2_parent",
            "color": "#0000ff",
        },
        {
            "label": "test_update_tag_v2_STANDARD_now_a_child",
            "name": "test_update_tag_v2_standard_now_a_child",
            "rawName": "test_update_tag_v2_standard",
            "color": "#0000ff",
            "parent": "test_update_tag_v2_parent_updated",
        },
    ]

    delete_tags([d["label"] for d in initial_data] + [d["label"] for d in updated_data])

    _resp = client.post_tag_v2({"add": initial_data})
    assert set(_resp.ids) == {d["name"] for d in initial_data}

    for i in range(len(initial_data)):
        _ = client.put_rename_tag_v2(
            {"name": initial_data[i]["name"], "new_name": updated_data[i]["label"]},
        )

    resp = client.post_tag_v2({"update": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchTagRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["name"] for d in updated_data}

    batch = get_batch()
    for tag in expected_data:
        assert any(tag.items() <= t.items() for t in batch["tags"])

    delete_tags([d["label"] for d in initial_data] + [d["label"] for d in updated_data])


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="delete_tag_v2",
    scope="session",
    depends=["create_tag_v2"],
)
def test_delete_tag_v2(delete_tags, client, get_batch):
    initial_data = {
        "label": "test_delete_tag_v2",
        "name": "test_delete_tag_v2",  # should be auto-generated normally
    }

    rename_data = {
        "name": initial_data["name"],
        "new_name": "test_delete_tag_v2_RENAMED",
    }

    delete_data = {"name": "test_delete_tag_v2_renamed"}

    delete_tags([initial_data["label"], rename_data["new_name"]])

    _resp = client.post_tag_v2({"add": [initial_data]})
    assert set(_resp.ids) == {initial_data["name"]}

    _ = client.put_rename_tag_v2(rename_data)

    resp = client.delete_tag_v2(delete_data)
    assert resp is None

    batch = get_batch()
    for tag in batch["tags"]:
        assert initial_data["name"] not in tag["name"]
        assert rename_data["new_name"] not in tag["name"]
        assert delete_data["name"] not in tag["name"]

        assert initial_data["name"] not in tag["rawName"]
        assert rename_data["new_name"] not in tag["rawName"]
        assert delete_data["name"] not in tag["rawName"]

        assert initial_data["label"] not in tag["label"]
        assert rename_data["new_name"] not in tag["label"]

    delete_tags([initial_data["label"], rename_data["new_name"]])


@pytest.mark.order(2)
@pytest.mark.dependency(
    name="tag_tasks_v2",
    scope="session",
    depends=["create_project_v2", "create_tag_v2", "create_task_v2"],
)
def test_tag_tasks_v2(
    generate_object_id,
    delete_projects,
    delete_tags,
    client,
    get_batch,
):
    project_data = {"id": generate_object_id(), "name": "test_tag_tasks_v2_PROJECT"}

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})
    assert set(_resp.ids) == {project_data["id"]}

    tag_data = [
        {
            "label": "test_tag_tasks_v2_TAG_A",
            "name": "test_tag_tasks_v2_tag_a",  # should be auto-generated normally
        },
        {
            "label": "test_tag_tasks_v2_TAG_B",
            "name": "test_tag_tasks_v2_tag_b",  # should be auto-generated normally
        },
    ]

    delete_tags([d["label"] for d in tag_data])

    _resp = client.post_tag_v2({"add": tag_data})
    assert set(_resp.ids) == {d["name"] for d in tag_data}

    task_data = [
        {
            "id": generate_object_id(),
            "title": "test_tag_tasks_v2_TASK_A",
            "project_id": project_data["id"],
            "tags": [tag_data[0]["name"]],
        },
        {
            "id": generate_object_id(),
            "title": "test_tag_tasks_v2_TASK_B",
            "project_id": project_data["id"],
            "tags": [tag_data[1]["name"]],
        },
        {
            "id": generate_object_id(),
            "title": "test_tag_tasks_v2_TASK_C",
            "project_id": project_data["id"],
            "tags": [tag_data[0]["name"], tag_data[1]["name"]],
        },
        {
            "id": generate_object_id(),
            "title": "test_tag_tasks_v2_TASK_D",
            "project_id": project_data["id"],
            "tags": [],
        },
    ]

    expected_tasks = [
        {
            "id": t["id"],
            "title": t["title"],
            "projectId": project_data["id"],
            "tags": t["tags"],
        }
        for t in task_data
    ]

    resp = client.post_task_v2({"add": task_data})
    assert set(resp.ids) == {d["id"] for d in task_data}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in expected_tasks:
        assert any(task.items() <= t.items() for t in batch_tasks)

    delete_projects([project_data["name"]])
    delete_tags([d["label"] for d in tag_data])
