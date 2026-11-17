from collections.abc import Iterator
from typing import Any
from unittest import mock

import pytest
from asgiref.sync import SyncToAsync, async_to_sync

from channels_extensions.middleware import ThreadSensitiveMiddleware


@pytest.fixture(autouse=True)
def mock_aclose_old_connections() -> Iterator[mock.AsyncMock]:
    with mock.patch("channels_extensions.middleware.aclose_old_connections", new_callable=mock.AsyncMock) as mocked:
        yield mocked


class TestThreadSensitiveMiddleware:
    def test_call_inner_application(self) -> None:
        scope: dict[str, Any] = {"type": "http"}
        receive = mock.AsyncMock()
        send = mock.AsyncMock()
        inner = mock.AsyncMock()

        async_to_sync(ThreadSensitiveMiddleware(inner))(scope, receive, send)

        inner.assert_awaited_once_with(scope, receive, send)

    def test_call_distinct_context_per_call(self) -> None:
        calls = range(3)
        contexts: list[object] = []

        async def inner(scope: dict[str, Any], receive: object, send: object) -> None:  # noqa: ARG001
            contexts.append(SyncToAsync.thread_sensitive_context.get())

        middleware = ThreadSensitiveMiddleware(inner)
        for _ in calls:
            async_to_sync(middleware)({}, mock.AsyncMock(), mock.AsyncMock())

        assert None not in contexts
        assert len({id(context) for context in contexts}) == len(calls)

    def test_call_context_cleared_afterwards(self) -> None:
        async def run() -> object:
            await ThreadSensitiveMiddleware(mock.AsyncMock())({}, mock.AsyncMock(), mock.AsyncMock())
            return SyncToAsync.thread_sensitive_context.get(None)

        assert async_to_sync(run)() is None

    def test_call_closes_old_connections(self, mock_aclose_old_connections: mock.AsyncMock) -> None:
        async_to_sync(ThreadSensitiveMiddleware(mock.AsyncMock()))({}, mock.AsyncMock(), mock.AsyncMock())

        mock_aclose_old_connections.assert_awaited_once_with()

    def test_call_closes_old_connections_when_inner_raises(self, mock_aclose_old_connections: mock.AsyncMock) -> None:
        inner = mock.AsyncMock(side_effect=RuntimeError("boom"))

        with pytest.raises(RuntimeError, match="boom"):
            async_to_sync(ThreadSensitiveMiddleware(inner))({}, mock.AsyncMock(), mock.AsyncMock())

        mock_aclose_old_connections.assert_awaited_once_with()
