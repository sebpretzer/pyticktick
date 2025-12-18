# Changelog

## 0.3.0

- Improve error messages for broken v2 headers; allow overriding headers [#227](https://github.com/sebpretzer/pyticktick/pull/227)
- Improve error messages for extra fields in models [#223](https://github.com/sebpretzer/pyticktick/pull/223)
- Add support for Python 3.14 and remove support for Python 3.9; fix broken v2 headers [#201](https://github.com/sebpretzer/pyticktick/pull/201)
- Add `background` field to `pyticktick.models.v2.ProjectV2` [#200](https://github.com/sebpretzer/pyticktick/pull/200)

## 0.2.0

- Add missing fields to `pyticktick.models.v2.TaskV2` [#86](https://github.com/sebpretzer/pyticktick/pull/86)
- Fix integration test warnings [#85](https://github.com/sebpretzer/pyticktick/pull/85)
- Fix unit test warnings [#84](https://github.com/sebpretzer/pyticktick/pull/84)
- Add `BaseModelV2` for all V2 models to inherit from [#83](https://github.com/sebpretzer/pyticktick/pull/83)
- Add models in `pyticktick.models.v2.models` to `pyticktick.models.v2` [#82](https://github.com/sebpretzer/pyticktick/pull/82)
- Fix `created_campaign` in `pyticktick.models.v2.UserProfileV2` [#79](https://github.com/sebpretzer/pyticktick/pull/79)
- Fix empty string conversion for `pyticktick.models.v2.TaskV2` [#78](https://github.com/sebpretzer/pyticktick/pull/78)
- Fix typos in `pyticktick.models.v2.GetClosedV2` [#77](https://github.com/sebpretzer/pyticktick/pull/77)
- Add support for 2FA [#72](https://github.com/sebpretzer/pyticktick/pull/72)
- Fix changelog extractor for release github action [#42](https://github.com/sebpretzer/pyticktick/pull/42)

## 0.1.0

- Refactor V1 model names to be more consistent with V2 model names [#40](https://github.com/sebpretzer/pyticktick/pull/40)
- Isolate generic Pydantic types that are used in both V1 and V2 APIs [#39](https://github.com/sebpretzer/pyticktick/pull/39)

## 0.0.3

- Switch Github Actions to use `uv` managed python installs [#38](https://github.com/sebpretzer/pyticktick/pull/38)
- Cleaned up type hints via upgrading to ruff 0.12.0 [#33](https://github.com/sebpretzer/pyticktick/pull/33)
- Fixed grammar in docs with help from Claude [#28](https://github.com/sebpretzer/pyticktick/pull/28)
- Added guides on how to authenticate the client [#26](https://github.com/sebpretzer/pyticktick/pull/26)

## 0.0.2

- Re-release of `0.0.1`, since `0.0.1` was already created during testing. [#3](https://github.com/sebpretzer/pyticktick/pull/3)

## 0.0.1

- Initial release of the `pyticktick` library.
