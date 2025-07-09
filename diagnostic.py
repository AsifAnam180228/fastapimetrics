"""
Simple diagnostic script to identify the exact import issue.
"""
import sys
import traceback

def test_step_by_step():
    """Test imports step by step to find the exact issue."""

    print("Testing step-by-step imports...")

    # Test 1: Basic imports
    try:
        import fastapi
        print("✓ fastapi imported")
    except Exception as e:
        print(f"✗ fastapi import failed: {e}")
        return False

    try:
        import uvicorn
        print("✓ uvicorn imported")
    except Exception as e:
        print(f"✗ uvicorn import failed: {e}")
        return False

    try:
        import prometheus_client
        print("✓ prometheus_client imported")
    except Exception as e:
        print(f"✗ prometheus_client import failed: {e}")
        return False

    try:
        import psutil
        print("✓ psutil imported")
    except Exception as e:
        print(f"✗ psutil import failed: {e}")
        return False

    # Test 2: Config
    try:
        from app.config import config
        print("✓ app.config imported")
    except Exception as e:
        print(f"✗ app.config import failed: {e}")
        traceback.print_exc()
        return False

    # Test 3: System metrics
    try:
        from app.metrics.system_metrics import system_metrics
        print("✓ app.metrics.system_metrics imported")
    except Exception as e:
        print(f"✗ app.metrics.system_metrics import failed: {e}")
        traceback.print_exc()
        return False

    # Test 4: HTTP metrics
    try:
        from app.metrics.http_metrics import http_metrics
        print("✓ app.metrics.http_metrics imported")
    except Exception as e:
        print(f"✗ app.metrics.http_metrics import failed: {e}")
        traceback.print_exc()
        return False

    # Test 5: Middleware
    try:
        from app.middleware.metrics_middleware import MetricsMiddleware
        print("✓ app.middleware.metrics_middleware imported")
    except Exception as e:
        print(f"✗ app.middleware.metrics_middleware import failed: {e}")
        traceback.print_exc()
        return False

    # Test 6: Routers
    try:
        from app.routers import api, health
        print("✓ app.routers imported")
    except Exception as e:
        print(f"✗ app.routers import failed: {e}")
        traceback.print_exc()
        return False

    # Test 7: Main app
    try:
        from app.main import app
        print("✓ app.main imported")
    except Exception as e:
        print(f"✗ app.main import failed: {e}")
        traceback.print_exc()
        return False

    print("\n✅ All imports successful!")
    return True

def test_app_creation():
    """Test if the FastAPI app can be created."""
    try:
        from app.main import app
        print(f"✓ FastAPI app created: {type(app)}")
        print(f"✓ App title: {app.title}")
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("FastAPI Metrics Monitoring System - Diagnostic Test")
    print("=" * 60)

    success = test_step_by_step()
    if success:
        print("\n" + "=" * 60)
        print("Testing app creation...")
        test_app_creation()

        print("\n" + "=" * 60)
        print("✅ All tests passed! The application should be ready to run.")
        print("\nTry running:")
        print("python -m app.main")
        print("or")
        print("uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    else:
        print("\n❌ There are import issues that need to be fixed.")
