#!/usr/bin/env python3
"""
Diagnostic script for troubleshooting Docker Compose issues
"""
import subprocess
import os
import json

def run_command_safe(command, description):
    """Run a command safely and return output."""
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run command: {e}")
        return False

def main():
    print("🔧 Docker Compose Diagnostic Tool")
    print("=" * 50)

    # Change to project directory
    project_dir = r"C:\Users\USER\PycharmProjects\MonitoringSystem"
    os.chdir(project_dir)

    # Check Docker status
    run_command_safe("docker --version", "Checking Docker version")
    run_command_safe("docker-compose --version", "Checking Docker Compose version")

    # Check running containers
    run_command_safe("docker ps", "Checking running containers")

    # Check Docker Compose status
    run_command_safe("docker-compose ps", "Checking Docker Compose services")

    # Check logs for each service
    services = ["prometheus", "grafana", "fastapi-metrics"]
    for service in services:
        run_command_safe(f"docker-compose logs --tail=20 {service}", f"Checking {service} logs")

    # Check if ports are in use
    run_command_safe("netstat -ano | findstr :9090", "Checking if port 9090 is in use")
    run_command_safe("netstat -ano | findstr :3000", "Checking if port 3000 is in use")
    run_command_safe("netstat -ano | findstr :8000", "Checking if port 8000 is in use")

    print("\n" + "=" * 50)
    print("Diagnostic complete! Check the output above for issues.")

if __name__ == "__main__":
    main()
