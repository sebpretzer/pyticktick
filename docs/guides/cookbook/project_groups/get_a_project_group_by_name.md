# Get a Project Group by Name

Let's assume we want to get a project group with the project group name `Project Group 2`.

This is what the `pyticktick` code would look like:

=== "V2"

    ```python
    import json
    from pyticktick import Client

    resp = client.get_batch_v2()
    if resp.project_groups is None:
        print("No project groups found.")
    else:
        for pg in resp.project_groups:
            if pg.name == "Project Group 2":
                print(json.dumps(pg.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "etag": "y8vuqi2b",
        "id": "6822056f27de221753d62ef0",
        "name": "Project Group 2",
        "sort_option": null,
        "view_mode": null,
        "deleted": 0,
        "show_all": true,
        "sort_order": -8658654068736,
        "sort_type": "",
        "team_id": null,
        "timeline": null,
        "user_id": 126406863
    }
    ```
