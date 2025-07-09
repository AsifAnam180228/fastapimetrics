#!/usr/bin/env python3
"""
Setup script for FastAPI Metrics Monitoring System with Docker
"""
import subprocess
import sys
import time
import requests
import os

def run_command(command, description, check_output=False):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return False
            print(f"✅ {description} completed successfully")
            return True
        else:
            subprocess.run(command, shell=True, check=True)
            print(f"✅ {description} completed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        return False

def wait_for_service(url, service_name, max_attempts=30):
    """Wait for a service to become available."""
    print(f"\n⏳ Waiting for {service_name} to start...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except:
            pass

        print(f"   Attempt {attempt + 1}/{max_attempts} - {service_name} not ready yet...")
        time.sleep(2)

    print(f"❌ {service_name} failed to start after {max_attempts * 2} seconds")
    return False

def main():
    print("🚀 FastAPI Metrics Monitoring System Setup")
    print("=" * 60)

    # Check if Docker is running
    if not run_command("docker --version", "Checking Docker installation", check_output=True):
        print("\n❌ Docker is not installed or not running.")
        print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        sys.exit(1)

    if not run_command("docker-compose --version", "Checking Docker Compose", check_output=True):
        print("\n❌ Docker Compose is not available.")
        sys.exit(1)

    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"\n📁 Working directory: {project_dir}")

    # Build and start services
    print("\n🏗️  Building and starting monitoring stack...")

    # Stop any existing containers
    run_command("docker-compose down", "Stopping existing containers")

    # Build the FastAPI image
    if not run_command("docker-compose build fastapi-metrics", "Building FastAPI image"):
        sys.exit(1)

    # Start all services
    if not run_command("docker-compose up -d", "Starting all services"):
        sys.exit(1)

    # Wait for services to be ready
    services = [
        ("http://localhost:8000/health", "FastAPI Application"),
        ("http://localhost:9090", "Prometheus"),
        ("http://localhost:3000", "Grafana")
    ]

    all_ready = True
    for url, name in services:
        if not wait_for_service(url, name):
            all_ready = False

    if all_ready:
        print("\n" + "🎉" * 20)
        print("SUCCESS! All services are running!")
        print("🎉" * 20)

        print("\n📊 Access your monitoring stack:")
        print("├── FastAPI Application: http://localhost:8000")
        print("├── API Documentation:   http://localhost:8000/docs")
        print("├── Health Check:        http://localhost:8000/health")
        print("├── Metrics Endpoint:    http://localhost:8000/metrics")
        print("├── Prometheus:          http://localhost:9090")
        print("└── Grafana Dashboard:   http://localhost:3000")

        print("\n🔐 Grafana Login:")
        print("├── Username: admin")
        print("└── Password: admin")

        print("\n🧪 Test the system:")
        print("# Generate some test traffic")
        print("curl -X POST http://localhost:8000/data -H 'Content-Type: application/json' -d '{\"key\": \"test\", \"value\": \"hello\"}'")
        print("curl http://localhost:8000/data")
        print("curl http://localhost:8000/health")

        print("\n📈 The FastAPI Metrics Dashboard should be automatically loaded in Grafana!")

    else:
        print("\n❌ Some services failed to start. Check the logs:")
        print("docker-compose logs")

    print(f"\n🛑 To stop all services: docker-compose down")

if __name__ == "__main__":
    main()
