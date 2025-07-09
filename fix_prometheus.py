#!/usr/bin/env python3
"""
Prometheus-specific diagnostic and fix script
"""
import subprocess
import time
import os
import requests

def run_command(cmd, description):
    """Run command and return result."""
    print(f"\n🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error:\n{result.stderr}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, "", str(e)

def test_prometheus_connection():
    """Test Prometheus connection with different methods."""
    print("\n🔍 Testing Prometheus connection...")

    # Test different endpoints
    endpoints = [
        "http://localhost:9090",
        "http://localhost:9090/-/healthy",
        "http://localhost:9090/-/ready",
        "http://localhost:9090/api/v1/status/config"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"✅ {endpoint}: Status {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:100]}...")
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection refused")
        except requests.exceptions.Timeout:
            print(f"⏳ {endpoint}: Timeout")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def main():
    print("🔍 Prometheus Diagnostic Tool")
    print("=" * 40)

    # Check container status
    success, stdout, stderr = run_command("docker-compose ps prometheus", "Checking Prometheus container status")

    # Check detailed container info
    run_command("docker inspect prometheus", "Getting detailed container info")

    # Check Prometheus logs (last 20 lines)
    run_command("docker-compose logs --tail=20 prometheus", "Checking recent Prometheus logs")

    # Check if Prometheus process is running inside container
    run_command("docker exec prometheus ps aux", "Checking processes inside Prometheus container")

    # Test network connectivity
    run_command("docker exec prometheus wget -qO- http://localhost:9090/-/healthy", "Testing internal Prometheus health")

    # Test external connectivity
    test_prometheus_connection()

    print("\n" + "=" * 40)
    print("🔧 Suggested fixes:")
    print("1. Restart Prometheus: docker-compose restart prometheus")
    print("2. Check config: docker exec prometheus promtool check config /etc/prometheus/prometheus.yml")
    print("3. Rebuild: docker-compose down && docker-compose up -d prometheus")

if __name__ == "__main__":
    os.chdir(r"C:\Users\USER\PycharmProjects\MonitoringSystem")
    main()
