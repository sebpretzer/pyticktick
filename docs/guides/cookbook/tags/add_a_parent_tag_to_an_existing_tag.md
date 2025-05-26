# Add a Parent Tag to an Existing Tag

Let's assume we want to add a parent tag to the tag `test_tag` from the [create tag recipe](create_a_tag.md). We now want it to have the parent tag `parent_tag`.

This is what the action would look like in the TickTick app:

<figure markdown="span">
    ![](./../../../_images/cookbook/tags/add_a_parent_tag_to_an_existing_tag_form.png){ width="90%" }
</figure>

This is what the `pyticktick` equivalent would look like:

=== "V2 - dict"

    ```python
    import json
    from pyticktick import Client

    client = Client()
    resp = client.get_batch_v2()
    tag = None
    for t in resp.tags:
        if t.name == "test_tag":
            tag = t
            break

    if tag is None:
        msg = "Tag not found"
        raise ValueError(msg)

    resp = client.post_tag_v2(
        data={"update": [{"label": tag.label, "parent": "parent_tag", "color": tag.color}]},
    )
    print(json.dumps(resp.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id2error": {},
        "id2etag": {
            "test_tag": "gkz3g2rx"
        }
    }
    ```

=== "V2 - model"

    ```python
    import json
    from pyticktick import Client
    from pyticktick.models.v2 import PostBatchTagV2, UpdateTagV2

    client = Client()
    resp = client.get_batch_v2()
    tag = None
    for t in resp.tags:
        if t.name == "test_tag":
            tag = t
            break

    if tag is None:
        msg = "Tag not found"
        raise ValueError(msg)

    resp = client.post_tag_v2(
        data=PostBatchTagV2(
            update=[UpdateTagV2(label=tag.label, parent="parent_tag", color=tag.color)],
        ),
    )
    print(json.dumps(resp.model_dump(mode="json"), indent=4))
    ```

    will return:

    ```json
    {
        "id2error": {},
        "id2etag": {
            "test_tag": "gkz3g2rx"
        }
    }
    ```

Here is the end result in the TickTick app:

<figure markdown="span">
    ![](./../../../_images/cookbook/tags/added_a_parent_tag_to_an_existing_tag.png){ width="300px" }
</figure>
