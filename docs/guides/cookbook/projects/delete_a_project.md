# Delete a Project

Let's assume we want to delete the project from the [create project recipe](create_a_project.md) and the [update project recipe](update_a_project.md), which had the project id `681ce1d98f0870ba1dd77ebe`.

This is what the `pyticktick` code would look like:

=== "V1"

    ```python
    from pyticktick import Client

    client = Client()
    client.delete_project_v1(project_id="681ce1d98f0870ba1dd77ebe")
    ```

    This will not return anything.

=== "V2 - dict"

    ```python
    from pyticktick import Client

    client = Client()
    resp = client.post_project_v2(data={"delete": ["681ce1d98f0870ba1dd77ebe"]})
    ```

    This will not return anything of value, just an empty `BatchRespV2` object.

=== "V2 - model"

    ```python
    from pyticktick import Client
    from pyticktick.models.v2 import PostBatchProjectV2

    client = Client()
    resp = client.post_project_v2(
        data=PostBatchProjectV2(delete=["681ce1d98f0870ba1dd77ebe"]),
    )
    ```

    This will not return anything of value, just an empty `BatchRespV2` object.
