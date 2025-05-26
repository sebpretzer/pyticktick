from pyticktick.models.v1 import CreateTaskV1, TaskV1, UpdateTaskV1


def test_get_task(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_create_task,
):
    test_project_name = "test_get_task"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_get_task_task"
    task_resp = helper_create_task(project_id, test_task_name)
    assert isinstance(task_resp, dict)
    task_id = task_resp.get("id")
    assert isinstance(task_id, str)

    task = client.get_task_v1(project_id, task_id)
    assert task is not None
    assert isinstance(task, TaskV1)
    assert task.id == task_id
    assert task.project_id == project_id
    assert task.title == test_task_name

    helper_delete_projects_if_exists(test_project_name)


def test_create_task(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_get_project_data,
):
    test_project_name = "test_get_task"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_get_task_task"
    task = client.create_task_v1(
        CreateTaskV1(project_id=project_id, title=test_task_name),
    )
    assert task is not None
    assert isinstance(task, TaskV1)
    assert task.project_id == project_id
    assert task.title == test_task_name

    resp = helper_get_project_data(project_id)
    assert isinstance(resp, dict)
    tasks = resp.get("tasks")
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    assert tasks[0].get("id") == task.id
    assert tasks[0].get("projectId") == task.project_id == project_id
    assert tasks[0].get("title") == task.title == test_task_name

    helper_delete_projects_if_exists(test_project_name)


def test_update_task(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_create_task,
):
    test_project_name = "test_update_task"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_update_task_task"
    task_resp = helper_create_task(project_id, test_task_name)
    assert isinstance(task_resp, dict)
    task_id = task_resp.get("id")
    assert isinstance(task_id, str)

    new_task_name = "test_update_task_task (updated)"
    task = client.update_task_v1(
        task_id,
        UpdateTaskV1(id=task_id, project_id=project_id, title=new_task_name),
    )
    assert task is not None
    assert isinstance(task, TaskV1)
    assert task.id == task_id
    assert task.project_id == project_id
    assert task.title == new_task_name

    helper_delete_projects_if_exists(test_project_name)


def test_complete_task(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_create_task,
    helper_get_task,
):
    test_project_name = "test_complete_task"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_complete_task_task"
    task_resp = helper_create_task(project_id, test_task_name)
    assert isinstance(task_resp, dict)
    task_id = task_resp.get("id")
    assert isinstance(task_id, str)

    resp_before = helper_get_task(project_id, task_id)
    assert isinstance(resp_before, dict)
    assert resp_before.get("status") == 0
    assert "completedTime" not in resp_before

    client.complete_task_v1(project_id, task_id)

    resp_after = helper_get_task(project_id, task_id)
    assert isinstance(resp_after, dict)
    assert resp_after.get("status") == 2
    assert resp_after.get("completedTime") is not None

    helper_delete_projects_if_exists(test_project_name)


def test_delete_task(
    client,
    helper_create_or_recreate_projects,
    helper_delete_projects_if_exists,
    helper_create_task,
    helper_get_task,
    helper_get_project_data,
):
    test_project_name = "test_delete_task"
    project_resp = helper_create_or_recreate_projects(test_project_name)
    assert isinstance(project_resp, dict)
    project_id = project_resp.get("id")
    assert isinstance(project_id, str)

    test_task_name = "test_delete_task_task"
    task_resp = helper_create_task(project_id, test_task_name)
    assert isinstance(task_resp, dict)
    task_id = task_resp.get("id")
    assert isinstance(task_id, str)

    resp_before = helper_get_task(project_id, task_id)
    assert isinstance(resp_before, dict)
    assert resp_before.get("status") == 0
    assert "completedTime" not in resp_before

    client.delete_task_v1(project_id, task_id)

    resp_after = helper_get_task(project_id, task_id)
    assert resp_before != resp_after

    project_resp = helper_get_project_data(project_id)
    assert isinstance(project_resp, dict)
    tasks = project_resp.get("tasks")
    assert isinstance(tasks, list)
    assert len(tasks) == 0

    helper_delete_projects_if_exists(test_project_name)
