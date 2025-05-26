from pyticktick.logger import InterceptHandler, _logger


def test_logger():
    assert _logger.name == "pyticktick.logger"
    assert _logger.level == 10
    assert len(_logger.handlers) == 1
    assert isinstance(_logger.handlers[0], InterceptHandler)
