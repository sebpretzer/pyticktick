# Code Conventions

The library follows a set of conventions in order to ensure a consistent and predictable interface for all users. User-facing code should follow these conventions. This mainly applies to the [Pydantic models](#pydantic-models), and the [client structure](#client-structure).

## Pydantic Models

### When to Use Pydantic Models

The library attempts to use [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) for all data entering or exiting its scope. This ensures that the library can validate and enforce data consistency on its own terms, rather than relying on external validation mechanisms. This means that all TickTick API request parameters and responses use Pydantic models. The library also relies on Pydantic to validate its [settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

If you want to learn more about the benefits of using Pydantic models, check out the [Pydantic documentation](https://docs.pydantic.dev/latest/why/).

### Model Organization

All models should be isolated to the `pyticktick/models` directory. This is somewhat of a standard practice, and you will notice it across other libraries as well.

Models are split between the `V1` and `V2` APIs to ensure isolation. Within each API version, the models are split yet again into parameters and responses. At that point, they are grouped based on their purpose and object-types they manipulate.

If there are any types that should be shared across multiple models, they should be placed in a shared file, still within the API version directory.

You can see the general structure below:

```text
pyticktick/models
├── v1
│   ├── parameters
│   │   ├── project.py
│   │   ├── task.py
│   │   └── ...
│   └── responses
│       ├── project.py
│       ├── task.py
│       └── ...
└── v2
    ├── parameters
    │   ├── project.py
    │   ├── task.py
    │   ├── tag.py
    │   └── ...
    ├── responses
    │   ├── project.py
    │   ├── task.py
    │   ├── tag.py
    │   └── ...
    ├── models.py
    └── types.py
```

### Naming Models

Parameter models attempt to follow the naming convention of request method, followed by endpoint name / TickTick object type, followed by API version. The rule does not have to be rigid, but should be descriptive enough to understand the purpose of the model. Here are some examples:

- `UpdateProjectV1()`
- `PostBatchProjectV2()`
- `GetClosedV2()`

Response models attempt to follow the naming convention of endpoint name / TickTick object type, followed by "resp", followed by API version. Here are some examples:

- `TaskV1()`
- `BatchTagRespV2()`
- `UserSignOnV2()`

## Client Structure

The majority of the library's functionality is encapsulated within the [`Client`](./../reference/client/v1.md) class. This class is responsible for managing the connection to the TickTick API, handling authentication, and providing a high-level interface for interacting with the API.

### Settings

The `Client` class is a subclass of the [`Settings`](./../reference/settings.md) class. This is what handles all the authentication and configuration for the client. There are two separate APIs, so authentication is handled differently for each. All attributes relating to one of the APIs are prefixed with `v1_` and `v2_` respectively. Helper functions for managing the authentication process should also have `v1_` and `v2_` prefixes.

### Function Naming

Functions are organized by API version. Similar to how [models are named](#naming-models), functions attempt to follow the naming convention of request method, followed by endpoint, followed by API version.

### Function Inputs and Outputs

Path parameters are given their own argument names in functions, whereas query parameters are passed in as a singular data object. The path parameters mostly only apply to the V1 API, as the V2 API mainly utilizes query parameters.

The client tries to be flexible by allowing query parameters to be passed in as a Pydantic model or dictionary representation of that model. If a dictionary is passed in, the function will do the validation on behalf of the user.

Any function that calls an API should return a response model.
