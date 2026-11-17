from typing import Any

import orjson
from channels.generic import websocket
from django_orjson import default

from channels_extensions._compat import override


class JsonWebsocketConsumer(websocket.JsonWebsocketConsumer):
    @override
    @classmethod
    def decode_json(cls, text_data: str) -> Any:
        return orjson.loads(text_data)

    @override
    @classmethod
    def encode_json(cls, content: Any) -> str:
        return orjson.dumps(content, default=default).decode()


class AsyncJsonWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
    @override
    @classmethod
    async def decode_json(cls, text_data: str) -> Any:
        return orjson.loads(text_data)

    @override
    @classmethod
    async def encode_json(cls, content: Any) -> str:
        return orjson.dumps(content, default=default).decode()
