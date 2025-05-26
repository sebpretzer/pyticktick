"""Retry decorators for the TickTick API.

This module contains the retry decorator for the TickTick API. This uses tenacity to
provide the retry mechanism. Currently, this only retries for V1 API errors, and
specifically for the `exceed_query_limit` error message. No other retriable errors are
known as of now, but this can be expanded in the future.

!!! Example
    ```python
    from pyticktick.retry import retry_api_v1


    @retry_api_v1(attempts=10, min_wait=4, max_wait=20)
    def my_function():
        pass
    ```
"""

from __future__ import annotations

import logging
from typing import Callable

from tenacity import (
    WrappedFn,
    before_sleep_log,
    retry,
    retry_if_exception_message,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from pyticktick.logger import _logger


def retry_api_v1(
    attempts: int = 10,
    min_wait: float = 4,
    max_wait: float = 20,
) -> Callable[[WrappedFn], WrappedFn]:
    """Retry decorator for the V1 API.

    This decorator retries the function if the error message is `exceed_query_limit`.
    The defaults have been set via trial and error, and may need to be adjusted
    depending on the use case.

    Args:
        attempts (int): The number of attempts to make. Defaults to 10.
        min_wait (float): The minimum wait time between attempts. Defaults to 4.
        max_wait (float): The maximum wait time between attempts. Defaults to 20.

    Returns:
        Callable[[WrappedFn], WrappedFn]: The tenacity retry decorator.
    """
    return retry(
        retry=(
            retry_if_exception_type(ValueError)
            & retry_if_exception_message(match=r"^.*exceed\_query\_limit.*$")
        ),
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        before_sleep=before_sleep_log(_logger, logging.INFO),
    )
