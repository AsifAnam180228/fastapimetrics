from prometheus_client import Counter, Histogram
from app.config import config

class HTTPMetricsCollector:
    """Collects HTTP request metrics for monitoring."""

    def __init__(self):
        # Request volume metrics
        self.requests_total = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status_code']
        )

        # Request performance metrics
        self.request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            buckets=config.REQUEST_DURATION_BUCKETS
        )

        # Request size metrics
        self.request_size = Histogram(
            'http_request_size_bytes',
            'HTTP request size in bytes',
            ['method', 'endpoint'],
            buckets=(100, 1000, 10000, 100000, 1000000, 10000000)
        )

        # Response size metrics
        self.response_size = Histogram(
            'http_response_size_bytes',
            'HTTP response size in bytes',
            ['method', 'endpoint', 'status_code'],
            buckets=(100, 1000, 10000, 100000, 1000000, 10000000)
        )

        # Active requests gauge
        from prometheus_client import Gauge
        self.active_requests = Gauge(
            'http_requests_active',
            'Number of active HTTP requests',
            ['method', 'endpoint']
        )

    def record_request(self, method: str, endpoint: str, status_code: int,
                      duration: float, request_size: int = 0, response_size: int = 0):
        """Record metrics for a completed HTTP request."""

        # Normalize endpoint to avoid high cardinality
        normalized_endpoint = self._normalize_endpoint(endpoint)

        # Record request count
        self.requests_total.labels(
            method=method,
            endpoint=normalized_endpoint,
            status_code=str(status_code)
        ).inc()

        # Record request duration
        self.request_duration.labels(
            method=method,
            endpoint=normalized_endpoint
        ).observe(duration)

        # Record request size
        if request_size > 0:
            self.request_size.labels(
                method=method,
                endpoint=normalized_endpoint
            ).observe(request_size)

        # Record response size
        if response_size > 0:
            self.response_size.labels(
                method=method,
                endpoint=normalized_endpoint,
                status_code=str(status_code)
            ).observe(response_size)

    def increment_active_requests(self, method: str, endpoint: str):
        """Increment active requests counter."""
        normalized_endpoint = self._normalize_endpoint(endpoint)
        self.active_requests.labels(
            method=method,
            endpoint=normalized_endpoint
        ).inc()

    def decrement_active_requests(self, method: str, endpoint: str):
        """Decrement active requests counter."""
        normalized_endpoint = self._normalize_endpoint(endpoint)
        self.active_requests.labels(
            method=method,
            endpoint=normalized_endpoint
        ).dec()

    def _normalize_endpoint(self, endpoint: str) -> str:
        """Normalize endpoint to reduce cardinality."""
        # Remove query parameters
        if '?' in endpoint:
            endpoint = endpoint.split('?')[0]

        # Replace path parameters with placeholders
        import re
        # Replace UUIDs with {uuid}
        endpoint = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', endpoint)
        # Replace numeric IDs with {id}
        endpoint = re.sub(r'/\d+', '/{id}', endpoint)

        return endpoint

# Global instance
http_metrics = HTTPMetricsCollector()
