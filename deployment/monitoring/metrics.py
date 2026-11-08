"""Publish interval request metrics and database connections without reading secrets."""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import tempfile

from common import AWS, REGION, run


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def request_events(output, start, end):
    events = []
    for line in output.splitlines():
        try:
            logged_at, message = line.split(" ", 1)
            if not start < timestamp(logged_at) <= end:
                continue
            event = json.loads(message)
            if "request_id" not in event:
                continue
            if not isinstance(event.get("success"), bool):
                raise ValueError("Invalid request outcome")
            duration = event.get("duration_ms")
            if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0:
                raise ValueError("Invalid duration")
            events.append(event)
        except (ValueError, TypeError):
            # Non-request diagnostic messages are not request samples.
            continue
    return events


def metric_data(events, identifier, end):
    dimensions = [{"Name": "InstanceId", "Value": identifier}]

    def metric(name, value, unit):
        return {"MetricName": name, "Dimensions": dimensions, "Timestamp": end.isoformat(), "Value": value, "Unit": unit}

    result = [
        metric("RequestCount", len(events), "Count"),
        metric("ErrorCount", sum(not event["success"] for event in events), "Count"),
        metric("ExporterHeartbeat", 1, "Count"),
    ]
    if events:
        durations = [event["duration_ms"] for event in events]
        result.append({
            "MetricName": "ResponseTime", "Dimensions": dimensions,
            "Timestamp": end.isoformat(), "Unit": "Milliseconds",
            "StatisticValues": {"SampleCount": len(durations), "Sum": sum(durations), "Minimum": min(durations), "Maximum": max(durations)},
        })
    return result


def main():
    import fcntl

    state_directory = Path("/var/lib/residential-monitoring")
    state_directory.mkdir(mode=0o750, parents=True, exist_ok=True)
    with (state_directory / "lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Collector already running.")
            return
        settings = json.loads(Path(__file__).with_name("settings.json").read_text())
        end = datetime.now(timezone.utc) - timedelta(seconds=3)
        checkpoint = state_directory / "checkpoint.json"
        start = timestamp(json.loads(checkpoint.read_text())["until"]) if checkpoint.exists() else end - timedelta(minutes=5)
        if start >= end:
            print("No new collection window.")
            return
        output = run([
            "docker", "logs", "--timestamps", "--since", start.isoformat(),
            "--until", end.isoformat(), "residential-gateway-1",
        ])
        events = request_events(output, start, end)
        metrics = metric_data(events, settings["instance_id"], end)
        dimensions = [{"Name": "InstanceId", "Value": settings["instance_id"]}]
        try:
            probe = run([
                "docker", "exec", "residential-mongodb-1", "mongosh", "--quiet", "--eval",
                'db.getSiblingDB("admin").auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD); print(db.serverStatus().connections.current);',
            ])
            connections = int(probe.splitlines()[-1])
            metrics.append({"MetricName": "DatabaseConnections", "Dimensions": dimensions, "Timestamp": end.isoformat(), "Value": connections, "Unit": "Count"})
            probe_failed = 0
        except (RuntimeError, ValueError, IndexError):
            probe_failed = 1
        metrics.append({"MetricName": "DatabaseProbeFailed", "Dimensions": dimensions, "Timestamp": end.isoformat(), "Value": probe_failed, "Unit": "Count"})
        run([AWS, "cloudwatch", "put-metric-data", "--namespace", "SAM10/Residential", "--metric-data", json.dumps(metrics), "--region", REGION, "--no-cli-pager"])
        with tempfile.NamedTemporaryFile(mode="w", dir=state_directory, delete=False) as temporary:
            json.dump({"until": end.isoformat()}, temporary)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = temporary.name
        os.replace(temporary_path, checkpoint)
        print(json.dumps({"event": "metrics_published", "from": start.isoformat(), "until": end.isoformat(), "requests": len(events), "errors": sum(not item["success"] for item in events), "database_probe_failed": probe_failed}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Metric export failed (" + type(error).__name__ + "). Check the instance role, Docker and AWS CLI connectivity.", file=sys.stderr)
        sys.exit(1)
