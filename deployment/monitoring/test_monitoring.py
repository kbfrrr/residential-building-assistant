"""Offline tests for metric boundaries and discovered log configuration."""

from datetime import datetime, timezone
import json
import unittest

from configure import agent_config
from metrics import metric_data, request_events


class MonitoringTests(unittest.TestCase):
    def test_interval_boundary_is_not_counted_twice(self):
        start = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)
        end = datetime(2026, 11, 8, 12, 1, tzinfo=timezone.utc)
        event = json.dumps({"request_id": "test", "success": True, "duration_ms": 100})
        output = start.isoformat() + " " + event + "\n" + end.isoformat() + " " + event
        self.assertEqual(len(request_events(output, start, end)), 1)

    def test_empty_interval_does_not_invent_latency(self):
        metrics = metric_data([], "i-test", datetime.now(timezone.utc))
        self.assertEqual(metrics[0]["Value"], 0)
        self.assertNotIn("ResponseTime", [metric["MetricName"] for metric in metrics])

    def test_latency_statistics_and_failure_count(self):
        events = [{"success": True, "duration_ms": 100}, {"success": False, "duration_ms": 300}]
        metrics = metric_data(events, "i-test", datetime.now(timezone.utc))
        self.assertEqual(metrics[1]["Value"], 1)
        self.assertEqual(metrics[-1]["StatisticValues"], {"SampleCount": 2, "Sum": 400, "Minimum": 100, "Maximum": 300})

    def test_discovered_paths_and_retention(self):
        containers = [{"Name": "/residential-gateway-1", "LogPath": "/var/lib/docker/containers/test/test-json.log", "HostConfig": {"LogConfig": {"Type": "json-file"}}}]
        entry = agent_config(containers)["logs"]["logs_collected"]["files"]["collect_list"][0]
        self.assertEqual(entry["retention_in_days"], 14)
        self.assertEqual(entry["log_group_name"], "/sam10/residential/gateway")


if __name__ == "__main__":
    unittest.main()
