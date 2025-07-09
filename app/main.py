from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import asyncio
import uvicorn
from contextlib import asynccontextmanager

from app.config import config
from app.middleware.metrics_middleware import MetricsMiddleware
from app.routers import api, health
from app.metrics.system_metrics import system_metrics

# Background task for system metrics collection
async def collect_system_metrics():
    """Background task to collect system metrics periodically."""
    while True:
        try:
            system_metrics.collect_metrics()
            await asyncio.sleep(config.METRICS_COLLECTION_INTERVAL)
        except Exception as e:
            print(f"Error in system metrics collection: {e}")
            await asyncio.sleep(config.METRICS_COLLECTION_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting FastAPI Metrics Monitoring System...")

    # Start background task for system metrics collection
    task = None
    if config.ENABLE_SYSTEM_METRICS:
        task = asyncio.create_task(collect_system_metrics())
        print("System metrics collection started")

    yield

    # Shutdown
    print("Shutting down FastAPI Metrics Monitoring System...")
    if task and config.ENABLE_SYSTEM_METRICS:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        print("System metrics collection stopped")

# Create FastAPI application
app = FastAPI(
    title="FastAPI Metrics Monitoring System",
    description="A comprehensive FastAPI application with built-in metrics collection using Prometheus",
    version=config.APP_VERSION,
    lifespan=lifespan
)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(api.router, tags=["api"])
app.include_router(health.router, tags=["health"])

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="info"
    )
