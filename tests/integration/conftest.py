from pathlib import Path

import pytest

from pyticktick import Client


@pytest.fixture()
def client() -> Client:
    if not (env_file_path := Path(__file__).parents[2].joinpath(".env")).exists():
        return Client()
    return Client(_env_file=env_file_path)  # pyright: ignore[reportCallIssue] # https://github.com/pydantic/pydantic/issues/3072
