from typing import TYPE_CHECKING, TypeGuard, assert_never

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, HTTPScope, Scope
from channels.middleware import BaseMiddleware
from opentelemetry import trace

from ._compat import override

if TYPE_CHECKING:
    from channels.utils import _ChannelApplication

tracer: trace.Tracer = trace.get_tracer(__name__)


def is_http_scope(scope: Scope) -> TypeGuard[HTTPScope]:
    return scope["type"] == "http"


class OTELMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> "_ChannelApplication":
        match scope["type"]:
            case "http":
                span_name = f"{scope['method']} {scope['path']}"
            case "websocket":
                span_name = f"WebSocket {scope['path']}"
            case "lifespan":
                span_name = "Lifespan"
            case "channel":
                span_name = f"receive {scope['channel']}"
            case _:
                assert_never(scope["type"])

        with tracer.start_as_current_span(name=span_name):
            return await super().__call__(scope, receive, send)  # type: ignore[arg-type]
