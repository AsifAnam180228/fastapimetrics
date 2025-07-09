from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
import json
import time
import asyncio

router = APIRouter()

# In-memory data store for demonstration
data_store: Dict[str, Any] = {}

class DataItem(BaseModel):
    key: str
    value: Any
    timestamp: float = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = time.time()
        super().__init__(**data)

class DataResponse(BaseModel):
    success: bool
    message: str
    data: Any = None

@router.get("/")
async def root():
    """Root endpoint with basic response."""
    return {
        "message": "FastAPI Metrics Monitoring System",
        "version": "1.0.0",
        "status": "running",
        "timestamp": time.time()
    }

@router.post("/data", response_model=DataResponse)
async def create_data(item: DataItem):
    """Sample data processing endpoint."""
    try:
        # Simulate some processing time
        await asyncio.sleep(0.01)

        # Store the data
        data_store[item.key] = {
            "value": item.value,
            "timestamp": item.timestamp,
            "created_at": time.time()
        }

        return DataResponse(
            success=True,
            message=f"Data stored successfully for key: {item.key}",
            data={"key": item.key, "stored_at": time.time()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

@router.get("/data", response_model=DataResponse)
async def get_all_data():
    """Sample data retrieval endpoint - get all data."""
    try:
        return DataResponse(
            success=True,
            message="Data retrieved successfully",
            data={
                "items": data_store,
                "count": len(data_store),
                "retrieved_at": time.time()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@router.get("/data/{key}", response_model=DataResponse)
async def get_data(key: str):
    """Sample data retrieval endpoint - get specific data by key."""
    try:
        if key not in data_store:
            raise HTTPException(status_code=404, detail=f"Data not found for key: {key}")

        return DataResponse(
            success=True,
            message=f"Data retrieved successfully for key: {key}",
            data=data_store[key]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@router.delete("/data/{key}", response_model=DataResponse)
async def delete_data(key: str):
    """Delete data by key."""
    try:
        if key not in data_store:
            raise HTTPException(status_code=404, detail=f"Data not found for key: {key}")

        deleted_item = data_store.pop(key)

        return DataResponse(
            success=True,
            message=f"Data deleted successfully for key: {key}",
            data={"deleted_item": deleted_item, "deleted_at": time.time()}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting data: {str(e)}")
