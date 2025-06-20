from pyticktick.models.v1 import (
    CreateProjectV1,
    ProjectDataRespV1,
    ProjectV1,
    UpdateProjectV1,
)
from pyticktick.models.v1.responses.project import ProjectRespV1, ProjectsRespV1


def test_get_projects(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
):
    test_project_names = ["test_get_projects_1", "test_get_projects_2"]
    helper_create_or_recreate_projects(test_project_names)

    resp = client.get_projects_v1()

    assert resp is not None
    assert isinstance(resp, ProjectsRespV1)
    assert all(isinstance(p, ProjectV1) for p in resp.root)

    for p in test_project_names:
        assert p in [p.name for p in resp.root]

    helper_delete_projects_if_exists(test_project_names)


def test_get_project(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
):
    test_project_name = "test_get_project"
    resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(resp, dict)
    project_id = resp.get("id")
    assert isinstance(project_id, str)

    resp = client.get_project_v1(project_id)
    assert resp is not None
    assert isinstance(resp, ProjectRespV1)
    assert resp.root.id == project_id
    assert resp.root.name == test_project_name

    helper_delete_projects_if_exists(test_project_name)


def test_get_project_with_data(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_create_task,
):
    test_project_name = "test_get_project_with_data"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_get_project_with_data__task"
    task_resp = helper_create_task(project_id, test_task_name)

    project = client.get_project_with_data_v1(project_id)
    assert project is not None
    assert isinstance(project, ProjectDataRespV1)
    assert isinstance(project.project, ProjectV1)
    assert project.project.id == project_id
    assert project.project.name == test_project_name
    assert isinstance(project.tasks, list)
    assert len(project.tasks) == 1
    assert project.tasks[0].id == task_resp.get("id")
    assert project.tasks[0].title == test_task_name

    helper_delete_projects_if_exists(test_project_name)


def test_create_project(
    client,
    helper_get_projects,
    helper_delete_projects_if_exists,
):
    test_project_name = "test_create_project"
    helper_delete_projects_if_exists(test_project_name)

    resp = client.create_project_v1(CreateProjectV1(name=test_project_name))

    assert resp is not None
    assert isinstance(resp, ProjectRespV1)
    assert resp.root.name == test_project_name

    project_dicts = helper_get_projects()
    assert test_project_name in [p["name"] for p in project_dicts]

    helper_delete_projects_if_exists(test_project_name)


def test_update_project(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
):
    test_project_name = "test_update_project"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_project_name_updated = "test_update_project (updated)"
    helper_delete_projects_if_exists(test_project_name_updated)

    project_updated = client.update_project_v1(
        project_id,
        UpdateProjectV1(name=test_project_name_updated),
    )
    assert project_updated.root.id == project_id
    assert project_updated.root.name == test_project_name_updated

    helper_delete_projects_if_exists([test_project_name, test_project_name_updated])


def test_delete_project(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_get_projects,
):
    test_project_name = "test_delete_project"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    client.delete_project_v1(project_id)

    project_dicts = helper_get_projects()
    assert test_project_name not in [p["name"] for p in project_dicts]

    helper_delete_projects_if_exists(test_project_name)
