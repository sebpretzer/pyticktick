#! /usr/bin/env uv run python

"""Script to clear all objects from a TickTick account.

This script will delete all objects from a TickTick account. This includes all tasks,
projects, project groups, and tags. This script is useful for cleaning up an account
that has been used for testing purposes. It is not intended for use on a production
account.
"""

from __future__ import annotations

from textwrap import dedent

from click import command, confirm, option
from loguru import logger

from pyticktick import Client


@command()
@option(
    "-u",
    "--username",
    "username",
    default=None,
    help="The username for the V2 API",
)
@option(
    "-p",
    "--password",
    "password",
    default=None,
    help="The password for the V2 API",
)
def main(username: str | None, password: str | None) -> None:  # noqa: C901
    """Delete all objects from a TickTick account.

    Args:
        username (Optional[str]): The username for the V2 API.
        password (Optional[str]): The password for the V2 API.
    """
    kwargs = {}
    if username is not None:
        kwargs["v2_username"] = username
    if password is not None:
        kwargs["v2_password"] = password

    client = Client.model_validate(kwargs)

    batch = client.get_batch_v2()

    tasks = batch.sync_task_bean.update
    projects = batch.project_profiles
    project_groups = batch.project_groups if batch.project_groups is not None else []
    tags = batch.tags

    if len(tasks) + len(projects) + len(project_groups) + len(tags) == 0:
        logger.info("No objects to delete.")
        return

    msg = dedent(f"""
    Are you sure you want to delete all objects?
    - {len(projects)} Projects
    - {len(project_groups)} Project Groups
    - {len(tasks)} Tasks
    - {len(tags)} Tags
    """)
    if confirm(msg):
        if len(tasks) > 0:
            logger.info("Deleting tasks")
            client.post_task_v2(
                {
                    "delete": [
                        {"project_id": t.project_id, "task_id": t.id} for t in tasks
                    ],
                },
            )

        if len(project_groups) > 0:
            logger.info("Deleting project groups")
            client.post_project_group_v2({"delete": [pg.id for pg in project_groups]})

        if len(projects) > 0:
            logger.info("Deleting projects")
            client.post_project_v2({"delete": [p.id for p in projects]})

        if len(tags) > 0:
            logger.info("Deleting tags")
            for tag in tags:
                client.delete_tag_v2({"name": tag.name})

        if len(tasks + projects + project_groups + tags) > 0:
            logger.info("All objects have been deleted.")
    else:
        logger.info("Exiting without deleting any objects.")


if __name__ == "__main__":
    main()
