"""ASGI middlewares."""

from __future__ import annotations

# Python 3.15+: defer importing ``channels.db`` until first use.
__lazy_modules__ = ["channels.db"]

from typing import TYPE_CHECKING, Any

from asgiref.sync import ThreadSensitiveContext
from channels.db import aclose_old_connections
from channels.middleware import BaseMiddleware

from ._compat import override

if TYPE_CHECKING:
    from asgiref.typing import ASGIReceiveCallable, ASGISendCallable


class ThreadSensitiveMiddleware(BaseMiddleware):
    """Run each connection inside its own :class:`asgiref.sync.ThreadSensitiveContext`.

    By default, every ``sync_to_async(thread_sensitive=True)`` call (the ORM, the async ORM)
    is serialized on a single process-wide thread. With this middleware each scope gets its
    own thread, so independent connections do not block each other.

    The context's thread is discarded when the scope ends, so database connections opened on
    it are closed before leaving the context. Otherwise, WebSocket consumers using
    ``sync_to_async`` or the async ORM would never return their connection to the pool.

    Place it as the outermost middleware, wrapping tracing, authentication and the like.
    Each WebSocket that queried the database holds a connection until it closes, so size the
    connection pool for the number of concurrent sockets.
    """

    @override
    async def __call__(self, scope: dict[str, Any], receive: ASGIReceiveCallable, send: ASGISendCallable) -> Any:  # type: ignore[override]
        """Call the inner application inside a new thread sensitive context."""
        async with ThreadSensitiveContext():
            try:
                return await super().__call__(scope, receive, send)  # type: ignore[arg-type]
            finally:
                await aclose_old_connections()
