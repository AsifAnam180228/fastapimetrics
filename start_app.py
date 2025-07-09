#!/usr/bin/env python3
"""
Simple startup script for FastAPI Metrics Monitoring System
"""
import os
import sys

def main():
    """Start the FastAPI application with proper error handling."""

    print("FastAPI Metrics Monitoring System - Startup")
    print("=" * 50)

    # Set the working directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # Add project directory to Python path
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[0]}")

    # Try to import and run the application
    try:
        print("\nTesting imports...")

        # Test basic imports
        import fastapi
        import uvicorn
        import prometheus_client
        import psutil
        print("✓ Basic dependencies imported successfully")

        # Test app config
        from app.config import config
        print("✓ Configuration loaded")

        # Test metrics modules
        from app.metrics.system_metrics import system_metrics
        from app.metrics.http_metrics import http_metrics
        print("✓ Metrics modules loaded")

        # Test middleware
        from app.middleware.metrics_middleware import MetricsMiddleware
        print("✓ Middleware loaded")

        # Test routers
        from app.routers import api, health
        print("✓ Routers loaded")

        # Test main app
        from app.main import app
        print("✓ Main application loaded")

        print("\n✅ All imports successful!")

        # Start the server
        print("\nStarting FastAPI server...")
        print("Server will be available at: http://127.0.0.1:8000")
        print("Health check: http://127.0.0.1:8000/health")
        print("Metrics: http://127.0.0.1:8000/metrics")
        print("API docs: http://127.0.0.1:8000/docs")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 50)

        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )

    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
