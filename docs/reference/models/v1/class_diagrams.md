```mermaid
classDiagram
    direction LR
    class ProjectV1 {
        id: str
        name: str
        color: str | None = None
        sort_order: int
        closed: bool | None = None
        group_id: str | None = None
        view_mode: Literal['list', 'kanban', 'timeline'] | None = None
        permission: Literal['read', 'write', 'comment'] | None = None
        kind: Literal['TASK', 'NOTE'] | None = None
    }

    class TaskV1 {
        id: str
        project_id: str
        title: str
        is_all_day: bool
        completed_time: str | None = None
        content: str | None = None
        desc: str | None = None
        due_date: str | None = None
        items: list[ItemV1] | None = None
        priority: Literal[0, 1, 3, 5]
        reminders: list[str] | None = None
        repeat_flag: str | None = None
        sort_order: int
        start_date: str | None = None
        status: bool
        time_zone: str
    }

    class UpdateTaskV1 {
        id: str
        project_id: str
        title: str | None = None
        content: str | None = None
        desc: str | None = None
        is_all_day: bool | None = None
        start_date: str | None = None
        due_date: str | None = None
        time_zone: str | None = None
        reminders: list[str] | None = None
        repeat_flag: str | None = None
        priority: Literal[0, 1, 3, 5] | None = None
        sort_order: int | None = None
        items: list[UpdateItemV1] | None = None
    }

    class CreateProjectV1 {
        name: str
        color: Color | None = None
        sort_order: int | None = None
        view_mode: Literal['list', 'kanban', 'timeline'] | None = None
        kind: Literal['TASK', 'NOTE'] | None = None
    }

    class CreateTaskV1 {
        id: str | None = None
        title: str
        project_id: str
        content: str | None = None
        desc: str | None = None
        is_all_day: bool | None = None
        start_date: str | None = None
        due_date: str | None = None
        time_zone: str | None = None
        reminders: list[str] | None = None
        repeat_flag: str | None = None
        priority: Literal[0, 1, 3, 5] | None = None
        sort_order: int | None = None
        items: list[CreateItemV1] | None = None
    }

    class OAuthAuthorizeURLV1 {
        client_id: str
        scope: Literal['tasks:read tasks:write'] = 'tasks:read tasks:write'
        state: Any = None
        response_type: Literal['code'] = 'code'
        base_url: HttpUrl = 'https://ticktick.com/oauth/authorize'
    }

    class UpdateProjectV1 {
        name: str | None = None
        color: Color | None = None
        sort_order: int | None = None
        view_mode: Literal['list', 'kanban', 'timeline'] | None = None
        kind: Literal['TASK', 'NOTE'] | None = None
    }

    class ProjectDataV1 {
        project: ProjectV1
        tasks: list[TaskV1]
        columns: list[ColumnV1]
    }

    class OAuthTokenV1 {
        access_token: UUID
        expires_in: int
        token_type: Literal['bearer'] = 'bearer'
        scope: Literal['tasks:read tasks:write'] = 'tasks:read tasks:write'
    }

    class OAuthTokenURLV1 {
        client_id: str
        client_secret: str
        code: str
        oauth_redirect_url: HttpUrl = 'http://127.0.0.1:8080/'
        scope: Literal['tasks:read tasks:write'] = 'tasks:read tasks:write'
        grant_type: Literal['authorization_code'] = 'authorization_code'
        base_url: HttpUrl = 'https://ticktick.com/oauth/token'
    }

    OAuthAuthorizeURLV1 ..> HttpUrl
    OAuthAuthorizeURLV1 ..> Any
    OAuthTokenURLV1 ..> HttpUrl
    CreateProjectV1 ..> Color
    UpdateProjectV1 ..> Color
    CreateTaskV1 ..> CreateItemV1
    UpdateTaskV1 ..> UpdateItemV1
    OAuthTokenV1 ..> UUID
    ProjectDataV1 ..> ProjectV1
    ProjectDataV1 ..> ColumnV1
    ProjectDataV1 ..> TaskV1
    TaskV1 ..> ItemV1


```

!!! info
    This was auto-generated code by [pydantic-2-mermaid](https://github.com/EricWebsmith/pydantic-2-mermaid).
