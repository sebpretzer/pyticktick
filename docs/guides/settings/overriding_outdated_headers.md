# Overriding Outdated Headers

You may sometimes encounter issues where the TickTick API returns a 429, similar to [sebpretzer/pyticktick#226](https://github.com/sebpretzer/pyticktick/issues/226) or [lazeroffmichael/ticktick-py#53](https://github.com/lazeroffmichael/ticktick-py/issues/53). The standard use case for 429 codes is that you are being [rate limited](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/429). But TickTick also returns a 429 due to outdated headers that are no longer valid.

To work around this, you can override the headers sent by setting the `v2_user_agent` and `v2_x_device` settings. For example:

```python
from pyticktick import Client

client = Client(
    v2_user_agent="TickTick/6.3.6 (iPhone; iOS 15.5; Scale/3.00)",
    v2_x_device={"platform":"web", "version":8000, "id":"694241d132d12fcc26e7a4d8"}
)
```

???+ question "Where do I find valid values for these headers?"

    In order to find valid values for these headers, you can inspect the network requests made by the TickTick app in your browser's developer tools. Look for requests to `https://api.ticktick.com` and check the `User-Agent` and `X-Device` headers.

    Not all values that are specified in your browser's request are required. The following is usually sufficient:

    - `User-Agent`: The app version, device type, OS version, and scale factor (e.g., `TickTick/6.3.6 (iPhone; iOS 15.5; Scale/3.00)`)
    - `X-Device`: A JSON string with at least the `platform`, `version`, and `id` fields (e.g., `{"platform":"web", "version":8000, "id":"694241d132d12fcc26e7a4d8"}`), where `id` is a [MongoDB ObjectId-like string](https://www.mongodb.com/docs/manual/reference/method/ObjectId/).
