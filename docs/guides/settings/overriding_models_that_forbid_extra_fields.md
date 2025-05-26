# Overriding Models That Forbid Extra Fields

When getting back response data from an API call, if you get an `extra_forbidden` error message like:

```bash
pydantic_core._pydantic_core.ValidationError: 1 validation error for RespModel
extra_field
    Extra inputs are not permitted [type=extra_forbidden, input_value='extra_value', input_type=str]
```

it may be due to the TickTick API adding new fields that are not yet supported by the response model (`RespModel`).

In this case, you can override the model behavior and allow extra fields. This can be done by setting `override_forbid_extra` to `True` in the client configuration:

```python
from pyticktick import Client

client = Client(override_forbid_extra=True)
```

You can see alternative ways to set `override_forbid_extra` in the [Settings](http://127.0.0.1:8000/reference/settings/#pyticktick.settings.Settings) reference.

!!! note

    This feature does not work in all cases, only when TickTick updates their API and this library has not yet been updated to support the new fields. If you encounter this error, it may be failing due to other reasons.

To see why this feature was built in this way, you can see the explanation in [Forbidding Extra Fields in API Models](../../explanations/forbidding_extra_fields_in_api_models.md).

If this does happen to you, please open an issue on the [GitHub repository](https://github.com/sebpretzer/pyticktick/issues/new) so this can be addressed.
