import pytest

from channels_extensions.consumers import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer


class TestJsonWebsocketConsumer:
    def test_decode_json(self) -> None:
        payload = '{"type":"message","text":"hello"}'

        result = JsonWebsocketConsumer.decode_json(payload)

        assert result == {"type": "message", "text": "hello"}

    def test_encode_json(self) -> None:
        payload = {"type": "message", "text": "hello"}

        result = JsonWebsocketConsumer.encode_json(payload)

        assert isinstance(result, str)
        assert result == '{"type":"message","text":"hello"}'


@pytest.mark.asyncio
class TestAsyncJsonWebsocketConsumer:
    async def test_decode_json(self) -> None:
        payload = '{"type":"message","text":"hello"}'

        result = await AsyncJsonWebsocketConsumer.decode_json(payload)

        assert result == {"type": "message", "text": "hello"}

    async def test_encode_json(self) -> None:
        payload = {"type": "message", "text": "hello"}

        result = await AsyncJsonWebsocketConsumer.encode_json(payload)

        assert isinstance(result, str)
        assert result == '{"type":"message","text":"hello"}'
