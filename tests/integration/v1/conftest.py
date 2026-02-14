from __future__ import annotations

import logging

import httpx
import pytest
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from pyticktick.logger import _logger

_retry = retry(
    retry=(retry_if_exception_type(ValueError)),
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=5, max=30),
    before_sleep=before_sleep_log(_logger, logging.INFO),  # ty: ignore[invalid-argument-type]
)


@pytest.fixture()
def helper_get_projects(client):
    def _get_projects():
        try:
            resp = httpx.get(
                url="https://api.ticktick.com/open/v1/project",
                headers=client.v1_headers,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_get_projects)


@pytest.fixture()
def helper_get_project_data(client):
    def _get_project_data(project_id: str):
        try:
            resp = httpx.get(
                url=f"https://api.ticktick.com/open/v1/project/{project_id}/data",
                headers=client.v1_headers,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_get_project_data)


@pytest.fixture()
def helper_create_project(client):
    def _create_project(project_name: str) -> dict:
        try:
            resp = httpx.post(
                url="https://api.ticktick.com/open/v1/project",
                headers=client.v1_headers,
                json={"name": project_name},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_create_project)


@pytest.fixture()
def helper_delete_project(client):
    def _delete_project(project_id: str):
        try:
            resp = httpx.delete(
                url=f"https://api.ticktick.com/open/v1/project/{project_id}",
                headers=client.v1_headers,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e

    return _retry(_delete_project)


@pytest.fixture()
def helper_create_or_recreate_projects(
    helper_get_projects,
    helper_create_project,
    helper_delete_project,
):
    def _create_or_recreate_projects(
        project_names: str | list[str],
    ) -> dict | list[dict]:
        if isinstance(project_names, str):
            project_names = [project_names]

        project_dicts = helper_get_projects()
        for p in project_dicts:
            if p["name"] in project_names:
                helper_delete_project(p["id"])

        resps = []
        for n in project_names:
            p = helper_create_project(n)
            resps.append(p)

        if len(resps) == 1:
            return resps[0]
        return resps

    return _create_or_recreate_projects


@pytest.fixture()
def helper_delete_projects_if_exists(helper_get_projects, helper_delete_project):
    def _delete_projects_if_exists(project_names: str | list[str]):
        if isinstance(project_names, str):
            project_names = [project_names]

        project_dicts = helper_get_projects()
        for p in project_dicts:
            if p["name"] in project_names:
                helper_delete_project(p["id"])

    return _delete_projects_if_exists


@pytest.fixture()
def helper_create_task(client):
    def _create_task(project_id: str, task_name: str) -> dict:
        try:
            resp = httpx.post(
                url="https://api.ticktick.com/open/v1/task",
                headers=client.v1_headers,
                json={"title": task_name, "projectId": project_id},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_create_task)


@pytest.fixture()
def helper_get_task(client):
    def _get_task(project_id: str, task_id: str) -> dict:
        try:
            resp = httpx.get(
                url=f"https://api.ticktick.com/open/v1/project/{project_id}/task/{task_id}",
                headers=client.v1_headers,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_get_task)
