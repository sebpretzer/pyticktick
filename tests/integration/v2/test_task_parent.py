import pytest

from pyticktick.models.v2 import BatchTaskParentRespV2


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="set_and_unset_task_parent_v2",
    scope="session",
    depends=["create_project_v2", "create_task_v2"],
)
def test_set_and_unset_task_parent_v2(
    generate_object_id,
    delete_projects,
    client,
    get_batch,
):
    project_data = {
        "id": generate_object_id(),
        "name": "test_set_and_unset_task_parent_v2",
    }

    delete_projects([project_data["name"]])

    _resp = client.post_project_v2({"add": [project_data]})
    assert set(_resp.ids) == {project_data["id"]}

    task_data = [
        {
            "id": generate_object_id(),
            "title": "test_set_and_unset_task_parent_v2_PARENT",
            "project_id": project_data["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_set_and_unset_task_parent_v2_CHILD_A",
            "project_id": project_data["id"],
        },
        {
            "id": generate_object_id(),
            "title": "test_set_and_unset_task_parent_v2_CHILD_B",
            "project_id": project_data["id"],
        },
    ]

    _resp = client.post_task_v2({"add": task_data})
    assert set(_resp.ids) == {d["id"] for d in task_data}

    initial_data = [
        {
            "parent_id": task_data[0]["id"],
            "task_id": task_data[1]["id"],
            "project_id": project_data["id"],
        },
    ]

    resp = client.post_task_parent_v2(initial_data)
    assert isinstance(resp, BatchTaskParentRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {t["id"] for t in task_data[:2]}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in task_data[:2]:
        assert any(task["id"] == t["id"] for t in batch_tasks)
    for t in batch_tasks:
        if t["id"] == task_data[0]["id"]:
            child_ids = t.get("childIds", None)
            assert child_ids is not None
            assert isinstance(child_ids, list)
            assert set(child_ids) == {task_data[1]["id"]}
        if t["id"] == task_data[1]["id"]:
            parent_id = t.get("parentId", None)
            assert parent_id is not None
            assert isinstance(parent_id, str)
            assert parent_id == task_data[0]["id"]

    updated_data = [
        {
            "parent_id": task_data[0]["id"],
            "task_id": task_data[2]["id"],
            "project_id": project_data["id"],
        },
        {
            "old_parent_id": task_data[0]["id"],
            "task_id": task_data[1]["id"],
            "project_id": project_data["id"],
        },
    ]

    resp = client.post_task_parent_v2(updated_data)
    assert isinstance(resp, BatchTaskParentRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {t["id"] for t in task_data}

    batch = get_batch()
    batch_tasks = batch["syncTaskBean"]["update"]
    for task in task_data:
        assert any(task["id"] == t["id"] for t in batch_tasks)
    for t in batch_tasks:
        if t["id"] == task_data[0]["id"]:
            child_ids = t.get("childIds", None)
            assert child_ids is not None
            assert isinstance(child_ids, list)
            assert set(child_ids) == {task_data[2]["id"]}
        if t["id"] == task_data[1]["id"]:
            parent_id = t.get("parentId", None)
            assert parent_id is None
        if t["id"] == task_data[2]["id"]:
            parent_id = t.get("parentId", None)
            assert parent_id is not None
            assert isinstance(parent_id, str)
            assert parent_id == task_data[0]["id"]

    delete_projects([project_data["name"]])
