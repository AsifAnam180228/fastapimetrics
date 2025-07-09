import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.metrics.http_metrics import http_metrics

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP request metrics."""

    async def dispatch(self, request: Request, call_next):
        # Skip metrics collection for the metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        # Extract request information
        method = request.method
        endpoint = request.url.path

        # Get request size
        request_size = 0
        if hasattr(request, 'headers'):
            content_length = request.headers.get('content-length')
            if content_length:
                try:
                    request_size = int(content_length)
                except ValueError:
                    pass

        # Increment active requests
        http_metrics.increment_active_requests(method, endpoint)

        # Record start time
        start_time = time.time()

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Get response size
            response_size = 0
            if hasattr(response, 'headers'):
                content_length = response.headers.get('content-length')
                if content_length:
                    try:
                        response_size = int(content_length)
                    except ValueError:
                        pass

            # Record metrics
            http_metrics.record_request(
                method=method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration=duration,
                request_size=request_size,
                response_size=response_size
            )

            return response

        except Exception as e:
            # Calculate duration for failed requests
            duration = time.time() - start_time

            # Record metrics for failed requests (500 status)
            http_metrics.record_request(
                method=method,
                endpoint=endpoint,
                status_code=500,
                duration=duration,
                request_size=request_size,
                response_size=0
            )

            # Re-raise the exception
            raise e

        finally:
            # Decrement active requests
            http_metrics.decrement_active_requests(method, endpoint)
