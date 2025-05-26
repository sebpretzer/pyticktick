import pytest

from pyticktick.models.v2 import BatchRespV2


@pytest.mark.order(1)
@pytest.mark.dependency(name="create_project_group_v2", scope="session")
def test_create_project_group_v2(
    generate_object_id,
    delete_project_groups,
    client,
    get_batch,
):
    data = [
        {"id": generate_object_id(), "name": "test_create_project_group_A"},
        {"id": generate_object_id(), "name": "test_create_project_group_B"},
        {"id": generate_object_id(), "name": "test_create_project_group_C"},
    ]

    delete_project_groups([d["name"] for d in data])

    resp = client.post_project_group_v2({"add": data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert len(resp.ids) == len(data)

    batch = get_batch()
    for group in data:
        assert any(group.items() <= pg.items() for pg in batch["projectGroups"])

    delete_project_groups([d["name"] for d in data])


@pytest.mark.order(1)
@pytest.mark.dependency(depends=["create_project_group_v2"])
def test_update_project_group_v2(
    generate_object_id,
    delete_project_groups,
    client,
    get_batch,
):
    initial_data = [
        {"id": generate_object_id(), "name": "test_update_project_group_A"},
        {"id": generate_object_id(), "name": "test_update_project_group_B"},
        {"id": generate_object_id(), "name": "test_update_project_group_C"},
    ]

    updated_data = [
        {
            "id": initial_data[0]["id"],
            "name": "test_update_project_group_A_updated",
        },
        {
            "id": initial_data[1]["id"],
            "name": "test_update_project_group_B_updated",
        },
        {
            "id": initial_data[2]["id"],
            "name": "test_update_project_group_C_updated",
        },
    ]

    delete_project_groups([d["name"] for d in initial_data + updated_data])

    _resp = client.post_project_group_v2({"add": initial_data})
    assert set(_resp.ids) == {d["id"] for d in initial_data}

    resp = client.post_project_group_v2({"update": updated_data})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert set(resp.ids) == {d["id"] for d in initial_data}

    batch = get_batch()
    for group in updated_data:
        assert any(group.items() <= pg.items() for pg in batch["projectGroups"])

    delete_project_groups([d["name"] for d in initial_data + updated_data])


@pytest.mark.order(1)
@pytest.mark.dependency(depends=["create_project_group_v2"])
def test_delete_project_group_v2(generate_object_id, delete_project_groups, client):
    data = [
        {"id": generate_object_id(), "name": "test_delete_project_group_A"},
        {"id": generate_object_id(), "name": "test_delete_project_group_B"},
        {"id": generate_object_id(), "name": "test_delete_project_group_C"},
    ]

    delete_project_groups([d["name"] for d in data])

    _resp = client.post_project_group_v2({"add": data})
    assert set(_resp.ids) == {d["id"] for d in data}

    resp = client.post_project_group_v2({"delete": [d["id"] for d in data]})
    assert resp is not None
    assert isinstance(resp, BatchRespV2)
    assert resp.ids is not None
    assert isinstance(resp.ids, list)
    assert len(resp.ids) == 0


@pytest.mark.order(1)
@pytest.mark.dependency(
    scope="session",
    depends=["create_project_group_v2", "create_project_v2", "update_project_v2"],
)
def test_add_and_update_project_with_group_v2(
    generate_object_id,
    delete_project_groups,
    delete_projects,
    client,
    get_batch,
):
    data = [
        {
            "id": generate_object_id(),
            "name": "test_add_and_update_project_with_group_GROUP_A",
        },
        {
            "id": generate_object_id(),
            "name": "test_add_and_update_project_with_group_GROUP_B",
        },
    ]

    project_data = {
        "id": generate_object_id(),
        "name": "test_add_and_update_project_with_group_PROJECT",
        "group_id": data[0]["id"],
    }

    delete_project_groups([d["name"] for d in data])
    delete_projects([project_data["name"]])

    resp = client.post_project_group_v2({"add": data})
    assert set(resp.ids) == {d["id"] for d in data}

    resp = client.post_project_v2({"add": [project_data]})
    assert set(resp.ids) == {project_data["id"]}
    batch = get_batch()
    profiles = [p for p in batch["projectProfiles"] if p["id"] == project_data["id"]]
    assert len(profiles) == 1
    assert profiles[0]["groupId"] == data[0]["id"]

    resp = client.post_project_v2(
        {
            "update": [
                {
                    "id": project_data["id"],
                    "name": project_data["name"],
                    "group_id": data[1]["id"],
                },
            ],
        },
    )
    assert set(resp.ids) == {project_data["id"]}
    batch = get_batch()
    profiles = [p for p in batch["projectProfiles"] if p["id"] == project_data["id"]]
    assert len(profiles) == 1
    assert profiles[0]["groupId"] == data[1]["id"]

    resp = client.post_project_v2(
        {
            "update": [
                {
                    "id": project_data["id"],
                    "name": project_data["name"],
                    "group_id": "NONE",
                },
            ],
        },
    )
    assert set(resp.ids) == {project_data["id"]}
    batch = get_batch()
    profiles = [p for p in batch["projectProfiles"] if p["id"] == project_data["id"]]
    assert len(profiles) == 1
    assert profiles[0]["groupId"] is None

    delete_projects([project_data["name"]])
    delete_project_groups([d["name"] for d in data])
