# pyticktick

`pyticktick` is the modern (unofficial) python library for interacting with [TickTick](https://ticktick.com/home). `pyticktick` supports both the official and unofficial APIs, provides elegant retry logic, and catches data errors early with [`pydantic`](https://docs.pydantic.dev/latest/).

______________________________________________________________________

Make sure you have `pyticktick` [installed](./guides/installation.md), then you can get all your projects and tasks:

```python
import json
from pyticktick import Client

client = Client(v2_username="username",v2_password="password")
resp = client.get_batch_v2()

print("My Projects:")
for project in resp.project_profiles:
    print(json.dumps(project.model_dump(mode="json"), indent=4))

print("My Tasks:")
for task in resp.sync_task_bean.update:
    print(json.dumps(task.model_dump(mode="json"), indent=4))
```

To see more, you can check out all the of recipes from the [cookbook](./guides/cookbook/settings/authenticate_client_via_python.md).

??? warning "Disclaimer"

    This project is not affiliated with [TickTick](https://ticktick.com/home), and parts of the API accessed by the client are not officially supported. It may even go against their [Terms of Service](https://ticktick.com/tos). See [_Which API should I use?_](./explanations/ticktick_api/two_apis.md#which-api-should-i-use) for more information.
