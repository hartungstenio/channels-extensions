# channels-extensions

[![PyPI - Version](https://img.shields.io/pypi/v/channels-extensions.svg)](https://pypi.org/project/channels-extensions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/channels-extensions.svg)](https://pypi.org/project/channels-extensions)

-----

## Installation

```console
pip install channels-extensions
```

## Usage

### DummyChannelLayer
```DummyChannelLayer``` is an noop (almost) implementation of `BaseChannelLayer`. Messages sent to it are never available, and `receive` never returns.

All methods work as checkpoints to the event loop, yielding control back to it at least once.

```python
CHANNEL_LAYERS = {
    "dummy": {
        "BACKEND": "channels_extensions.layers.DummyChannelLayer",
    }
}
```

### get_channel_layer
This is simply a version of channels `get_channel_layer`, but it raises an `ImproperlyConfigured` if the alias does not exist.

### CurrentSiteMiddleware
A middleware that mimics django's `CurrentSiteMiddleware`. It adds a `site` key to the scope:
```python
class EchoSiteConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": self.scope["site"],
        })

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            CurrentSiteMiddleware(
                URLRouter([
                    path("echo/", EchoSiteConsumer.as_asgi()),
                ])
            )
        )
    ),
})
```

## License

`channels-extensions` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
