import asyncio
from copy import copy
from typing import Any

from asgiref.typing import ASGIApplication, ASGIReceiveCallable, ASGISendCallable
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.sites.models import Site


class CurrentSiteMiddleware(BaseMiddleware):
    """
    Middleware that adds the current Site object to the scope.
    """

    def __init__(self, inner: ASGIApplication) -> None:
        super().__init__(inner)
        self._lock = asyncio.Lock()

    async def __call__(self, scope: dict[str, Any], receive: ASGIReceiveCallable, send: ASGISendCallable) -> Any:  # type: ignore[override]
        if "site" not in scope:
            async with self._lock:
                if "site" not in scope:
                    scope = copy(scope)
                    scope["site"] = await database_sync_to_async(Site.objects.get_current)()
        return await super().__call__(scope, receive, send)  # type: ignore[arg-type]
