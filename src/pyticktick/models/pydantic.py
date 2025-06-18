"""Generic custom pydantic types, not specific to any API version."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import HttpUrl as PydanticHttpUrl
from pydantic_core import CoreSchema, core_schema
from pydantic_extra_types.color import Color as PydanticColor

if TYPE_CHECKING:
    from collections.abc import Callable


class Color(PydanticColor):
    """Represents a color in pydantic-based TickTick models."""

    @classmethod
    def __get_pydantic_core_schema__(  # noqa: DOC101, DOC103, DOC203
        cls,
        source: type[Any],
        handler: Callable[[Any], CoreSchema],
    ) -> core_schema.CoreSchema:
        """Change the serialization logic of the color field to always be a string.

        This method mirrors the logic of the standard [`__get_pydantic_core_schema__` method](https://github.com/pydantic/pydantic-extra-types/blob/1da2a1caeb7502e40037e2e3e2961726c2c5c002/pydantic_extra_types/color.py#L213-L219)
        in [`pydantic_extra_types.color.Color`](https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/),
        but changes the `when_used` parameter to be `"always"` instead of the default of
        `"json-unless-none"`.
        """  # noqa: DOC201
        return core_schema.with_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.to_string_ser_schema(when_used="always"),
        )

    def __str__(self) -> str:
        """Return the color as a hex string.

        TickTick uses the long hex format for colors, so this method allows for easy
        serialization of the color field into the correct format. Equivalent to calling
        [`as_hex(format="long")`](https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/#pydantic_extra_types.color.Color.as_hex).
        It will be lowercase and always have 7 characters (and `#`): `#rrggbb`.

        !!! Example
            ```python
            color = Color((0, 255, 255))
            assert color.as_named() == "cyan"
            assert str(color) == "#00ffff"
            ```

        Returns:
            str: The color as a hex string.
        """
        return self.as_hex(format="long")


class HttpUrl(PydanticHttpUrl):
    """Represents an HTTP URL in pydantic-based TickTick models."""

    def join(self, *args: str) -> HttpUrl:
        """Join the current URL with additional path segments.

        This method is a convenience method to join additional path segments to the
        current URL. It takes its inspiration from the [`urllib.parse.urljoin`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin)
        and [`pathlib.PurePath.joinpath`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.joinpath)
        methods in Python.

        !!! Example
            ```python
            from pyticktick.models.v2 import HttpUrl

            url = HttpUrl("https://example.com")
            assert url.join("foo") == HttpUrl("https://example.com/foo")
            assert url.join("foo", "bar") == HttpUrl("https://example.com/foo/bar")
            ```

        Args:
            *args (str): The path segments to join with the current URL.

        Returns:
            HttpUrl: A new URL with the path segments joined to the current URL.
        """
        if len(args) == 0:
            return self

        url = str(self).rstrip("/")
        for arg in args:
            url = f"{url.rstrip('/')}/{arg.lstrip('/')}"
        return self.__class__(url)
