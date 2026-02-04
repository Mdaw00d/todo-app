"""
Metrics collection utilities for the Todo AI Chatbot.
Provides basic metrics for monitoring system performance.
"""

import time
from typing import Dict, Optional
from threading import Lock
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    start_time: float
    user_id: str
    endpoint: str
    method: str


class MetricsCollector:
    """Simple metrics collector for tracking system performance."""

    def __init__(self):
        self._requests: list = []
        self._lock = Lock()
        self._request_count = 0
        self._error_count = 0

    def start_request(self, user_id: str, endpoint: str, method: str) -> RequestMetrics:
        """
        Start tracking a request.

        Args:
            user_id: ID of the user making the request
            endpoint: API endpoint being called
            method: HTTP method (GET, POST, etc.)

        Returns:
            RequestMetrics object to track this request
        """
        metrics = RequestMetrics(
            start_time=time.time(),
            user_id=user_id,
            endpoint=endpoint,
            method=method
        )
        return metrics

    def end_request(self, metrics: RequestMetrics, status_code: int) -> float:
        """
        End tracking a request and calculate duration.

        Args:
            metrics: RequestMetrics object from start_request
            status_code: HTTP status code of the response

        Returns:
            Duration in seconds
        """
        duration = time.time() - metrics.start_time

        with self._lock:
            self._request_count += 1
            if 400 <= status_code < 600:
                self._error_count += 1

        # In a real implementation, you would send this to a metrics system
        # For now, we'll just store it for reporting
        request_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": metrics.user_id,
            "endpoint": metrics.endpoint,
            "method": metrics.method,
            "duration": duration,
            "status_code": status_code
        }

        with self._lock:
            self._requests.append(request_info)

            # Keep only last 1000 requests to prevent memory issues
            if len(self._requests) > 1000:
                self._requests = self._requests[-1000:]

        return duration

    def get_summary(self) -> Dict[str, any]:
        """
        Get a summary of collected metrics.

        Returns:
            Dictionary with summary metrics
        """
        with self._lock:
            if not self._requests:
                return {
                    "total_requests": self._request_count,
                    "total_errors": self._error_count,
                    "error_rate": 0.0,
                    "avg_response_time": 0.0,
                    "recent_requests": []
                }

            total_duration = sum(req["duration"] for req in self._requests)
            avg_response_time = total_duration / len(self._requests)
            error_rate = (self._error_count / self._request_count) if self._request_count > 0 else 0.0

            return {
                "total_requests": self._request_count,
                "total_errors": self._error_count,
                "error_rate": error_rate,
                "avg_response_time": avg_response_time,
                "recent_requests": self._requests[-10:]  # Last 10 requests
            }

    def reset(self) -> None:
        """Reset all metrics counters."""
        with self._lock:
            self._requests.clear()
            self._request_count = 0
            self._error_count = 0


# Global metrics collector instance
metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return metrics_collector