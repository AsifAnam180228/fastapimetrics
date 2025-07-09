#!/usr/bin/env python3
"""
Test script to verify FastAPI Metrics Monitoring System is working correctly.
"""
import sys
import os
import subprocess
import time
import requests
from pathlib import Path

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    try:
        from app.config import config
        from app.metrics.system_metrics import system_metrics
        from app.metrics.http_metrics import http_metrics
        from app.middleware.metrics_middleware import MetricsMiddleware
        from app.routers import api, health
        from app.main import app
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed."""
    print("Testing dependencies...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'prometheus-client',
        'psutil',
        'pydantic'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")

    if missing_packages:
        print(f"\nPlease install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    return True

def test_application_startup():
    """Test that the application can start without errors."""
    print("Testing application startup...")
    try:
        from app.main import app
        print("✓ Application object created successfully")
        return True
    except Exception as e:
        print(f"✗ Application startup error: {e}")
        return False

def run_server_test():
    """Run the server and test basic endpoints."""
    print("Starting server test...")

    # Start the server in a subprocess
    try:
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 'app.main:app',
            '--host', '127.0.0.1', '--port', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for server to start
        time.sleep(3)

        # Test endpoints
        base_url = "http://127.0.0.1:8000"

        # Test root endpoint
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print("✓ Root endpoint working")
            else:
                print(f"✗ Root endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Root endpoint error: {e}")

        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Health endpoint working")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Health endpoint error: {e}")

        # Test metrics endpoint
        try:
            response = requests.get(f"{base_url}/metrics", timeout=5)
            if response.status_code == 200:
                print("✓ Metrics endpoint working")
                print(f"  Metrics data length: {len(response.text)} characters")
            else:
                print(f"✗ Metrics endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Metrics endpoint error: {e}")

        # Test POST endpoint
        try:
            response = requests.post(f"{base_url}/data", json={
                "key": "test",
                "value": "test_value"
            }, timeout=5)
            if response.status_code == 200:
                print("✓ POST data endpoint working")
            else:
                print(f"✗ POST data endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"✗ POST data endpoint error: {e}")

    except Exception as e:
        print(f"✗ Server test error: {e}")
    finally:
        # Cleanup
        if 'process' in locals():
            process.terminate()
            process.wait()

def main():
    """Run all tests."""
    print("FastAPI Metrics Monitoring System - Test Suite")
    print("=" * 50)

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Application Startup", test_application_startup),
    ]

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        if not success:
            print(f"\n❌ Test failed: {test_name}")
            print("Please fix the issues above before proceeding.")
            return False

    print(f"\n✅ All basic tests passed!")

    # Ask user if they want to run server test
    try:
        answer = input("\nDo you want to run the server test? (y/n): ").lower()
        if answer == 'y':
            run_server_test()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    main()
