import os
from typing import Optional

class Config:
    """Configuration settings for the metrics monitoring system."""

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Metrics configuration
    METRICS_COLLECTION_INTERVAL: int = int(os.getenv("METRICS_COLLECTION_INTERVAL", "5"))
    ENABLE_SYSTEM_METRICS: bool = os.getenv("ENABLE_SYSTEM_METRICS", "true").lower() == "true"

    # Histogram buckets for request duration (in seconds)
    REQUEST_DURATION_BUCKETS: tuple = (
        0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0
    )

    # Application metadata
    APP_NAME: str = os.getenv("APP_NAME", "fastapi-metrics-app")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # Prometheus metrics endpoint
    METRICS_PATH: str = "/metrics"

config = Config()
