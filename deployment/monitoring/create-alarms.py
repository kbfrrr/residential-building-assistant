"""Preview or apply the six project alarms from AWS CloudShell (setup role)."""
import argparse
import json
import shutil
import subprocess

REGION = "ap-southeast-1"
ACCOUNT = "125035824720"
INSTANCE = "i-09ac9cdde1117185b"
TOPIC = f"arn:aws:sns:{REGION}:{ACCOUNT}:residential-assistant-alerts"


def definitions():
    rows = [
        ("HighCPU", "AWS/EC2", "CPUUtilization", "Average", 300, 2, 85, "Percent", "GreaterThanThreshold"),
        ("InstanceStatusFailed", "AWS/EC2", "StatusCheckFailed", "Maximum", 60, 1, 1, "Count", "GreaterThanOrEqualToThreshold"),
        ("HighDisk", "CWAgent", "disk_used_percent", "Maximum", 60, 3, 85, "Percent", "GreaterThanThreshold"),
        ("HighMemory", "CWAgent", "mem_used_percent", "Average", 60, 5, 90, "Percent", "GreaterThanThreshold"),
        ("ApplicationErrors", "SAM10/Residential", "ErrorCount", "Sum", 300, 1, 1, "Count", "GreaterThanOrEqualToThreshold"),
        ("SlowResponses", "SAM10/Residential", "ResponseTime", "Average", 300, 2, 10000, "Milliseconds", "GreaterThanThreshold"),
    ]
    return [dict(
        AlarmName=f"Residential-{name}",
        AlarmDescription=f"Residential project: {metric}; initial threshold, review after representative workload.",
        ActionsEnabled=True, AlarmActions=[TOPIC], OKActions=[TOPIC],
        Namespace=namespace, MetricName=metric, Statistic=statistic,
        Dimensions=[{"Name": "InstanceId", "Value": INSTANCE}],
        Period=period, EvaluationPeriods=periods, DatapointsToAlarm=periods,
        Threshold=threshold, ComparisonOperator=comparison,
        TreatMissingData="notBreaching", Unit=unit,
    ) for name, namespace, metric, statistic, period, periods, threshold, unit, comparison in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create/update these six named alarms in AWS")
    args = parser.parse_args()
    alarms = definitions()
    if not args.apply:
        print(json.dumps(alarms, indent=2))
        print("Preview only. No AWS calls. Use --apply in CloudShell under the setup role.")
        return
    aws = shutil.which("aws")
    if not aws:
        raise SystemExit("AWS CLI not found. Run this file in AWS CloudShell.")

    def call(*arguments):
        result = subprocess.run([aws, *arguments, "--region", REGION, "--no-cli-pager"],
                                capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise SystemExit("AWS operation failed: " + result.stderr.strip())
        return result.stdout.strip()

    account = call("sts", "get-caller-identity", "--query", "Account", "--output", "text")
    if account != ACCOUNT:
        raise SystemExit("Wrong AWS account. No alarms changed.")
    topic = json.loads(call("sns", "get-topic-attributes", "--topic-arn", TOPIC))
    if int(topic["Attributes"].get("SubscriptionsConfirmed", "0")) < 1:
        raise SystemExit("SNS topic has no confirmed subscription. No alarms changed.")
    for alarm in alarms:
        call("cloudwatch", "put-metric-alarm", "--cli-input-json", json.dumps(alarm))
        print("Created/updated: " + alarm["AlarmName"])
    print("Six alarms configured. Verify their actions and test actual email delivery next.")


if __name__ == "__main__":
    main()
