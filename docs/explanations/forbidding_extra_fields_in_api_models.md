# Forbidding Extra Fields in API Models

## Which Models Forbid Extra Fields?

The V2 API models in `pyticktick.models.v2` forbid [extra fields](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra). This means that any unexpected fields in the JSON data will raise a `pydantic.ValidationError` of type [extra_forbidden](https://docs.pydantic.dev/latest/errors/validation_errors/#extra_forbidden). For V1 models, we allow extra fields on response models (`pyticktick.models.v1.response`) but not on request parameter models (`pyticktick.models.v1.parameters`).

## Why Forbid Extra Fields?

We forbid extra fields to ensure that the models are robust. On the response side, we have no knowledge of when TickTick will update their API, so we must be alerted to any changes and update our models accordingly. This means that our response models must be more strict than Pydantic's default.

On the request side, we do not want users accidentally attempting to add any fields that are irrelevant to the API. By default, [Pydantic will just ignore any extra fields](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra).
This silent error handling can mislead users into thinking their extra fields are being accepted by the API.

## What if the API Changes?

If the V2 API changes, we will need to update our models. If there is any lag between the API update and the model update, the models will through a validation error. We have an [escape hatch to override this behavior](../guides/settings/overriding_models_that_forbid_extra_fields.md), at least on the response side.

## Why Ignore Extra Fields in V1 Response Models?

TickTick provides [documentation for the V1 API](https://developer.ticktick.com/), so we should remain as faithful as possible to their API. Unfortunately, their documentation is not fully
up to date. Extra undocumented fields appear in the API responses, so we just ignore them to most closely represent their API.
