# Images Directory for FastAPI Metrics Monitoring System

This directory contains screenshots and visual documentation for the monitoring system.

## Contents

- `http_requests_total.png` - HTTP requests metrics showing request volume by endpoint
- `process_cpu_seconds_total.png` - CPU usage metrics over time
- `process_resident_memory_bytes.png` - Memory consumption tracking
- `http_request_duration_histogram.png` - Response time histogram metrics

## Usage

These images are referenced in the main README.md to show working examples of the metrics system.
![http_requests_total.png](../../../../Pictures/Prometheus/http_requests_total.png)
![process_cpu_seconds_total.png](../../../../Pictures/Prometheus/process_cpu_seconds_total.png)
![process_resident_memory_bytes.png](../../../../Pictures/Prometheus/process_resident_memory_bytes.png)
![histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)).png](../../../../Pictures/Prometheus/histogram_quantile%280.95%2C%20sum%28rate%28http_request_duration_seconds_bucket%5B5m%5D%29%29%20by%20%28le%29%29.png)