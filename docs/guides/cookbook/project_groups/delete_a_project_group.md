# Delete a Project Group

Let's assume we want to delete the project group from the [create project group recipe](create_a_project_group.md) and the [update project group recipe](update_a_project_group.md), which had the project group id `6821f8618f08de9a850d65ce`.

This is what the `pyticktick` code would look like:

=== "V2 - dict"

    ```python
    from pyticktick import Client

    client = Client()
    resp = client.post_project_group_v2(data={"delete": ["6821f8618f08de9a850d65ce"]})
    ```

    This will not return anything of value, just an empty `BatchRespV2` object.

=== "V2 - model"

    ```python
    from pyticktick import Client
    from pyticktick.models.v2 import PostBatchProjectGroupV2

    resp = client.post_project_group_v2(
        data=PostBatchProjectGroupV2(delete=["6821f8618f08de9a850d65ce"]),
    )
    ```

    This will not return anything of value, just an empty `BatchRespV2` object.
