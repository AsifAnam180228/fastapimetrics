#!/usr/bin/env python3
"""
Step-by-step troubleshooting and setup for FastAPI monitoring stack
"""
import subprocess
import time
import os
import sys

def run_command(cmd, description, show_output=True):
    """Run command with error handling."""
    print(f"\n🔧 {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if show_output and result.stdout:
            print(f"✅ Output:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️  Stderr:\n{result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 FastAPI Monitoring Stack - Step by Step Setup")
    print("=" * 60)

    # Step 1: Clean up any existing containers
    print("\n📋 Step 1: Cleaning up existing containers")
    run_command("docker-compose down", "Stopping all containers")
    run_command("docker system prune -f", "Cleaning up Docker system")

    # Step 2: Check for port conflicts
    print("\n📋 Step 2: Checking for port conflicts")
    ports = ["8000", "9090", "3000"]
    for port in ports:
        run_command(f"netstat -ano | findstr :{port}", f"Checking port {port}")

    # Step 3: Validate configuration files
    print("\n📋 Step 3: Validating configuration files")

    # Check if prometheus.yml exists and is readable
    if os.path.exists("prometheus.yml"):
        print("✅ prometheus.yml exists")
        with open("prometheus.yml", "r") as f:
            content = f.read()
            print(f"📄 Prometheus config preview:\n{content[:200]}...")
    else:
        print("❌ prometheus.yml not found")
        return False

    # Step 4: Build FastAPI image first
    print("\n📋 Step 4: Building FastAPI application")
    if not run_command("docker-compose build fastapi-metrics", "Building FastAPI image"):
        print("❌ Failed to build FastAPI image. Check Dockerfile.")
        return False

    # Step 5: Start services one by one
    print("\n📋 Step 5: Starting services individually")

    # Start Prometheus first
    print("\n🔍 Starting Prometheus...")
    if not run_command("docker-compose up -d prometheus", "Starting Prometheus"):
        print("❌ Prometheus failed to start")
        run_command("docker-compose logs prometheus", "Checking Prometheus logs")
        return False

    # Wait for Prometheus
    print("\n⏳ Waiting for Prometheus to be ready...")
    for i in range(15):
        result = subprocess.run("docker-compose ps prometheus", shell=True, capture_output=True, text=True)
        if "Up" in result.stdout:
            print("✅ Prometheus container is up")
            break
        time.sleep(2)
        print(f"   Waiting... ({i+1}/15)")

    # Start FastAPI
    print("\n🔍 Starting FastAPI...")
    if not run_command("docker-compose up -d fastapi-metrics", "Starting FastAPI"):
        print("❌ FastAPI failed to start")
        run_command("docker-compose logs fastapi-metrics", "Checking FastAPI logs")
        return False

    # Start Grafana
    print("\n🔍 Starting Grafana...")
    if not run_command("docker-compose up -d grafana", "Starting Grafana"):
        print("❌ Grafana failed to start")
        run_command("docker-compose logs grafana", "Checking Grafana logs")
        return False

    # Step 6: Final status check
    print("\n📋 Step 6: Final status check")
    run_command("docker-compose ps", "Checking all services status")

    # Step 7: Test endpoints
    print("\n📋 Step 7: Testing endpoints")
    endpoints = [
        ("http://localhost:8000/health", "FastAPI Health"),
        ("http://localhost:9090", "Prometheus"),
        ("http://localhost:3000", "Grafana")
    ]

    time.sleep(5)  # Give services time to fully start

    for url, name in endpoints:
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=5)
            print(f"✅ {name} is accessible at {url}")
        except Exception as e:
            print(f"❌ {name} is not accessible at {url}: {e}")

    print("\n" + "🎉" * 20)
    print("Setup Complete!")
    print("🎉" * 20)

    print("\n📊 Access URLs:")
    print("├── FastAPI: http://localhost:8000")
    print("├── Prometheus: http://localhost:9090")
    print("└── Grafana: http://localhost:3000 (admin/admin)")

    print("\n🔧 If issues persist, check logs with:")
    print("docker-compose logs [service-name]")

if __name__ == "__main__":
    # Change to project directory
    project_dir = r"C:\Users\USER\PycharmProjects\MonitoringSystem"
    os.chdir(project_dir)
    main()
