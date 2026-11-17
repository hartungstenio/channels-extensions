"""WebSocket consumers backed by ``orjson``."""

from __future__ import annotations

# Python 3.15+: defer importing the optional ``orjson`` extra until first use.
__lazy_modules__ = ["orjson", "django_orjson"]

from typing import Any

import orjson
from channels.generic import websocket
from django_orjson import default

from channels_extensions._compat import override


class JsonWebsocketConsumer(websocket.JsonWebsocketConsumer):
    """Synchronous JSON WebSocket consumer that encodes and decodes with ``orjson``."""

    @override
    @classmethod
    def decode_json(cls, text_data: str) -> Any:
        return orjson.loads(text_data)

    @override
    @classmethod
    def encode_json(cls, content: Any) -> str:
        return orjson.dumps(content, default=default).decode()


class AsyncJsonWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
    """Asynchronous JSON WebSocket consumer that encodes and decodes with ``orjson``."""

    @override
    @classmethod
    async def decode_json(cls, text_data: str) -> Any:
        return orjson.loads(text_data)

    @override
    @classmethod
    async def encode_json(cls, content: Any) -> str:
        return orjson.dumps(content, default=default).decode()
