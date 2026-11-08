"""Shared host-side helpers. AWS CLI uses the EC2 instance role."""

import subprocess
from urllib.request import Request, urlopen

REGION = "ap-southeast-1"
AWS = "/usr/local/bin/aws"


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError("Command failed: " + command[0])
    return result.stdout.strip()


def instance_id():
    request = Request(
        "http://169.254.169.254/latest/api/token", method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
    )
    with urlopen(request, timeout=5) as response:
        token = response.read().decode()
    request = Request(
        "http://169.254.169.254/latest/meta-data/instance-id",
        headers={"X-aws-ec2-metadata-token": token},
    )
    with urlopen(request, timeout=5) as response:
        return response.read().decode().strip()
