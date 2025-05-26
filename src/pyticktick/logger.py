"""Logging workound to use Loguru in conjunction with the standard logging module.

!!! Warning
    Users are not expected to use the module directly, this is for internal use only. It
    is being documented for transparency and to provide context in case users encounter
    any issues.

This module contains a workaround when a function expects the standard logging module
but you want to use Loguru. This is done by creating a custom logging handler that
sends logs to Loguru. This is intended to be used in rare cases, such as with tenacity.
You should use `from loguru import logger` for all other logging needs.

This module was taken from [Delgan/loguru#969 (comment)](https://github.com/Delgan/loguru/issues/969#issuecomment-1703869863)
and is endorsed as the best current workaround by the author of Loguru.

!!! Example
    ```python
    from loguru import logger
    from pyticktick.logger import _logger

    logger.info("This is a Loguru message")
    _logger.info("This is a standard logging message that will be sent to Loguru")
    ```
"""

import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):  # noqa: D101
    def emit(self, record: logging.LogRecord) -> None:  # noqa: D102
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6  # noqa: SLF001
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


_logger = logging.getLogger(__name__)
_logger.addHandler(InterceptHandler())
_logger.setLevel(logging.DEBUG)
