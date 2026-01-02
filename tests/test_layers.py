import asyncio

import pytest
from asyncio_extensions import TaskGroup, checkpoint
from channels.layers import BaseChannelLayer
from django.core.exceptions import ImproperlyConfigured
from faker import Faker
from pytest_django.fixtures import SettingsWrapper

from channels_extensions.layers import DummyChannelLayer, get_channel_layer


@pytest.mark.asyncio
class TestDummyChannelLayer:
    async def test_send(self) -> None:
        channel_layer = DummyChannelLayer()

        await channel_layer.send("black hole", {})

    async def test_receive(self) -> None:
        channel_layer = DummyChannelLayer()

        with pytest.raises(asyncio.TimeoutError):
            async with asyncio.timeout(3):
                await channel_layer.receive("black hole")

    async def test_receive_concurrency(self) -> None:
        channel_layer = DummyChannelLayer()

        with pytest.raises(asyncio.TimeoutError):  # noqa: PT012
            async with asyncio.timeout(3), TaskGroup() as tg:
                to_cancel = [tg.create_task(channel_layer.receive("black hole")) for _ in range(5)]
                for _ in range(3):
                    tg.create_task(channel_layer.receive("black hole"))

                await checkpoint()

                for t in to_cancel:
                    t.cancel()

    async def test_new_channel(self) -> None:
        channel_layer = DummyChannelLayer()
        expected_prefix = "specific.null!"

        got: str = await channel_layer.new_channel()

        assert got.startswith(expected_prefix)
        assert len(got) == len(expected_prefix) + 12

    async def test_new_channel_custom_prefix(self) -> None:
        channel_layer = DummyChannelLayer()
        expected_prefix = "something.null!"

        got: str = await channel_layer.new_channel("something")

        assert got.startswith(expected_prefix)
        assert len(got) == len(expected_prefix) + 12

    async def test_flush(self) -> None:
        channel_layer = DummyChannelLayer()

        await channel_layer.flush()

    async def test_group_add(self) -> None:
        channel_layer = DummyChannelLayer()

        await channel_layer.group_add("group", "channel")

    async def test_group_discard(self) -> None:
        channel_layer = DummyChannelLayer()

        await channel_layer.group_discard("group", "channel")

    async def test_group_send(self) -> None:
        channel_layer = DummyChannelLayer()

        await channel_layer.group_send("group", {})


class TestGetChannelLayer:
    @pytest.fixture(autouse=True)
    def channel_layers(self, settings: SettingsWrapper) -> None:
        """Channel layers to test."""
        settings.CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "channels.layers.InMemoryChannelLayer",
                "CONFIG": {
                    "capacity": 10,
                },
            },
            "custom": {
                "BACKEND": "channels.layers.InMemoryChannelLayer",
                "CONFIG": {
                    "capacity": 20,
                },
            },
        }

    def test_get_channel_layer_default(self) -> None:
        """Test if :func:`get_channel_layer` uses the default alias."""
        channel_layer: BaseChannelLayer = get_channel_layer()

        assert isinstance(channel_layer, BaseChannelLayer)
        assert channel_layer.capacity == 10

    def test_get_channel_layer_by_alias(self) -> None:
        """Test if :func:`get_channel_layer` uses a custom alias."""
        channel_layer: BaseChannelLayer = get_channel_layer("custom")

        assert isinstance(channel_layer, BaseChannelLayer)
        assert channel_layer.capacity == 20

    def test_get_channel_layer_invalid(self, faker: Faker) -> None:
        """Test if :func:`get_channel_layer` raises for invalid alias."""
        with pytest.raises(ImproperlyConfigured):
            get_channel_layer(faker.slug())
