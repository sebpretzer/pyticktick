# Get a Project by ID

Let's assume we want to get a project with the project ID `681d63f18f0892430630d16b`.

This is what the `pyticktick` code would look like:

=== "V1"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    project = client.get_project_v1(project_id="681d63f18f0892430630d16b")
    print(json.dumps(project.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id": "681d63f18f0892430630d16b",
        "name": "Project 1",
        "color": "#FF6161",
        "sort_order": -3298534883328,
        "closed": null,
        "group_id": null,
        "view_mode": "list",
        "permission": null,
        "kind": "TASK"
    }
    ```

=== "V2"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    resp = client.get_batch_v2()
    for p in resp.project_profiles:
        if p.id == "681d63f18f0892430630d16b":
            print(json.dumps(p.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "color": "#ff6161",
        "etag": "s83jq7d8",
        "group_id": null,
        "id": "681d63f18f0892430630d16b",
        "in_all": true,
        "kind": "TASK",
        "modified_time": "2025-05-09T02:10:16.671000Z",
        "name": "Project 1",
        "sort_option": null,
        "view_mode": "list",
        "barcode_need_audit": false,
        "is_owner": true,
        "sort_order": -3298534883328,
        "sort_type": null,
        "user_count": 1,
        "closed": null,
        "muted": false,
        "transferred": null,
        "notification_options": null,
        "team_id": null,
        "permission": null,
        "timeline": null,
        "need_audit": true,
        "open_to_team": false,
        "team_member_permission": null,
        "source": 1,
        "show_type": null,
        "reminder_type": null
    }
    ```
