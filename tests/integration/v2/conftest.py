from __future__ import annotations

import logging

import httpx
import pytest
from bson import ObjectId
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
def generate_object_id():
    def _generate_object_id():
        return str(ObjectId())

    return _generate_object_id


@pytest.fixture()
def get_batch(client):
    def _get_batch():
        try:
            resp = httpx.get(
                url="https://api.ticktick.com/api/v2/batch/check/0",
                headers=client.v2_headers,
                cookies=client.v2_cookies,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_get_batch)


@pytest.fixture()
def get_task_v2(client):
    def _get_task(project_id: str, task_id: str):
        try:
            resp = httpx.get(
                url=f"https://api.ticktick.com/api/v2/task/{task_id}",
                headers=client.v2_headers,
                cookies=client.v2_cookies,
                params={"projectId": project_id},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e
        return resp.json()

    return _retry(_get_task)


@pytest.fixture()
def delete_projects(client, get_batch):
    def _delete_projects(names: list[str]):
        batch = get_batch()

        project_ids = [
            p.get("id")
            for p in batch.get("projectProfiles", [])
            if p.get("name") in names
        ]
        if len(project_ids) == 0:
            return

        try:
            resp = httpx.post(
                url="https://api.ticktick.com/api/v2/batch/project",
                headers=client.v2_headers,
                cookies=client.v2_cookies,
                json={"delete": project_ids},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e

    return _retry(_delete_projects)


@pytest.fixture()
def delete_project_groups(client, get_batch):
    def _delete_project_groups(names: list[str]):
        batch = get_batch()

        project_group_ids = [
            p.get("id")
            for p in batch.get("projectGroups", [])
            if p.get("name") in names
        ]
        if len(project_group_ids) == 0:
            return

        try:
            resp = httpx.post(
                url="https://api.ticktick.com/api/v2/batch/projectGroup",
                headers=client.v2_headers,
                cookies=client.v2_cookies,
                json={"delete": project_group_ids},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e

    return _retry(_delete_project_groups)


@pytest.fixture()
def delete_tags(client, get_batch):
    def _delete_tags(labels: list[str]):
        batch = get_batch()

        tag_names = [
            p.get("name") for p in batch.get("tags", []) if p.get("label") in labels
        ]

        try:
            for name in tag_names:
                resp = httpx.delete(
                    url="https://api.ticktick.com/api/v2/tag",
                    headers=client.v2_headers,
                    cookies=client.v2_cookies,
                    params={"name": name},
                )
                resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Response [{e.response.status_code}]:\n{e.response.text}"
            raise ValueError(msg) from e

    return _retry(_delete_tags)
