"""Site-related ASGI middlewares."""

from __future__ import annotations

# Python 3.15+: defer importing models until first use, so this module can be imported before the app registry is ready.
__lazy_modules__ = ["django.contrib.sites.models"]

import asyncio
from copy import copy
from typing import TYPE_CHECKING, Any

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.sites.models import Site

if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication, ASGIReceiveCallable, ASGISendCallable


class CurrentSiteMiddleware(BaseMiddleware):
    """Middleware that adds the current Site object to the scope."""

    def __init__(self, inner: ASGIApplication) -> None:
        """Wrap the ``inner`` ASGI application."""
        super().__init__(inner)
        self._lock = asyncio.Lock()

    async def __call__(self, scope: dict[str, Any], receive: ASGIReceiveCallable, send: ASGISendCallable) -> Any:  # type: ignore[override]  # noqa: ANN401
        """Add ``site`` to the scope, if missing, and call the inner application."""
        if "site" not in scope:
            async with self._lock:
                if "site" not in scope:
                    scope = copy(scope)
                    scope["site"] = await database_sync_to_async(Site.objects.get_current)()
        return await super().__call__(scope, receive, send)  # type: ignore[arg-type]
