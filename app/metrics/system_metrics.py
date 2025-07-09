import time
import psutil
import os
import sys
from prometheus_client import Gauge, Counter, Info, Histogram
import threading

class SystemMetricsCollector:
    """Collects system-level metrics for monitoring using standard Prometheus metric names."""

    def __init__(self):
        # Standard Prometheus process metrics (to match dashboard expectations)
        self.process_cpu_seconds_total = Counter(
            'process_cpu_seconds_custom',  # Use different name to avoid conflict
            'Total CPU time consumed by the process'
        )

        self.process_resident_memory_bytes = Gauge(
            'process_resident_memory_bytes_custom',
            'Physical memory currently used by the process'
        )

        self.process_virtual_memory_bytes = Gauge(
            'process_virtual_memory_bytes_custom',
            'Virtual memory allocated by the process'
        )

        # CPU usage percentage (more intuitive)
        self.cpu_usage_percent = Gauge(
            'fastapi_cpu_usage_percent',
            'CPU usage percentage of the process'
        )

        # Process information
        self.process_start_time_seconds = Gauge(
            'process_start_time_seconds_custom',
            'Start time of the process since Unix epoch'
        )

        self.process_uptime_seconds = Gauge(
            'fastapi_uptime_seconds',
            'Process uptime in seconds'
        )

        # Additional system metrics
        self.process_open_fds = Gauge(
            'process_open_fds_custom',
            'Number of open file descriptors'
        )

        self.process_threads = Gauge(
            'fastapi_thread_count',
            'Number of OS threads in the process'
        )

        # GC and additional stats
        self.gc_collections_total = Counter(
            'python_gc_collections_total',
            'Number of garbage collections',
            ['generation']
        )

        # Application info
        self.fastapi_app_info = Info(
            'fastapi_app_info',
            'FastAPI application information'
        )

        self.process_info = Info(
            'fastapi_process_info',
            'Process information'
        )

        # Initialize process object and start time
        self.process = psutil.Process()
        self.process_start_time_value = self.process.create_time()
        self._last_cpu_times = self.process.cpu_times()
        self._last_collection_time = time.time()

        # Set static metrics
        self.process_start_time_seconds.set(self.process_start_time_value)

        try:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except:
            python_version = "unknown"

        self.fastapi_app_info.info({
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'name': os.getenv('APP_NAME', 'fastapi-metrics-app'),
            'python_version': python_version
        })

        self.process_info.info({
            'pid': str(self.process.pid),
            'started': str(self.process_start_time_value),
            'cwd': os.getcwd(),
            'exe': sys.executable
        })

    def collect_metrics(self):
        """Collect current system metrics."""
        try:
            current_time = time.time()

            # CPU metrics
            cpu_times = self.process.cpu_times()
            total_cpu_time = cpu_times.user + cpu_times.system

            # Update CPU seconds total (increment since last measurement)
            time_diff = current_time - self._last_collection_time
            if time_diff > 0:
                cpu_time_diff = total_cpu_time - (self._last_cpu_times.user + self._last_cpu_times.system)
                if cpu_time_diff >= 0:
                    # Add the difference to our counter
                    self.process_cpu_seconds_total._value._value += cpu_time_diff

            self._last_cpu_times = cpu_times
            self._last_collection_time = current_time

            # CPU usage percentage
            cpu_percent = self.process.cpu_percent()
            self.cpu_usage_percent.set(cpu_percent)

            # Memory metrics
            memory_info = self.process.memory_info()
            self.process_resident_memory_bytes.set(memory_info.rss)
            self.process_virtual_memory_bytes.set(memory_info.vms)

            # Process uptime
            uptime = current_time - self.process_start_time_value
            self.process_uptime_seconds.set(uptime)

            # Thread count
            self.process_threads.set(self.process.num_threads())

            # File descriptors (Unix/Linux) or handles (Windows)
            try:
                if hasattr(self.process, 'num_fds'):
                    self.process_open_fds.set(self.process.num_fds())
                elif hasattr(self.process, 'num_handles'):  # Windows
                    self.process_open_fds.set(self.process.num_handles())
            except (AttributeError, psutil.AccessDenied):
                pass

            # Garbage collection stats
            try:
                import gc
                for i in range(3):  # Python has 3 GC generations
                    collections = gc.get_stats()[i]['collections']
                    self.gc_collections_total.labels(generation=str(i))._value._value = collections
            except:
                pass

        except psutil.NoSuchProcess:
            # Process no longer exists
            pass
        except Exception as e:
            # Log error but don't crash the application
            print(f"Error collecting system metrics: {e}")

# Global instance
system_metrics = SystemMetricsCollector()
