import re
from typing import Any

from asyncio_extensions import checkpoint, sleep_forever
from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import BaseChannelLayer
from channels.layers import get_channel_layer as original_get_channel_layer
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string

from ._compat import override


class DummyChannelLayer(BaseChannelLayer):
    """Dummy channel layer implementation.

    This is a no-op channel layer. It never send or receive any message.
    """

    extensions = ["groups", "flush"]  # noqa: RUF012

    def __init__(
        self,
        expiry: int = 60,
        capacity: int = 100,
        channel_capacity: dict[re.Pattern[str] | str, int] | None = None,
    ) -> None:
        super().__init__(expiry, capacity, channel_capacity)

    @override
    async def send(self, channel: str, message: dict[str, Any]) -> None:  # noqa: ARG002
        """
        Send a message onto a (general or specific) channel.

        Do nothing.
        """
        await checkpoint()

    @override
    async def receive(self, channel: str) -> dict[str, Any]:  # noqa: ARG002
        """
        Receive the first message that arrives on the channel.

        Never returns.
        """
        await sleep_forever()

    @override
    async def new_channel(self, prefix: str = "specific") -> str:
        """
        Returns a new channel name that can be used by something in our
        process as a specific channel.
        """
        return f"{prefix}.null!{get_random_string(12)}"

    @override
    async def flush(self) -> None:
        """Resets the channel layer to a blank state."""
        await checkpoint()

    @override
    async def group_add(self, group: str, channel: str) -> None:  # noqa: ARG002
        """Add a channel to the group."""
        await checkpoint()

    @override
    async def group_discard(self, group: str, channel: str) -> None:  # noqa: ARG002
        """Remove the channel from the group."""
        await checkpoint()

    @override
    async def group_send(self, group: str, message: dict[str, Any]) -> None:  # noqa: ARG002
        """Send a message to the group."""
        await checkpoint()


def get_channel_layer(alias: str = DEFAULT_CHANNEL_LAYER) -> BaseChannelLayer:
    """Returns a channel layer by alias.

    This is a wrapper around :func:`channels.layers.get_channel_layer` that throws an error for
    invalid aliases.

    Returns:
        The channel layer.

    Raises:
        ImproperlyConfigured: when the alias is invalid.
    """
    channel_layer: BaseChannelLayer | None = original_get_channel_layer(alias)

    if not channel_layer:
        msg: str = "{alias} isn't an available channel layer"
        raise ImproperlyConfigured(msg)

    return channel_layer
