"""Client module for TickTick API.

This module contains the client class for TickTick API. It provides methods to interact
with the API endpoints and handle the responses.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Union

import httpx
from loguru import logger

from pyticktick.models.v1.parameters.project import CreateProjectV1, UpdateProjectV1
from pyticktick.models.v1.parameters.task import CreateTaskV1, UpdateTaskV1
from pyticktick.models.v1.responses.project import (
    ProjectDataRespV1,
    ProjectRespV1,
    ProjectsRespV1,
)
from pyticktick.models.v1.responses.task import TaskRespV1
from pyticktick.models.v2.parameters.closed import GetClosedV2
from pyticktick.models.v2.parameters.project import PostBatchProjectV2
from pyticktick.models.v2.parameters.project_group import PostBatchProjectGroupV2
from pyticktick.models.v2.parameters.tag import DeleteTagV2, PostBatchTagV2, RenameTagV2
from pyticktick.models.v2.parameters.task import PostBatchTaskV2
from pyticktick.models.v2.parameters.task_parent import PostBatchTaskParentV2
from pyticktick.models.v2.responses.batch import BatchRespV2, GetBatchV2
from pyticktick.models.v2.responses.closed import ClosedRespV2
from pyticktick.models.v2.responses.tag import BatchTagRespV2
from pyticktick.models.v2.responses.task_parent import BatchTaskParentRespV2
from pyticktick.models.v2.responses.user import (
    UserProfileV2,
    UserStatisticsV2,
    UserStatusV2,
)
from pyticktick.pydantic import update_model_config
from pyticktick.retry import retry_api_v1
from pyticktick.settings import Settings

if TYPE_CHECKING:
    from pydantic import BaseModel


class Client(Settings):
    """Client class for TickTick API.

    The client class provides methods to interact with both the V1 and V2 API endpoints.
    This can be used to get, create, update, and delete, projects, tasks, tags, and
    other objects in the TickTick application.

    ??? example "Authenticating the client"
        The client class requires the user to be authenticated. The user must login to
        the V1 and/or V2 API endpoints before using the client class:

        ```python
        from pyticktick import Client

        client = Client(
            v1_client_id="client_id",
            v1_client_secret="client_secret",
            v1_token={
                "value": "fa371b10-8b95-442b-b4a5-11a9959d3590",
                "expiration": 1701701789,
            },
            v2_username="username",
            v2_password="password",
        )
        ```
        To see more details on how to authenticate, refer to
        [`pyticktick.Settings`](../settings.md).
        The client class inherits the `Settings` class, so all the setting
        configurations will be available in the client class.
    """

    @staticmethod
    def _model_dump(model: BaseModel) -> dict[str, Any]:
        return model.model_dump(by_alias=True, mode="json")

    @retry_api_v1()
    def _get_api_v1(self, endpoint: str) -> Any:  # noqa: ANN401
        try:
            resp = httpx.get(
                url=str(self.v1_base_url.join(endpoint)),
                headers=self.v1_headers,
            )
            resp.raise_for_status()
            if resp.content is None or len(resp.content) == 0:
                msg = "Response content is empty"
                raise ValueError(msg)
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

        return resp.json()

    @retry_api_v1()
    def _post_api_v1(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> Any:  # noqa: ANN401
        if data is None:
            data = {}
        try:
            resp = httpx.post(
                url=str(self.v1_base_url.join(endpoint)),
                headers=self.v1_headers,
                json=data,
            )
            resp.raise_for_status()
            if resp.content is None or len(resp.content) == 0:
                msg = "Response content is empty"
                raise ValueError(msg)
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

        return resp.json()

    @retry_api_v1()
    def _delete_api_v1(self, endpoint: str) -> None:
        try:
            resp = httpx.delete(
                url=str(self.v1_base_url.join(endpoint)),
                headers=self.v1_headers,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

    def get_projects_v1(self) -> ProjectsRespV1:
        """Get all projects from the V1 API.

        This method gets all the active projects from the [`GET /project`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-user-project)
        V1 endpoint.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            projects = client.get_projects_v1()
            for project in projects:
                print(project.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67ec23b18f08cf38dd957e10",
                "name": "Project 1",
                "color": null,
                "sort_order": -3298534883328,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            {
                "id": "67ec23b68f08cf38dd957ece",
                "name": "Project 2",
                "color": null,
                "sort_order": -2199023255552,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            {
                "id": "67ec23c28f08cf38dd957ff1",
                "name": "Project 3",
                "color": null,
                "sort_order": -1649267441664,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            ```

        Returns:
            ProjectsRespV1: List of projects from the V1 API.
        """
        resp = self._get_api_v1("/project")
        return ProjectsRespV1.model_validate(resp)

    def get_project_v1(self, project_id: str) -> ProjectRespV1:
        """Get a single project from the V1 API.

        This method calls the [`GET /project/{project_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-project-by-id)
        V1 endpoint, where `project_id` is the identifier of the project. It is
        equivalent to `get_projects_v1` followed by filtering to the project with the
        given `project_id`.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            project = client.get_project_v1("67ec23b18f08cf38dd957e10")
            print(project.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67ec23b18f08cf38dd957e10",
                "name": "Project 1",
                "color": null,
                "sort_order": -3298534883328,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            ```
        Args:
            project_id (str): Identifier of the project to retrieve.

        Returns:
            ProjectRespV1: Project object containing project details.
        """
        resp = self._get_api_v1(f"/project/{project_id}")
        return ProjectRespV1.model_validate(resp)

    def get_project_with_data_v1(self, project_id: str) -> ProjectDataRespV1:
        """Get details of a single project from the V1 API.

        This method calls the [`GET /project/{project_id}/data`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-project-with-data)
        V1 endpoint, where `project_id` is the identifier of the project. It provides a
        superset of the information available in `get_project_v1`.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            project_data = client.get_project_with_data_v1("67ec23b18f08cf38dd957e10")
            print(project_data.model_dump())
            ```

            will output:
            ```json
            {
                "project": {
                    "id": "67ec23b18f08cf38dd957e10",
                    "name": "Project 1",
                    "color": null,
                    "sort_order": -3298534883328,
                    "closed": null,
                    "group_id": null,
                    "view_mode": "list",
                    "permission": null,
                    "kind": "TASK"
                },
                "tasks": [
                    {
                        "id": "67ec273212e1101e875f078b",
                        "project_id": "67ec23b18f08cf38dd957e10",
                        "title": "Task 1",
                        "is_all_day": false,
                        "completed_time": null,
                        "content": "",
                        "desc": null,
                        "due_date": null,
                        "items": null,
                        "priority": 0,
                        "reminders": null,
                        "repeat_flag": null,
                        "sort_order": -4398046511104,
                        "start_date": null,
                        "status": false,
                        "time_zone": "America/Chicago",
                        "etag": "k9r8mw9b",
                        "kind": "TEXT"
                    },
                    {
                        "id": "67ec273412e1101e875f0791",
                        "project_id": "67ec23b18f08cf38dd957e10",
                        "title": "Task 2 ",
                        "is_all_day": false,
                        "completed_time": null,
                        "content": "",
                        "desc": null,
                        "due_date": null,
                        "items": null,
                        "priority": 0,
                        "reminders": null,
                        "repeat_flag": null,
                        "sort_order": -2199023255552,
                        "start_date": null,
                        "status": false,
                        "time_zone": "America/Chicago",
                        "etag": "1q51czxo",
                        "kind": "TEXT"
                    },
                    {
                        "id": "67ec273a12e1101e875f079e",
                        "project_id": "67ec23b18f08cf38dd957e10",
                        "title": "Task 3",
                        "is_all_day": false,
                        "completed_time": null,
                        "content": "",
                        "desc": null,
                        "due_date": null,
                        "items": null,
                        "priority": 0,
                        "reminders": null,
                        "repeat_flag": null,
                        "sort_order": -1099511627776,
                        "start_date": null,
                        "status": false,
                        "time_zone": "America/Chicago",
                        "etag": "pan652fb",
                        "kind": "TEXT"
                    }
                ],
                "columns": []
            }
            ```
        Args:
            project_id (str): Identifier of the project to retrieve.

        Returns:
            ProjectDataRespV1: Project data object containing project and task details.
        """
        resp = self._get_api_v1(f"/project/{project_id}/data")
        return ProjectDataRespV1.model_validate(resp)

    def create_project_v1(
        self,
        data: Union[CreateProjectV1, dict[str, Any]],
    ) -> ProjectRespV1:
        """Create a project in the V1 API.

        This method creates a new project in the TickTick application using the
        [`POST /project`](https://developer.ticktick.com/docs/index.html#/openapi?id=create-project)
        V1 endpoint. The `data` parameter can be a `CreateProjectV1` model or a
        dictionary that matches the same structure. The method returns the created
        project as a `ProjectV1` model.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v1 import CreateProjectV1

            client = Client()
            project = client.create_project_v1(
                data=CreateProjectV1(
                    name="Test Project",
                    color="#002fa7",
                    sort_order=50,
                    view_mode="list",
                    kind="TASK",
                ),
            )
            print(project.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67ec9d148f08723133663fd1",
                "name": "Test Project",
                "color": "#002fa7",
                "sort_order": 50,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            ```

        Args:
            data (Union[CreateProjectV1, dict[str, Any]]): Data to create the project.

        Returns:
            ProjectRespV1: Created project.
        """
        if isinstance(data, dict):
            data = CreateProjectV1.model_validate(data)
        resp = self._post_api_v1("/project", data=self._model_dump(data))
        return ProjectRespV1.model_validate(resp)

    def update_project_v1(
        self,
        project_id: str,
        data: Union[UpdateProjectV1, dict[str, Any]],
    ) -> ProjectRespV1:
        """Update a project in the V1 API.

        This method updates an existing project in the TickTick application using the
        [`POST /project/{project_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=update-project)
        V1 endpoint. The `data` parameter can be an `UpdateProjectV1` model or a
        dictionary that matches the same structure. The method returns the updated
        project as a `ProjectV1` model.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v1 import UpdateProjectV1

            client = Client()
            project = client.update_project_v1(
                project_id="67ec9d148f08723133663fd1",
                data=UpdateProjectV1(
                    name="Updated Project",
                    color="#ee6c4d",
                    sort_order=100,
                    view_mode="list",
                    kind="TASK",
                ),
            )
            print(project.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67ec9d148f08723133663fd1",
                "name": "Updated Project",
                "color": "#ee6c4d",
                "sort_order": 100,
                "closed": null,
                "group_id": null,
                "view_mode": "list",
                "permission": null,
                "kind": "TASK"
            }
            ```
        Args:
            project_id (str): Identifier of the project to update.
            data (Union[UpdateProjectV1, dict[str, Any]]): Data to update the project.

        Returns:
            ProjectRespV1: Updated project.
        """
        if isinstance(data, dict):
            data = UpdateProjectV1.model_validate(data)
        resp = self._post_api_v1(f"/project/{project_id}", data=self._model_dump(data))
        return ProjectRespV1.model_validate(resp)

    def delete_project_v1(self, project_id: str) -> None:
        """Delete a project in the V1 API.

        This method deletes an existing project in the TickTick application using the
        [`DELETE /project/{project_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=delete-project)
        V1 endpoint. The `project_id` parameter is the identifier of the project to
        delete.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            client.delete_project_v1("67ec9d148f08723133663fd1")
            ```
            This will return nothing if the project is successfully deleted.

        Args:
            project_id (str): Identifier of the project to delete.
        """
        self._delete_api_v1(f"/project/{project_id}")

    def get_task_v1(self, project_id: str, task_id: str) -> TaskRespV1:
        """Get a single task from the V1 API.

        This method calls the [`GET /project/{project_id}/task/{task_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=get-task-by-project-id-and-task-id)
        V1 endpoint, where `project_id` and `task_id` are the identifiers of the
        project and task, respectively.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            task = client.get_task_v1(
                project_id="67ec23b18f08cf38dd957e10",
                task_id="67ec273212e1101e875f078b",
            )
            print(task.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67ec273212e1101e875f078b",
                "project_id": "67ec23b18f08cf38dd957e10",
                "title": "Task 1",
                "is_all_day": false,
                "completed_time": null,
                "content": "",
                "desc": null,
                "due_date": null,
                "items": null,
                "priority": 0,
                "reminders": null,
                "repeat_flag": null,
                "sort_order": -4398046511104,
                "start_date": null,
                "status": false,
                "time_zone": "America/Chicago",
                "etag": "k9r8mw9b",
                "kind": "TEXT"
            }
            ```

        Args:
            project_id (str): Identifier of the project containing the task.
            task_id (str): Identifier of the task to retrieve.

        Returns:
            TaskRespV1: The task object retrieved from the API.
        """
        resp = self._get_api_v1(f"/project/{project_id}/task/{task_id}")
        return TaskRespV1.model_validate(resp)

    def create_task_v1(self, data: Union[CreateTaskV1, dict[str, Any]]) -> TaskRespV1:
        """Create a task in the V1 API.

        This method creates a new task in the TickTick application using the [`POST /task`](https://developer.ticktick.com/docs/index.html#/openapi?id=create-task)
        V1 endpoint. The `data` parameter can be a `CreateTaskV1` model or a dictionary
        that matches the same structure. The method returns the created task as a
        `TaskRespV1` model.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v1 import CreateTaskV1

            client = Client()
            task = client.create_task_v1(
                data=CreateTaskV1(
                    project_id="67eca3918f08e7c706354740",
                    title="Test Task",
                    content="This is a test task.",
                    start_date="2025-11-13T03:00:00+0000",
                    due_date="2025-11-14T03:00:00+0000",
                ),
            )
            print(task.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67eca3b78f08cf38dda26ca4",
                "project_id": "67eca3918f08e7c706354740",
                "title": "Test Task",
                "is_all_day": false,
                "completed_time": null,
                "content": "This is a test task.",
                "desc": null,
                "due_date": "2025-11-14T03:00:00.000+0000",
                "items": null,
                "priority": 0,
                "reminders": null,
                "repeat_flag": null,
                "sort_order": -1099511627776,
                "start_date": "2025-11-14T03:00:00.000+0000",
                "status": false,
                "time_zone": "America/Chicago",
                "tags": [],
                "etag": "8yp4pfmh",
                "kind": "TEXT"
            }
            ```
        Args:
            data (Union[CreateTaskV1, dict[str, Any]]): Data to create the task.

        Returns:
            TaskRespV1: Created task object.
        """
        if isinstance(data, dict):
            data = CreateTaskV1.model_validate(data)
        resp = self._post_api_v1("/task", self._model_dump(data))
        return TaskRespV1.model_validate(resp)

    def update_task_v1(
        self,
        task_id: str,
        data: Union[UpdateTaskV1, dict[str, Any]],
    ) -> TaskRespV1:
        """Update a task in the V1 API.

        This method updates an existing task in the TickTick application using the
        [`POST /task/{task_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=update-task)
        V1 endpoint. The `data` parameter can be an `UpdateTaskV1` model or a dictionary
        that matches the same structure. The method returns the updated task as a
        `TaskRespV1` model.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v1 import UpdateTaskV1

            client = Client()
            task = client.update_task_v1(
                task_id="67eca3b78f08cf38dda26ca4",
                data=UpdateTaskV1(
                    id="67eca3b78f08cf38dda26ca4",
                    project_id="67eca3918f08e7c706354740",
                    title="Updated test task",
                    content="This is a test task that has been updated.",
                    start_date="2026-03-13T03:00:00+0000",
                    due_date="2026-03-14T03:00:00+0000",
                ),
            )
            print(task.model_dump())
            ```

            will output:
            ```json
            {
                "id": "67eca3b78f08cf38dda26ca4",
                "project_id": "67eca3918f08e7c706354740",
                "title": "Updated test task",
                "is_all_day": false,
                "completed_time": null,
                "content": "This is a test task that has been updated.",
                "desc": null,
                "due_date": "2026-03-14T03:00:00.000+0000",
                "items": null,
                "priority": 0,
                "reminders": null,
                "repeat_flag": null,
                "sort_order": -1099511627776,
                "start_date": "2026-03-14T03:00:00.000+0000",
                "status": false,
                "time_zone": "America/Chicago",
                "etag": "3x4xgnmn",
                "kind": "TEXT"
            }
            ```

        Args:
            task_id (str): Identifier of the task to update.
            data (Union[UpdateTaskV1, dict[str, Any]]): Data to update the task.

        Returns:
            TaskRespV1: Updated task.
        """
        if isinstance(data, dict):
            data = UpdateTaskV1.model_validate(data)
        resp = self._post_api_v1(f"/task/{task_id}", self._model_dump(data))
        return TaskRespV1.model_validate(resp)

    def complete_task_v1(self, project_id: str, task_id: str) -> None:
        """Complete a task in the V1 API.

        This method marks a task as completed in the TickTick application using the
        [`POST /project/{project_id}/task/{task_id}/complete`](https://developer.ticktick.com/docs/index.html#/openapi?id=complete-task)
        V1 endpoint. The `project_id` and `task_id` parameters are the identifiers of
        the project and task to complete.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            client.complete_task_v1(
                project_id="67eca3918f08e7c706354740",
                task_id="67eca3b78f08cf38dda26ca4",
            )
            ```
            This will return nothing if the task is successfully completed.

        Args:
            project_id (str): Identifier of the project containing the task.
            task_id (str): Identifier of the task to complete.

        Raises:
            ValueError: If there is an error in HTTP request or response, except when
                the response content is empty.
        """
        try:
            self._post_api_v1(f"/project/{project_id}/task/{task_id}/complete")
        except ValueError as e:
            if "Response content is empty" in str(e):
                return
            raise

    def delete_task_v1(self, project_id: str, task_id: str) -> None:
        """Delete a task in the V1 API.

        This method deletes an existing task in the TickTick application using the
        [`DELETE /project/{project_id}/task/{task_id}`](https://developer.ticktick.com/docs/index.html#/openapi?id=delete-task)
        V1 endpoint. The `project_id` and `task_id` parameters are the identifiers of
        the project and task to delete.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            client.delete_task_v1(
                project_id="67eca3918f08e7c706354740",
                task_id="67eca3b78f08cf38dda26ca4",
            )
            ```
            This will return nothing if the task is successfully deleted.

        Args:
            project_id (str): Identifier of the project containing the task.
            task_id (str): Identifier of the task to delete.
        """
        self._delete_api_v1(f"/project/{project_id}/task/{task_id}")

    def _get_api_v2(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> Any:  # noqa: ANN401
        try:
            resp = httpx.get(
                url=str(self.v2_base_url.join(endpoint)),
                headers=self.v2_headers,
                cookies=self.v2_cookies,
                params=data,
            )
            resp.raise_for_status()
            if resp.content is None or len(resp.content) == 0:
                msg = "Response content is empty"
                raise ValueError(msg)
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

        return resp.json()

    def _post_api_v2(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> Any:  # noqa: ANN401
        if data is None:
            data = {}
        try:
            resp = httpx.post(
                url=str(self.v2_base_url.join(endpoint)),
                headers=self.v2_headers,
                cookies=self.v2_cookies,
                json=data,
            )
            resp.raise_for_status()
            if resp.content is None or len(resp.content) == 0:
                msg = "Response content is empty"
                raise ValueError(msg)
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

        return resp.json()

    def _delete_api_v2(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        try:
            resp = httpx.delete(
                url=str(self.v2_base_url.join(endpoint)),
                headers=self.v2_headers,
                cookies=self.v2_cookies,
                params=data,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

    def get_profile_v2(self) -> UserProfileV2:
        """Get the user profile from the V2 API.

        This method gets the user profile from the `GET /user/profile` V2 endpoint.
        This endpoint provides information about the user's profile, including their
        name, email, and other details.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            profile = client.get_profile_v2()
            print(profile.model_dump())
            ```

            will output:
            ```json
            {
                "etimestamp": null,
                "username": "username@username.com",
                "site_domain": "ticktick.com",
                "created_campaign": "",
                "created_device_info": null,
                "filled_password": true,
                "account_domain": null,
                "extenal_id": null,
                "email": null,
                "verified_email": true,
                "faked_email": false,
                "phone": null,
                "name": null,
                "given_name": null,
                "family_name": null,
                "link": null,
                "picture": "https://secure.gravatar.com/avatar/63a5deb18f37c35393c70de1ef53cb6a;size=50?default=https://d3qg9zffrnl4ph.cloudfront.net/image/avatar.png",
                "gender": null,
                "locale": "en_US",
                "user_code": "58822351-89dd-432a-90ed-772a47fb15b5",
                "ver_code": null,
                "ver_key": null,
                "external_id": null,
                "phone_without_country_code": null,
                "display_name": "username@username.com"
            }
            ```

        Returns:
            UserProfileV2: The user profile object retrieved from the API.
        """
        resp = self._get_api_v2("/user/profile")
        if self.override_forbid_extra:
            update_model_config(UserProfileV2, extra="allow")
        return UserProfileV2.model_validate(resp)

    def get_status_v2(self) -> UserStatusV2:
        """Get the user status from the V2 API.

        This method gets the user status from the `GET /user/status` V2 endpoint. This
        user "status" is mainly about the user's subscription status, rather than
        their current activity on TickTick. This may still be useful for confirming if
        a user is a premium subscriber or not. A free account is much more limited in
        terms of its features, and TickTick does not provide feedback on if a request
        fails due to a hitting a free limit or not.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            status = client.get_status_v2()
            print(status.model_dump())
            ```

            will output:
            ```json
            {
                "user_id": "213928392",
                "user_code": "58822351-89dd-432a-90ed-772a47fb15b5",
                "username": "username@username.com",
                "team_pro": false,
                "pro_start_date": "2024-12-25T16:18:28.000+0000",
                "pro_end_date": "2026-12-26T16:18:19.000+0000",
                "subscribe_type": "stripe_subscribe",
                "subscribe_freq": "Year",
                "need_subscribe": false,
                "freq": "Year",
                "inbox_id": "inbox213928392",
                "team_user": false,
                "active_team_user": false,
                "free_trial": false,
                "pro": true,
                "ds": false,
                "time_stamp": 1735898435,
                "grace_period": false
            }
            ```

        Returns:
            UserStatusV2: The user status object retrieved from the API.
        """
        resp = self._get_api_v2("/user/status")
        if self.override_forbid_extra:
            update_model_config(UserStatusV2, extra="allow")
        return UserStatusV2.model_validate(resp)

    def get_statistics_v2(self) -> UserStatisticsV2:
        """Get user statistics from the V2 API.

        This method gets the user statistics from the `GET /statistics/general` V2
        endpoint. This endpoint provides information about the user's statistics, such
        as number of tasks completed per day, week, or month, and other metrics.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            statistics = client.get_statistics_v2()
            print(statistics.model_dump())
            ```

            will output:
            ```json
            {
                "score": 8211,
                "level": 7,
                "yesterday_completed": 6,
                "today_completed": 4,
                "total_completed": 2187,
                "score_by_day": {
                    "2025-03-27": 7939,
                    ...
                    "2025-04-01": 8149,
                    "2025-04-02": 8189
                },
                "task_by_day": {
                    "2025-03-27": {
                        "complete_count": 3,
                        "not_complete_count": 2
                    },
                    ...
                    "2025-04-01": {
                        "complete_count": 6,
                        "not_complete_count": 1
                    },
                    "2025-04-02": {
                        "complete_count": 4,
                        "not_complete_count": 0
                    }
                },
                "task_by_week": {
                    "2025-02-16": {
                        "complete_count": 214,
                        "not_complete_count": 3
                    },
                    ...
                    "2025-03-23": {
                        "complete_count": 64,
                        "not_complete_count": 8
                    },
                    "2025-03-30": {
                        "complete_count": 22,
                        "not_complete_count": 10
                    }
                },
                "task_by_month": {
                    "2024-10-01": {
                        "complete_count": 0,
                        "not_complete_count": 0
                    },
                    ...
                    "2025-03-01": {
                        "complete_count": 654,
                        "not_complete_count": 14
                    },
                    "2025-04-01": {
                        "complete_count": 10,
                        "not_complete_count": 29
                    }
                },
                "today_pomo_count": 0,
                "yesterday_pomo_count": 0,
                "total_pomo_count": 0,
                "today_pomo_duration": 0,
                "yesterday_pomo_duration": 0,
                "total_pomo_duration": 0,
                "pomo_goal": 0,
                "pomo_duration_goal": 0,
                "pomo_by_day": {},
                "pomo_by_week": {},
                "pomo_by_month": {}
            }
            ```

        Returns:
            UserStatisticsV2: The user statistics object retrieved from the API.
        """
        resp = self._get_api_v2("/statistics/general")
        if self.override_forbid_extra:
            update_model_config(UserStatisticsV2, extra="allow")
        return UserStatisticsV2.model_validate(resp)

    def get_project_all_closed_v2(
        self,
        data: Union[GetClosedV2, dict[str, Any]],
    ) -> ClosedRespV2:
        """Get all completed or abandoned tasks from the V2 API.

        This method gets all completed or abandoned tasks from the
        `GET /project/all/closed` V2 endpoint. Abandoned tasks are referred to as
        _won't do_ tasks by TickTick. They have some documentation on them [here](https://help.ticktick.com/articles/7055782408586526720#won't-do).

        ??? example "Get all completed tasks"
            ```python hl_lines="4"
            from pyticktick import Client
            from pyticktick.models.v2 import GetClosedV2

            client = Client()
            resp = client.get_project_all_closed_v2(GetClosedV2(status="Completed"))

            print(resp.model_dump())
            ```

            will output:
            ```json
            [
                {
                    "child_ids": null,
                    "completed_time": "2020-04-25T15:25:22Z",
                    "content": "",
                    "created_time": "2020-03-23T15:02:17Z",
                    "desc": "",
                    "due_date": "2020-04-22T05:00:00Z",
                    "etag": "czt0y615",
                    "id": "680be962126b914e0ff59951",
                    "is_all_day": true,
                    "is_floating": false,
                    "items": [],
                    "kind": "TEXT",
                    "modified_time": "2025-04-15T15:15:35Z",
                    "parent_id": null,
                    "priority": 0,
                    "progress": 0,
                    "project_id": "inbox213928392",
                    "repeat_from": 2,
                    "reminder": null,
                    "reminders": [],
                    "repeat_flag": null,
                    "repeat_task_id": "67e022795985d10fd77abff8",
                    "start_date": "2020-04-21T05:00:00Z",
                    "status": 2,
                    "tags": [...],
                    "title": "Completed task",
                    "time_zone": "America/New_York",
                    "attachments": [],
                    "annoying_alert": null,
                    "column_id": null,
                    "comment_count": 0,
                    "completed_user_id": 213928392,
                    "creator": 213928392,
                    "sort_order": -6917533425701748736
                },
                ...
            ]
            ```
            You will notice that the `status` field is set to `2` for completed tasks.

        ??? example "Get all abandoned tasks"
            ```python hl_lines="4"
            from pyticktick import Client
            from pyticktick.models.v2 import GetClosedV2

            client = Client()
            resp = client.get_project_all_closed_v2(GetClosedV2(status="Abandoned"))

            print(resp.model_dump())
            ```

            will output:
            ```json
            [
                {
                    "child_ids": null,
                    "completed_time": "2025-04-15T15:15:35Z",
                    "content": "",
                    "created_time": "2025-03-23T15:02:17Z",
                    "desc": "",
                    "due_date": "2025-04-15T05:00:00Z",
                    "etag": "xkpljy8f",
                    "id": "67fe78173624110bff1cb96a",
                    "is_all_day": true,
                    "is_floating": false,
                    "items": [],
                    "kind": "TEXT",
                    "modified_time": "2025-04-08T15:00:26Z",
                    "parent_id": null,
                    "priority": 0,
                    "progress": 0,
                    "project_id": "676c6de2c447d18b6d0a8bac",
                    "repeat_from": 2,
                    "reminder": null,
                    "reminders": [],
                    "repeat_flag": null,
                    "repeat_task_id": "67e022795985d10fd77abff8",
                    "start_date": "2025-04-15T05:00:00Z",
                    "status": -1,
                    "tags": ["family"],
                    "title": "\u260e\ufe0f Call Mom",
                    "time_zone": "America/Chicago",
                    "attachments": [],
                    "annoying_alert": null,
                    "column_id": null,
                    "comment_count": 0,
                    "completed_user_id": 125986193,
                    "creator": 125986193,
                    "sort_order": -6917533425701748736
                }
            ]
            ```
            You will notice that the `status` field is set to `-1` for abandoned tasks.

        Args:
            data (Union[GetClosedV2, dict[str, Any]]): Data to get the completed /
                abandoned tasks.

        Returns:
            ClosedRespV2: The completed / abandoned tasks object retrieved from the API.

        """
        if isinstance(data, dict):
            data = GetClosedV2.model_validate(data)
        resp = self._get_api_v2("/project/all/closed", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(ClosedRespV2, extra="allow")
        return ClosedRespV2.model_validate(resp)

    def get_batch_v2(self) -> GetBatchV2:
        """Get all active objects for the current user from the V2 API.

        This method gets the status of all objects for the current user from the
        `GET /batch/check/0` V2 endpoint. This endpoint provides information about
        the status of all active objects, including projects, tasks, etc. The structure
        of the response is a little confusing. It seems like it was designed to be used
        as an [Entity Bean](https://en.wikipedia.org/wiki/Entity_Bean),
        making it easy to sync back to TickTick.

        ??? example "Example"
            ```python hl_lines="4"
            from pyticktick import Client

            client = Client()
            batch = client.get_batch_v2()
            print(batch.model_dump())
            ```

            will output:
            ```json
            {
                "inbox_id": "inbox213928392",
                "project_groups": [...],
                "project_profiles": [...],
                "sync_task_bean": {
                    "update": [...],
                    "add": [],
                    "delete": [],
                    "empty": false,
                    "tag_update": []
                },
                "tags": [...],
                "check_point": 2658743443697,
                "checks": null,
                "filters": [...],
                "sync_order_bean": {
                    "orderByType": {}
                },
                "sync_order_bean_v3": {
                    "order_by_type": {
                    "taskBy#dueDate|20250224_dueDate": {
                        "all": {
                        "changed": [...],
                        "deleted": []
                        }
                    },
                    "taskBy#dueDate|20250109_dueDate": {
                        "all": {
                        "changed": [],
                        "deleted": [...]
                        }
                    }
                    }
                },
                "sync_task_order_bean": {
                    "task_order_by_date": {},
                    "task_order_by_priority": {},
                    "task_order_by_project": {}
                },
                "remind_changes": []
            }
            ```
            This response is so large, that it was trimmed down significantly. Anywhere
            you see `...`, it means there should have been more data.

        Returns:
            GetBatchV2: The batch object retrieved from the API.
        """
        resp = self._get_api_v2("/batch/check/0")
        if self.override_forbid_extra:
            update_model_config(GetBatchV2, extra="allow")
        return GetBatchV2.model_validate(resp)

    def post_project_v2(
        self,
        data: Union[PostBatchProjectV2, dict[str, Any]],
    ) -> BatchRespV2:
        """Create, update, or delete projects in bulk against the V2 API.

        This method creates, updates, and deletes projects in bulk using the
        `POST /batch/project` V2 endpoint. TickTick refers to these as lists, and you
        can read more with [this guide](https://help.ticktick.com/articles/7055782283059396608).

        ??? example "Add a project"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchProjectV2, CreateProjectV2

            client = Client()
            resp = client.post_project_v2(
                data=PostBatchProjectV2(
                    add=[
                        CreateProjectV2(
                            name="test_project",
                            group_id="680be2008f08b6b4618a3c89",
                            color="blue",
                            view_mode="list",
                        ),
                    ],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "680bab7c8f08b6b4618b657d": "8j9rd7ug"
                }
            }
            ```

        ??? example "Update a project"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchProjectV2, UpdateProjectV2

            client = Client()
            resp = client.post_project_v2(
                data=PostBatchProjectV2(
                    update=[
                        UpdateProjectV2(
                            id="680bab7c8f08b6b4618b657d",
                            name="test_project_renamed",
                            color="red",
                        ),
                    ],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "680bab7c8f08b6b4618b657d": "2a5jlehm"
                }
            }
            ```

        ??? example "Delete a project"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchProjectV2

            client = Client()
            resp = client.post_project_v2(
                data=PostBatchProjectV2(delete=["680bab7c8f08b6b4618b657d"]),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {}
            }
            ```

        Args:
            data (Union[PostBatchProjectV2, dict[str, Any]]): Data to create, update,
                or delete projects.

        Returns:
            BatchRespV2: The response object containing the status of the batch
                operation.
        """
        if isinstance(data, dict):
            data = PostBatchProjectV2.model_validate(data)
        resp = self._post_api_v2("/batch/project", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(BatchRespV2, extra="allow")
        return BatchRespV2.model_validate(resp)

    def post_task_v2(self, data: Union[PostBatchTaskV2, dict[str, Any]]) -> BatchRespV2:
        """Create, update, or delete tasks in bulk against the V2 API.

        This method creates, updates, and deletes tasks in bulk using the
        `POST /batch/task` V2 endpoint. TickTick has a handful of guides on how to use
        tasks, which you can find [here](https://help.ticktick.com/articles/7055782436621254656).

        The degree of configuration is quite high for tasks, so the examples below show
        just a limited number of fields to configure. The full list of fields can be
        found in the `PostBatchTaskV2` model.

        ??? example "Add a task"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTaskV2, CreateTaskV2

            client = Client()
            resp = client.post_task_v2(
                data=PostBatchTaskV2(
                    add=[
                        CreateTaskV2(
                            title="test task",
                            project_id="681180d78f08af4931b657e8",
                            desc="test description",
                            is_all_day=False,
                            start_date="2023-01-01T00:00:00Z",
                            due_date="2023-01-03T00:00:00Z",
                            time_zone="America/New_York",
                            repeat_flag="RRULE:FREQ=DAILY;INTERVAL=1",
                            priority=1,
                            items=[CreateItemV2(title="test item", status=0)],
                            kind="CHECKLIST",
                            status=0,
                        ),
                    ],
                ),
            )

            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "6812d7d68f081558b9bfdb6b": "0gntz779"
                }
            }
            ```

        ??? example "Update a task"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTaskV2, UpdateTaskV2

            client = Client()
            resp = client.post_task_v2(
                data=PostBatchTaskV2(
                    update=[
                        UpdateTaskV2(
                            id="6812d7d68f081558b9bfdb6b",
                            title="test task updated",
                            project_id="681180d78f08af4931b657e8",
                            content="test description is now content",
                            due_date="2023-01-03T00:00:00Z",
                            repeat_flag="RRULE:FREQ=WEEKLY;INTERVAL=1",
                            kind="TEXT",
                        ),
                    ],
                ),
            )

            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "6812d7d68f081558b9bfdb6b": "0r7p6no6"
                }
            }
            ```

        ??? example "Delete a task"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTaskV2, DeleteTaskV2

            client = Client()
            resp = client.post_task_v2(
                data=PostBatchTaskV2(
                    delete=[
                        DeleteTaskV2(
                            task_id="6812d7d68f081558b9bfdb6b",
                            project_id="681180d78f08af4931b657e8",
                        ),
                    ],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {}
            }
            ```

        Args:
            data (Union[PostBatchTaskV2, dict[str, Any]]): Data to create, update,
                or delete tasks.

        Returns:
            BatchRespV2: The response object containing the status of the batch
                operation.
        """
        if isinstance(data, dict):
            data = PostBatchTaskV2.model_validate(data)
        resp = self._post_api_v2("/batch/task", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(BatchRespV2, extra="allow")
        return BatchRespV2.model_validate(resp)

    def post_project_group_v2(
        self,
        data: Union[PostBatchProjectGroupV2, dict[str, Any]],
    ) -> BatchRespV2:
        """Create, update, or delete project groups in bulk against the V2 API.

        The method creates, updates, and deletes project groups in bulk using the
        `POST /batch/projectGroup` V2 endpoint. This used to create what TickTick calls
        folders. They have a [small guide](https://help.ticktick.com/articles/7055782296019795968)
        on them if you want to learn more.

        ??? example "Add a project group"
            ```python hl_lines="8"
            from pyticktick import Client
            from pyticktick.models.v2 import (
                PostBatchProjectGroupV2,
                CreateProjectGroupV2,
            )

            client = Client()
            resp = client.post_project_group_v2(
                data=PostBatchProjectGroupV2(
                    add=[CreateProjectGroupV2(name="test_group")],
                )
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "680be2008f08b6b4618a3c89": "znr6783z"
                }
            }
            ```

        ??? example "Update a project group"
            ```python hl_lines="8"
            from pyticktick import Client
            from pyticktick.models.v2 import (
                PostBatchProjectGroupV2,
                UpdateProjectGroupV2,
            )

            client = Client()
            resp = client.post_project_group_v2(
                data=PostBatchProjectGroupV2(
                    update=[
                        UpdateProjectGroupV2(
                            name="test_group_renamed",
                            id="680be2008f08b6b4618a3c89",
                        ),
                    ],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "680be2008f08b6b4618a3c89": "2qoky0fw"
                }
            }
            ```

        ??? example "Delete a project group"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchProjectGroupV2

            client = Client()
            resp = client.post_project_group_v2(
                data=PostBatchProjectGroupV2(delete=["680be2008f08b6b4618a3c89"]),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {}
            }
            ```

        Args:
            data (Union[PostBatchProjectGroupV2, dict[str, Any]]): Data to create,
                update, or delete project groups.

        Returns:
            BatchRespV2: The response object containing the status of the batch
                operation.
        """
        if isinstance(data, dict):
            data = PostBatchProjectGroupV2.model_validate(data)
        resp = self._post_api_v2("/batch/projectGroup", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(BatchRespV2, extra="allow")
        return BatchRespV2.model_validate(resp)

    def post_task_parent_v2(
        self,
        data: Union[PostBatchTaskParentV2, list[Any]],
    ) -> BatchTaskParentRespV2:
        """Set or unset a task parent in bulk against the V2 API.

        This method sets and/or unsets task parents in bulk using the
        `POST /batch/taskParent` V2 endpoint. This is used to create what
        TickTick refers to as subtasks. This is notably different from a
        checklist task. You can see [TickTick's guide on subtasks / _Multilevel Tasks_](https://help.ticktick.com/articles/7055782219767349248)
        for more information.

        ??? example "Set and unset task parents"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import (
                PostBatchTaskParentV2,
                SetTaskParentV2,
                UnSetTaskParentV2,
            )

            client = Client()
            resp = client.post_task_parent_v2(
                data=PostBatchTaskParentV2(
                    [
                        SetTaskParentV2(
                            project_id="681180d78f08af4931b657e8",
                            parent_id="68117d7327de22223ea29ffd",
                            task_id="68117d7627de22223ea2a003",
                        ),
                        UnSetTaskParentV2(
                            project_id="681180d78f08af4931b657e8",
                            old_parent_id="6811803d27de22223ea2a011",
                            task_id="6811803f27de22223ea2a017",
                        ),
                    ],
                ),
            )

            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "68117d7627de22223ea2a003": {
                        "id": "68117d7627de22223ea2a003",
                        "parent_id": "68117d7327de22223ea29ffd",
                        "child_ids": null,
                        "etag": "07s4q5a6"
                    },
                    "68117d7327de22223ea29ffd": {
                        "id": "68117d7327de22223ea29ffd",
                        "parent_id": null,
                        "child_ids": [
                            "68117d7627de22223ea2a003"
                        ],
                        "etag": "df6fxmtg"
                    },
                    "6811803f27de22223ea2a017": {
                        "id": "6811803f27de22223ea2a017",
                        "parent_id": null,
                        "child_ids": null,
                        "etag": "fhuwhgge"
                    },
                    "6811803d27de22223ea2a011": {
                        "id": "6811803d27de22223ea2a011",
                        "parent_id": null,
                        "child_ids": [],
                        "etag": "idwvx8sx"
                    }
                }
            }
            ```

        Args:
            data (Union[PostBatchTaskParentV2, list[Any]]): Data to set or unset task
                parents.

        Returns:
            BatchTaskParentRespV2: Response from the API after setting or unsetting the
            task parents.
        """
        if isinstance(data, list):
            data = PostBatchTaskParentV2.model_validate(data)
        resp = self._post_api_v2("/batch/taskParent", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(BatchTaskParentRespV2, extra="allow")
        return BatchTaskParentRespV2.model_validate(resp)

    def post_tag_v2(
        self,
        data: Union[PostBatchTagV2, dict[str, Any]],
    ) -> BatchTagRespV2:
        """Create or update tags in bulk against the V2 API.

        This method creates or updates tags in bulk using the `POST /batch/tag` V2
        endpoint. Tags are used to help organize tasks. Tasks can be tagged with
        multiple tags, and they can be nested as well. They are often associated with
        categories, status, or location. You can see [TickTick's guide](https://help.ticktick.com/articles/7055782255804809216)
        for more info.

        !!! warning "Not all operations supported"
            While batch operations usually support adding, updating, and deleting, this
            endpoint only supports adding and updating tags. Deleting tags supported
            separately, see `delete_tag_v2`. Updating tag names is also supported,
            separately through the `put_rename_tag_v2` function.

        ??? example "Add a tag"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTagV2, CreateTagV2

            client = Client()
            resp = client.post_tag_v2(
                data=PostBatchTagV2(
                    add=[CreateTagV2(label="test_tag", color="#002fa7")],
                )
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "test_tag": "6pkt0zoq"
                }
            }
            ```
        ??? example "Update a tag"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTagV2, UpdateTagV2

            client = Client()
            resp = client.post_tag_v2(
                data=PostBatchTagV2(
                    update=[UpdateTagV2(label="test_tag", color="#ee6c4d")],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "test_tag": "fcutpk78"
                }
            }
            ```

        ??? example "Add a nested tag"
            ```python hl_lines="5 14"
            from pyticktick import Client
            from pyticktick.models.v2 import PostBatchTagV2, CreateTagV2, UpdateTagV2

            client = Client()
            resp = client.post_tag_v2(
                data=PostBatchTagV2(
                    add=[
                        CreateTagV2(label="parent_tag", color="#002fa7"),
                        CreateTagV2(label="child_tag", color="#ee6c4d"),
                    ],
                ),
            )
            print(resp.model_dump())
            resp = client.post_tag_v2(
                data=PostBatchTagV2(
                    update=[
                        UpdateTagV2(label="child_tag", parent="parent_tag"),
                    ],
                ),
            )
            print(resp.model_dump())
            ```

            will output:
            ```json
            {
                "id2error": {},
                "id2etag": {
                    "parent_tag": "ffmehyan",
                    "child_tag": "1uuc4fz1"
                }
            }
            {
                "id2error": {},
                "id2etag": {
                    "child_tag": "65lj6uj9"
                }
            }
            ```

        Args:
            data (Union[PostBatchTagV2, dict[str, Any]]): Data to create or update tags.

        Returns:
            BatchTagRespV2: Response from the API after creating or updating the tags.
        """
        if isinstance(data, dict):
            data = PostBatchTagV2.model_validate(data)
        resp = self._post_api_v2("/batch/tag", data=self._model_dump(data))
        if self.override_forbid_extra:
            update_model_config(BatchTagRespV2, extra="allow")
        return BatchTagRespV2.model_validate(resp)

    def put_rename_tag_v2(self, data: Union[RenameTagV2, dict[str, Any]]) -> None:
        """Rename a tag in the V2 API.

        Update a tag name using the `PUT /tag/rename` V2 endpoint. This endpoint allows
        you to specifically rename a tag. Any other _update_ operations should be done
        using the `post_tag_v2` method.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import RenameTagV2

            client = Client()
            client.put_rename_tag_v2(
                data=RenameTagV2(
                    name="test_tag",
                    new_name="test_tag_renamed",
                ),
            )
            ```
            This will return nothing if the tag is successfully renamed. Just know, even
            if the rename is _unsuccessful_, the API probably won't return an error.

        Args:
            data (Union[RenameTagV2, dict[str, Any]]): Data to rename the tag.

        Raises:
            ValueError: The response had an error HTTP status of `4xx` or `5xx`.
        """
        if isinstance(data, dict):
            data = RenameTagV2.model_validate(data)
        try:
            resp = httpx.put(
                url=str(self.v2_base_url.join("/tag/rename")),
                headers=self.v2_headers,
                cookies=self.v2_cookies,
                json=self._model_dump(data),
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                content = e.response.json()
            except json.decoder.JSONDecodeError:
                content = e.response.content.decode()
            msg = f"Response [{e.response.status_code}]: {content}"
            logger.error(msg)
            raise ValueError(msg)  # noqa: B904

    def delete_tag_v2(self, data: Union[DeleteTagV2, dict[str, Any]]) -> None:
        """Delete a tag in the V2 API.

        Delete a tag using the `DELETE /tag` V2 endpoint.

        ??? example "Example"
            ```python hl_lines="5"
            from pyticktick import Client
            from pyticktick.models.v2 import DeleteTagV2

            client = Client()
            client.delete_tag_v2(
                data=DeleteTagV2(name="test_tag"),
            )
            ```
            This will return nothing if the tag is successfully deleted. Just know,
            even if the delete is _unsuccessful_, the API probably won't return an
            error.

        Args:
            data (Union[DeleteTagV2, dict[str, Any]]): Data to delete a tag.
        """
        if isinstance(data, dict):
            data = DeleteTagV2.model_validate(data)
        self._delete_api_v2("/tag", data=self._model_dump(data))
