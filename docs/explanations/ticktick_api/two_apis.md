# The Two TickTick APIs

## Overview

You may notice throughout this documentation that there are two different APIs that are referenced and supported. This is because TickTick has provided two different interfaces that users can, in theory, interact with. The first, [_API V1_](#api-v1), is the official API that TickTick has provided to developers. The second, [_API V2_](#api-v2), is an unofficial API that has been reverse-engineered by the community, and can be observed by inspecting network requests made by the TickTick web app.

### API V1

The official API, formally known as the _TickTick Open API_, is a RESTful API for managing user tasks, and lists. You can learn more from their [official documentation](https://developer.ticktick.com/docs#/openapi). Given that there are two APIs, and this API's URL starts with `api.ticktick.com/open/v1/`, we will refer to this as _API V1_.

### API V2

The unofficial API does not have an formal name, but we refer to it as _API V2_, given the URL starts with `api.ticktick.com/api/v2/`. This API is undocumented, so the information provided in this documentation is based on other projects' efforts to reverse-engineer the API, as well as our own observations, and may not be entirely accurate. This is the API that the TickTick web app uses to communicate with the TickTick servers, so anything you can do in the web app, you can do with this API.

## Why support two APIs?

The goal is to provide the best experience possible for developers using this library. The official API is well-documented, and is the one that TickTick has provided. However, the unofficial API is more robust, and provides significantly more functionality than the official API. _API V1_ is limited to managing lists and tasks alone (not including the inbox list). _API V2_, on the other hand, provides access to all of the features that the TickTick web app has, including tags, sublists, subtasks, and more. This is why this library supports both APIs.

## Which API should I use?

TickTick has not mentioned the _API V2_ anywhere on their website, but it provides a better experience for developers. Given that TickTick has not given explicit permission to use it, it may go against their [Terms of Service](https://ticktick.com/tos). This was discussed in [lazeroffmichael/ticktick-py#38](https://github.com/lazeroffmichael/ticktick-py/issues/38) if you want to see other developers' opinions on the matter. The recommendation of this library is to use the official API where possible, and only use the unofficial API when necessary. The library client is designed to be flexible, so you can do whatever you feel comfortable with.
