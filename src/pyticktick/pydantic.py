"""Custom Pydantic utilities that are not currently supported by Pydantic libraries.

!!! Warning
    Users are not expected to use the module directly, this is for internal use only. It
    is being documented for transparency and to provide context in case users encounter
    any issues.
"""

from __future__ import annotations

import types
from sys import version_info
from typing import Any, Union, get_origin

from pydantic import BaseModel, ConfigDict


# https://discuss.python.org/t/how-to-check-if-a-type-annotation-represents-an-union/77692
def _is_union(annotation: type[Any]) -> bool:
    if version_info >= (3, 10):
        return get_origin(annotation) in {Union, types.UnionType}  # pyright: ignore[reportAttributeAccessIssue]
    return get_origin(annotation) == Union


def _check_field_for_submodel(
    annotation: type[Any] | None,
    **config_kwargs: Any,  # noqa: ANN401
) -> None:
    """Check if a field is a Pydantic model and attempt to update its config if it is.

    This function checks if the input `annotation` is a Pydantic model and calls
    [`update_model_config`](pydantic.md#pyticktick.pydantic.update_model_config)
    on it, if it is.

    This function is used internally by Pyticktick to ensure that all nested submodels
    have the same config as the top-level model.

    Args:
        annotation (Optional[type[Any]]): The [Pydantic.FieldInfo](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.FieldInfo)
            annotation to check.
        **config_kwargs (Any): The key-value pairs to update the model config with,
            should be only values found in [`pydantic.ConfigDict`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict).
    """
    if annotation is None:
        return
    if isinstance(annotation, types.GenericAlias):
        _origin = annotation.__origin__
        _args = annotation.__args__
        if _origin is list and issubclass(_args[0], BaseModel):
            update_model_config(_args[0], **config_kwargs)
        elif _origin is dict and issubclass(_args[1], BaseModel):
            update_model_config(_args[1], **config_kwargs)
    elif _is_union(annotation):
        for _arg in annotation.__args__:
            _check_field_for_submodel(_arg, **config_kwargs)
    elif issubclass(annotation, BaseModel):
        update_model_config(annotation, **config_kwargs)


def update_model_config(model: type[BaseModel], **config_kwargs: Any) -> None:  # noqa: ANN401
    """Dynamically update a Pydantic model config, including nested submodels.

    This function updates the input `model.model_config`, and forces a rebuild with the
    updated config. In general, that process only works for the top-level model, it does
    not work for nested submodels. This function works in tandem with
    [`_check_field_for_submodel`](pydantic.md#pyticktick.pydantic._check_field_for_submodel)
    to recursively update the config of nested Pydantic submodels.

    This takes inspiration from [pydantic/pydantic#2518](https://github.com/pydantic/pydantic/discussions/2518),
    which built a similar function for Pydantic V1. [pydantic/pydantic#2652](https://github.com/pydantic/pydantic/discussions/2652)
    is a feature request to add the functionality present here to the core of Pydantic
    V2.

    Args:
        model (type[BaseModel]): The Pydantic model to update.
        **config_kwargs (Any): The key-value pairs to update the model config with,
            should be only values found in [`pydantic.ConfigDict`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict).

    Raises:
        ValueError: If no config key-value pairs are provided.
    """
    if len(config_kwargs) == 0:
        msg = "`update_model_config()` requires at least 1 Model Config key-value pair argument"  # noqa: E501
        raise ValueError(msg)

    for field in model.__pydantic_fields__.values():
        _check_field_for_submodel(field.annotation, **config_kwargs)

    model.model_config.update(ConfigDict(**config_kwargs))  # type: ignore[typeddict-item]
    model.model_rebuild(force=True)
