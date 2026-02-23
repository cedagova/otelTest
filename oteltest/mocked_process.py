"""Mocked process for telemetry demo: network, db, and business logic with spans."""

import time
from opentelemetry.trace import Tracer


def fetch_external_api(tracer: Tracer) -> None:
    """Mock outgoing network request (e.g. call to payment or partner API)."""
    with tracer.start_as_current_span("fetch_external_api") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("peer.service", "mock-external-api")
        time.sleep(0.15)


def query_database(tracer: Tracer) -> None:
    """Mock database query."""
    with tracer.start_as_current_span("query_database") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.operation", "SELECT")
        time.sleep(0.25)


def run_business_logic(tracer: Tracer) -> None:
    """Mock business logic (validation, rules, aggregation)."""
    with tracer.start_as_current_span("run_business_logic") as span:
        span.set_attribute("business.operation", "process")
        time.sleep(0.2)


def run_mocked_process(tracer: Tracer) -> None:
    """Run the full mocked process: network → db → business logic (showcase trace)."""
    with tracer.start_as_current_span("run_mocked_process") as span:
        span.set_attribute("process.type", "traces_demo")
        fetch_external_api(tracer)
        query_database(tracer)
        run_business_logic(tracer)
