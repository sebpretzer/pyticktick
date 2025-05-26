# Delete a Task

Let's assume we want to delete the task from the [create a basic task recipe](./create_a_basic_task.md) and the [update a basic task recipe](./update_a_basic_task.md). This had the ID `68336a02ec201a48c7aadedf` and the project ID `683217b48f08892e6997ef03`.

This is what the `pyticktick` code would look like:

=== "V1"

    ```python
    from pyticktick import Client

    client = Client()
    client.delete_task_v1(
        project_id="683217b48f08892e6997ef03",
        task_id="68336a02ec201a48c7aadedf",
    )
    ```

    This will not return anything.

=== "V2 - dict"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    resp = client.post_task_v2(
        data={
            "delete": [
                {
                    "project_id": "683217b48f08892e6997ef03",
                    "task_id": "68336a02ec201a48c7aadedf",
                },
            ],
        },
    )
    print(json.dumps(resp.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id2error": {},
        "id2etag": {}
    }
    ```

=== "V2 - model"

    ```python
    import json
    from pyticktick import Client
    from pyticktick.models.v2 import PostBatchTaskV2, DeleteTaskV2

    client = Client()
    resp = client.post_task_v2(
        data=PostBatchTaskV2(
            delete=[
                DeleteTaskV2(
                    project_id="683217b48f08892e6997ef03",
                    task_id="68336a02ec201a48c7aadedf",
                ),
            ],
        ),
    )
    print(json.dumps(resp.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id2error": {},
        "id2etag": {}
    }
    ```
