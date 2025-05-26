import pytest

from pyticktick.models.v2 import HttpUrl


@pytest.mark.parametrize(
    ("base", "to_join", "expected"),
    [
        ("https://example.com", ["foo"], "https://example.com/foo"),
        ("https://example.com", ["/foo"], "https://example.com/foo"),
        ("https://example.com", ["foo/"], "https://example.com/foo/"),
        ("https://example.com", ["/foo/"], "https://example.com/foo/"),
        ("https://example.com/", ["foo"], "https://example.com/foo"),
        ("https://example.com/", ["/foo"], "https://example.com/foo"),
        ("https://example.com/", ["foo/"], "https://example.com/foo/"),
        ("https://example.com/", ["/foo/"], "https://example.com/foo/"),
        ("https://example.com", ["foo", "bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["/foo", "bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["foo/", "bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["/foo/", "bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["foo", "/bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["/foo", "/bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["foo/", "/bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["/foo/", "/bar"], "https://example.com/foo/bar"),
        ("https://example.com", ["foo", "bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["/foo", "bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["foo/", "bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["/foo/", "bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["foo", "/bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["/foo", "/bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["foo/", "/bar/"], "https://example.com/foo/bar/"),
        ("https://example.com", ["/foo/", "/bar/"], "https://example.com/foo/bar/"),
    ],
)
def test_joinpath(base, to_join, expected):
    assert HttpUrl(base).join(*to_join) == HttpUrl(expected)
