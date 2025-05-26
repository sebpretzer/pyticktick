# Get a Task by Name

Let's assume we want to get the task with the name `"Task 5"`, one of the tasks in the [Get All Tasks recipe](./get_all_tasks.md).

This is what the `pyticktick` code looks like:

=== "V1"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    projects = client.get_projects_v1()
    for project in projects:
        data = client.get_project_with_data_v1(project_id=project.id)
        for task in data.tasks:
            if task.title == "Task 5":
                print(json.dumps(task.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id": "6834aabbec201a7f471a2e80",
        "project_id": "6834a28d8f08df73a73c46a8",
        "title": "Task 5",
        "is_all_day": true,
        "completed_time": null,
        "content": "",
        "desc": null,
        "due_date": "2025-01-02T06:00:00.000+0000",
        "items": null,
        "priority": 0,
        "reminders": null,
        "repeat_flag": "RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=WE,MO,TU,TH,FR",
        "sort_order": 3298534883328,
        "start_date": "2025-01-02T06:00:00.000+0000",
        "status": false,
        "time_zone": "America/Chicago"
    }
    ```

=== "V2"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    resp = client.get_batch_v2()
    for task in resp.sync_task_bean.update:
        if task.title == "Task 5":
            print(json.dumps(task.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "child_ids": null,
        "completed_time": null,
        "content": "",
        "created_time": "2025-05-26T17:54:03Z",
        "desc": null,
        "due_date": "2025-01-02T06:00:00Z",
        "etag": "umaki4zx",
        "id": "6834aabbec201a7f471a2e80",
        "is_all_day": true,
        "is_floating": false,
        "items": [],
        "kind": "TEXT",
        "modified_time": "2025-05-26T17:54:08Z",
        "parent_id": null,
        "priority": 0,
        "progress": 0,
        "project_id": "6834a28d8f08df73a73c46a8",
        "reminder": null,
        "reminders": [],
        "repeat_first_date": null,
        "repeat_flag": "RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=WE,MO,TU,TH,FR",
        "repeat_from": 2,
        "repeat_task_id": null,
        "start_date": "2025-01-02T06:00:00Z",
        "status": 0,
        "tags": [],
        "title": "Task 5",
        "time_zone": "America/Chicago",
        "attachments": [],
        "annoying_alert": null,
        "column_id": null,
        "comment_count": null,
        "completed_user_id": null,
        "creator": 126406863,
        "deleted": 0,
        "ex_date": [],
        "img_mode": null,
        "focus_summaries": [],
        "sort_order": 3298534883328
    }
    ```
