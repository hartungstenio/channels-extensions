from typing import Any

import orjson
from channels.generic import websocket
from django_orjson import default


class JsonWebsocketConsumer(websocket.JsonWebsocketConsumer):
    @classmethod
    def decode_json(cls, text_data) -> Any:
        return orjson.loads(text_data)

    @classmethod
    def encode_json(cls, content) -> str:
        return orjson.dumps(content).decode()


class AsyncJsonWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
    @classmethod
    async def decode_json(cls, text_data) -> Any:
        return orjson.loads(text_data)

    @classmethod
    async def encode_json(cls, content) -> str:
        return orjson.dumps(content, default=default).decode()
