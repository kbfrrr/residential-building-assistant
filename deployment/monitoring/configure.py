"""Discover Docker logs and configure the installed CloudWatch agent and metric timer."""

import json
import os
from pathlib import Path
import sys

from common import REGION, instance_id, run

CONTAINERS = {
    "residential-gateway-1": "gateway",
    "residential-api-1": "api",
    "residential-mongodb-1": "mongodb",
}


def agent_config(containers):
    logs = []
    for container in containers:
        name = container["Name"].lstrip("/")
        path = container.get("LogPath")
        if not path or container["HostConfig"]["LogConfig"]["Type"] != "json-file":
            raise ValueError("Expected Docker json-file logs for " + name)
        logs.append({
            "file_path": path,
            "log_group_name": "/sam10/residential/" + CONTAINERS[name],
            "log_stream_name": "{instance_id}-" + CONTAINERS[name],
            "retention_in_days": 14,
        })
    return {
        "agent": {"metrics_collection_interval": 60, "run_as_user": "root", "region": REGION},
        "metrics": {
            "namespace": "CWAgent",
            "append_dimensions": {"InstanceId": "${aws:InstanceId}"},
            "aggregation_dimensions": [["InstanceId"]],
            "metrics_collected": {
                "mem": {"measurement": ["mem_used_percent"], "metrics_collection_interval": 60},
                "disk": {
                    "measurement": ["used_percent"], "resources": ["/"],
                    "drop_device": True, "drop_original_metrics": ["disk_used_percent"],
                    "metrics_collection_interval": 60,
                },
            },
        },
        "logs": {"force_flush_interval": 5, "logs_collected": {"files": {"collect_list": logs}}},
    }


def main():
    if os.geteuid() != 0:
        raise ValueError("Run with sudo.")
    directory = Path(__file__).resolve().parent
    containers = json.loads(run(["docker", "inspect", *CONTAINERS]))
    identifier = instance_id()
    config_path = directory / "cloudwatch-agent.json"
    config_path.write_text(json.dumps(agent_config(containers), indent=2) + "\n")
    (directory / "settings.json").write_text(json.dumps({"instance_id": identifier}))
    controller = "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl"
    print(run([controller, "-a", "fetch-config", "-m", "ec2", "-c", "file:" + str(config_path), "-s"]))
    service = """[Unit]
Description=Publish residential application metrics
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 """ + str(directory / "metrics.py") + """
TimeoutStartSec=120
"""
    timer = """[Unit]
Description=Collect residential application metrics every minute

[Timer]
OnBootSec=60
OnUnitActiveSec=60
AccuracySec=1

[Install]
WantedBy=timers.target
"""
    Path("/etc/systemd/system/residential-metrics.service").write_text(service)
    Path("/etc/systemd/system/residential-metrics.timer").write_text(timer)
    run(["systemctl", "daemon-reload"])
    run(["systemctl", "enable", "--now", "residential-metrics.timer"])
    run(["systemctl", "start", "residential-metrics.service"])
    print("Monitoring configured. Verify CloudWatch agent status and published metrics next.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Monitoring configuration failed (" + type(error).__name__ + "). Check agent validation logs and the metric service journal.", file=sys.stderr)
        sys.exit(1)
