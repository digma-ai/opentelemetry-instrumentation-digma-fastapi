# opentelemetry-instrumentation-digma-fastapi
[![Tests](https://github.com/digma-ai/opentelemetry-instrumentation-digma-fastapi/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/digma-ai/opentelemetry-instrumentation-digma-fastapi/actions/workflows/unit-tests.yml)
[![PyPI version](https://badge.fury.io/py/opentelemetry-instrumentation-digma-fastapi.svg)](https://badge.fury.io/py/opentelemetry-instrumentation-digma-fastapi)

This package extends the default FastAPI instrumentation for OTEL to provide additional attributes which can be used to facilitate Continuous Feedback back to the code. 

## Installing the package
```bash
pip install opentelemetry-instrumentation-digma-fastapi
```
Or add it to your requirements/poetry file.

## Instrumenting your FastAPI project

### Enable OpenTelemetry in your project
First, configure OpenTelemetry in your project. See the [Digma instrumentation](https://github.com/digma-ai/opentelemetry-instrumentation-digma) repo for quick instructions on getting that done, whether you're already using OTEL or not.

Make sure you've instrumented your FastAPI application using the standard Pypi package.
1. Install the package:
``` pip install opentelemetry-instrumentation-fastapi ```
2. Instrument the FastAPI app by adding the following to your app setup: 
```python 
FastAPIInstrumentor.instrument_app(app) 
```

More info can be found in the [official package documentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html). 

### Enable the Digma OpenTelemetry instrumentation

Before or after the call to ```FastAPIInstrumentor.instrument``` to enable OTEL, also add the following:

```python 
DigmaFastAPIInstrumentor().instrument_app(app)
```

### Check out some sample projects

You can review a simple example in the [FastAPI Sample Repo](https://github.com/digma-ai/otel-sample-fastapi)
Or a more complex real world example in the [Gringotts Vault API application](https://github.com/doppleware/gringotts-vault-api) (which includes both FastAPI, Postgres, RabbitMQ and other technologies)
