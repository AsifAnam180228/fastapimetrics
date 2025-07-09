import time
import psutil
import os
import sys
from prometheus_client import Gauge, Counter, Info

class SystemMetricsCollector:
    """Collects system-level metrics for monitoring."""

    def __init__(self):
        # CPU metrics
        self.cpu_seconds_total = Counter(
            'process_cpu_seconds_total',
            'Total CPU time consumed by the process'
        )

        # Memory metrics
        self.resident_memory_bytes = Gauge(
            'process_resident_memory_bytes',
            'Physical memory currently used by the process'
        )

        self.virtual_memory_bytes = Gauge(
            'process_virtual_memory_bytes',
            'Virtual memory allocated by the process'
        )

        # Process information
        self.process_start_time = Gauge(
            'process_start_time_seconds',
            'Start time of the process since Unix epoch'
        )

        self.process_uptime = Gauge(
            'process_uptime_seconds',
            'Process uptime in seconds'
        )

        # File descriptor metrics
        self.open_fds = Gauge(
            'process_open_fds',
            'Number of open file descriptors'
        )

        # Thread metrics
        self.threads = Gauge(
            'process_threads',
            'Number of OS threads in the process'
        )

        # Application info
        self.app_info = Info(
            'fastapi_app_info',
            'FastAPI application information'
        )

        # Initialize process object
        self.process = psutil.Process()
        self.process_start_time_value = self.process.create_time()

        # Set static metrics
        self.process_start_time.set(self.process_start_time_value)

        # Fix the psutil version info access
        try:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except:
            python_version = "unknown"

        self.app_info.info({
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'name': os.getenv('APP_NAME', 'fastapi-metrics-app'),
            'python_version': python_version
        })

    def collect_metrics(self):
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_times = self.process.cpu_times()
            self.cpu_seconds_total._value._value = cpu_times.user + cpu_times.system

            # Memory metrics
            memory_info = self.process.memory_info()
            self.resident_memory_bytes.set(memory_info.rss)
            self.virtual_memory_bytes.set(memory_info.vms)

            # Process uptime
            current_time = time.time()
            uptime = current_time - self.process_start_time_value
            self.process_uptime.set(uptime)

            # File descriptors (Unix/Linux only)
            try:
                if hasattr(self.process, 'num_fds'):
                    self.open_fds.set(self.process.num_fds())
            except (AttributeError, psutil.AccessDenied):
                pass

            # Thread count
            self.threads.set(self.process.num_threads())

        except psutil.NoSuchProcess:
            # Process no longer exists
            pass
        except Exception as e:
            # Log error but don't crash the application
            print(f"Error collecting system metrics: {e}")

# Global instance
system_metrics = SystemMetricsCollector()
