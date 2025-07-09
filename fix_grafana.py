#!/usr/bin/env python3
"""
Grafana Dashboard Troubleshooting Script
"""
import requests
import json
import time

def check_prometheus():
    """Check if Prometheus is working and has data."""
    print("🔍 Checking Prometheus...")

    try:
        # Check Prometheus health
        response = requests.get("http://localhost:9090/-/healthy", timeout=5)
        print(f"✅ Prometheus health: {response.status_code}")

        # Check if FastAPI metrics are being scraped
        response = requests.get("http://localhost:9090/api/v1/query?query=up", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Prometheus query API working")
            print(f"   Targets up: {len(data['data']['result'])}")
            for result in data['data']['result']:
                job = result['metric'].get('job', 'unknown')
                instance = result['metric'].get('instance', 'unknown')
                value = result['value'][1]
                print(f"   - {job} ({instance}): {value}")

        # Check for FastAPI specific metrics
        metrics_to_check = [
            "http_requests_total",
            "fastapi_cpu_usage_percent",
            "process_resident_memory_bytes"
        ]

        for metric in metrics_to_check:
            response = requests.get(f"http://localhost:9090/api/v1/query?query={metric}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                result_count = len(data['data']['result'])
                if result_count > 0:
                    print(f"✅ {metric}: {result_count} series found")
                else:
                    print(f"❌ {metric}: No data found")
            else:
                print(f"❌ {metric}: Query failed")

    except Exception as e:
        print(f"❌ Prometheus check failed: {e}")

def test_grafana_datasource():
    """Test Grafana's connection to Prometheus."""
    print("\n🔍 Testing Grafana datasource...")

    try:
        # Check Grafana health
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        print(f"✅ Grafana health: {response.status_code}")

        # Check datasources (requires auth)
        auth = ('admin', 'admin')
        response = requests.get("http://localhost:3000/api/datasources", auth=auth, timeout=5)
        if response.status_code == 200:
            datasources = response.json()
            print(f"✅ Found {len(datasources)} datasource(s)")
            for ds in datasources:
                print(f"   - {ds['name']}: {ds['type']} ({ds['url']})")
        else:
            print(f"❌ Could not fetch datasources: {response.status_code}")

    except Exception as e:
        print(f"❌ Grafana check failed: {e}")

def generate_test_traffic():
    """Generate some test traffic to create metrics."""
    print("\n🚦 Generating test traffic...")

    endpoints = [
        "http://localhost:8000/",
        "http://localhost:8000/health",
        "http://localhost:8000/data"
    ]

    for i in range(5):
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=2)
                print(f"✅ {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint}: {e}")

        if i < 4:  # Don't sleep after the last iteration
            time.sleep(1)

    # Generate some POST requests
    try:
        for i in range(3):
            data = {"key": f"test{i}", "value": f"value{i}"}
            response = requests.post("http://localhost:8000/data", json=data, timeout=2)
            print(f"✅ POST /data: {response.status_code}")
    except Exception as e:
        print(f"❌ POST requests failed: {e}")

def main():
    print("📊 Grafana Dashboard Troubleshooting")
    print("=" * 50)

    check_prometheus()
    test_grafana_datasource()
    generate_test_traffic()

    print("\n" + "=" * 50)
    print("🔧 Next steps:")
    print("1. Wait 1-2 minutes for metrics to populate")
    print("2. Go to Grafana: http://localhost:3000")
    print("3. Login: admin/admin")
    print("4. Check: Configuration → Data Sources → Prometheus")
    print("5. Test the connection")
    print("6. Go to Dashboards → FastAPI Metrics")

if __name__ == "__main__":
    main()
