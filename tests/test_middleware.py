from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.instrumentation.digma import digma_opentelemetry_boostrap, DigmaConfiguration
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import _Span
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span

from src.opentelemetry.instrumentation.digma.fastapi import DigmaFastAPIInstrumentor


class TestDigmaMiddleware:


    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        app = FastAPI()
        self.app=app

        tracer = trace.get_tracer(__name__)
        digma_opentelemetry_boostrap(service_name='server-ms', digma_backend="http://localhost:5050",
                                     configuration=DigmaConfiguration().trace_this_package())
        FastAPIInstrumentor.instrument_app(app)
        DigmaFastAPIInstrumentor.instrument_app(app)

        self.client = TestClient(self.app)



    def test_creates_default_span_for_request(self):

        in_context_span: Span=None

        @self.app.get("/")
        async def read_main():
            in_context_span=trace.get_current_span()
            return {"current_span": trace.get_current_span().name}

        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"current_span": "/"}


    def test_injects_digma_required_attributes(self):

        internal_span_attr: Dict[str,str]= {}

        @self.app.get("/")
        async def read_main():
            in_context_span : _Span=trace.get_current_span()
            for key in in_context_span.attributes.keys():
                internal_span_attr[key]=in_context_span.attributes.get(key)
            return {"current_span": trace.get_current_span().name}

        response = self.client.get("/")
        assert response.status_code == 200

        assert SpanAttributes.CODE_NAMESPACE in internal_span_attr
        assert internal_span_attr[SpanAttributes.CODE_NAMESPACE] == read_main.__module__
        assert SpanAttributes.CODE_FUNCTION in internal_span_attr
        assert internal_span_attr[SpanAttributes.CODE_FUNCTION] == read_main.__qualname__
        assert SpanAttributes.CODE_FILEPATH in internal_span_attr
        assert internal_span_attr[SpanAttributes.CODE_FILEPATH] == read_main.__code__.co_filename
        assert SpanAttributes.CODE_LINENO in internal_span_attr
        assert internal_span_attr[SpanAttributes.CODE_LINENO] == read_main.__code__.co_firstlineno

