"""Start the deployment with secrets retrieved into memory from Parameter Store."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def load_environment():
    result = subprocess.run(
        [
            "/usr/local/bin/aws", "ssm", "get-parameter",
            "--name", "/sam10/residential/app-secrets", "--with-decryption",
            "--region", "ap-southeast-1", "--query", "Parameter.Value",
            "--output", "text", "--no-cli-pager",
        ],
        capture_output=True, text=True, timeout=45,
    )
    if result.returncode:
        raise ValueError("Unable to retrieve app secrets. Check instance-role access.")
    values = json.loads(result.stdout)
    required = {
        "mongo_root_password": 64, "mongo_app_password": 64,
        "jwt_secret": 64, "jwt_refresh_secret": 64,
        "creds_key": 64, "creds_iv": 32,
    }
    if not isinstance(values, dict):
        raise ValueError("App secrets must be a JSON object.")
    for name, length in required.items():
        if not isinstance(values.get(name), str) or not re.fullmatch(
            "[0-9a-fA-F]{" + str(length) + "}", values[name]
        ):
            raise ValueError("App secrets contain an invalid field: " + name)
    environment = os.environ.copy()
    environment.update({name.upper(): values[name] for name in required})
    environment["MONGO_URI"] = (
        "mongodb://residentapp:" + values["mongo_app_password"]
        + "@mongodb:27017/LibreChat?authSource=LibreChat"
    )
    environment["RESIDENT_GATEWAY_KEY"] = hashlib.sha256(
        ("resident-gateway:" + values["creds_key"]).encode()
    ).hexdigest()
    return environment


def main():
    commands = {
        "start": ["up", "-d", "--build", "--wait", "--wait-timeout", "300"],
        "publish": ["--profile", "public", "up", "-d", "--wait", "--wait-timeout", "300"],
        "create-user": ["exec", "api", "npm", "run", "create-user"],
        "status": ["ps", "-a"],
        "logs": ["logs", "--tail", "60", "api", "gateway", "mongodb"],
        "stop": ["--profile", "public", "stop"],
    }
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        raise ValueError("Usage: sudo python3 start.py " + "|".join(commands))
    environment = load_environment()
    return subprocess.call(
        ["docker", "compose", "-p", "residential", "-f", "compose.yaml"]
        + commands[sys.argv[1]],
        cwd=Path(__file__).resolve().parent, env=environment,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        # Never print subprocess output, secret values, or exception payloads.
        print("Deployment startup failed. Check command usage, secret format, and AWS access.", file=sys.stderr)
        sys.exit(1)
