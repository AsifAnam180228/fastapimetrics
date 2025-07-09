from fastapi import APIRouter
from pydantic import BaseModel
import time
import psutil
from typing import Dict, Any

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    uptime: float
    system: Dict[str, Any]
    application: Dict[str, Any]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with system information."""
    try:
        process = psutil.Process()
        current_time = time.time()

        # Calculate uptime
        uptime = current_time - process.create_time()

        # Get system information
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Get process information
        process_memory = process.memory_info()

        return HealthResponse(
            status="healthy",
            timestamp=current_time,
            uptime=uptime,
            system={
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "used": disk.used,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            application={
                "process_id": process.pid,
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads(),
                "status": process.status()
            }
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            timestamp=time.time(),
            uptime=0,
            system={},
            application={"error": str(e)}
        )

@router.get("/health/ready")
async def readiness_check():
    """Readiness check for Kubernetes/container orchestration."""
    return {"status": "ready", "timestamp": time.time()}

@router.get("/health/live")
async def liveness_check():
    """Liveness check for Kubernetes/container orchestration."""
    return {"status": "alive", "timestamp": time.time()}
