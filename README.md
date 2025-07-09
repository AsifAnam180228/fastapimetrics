# FastAPI Metrics Monitoring System

A comprehensive FastAPI application that implements both system-level and application-level metrics monitoring using Prometheus metrics format.

## Features

- **System Metrics**: CPU usage, memory consumption, process statistics
- **HTTP Metrics**: Request volume, performance, latency tracking
- **Real-time Monitoring**: Live metrics collection and exposition
- **Production Ready**: Proper error handling and configuration management
- **Prometheus Compatible**: Standard metrics format for easy integration

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MonitoringSystem
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode
python -m app.main

# Production mode with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Core Endpoints

- `GET /`: Root endpoint with basic information
- `GET /health`: Comprehensive health check with system information  
- `GET /health/ready`: Readiness check for orchestration
- `GET /health/live`: Liveness check for orchestration
- `GET /metrics`: Prometheus metrics exposition endpoint

### Data Endpoints

- `POST /data`: Create/store data items
- `GET /data`: Retrieve all stored data
- `GET /data/{key}`: Retrieve specific data by key
- `DELETE /data/{key}`: Delete data by key

## Metrics Reference

### System Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `process_cpu_seconds_total` | Counter | Total CPU time consumed by the process |
| `process_resident_memory_bytes` | Gauge | Physical memory currently used |
| `process_virtual_memory_bytes` | Gauge | Virtual memory allocated |
| `process_start_time_seconds` | Gauge | Process start time since Unix epoch |
| `process_uptime_seconds` | Gauge | Process uptime in seconds |
| `process_open_fds` | Gauge | Number of open file descriptors |
| `process_threads` | Gauge | Number of OS threads |

### HTTP Metrics

| Metric Name | Type | Description | Labels |
|-------------|------|-------------|--------|
| `http_requests_total` | Counter | Total HTTP requests | method, endpoint, status_code |
| `http_request_duration_seconds` | Histogram | Request duration in seconds | method, endpoint |
| `http_request_size_bytes` | Histogram | Request size in bytes | method, endpoint |
| `http_response_size_bytes` | Histogram | Response size in bytes | method, endpoint, status_code |
| `http_requests_active` | Gauge | Number of active requests | method, endpoint |

### Example Prometheus Queries

```promql
# Request rate per second
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU usage rate
rate(process_cpu_seconds_total[5m])

# Memory usage
process_resident_memory_bytes / 1024 / 1024  # MB
```

## Configuration

Environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `METRICS_COLLECTION_INTERVAL` | `5` | System metrics collection interval (seconds) |
| `ENABLE_SYSTEM_METRICS` | `true` | Enable system metrics collection |
| `APP_NAME` | `fastapi-metrics-app` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  fastapi-metrics:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - METRICS_COLLECTION_INTERVAL=5
      - ENABLE_SYSTEM_METRICS=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
```

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi-metrics'
    static_configs:
      - targets: ['fastapi-metrics:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

## Monitoring Setup

### Grafana Dashboard

Key metrics to monitor:

1. **Request Volume**: `rate(http_requests_total[5m])`
2. **Error Rate**: `rate(http_requests_total{status_code=~"5.."}[5m])`
3. **Response Time**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
4. **CPU Usage**: `rate(process_cpu_seconds_total[5m])`
5. **Memory Usage**: `process_resident_memory_bytes`

### Alerting Rules

Example Prometheus alerting rules:

```yaml
groups:
  - name: fastapi-metrics
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
```

## Development

### Project Structure

```
fastapi-metrics-app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── system_metrics.py  # CPU, memory metrics
│   │   └── http_metrics.py    # HTTP request metrics
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── metrics_middleware.py
│   └── routers/
│       ├── __init__.py
│       ├── api.py             # Business logic endpoints
│       └── health.py          # Health check endpoints
├── requirements.txt
└── README.md
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Load testing
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{"key": "test", "value": "data"}'
```

## Performance Considerations

- Metrics collection adds minimal overhead (~1-2ms per request)
- System metrics collection runs in background every 5 seconds
- Endpoint normalization prevents cardinality explosion
- Histogram buckets are optimized for typical web application latencies

## Security

- No authentication required for metrics endpoint (standard practice)
- Metrics endpoint only exposes operational data, not business data
- Consider network-level restrictions for metrics endpoint in production

## Troubleshooting

### Common Issues

1. **High Memory Usage**: Adjust `METRICS_COLLECTION_INTERVAL` or disable system metrics
2. **Missing Metrics**: Check middleware configuration and endpoint normalization
3. **Performance Impact**: Monitor metrics collection overhead and adjust as needed

### Debugging

```bash
# Check metrics endpoint
curl http://localhost:8000/metrics

# Check health endpoint
curl http://localhost:8000/health

# Monitor logs
tail -f /var/log/fastapi-metrics.log
```

## License

This project is licensed under the MIT License.
