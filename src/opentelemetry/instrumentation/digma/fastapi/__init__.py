from os import environ
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class DigmaFastAPIInstrumentor:

    @staticmethod
    def instrument_app(app: FastAPI):
        if hasattr(app, "_is_instrumented_by_opentelemetry") and app._is_instrumented_by_opentelemetry:
            app.user_middleware.append(
                Middleware(BaseHTTPMiddleware, dispatch=DigmaFastAPIInstrumentor.add_digma_attributes))
            app.middleware_stack = app.build_middleware_stack()

        else:
            app.add_middleware(BaseHTTPMiddleware, dispatch=DigmaFastAPIInstrumentor.add_digma_attributes)


    @staticmethod
    async def add_digma_attributes(request: Request, call_next):
        span = trace.get_current_span()
        if span and span.is_recording():
            view_routes = [route for route in request.app.routes if route.path == request.scope["path"]]
            if (view_routes and len(view_routes) == 1):
                view_func = view_routes[0].dependant.call
                span.set_attribute(SpanAttributes.CODE_NAMESPACE, view_func.__module__)
                span.set_attribute(SpanAttributes.CODE_FUNCTION, view_func.__qualname__)
                span.set_attribute(SpanAttributes.CODE_FILEPATH, view_func.__code__.co_filename)
                span.set_attribute(SpanAttributes.CODE_LINENO, view_func.__code__.co_firstlineno)
        response = await call_next(request)
        return response

