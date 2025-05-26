import pytest


# https://stackoverflow.com/a/61193490/13001770
def pytest_addoption(parser):
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="run local-only tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "local: mark test as only able to run locally")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--local"):
        return
    skip_local = pytest.mark.skip(reason="need --local option to run")
    for item in items:
        if "local" in item.keywords:
            item.add_marker(skip_local)
