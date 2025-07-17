# Comparison of Similar Libraries

There are a few Python libraries that provide similar functionality to `pyticktick`:

1. [ticktick-py](https://lazeroffmichael.github.io/ticktick-py/)
1. [dida365](https://cyfine.github.io/TickTick-Dida365-API-Client/)
1. [didatodolist](https://github.com/GalaxyXieyu/dida_api)
1. [tickthon](https://github.com/anggelomos/tickthon)

These libraries are all designed independently to interact with the TickTick API. `pyticktick` is another library that overlaps with these other libraries, making it the target of this xkcd joke:

<figure markdown="span">
    <a href="https://xkcd.com/927/">
        ![xkcd 927](../_images/similar_libraries/xkcd_927.png){ width="60%" }
    </a>
    <figcaption>Relevant xkcd #927</figcaption>
</figure>

The other libraries came first, and were inspiration for `pyticktick`. So by all means, use them if they better suit your needs. They have been around for longer, so are probably more bug-free. `pyticktick` does take advantage of learnings in those libraries, and this explanation attempts to make a helpful comparison of the other libraries to `pyticktick`.

??? warning "Out of Date Comparisons!"

    The hope is that this document will serve as a reference for users who are considering using the right library for their needs. It is a best attempt at providing a comprehensive comparison, but it may not be up to date, as the other libraries may add functionality. You can see the last time this document was updated at the very bottom.

## High-Level Comparison

At a high level, this is a breakdown of the features and capabilities of each library:

| Feature                                  | pyticktick         | [ticktick-py](https://lazeroffmichael.github.io/ticktick-py/) | [dida365](https://cyfine.github.io/TickTick-Dida365-API-Client/) | [didatodolist](https://github.com/GalaxyXieyu/dida_api) | [tickthon](https://github.com/anggelomos/tickthon) |
| ---------------------------------------- | ------------------ | ------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| [V1 Support](#v1-support)                | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [V2 Support](#v2-support)                | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :white_check_mark:                                      | :white_check_mark:                                 |
| [V1 / V2 Isolation](#v1-v2-isolation)    | :white_check_mark: | :x:                                                           | :x:                                                              | :x:                                                     | :x:                                                |
| [Pydantic Support](#pydantic-support)    | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Retry Support](#retry-support)          | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Async Support](#async-support)          | :x:                | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [TickTick Support](#ticktick-vs-dida365) | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :white_check_mark:                                 |
| [DIDA365 Support](#ticktick-vs-dida365)  | :x:                | :x:                                                           | :white_check_mark:                                               | :white_check_mark:                                      | :x:                                                |

!!! note

    This chart does not provide the full picture, and a lot of the provided features are more nuanced than a binary supported or not.

## V1 Support

The TickTick V1 API has a handful of endpoints that are supported. [TickTick provides a spec](https://developer.ticktick.com/docs/index.html#/openapi?id=api-reference) to work off of. While it may seem like some libraries are missing features, they may just be [supporting the V2 API](#v2-support), since there is a lot of overlap.

| Components                                                                                                      | pyticktick         | [ticktick-py](https://lazeroffmichael.github.io/ticktick-py/) | [dida365](https://cyfine.github.io/TickTick-Dida365-API-Client/) | [didatodolist](https://github.com/GalaxyXieyu/dida_api) | [tickthon](https://github.com/anggelomos/tickthon) |
| --------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| [Get Task by ID](https://developer.ticktick.com/docs/index.html#/openapi?id=get-task-by-project-id-and-task-id) | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Create Task](https://developer.ticktick.com/docs/index.html#/openapi?id=create-task)                           | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Update Task](https://developer.ticktick.com/docs/index.html#/openapi?id=update-task)                           | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Complete Task](https://developer.ticktick.com/docs/index.html#/openapi?id=complete-task)                       | :white_check_mark: | :white_check_mark:                                            | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Delete Task](https://developer.ticktick.com/docs/index.html#/openapi?id=delete-task)                           | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Get Projects](https://developer.ticktick.com/docs/index.html#/openapi?id=get-user-project)                     | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Get Project by ID](https://developer.ticktick.com/docs/index.html#/openapi?id=get-project-by-id)               | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Get Project With Data](https://developer.ticktick.com/docs/index.html#/openapi?id=get-project-with-data)       | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Create Project](https://developer.ticktick.com/docs/index.html#/openapi?id=create-project)                     | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Update Project](https://developer.ticktick.com/docs/index.html#/openapi?id=update-project)                     | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |
| [Delete Project](https://developer.ticktick.com/docs/index.html#/openapi?id=delete-project)                     | :white_check_mark: | :x:                                                           | :white_check_mark:                                               | :x:                                                     | :x:                                                |

## V2 Support

The TickTick V2 API is undocumented, so the descriptions below may not be fully accurate. There may also be unknown endpoints that are not documented here.

| Components                   | pyticktick         | [ticktick-py](https://lazeroffmichael.github.io/ticktick-py/) | [dida365](https://cyfine.github.io/TickTick-Dida365-API-Client/) | [didatodolist](https://github.com/GalaxyXieyu/dida_api) | [tickthon](https://github.com/anggelomos/tickthon) |
| ---------------------------- | ------------------ | ------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| Get Active Data Endpoint     | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :white_check_mark:                                      | :white_check_mark:                                 |
| Get Completed Tasks Endpoint | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :x:                                                     | :white_check_mark:                                 |
| Get User Setting Endpoints   | :white_check_mark: | :x:                                                           | :x:                                                              | :x:                                                     | :x:                                                |
| Post Project Endpoints       | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :white_check_mark:                                      | :x:                                                |
| Post Task Endpoints          | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :white_check_mark:                                      | :white_check_mark:                                 |
| Post Tag Endpoints           | :white_check_mark: | :white_check_mark:                                            | :x:                                                              | :white_check_mark:                                      | :x:                                                |
| Post Pomodoro Endpoints      | :x:                | :x:                                                           | :x:                                                              | :x:                                                     | :white_check_mark:                                 |
| Post Habits Endpoints        | :x:                | :x:                                                           | :x:                                                              | :x:                                                     | :white_check_mark:                                 |
| Post Countdown Endpoints     | :x:                | :x:                                                           | :x:                                                              | :x:                                                     | :x:                                                |
| 2FA Support                  | :white_check_mark: | :x:                                                           | :x:                                                              | :x:                                                     | :x:                                                |

??? Question "Why no support for pomodoro, habits, countdown, etc?"

    The essential features of TickTick are the projects, tasks, and tags components. These are fully supported in `pyticktick`. The other features are not essential to everyone, but might be important to you. If you need support for these features, please open an issue on the [GitHub repository](https://github.com/sebpretzer/pyticktick/issues/new?template=feature.yaml).

## V1 / V2 Isolation

`pyticktick` is the only library that supports both V1 and V2 endpoints in a way that they can be used independently. `ticktick-py` has limited support for V1 endpoints, but its entangled with V2 endpoints. To see why `pyticktick` built isolated functionality for V1 and V2 endpoints, you should read [why `pyticktick` supports two apis](ticktick_api/two_apis.md#why-support-two-apis).

## Pydantic Support

`pyticktick` and `dida365` both support Pydantic models for their data structures. This allows for easier data validation and stronger guarantees about the data being sent to and from the TickTick API. `pyticktick` is the only library to support this for the V2 endpoint.

## Retry support

`pyticktick` and `dida365` both support retrying when the V1 endpoint is overloaded with too many requests. `ticktick-py` is the only library to support retries for both V1 and V2 endpoints. This was not implemented in `pyticktick` since it was impossible to determine which V2 calls were failing due to rate limits versus other errors.

## Async Support

`dida365` is the only library to support asynchronous operations, although it does not support synchronous operations, that must be handled manually.

## TickTick vs DIDA365

[TickTick](https://ticktick.com/home) and [DIDA365](https://dida365.com/home) are the same application, but DIDA365 is the Chinese version. They share similar API endpoints, but with different URLs. The names of the libraries match the names of the applications they support, with the exception of `dida365`, which has the ability to support both `TickTick` and `DIDA365` endpoints.

## What Makes `pyticktick` Worth Using?

`pyticktick` has been designed to provide the best experience to developers with:

1. An emphasis on user experience, providing flexibility where it can ([V1 / V2 Support](#v1-v2-isolation)), and providing rigidity where it should ([Pydantic Support](#pydantic-support)).
1. A consistent interface that is easy to use and understand.
1. Thorough documentation, to make learning as easy as possible.
