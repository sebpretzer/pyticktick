from types import FunctionType

import pytest
from tenacity import RetryError, Retrying, retry_if_exception_message

from pyticktick.retry import retry_api_v1


# https://github.com/jd/tenacity/issues/106#issuecomment-2213584949
# https://stackoverflow.com/a/73890688
@pytest.fixture(autouse=True)
def tenacity_wait(mocker):
    mocker.patch("tenacity.nap.time")


def test_retry_api_v1():
    attempts = 5
    min_wait = 0.1
    max_wait = 0.2

    decorator = retry_api_v1(attempts=attempts, min_wait=min_wait, max_wait=max_wait)
    assert isinstance(decorator, FunctionType)

    def _func() -> None:
        msg = "exceed_query_limit"
        raise ValueError(msg)

    wrapped_function = decorator(_func)
    assert isinstance(wrapped_function, FunctionType)

    assert isinstance(wrapped_function.retry, Retrying)
    assert wrapped_function.retry.stop.max_attempt_number == attempts
    assert wrapped_function.retry.wait.min == min_wait
    assert wrapped_function.retry.wait.max == max_wait

    retries = wrapped_function.retry.retry.retries
    assert len(retries) == 2
    assert any(isinstance(retry, retry_if_exception_message) for retry in retries)

    assert wrapped_function.statistics == {}
    with pytest.raises(RetryError):
        wrapped_function()
    assert wrapped_function.statistics.get("attempt_number") == attempts
