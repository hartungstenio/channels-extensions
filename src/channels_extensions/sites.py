import asyncio
from copy import copy
from typing import TYPE_CHECKING

from asgiref.typing import ASGIApplication, ASGIReceiveCallable, ASGISendCallable, Scope
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.sites.models import Site

if TYPE_CHECKING:
    from channels.utils import _ChannelApplication


class CurrentSiteMiddleware(BaseMiddleware):
    """
    Middleware that adds the current Site object to the scope.
    """

    def __init__(self, inner: ASGIApplication) -> None:
        super().__init__(inner)
        self._lock = asyncio.Lock()

    async def __call__(
        self,
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> "_ChannelApplication":
        if "site" not in scope:
            async with self._lock:
                if "site" not in scope:
                    scope = copy(scope)
                    scope["site"] = await database_sync_to_async(Site.objects.get_current)()  # type: ignore[typeddict-unknown-key]
        return await super().__call__(scope, receive, send)  # type: ignore[arg-type]
