import pytest

from pyticktick.models.v2 import BatchRespV2


@pytest.mark.order(1)
@pytest.mark.dependency(name="create_project_v2", scope="session")
def test_create_project_v2(generate_object_id, delete_projects, client, get_batch):
    data = [
        {
            "id": generate_object_id(),
            "name": "test_create_project_A",
            "color": "#ff0000",
            "view_mode": "list",
            "kind": "TASK",
        },
        {
            "id": generate_object_id(),
            "name": "test_create_project_B",
            "color": "rgb(255, 255, 0)",  # #ffff00
            "view_mode": "kanban",
            "kind": "NOTE",
        },
        {
            "id": generate_object_id(),
            "name": "test_create_project_C",
            "color": "Blue",  # #0000ff
            "view_mode": "timeline",
            "kind": "TASK",
        },
    ]

    expected_profiles = [
        {
            "id": data[0]["id"],
            "name": "test_create_project_A",
            "color": "#ff0000",
            "viewMode": "list",
            "kind": "TASK",
            "groupId": None,
        },
        {
            "id": data[1]["id"],
            "name": "test_create_project_B",
            "color": "#ffff00",
            "viewMode": "kanban",
            "kind": "NOTE",
            "groupId": None,
        },
        {
            "id": data[2]["id"],
            "name": "test_create_project_C",
            "color": "#0000ff",
            "viewMode": "timeline",
            "kind": "TASK",
            "groupId": None,
        },
    ]

    delete_projects([d["name"] for d in data])

    resp = client.post_project_v2({"add": data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in data}

    batch = get_batch()
    for profile in expected_profiles:
        assert any(profile.items() <= p.items() for p in batch["projectProfiles"])

    delete_projects([d["name"] for d in data])


@pytest.mark.order(1)
@pytest.mark.dependency(
    name="update_project_v2",
    scope="session",
    depends=["create_project_v2"],
)
def test_update_project_v2(generate_object_id, delete_projects, client, get_batch):
    initial_data = [
        {
            "id": generate_object_id(),
            "name": "test_update_project_A",
            "color": "#ff0000",
            "view_mode": "list",
            "kind": "TASK",
        },
        {
            "id": generate_object_id(),
            "name": "test_update_project_B",
            "color": "rgb(255, 255, 0)",  # #ffff00
            "view_mode": "kanban",
            "kind": "NOTE",
        },
        {
            "id": generate_object_id(),
            "name": "test_update_project_C",
            "color": "Blue",  # #0000ff
            "view_mode": "timeline",
            "kind": "TASK",
        },
    ]

    updated_data = [
        {
            "id": initial_data[0]["id"],
            "name": "test_update_project_A_updated",
            "color": "Blue",  # #0000ff
            "view_mode": "timeline",
            "kind": "NOTE",
        },
        {
            "id": initial_data[1]["id"],
            "name": "test_update_project_B_updated",
            "color": "#ff0000",
            "view_mode": "list",
            "kind": "TASK",
        },
        {
            "id": initial_data[2]["id"],
            "name": "test_update_project_C_updated",
            "color": "rgb(255, 255, 0)",  # #ffff00
            "view_mode": "kanban",
            "kind": "NOTE",
        },
    ]

    expected_profiles = [
        {
            "id": initial_data[0]["id"],
            "name": "test_update_project_A_updated",
            "color": "#0000ff",
            "viewMode": "timeline",
            "kind": "NOTE",
            "groupId": None,
        },
        {
            "id": initial_data[1]["id"],
            "name": "test_update_project_B_updated",
            "color": "#ff0000",
            "viewMode": "list",
            "kind": "TASK",
            "groupId": None,
        },
        {
            "id": initial_data[2]["id"],
            "name": "test_update_project_C_updated",
            "color": "#ffff00",
            "viewMode": "kanban",
            "kind": "NOTE",
            "groupId": None,
        },
    ]

    delete_projects([d["name"] for d in initial_data + updated_data])

    _resp = client.post_project_v2({"add": initial_data})
    assert set(_resp.ids) == {d["id"] for d in initial_data}

    resp = client.post_project_v2({"update": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in initial_data}

    batch = get_batch()
    for profile in expected_profiles:
        assert any(profile.items() <= p.items() for p in batch["projectProfiles"])

    delete_projects([d["name"] for d in initial_data + updated_data])


@pytest.mark.order(1)
@pytest.mark.dependency(depends=["create_project_v2"])
def test_delete_project_v2(generate_object_id, delete_projects, client):
    data = [
        {"id": generate_object_id(), "name": "test_delete_project_A"},
        {"id": generate_object_id(), "name": "test_delete_project_B"},
        {"id": generate_object_id(), "name": "test_delete_project_C"},
    ]

    delete_projects([d["name"] for d in data])

    _resp = client.post_project_v2({"add": data})
    assert set(_resp.ids) == {d["id"] for d in data}

    resp = client.post_project_v2({"delete": [d["id"] for d in data]})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert len(resp.ids) == 0
