# Monitoring Setup

The student installed CloudWatch agent 1.300074.1b2005-1 on Ubuntu and demonstrated receipt of a direct SNS test email. The SNS topic is residential-assistant-alerts in Singapore. An actual CloudWatch alarm email has not yet been tested. Email screenshots and subscription links remain local and must be redacted before final evidence selection.

This bundle uses the existing EC2 instance role and installed AWS CLI and CloudWatch agent. It contains no credentials, subscription endpoint, or evidence images. The IAM runtime-access policy must include the exact S3 object deployment/monitoring-bundle.zip before transfer. CloudWatchAgentServerPolicy provides metric publication, log creation, and retention permissions. Agent configuration is loaded from a local file; no extra Parameter Store parameter is needed.

## Transfer and configure

Upload monitoring-bundle.zip privately under deployment/ in sam10-residential-content-1229. Run these commands separately in Session Manager:

```bash
/usr/local/bin/aws s3 cp s3://sam10-residential-content-1229/deployment/monitoring-bundle.zip /tmp/monitoring-bundle.zip --region ap-southeast-1
```

```bash
sudo install -d -m 0750 -o "$(id -u)" -g "$(id -g)" /opt/residential-assistant/monitoring
```

```bash
unzip /tmp/monitoring-bundle.zip -d /opt/residential-assistant/monitoring
```

```bash
cd /opt/residential-assistant/monitoring
```

```bash
sudo python3 configure.py
```

configure.py discovers the current Docker JSON log paths, retrieves the instance ID through IMDSv2, configures the agent, and installs a systemd service/timer for custom app metrics. It does not modify the application containers. Re-run configuration after recreating app containers so the agent follows their new log paths. Read source files before execution.

## What is collected

- Native EC2 CPUUtilization and StatusCheckFailed remain available through AWS/EC2 basic monitoring.
- CWAgent publishes mem_used_percent and disk_used_percent every 60 seconds. Disk collection is limited to / and is rolled up by InstanceId.
- Log groups /sam10/residential/gateway, /sam10/residential/api and /sam10/residential/mongodb have 14-day retention. Docker JSON wrappers are preserved; the gateway's inner log text contains request fields. In Logs Insights, parse the log field when querying request content.
- SAM10/Residential publishes RequestCount, ErrorCount, ExporterHeartbeat and DatabaseProbeFailed every collection interval. DatabaseConnections is included when the database probe succeeds. The diagnostic probe connection itself contributes to that connection count.
- ResponseTime uses the observed durations in milliseconds with SampleCount, Sum, Minimum and Maximum. It is absent when no requests occur; no zero-latency sample is invented.
- All custom metric series use the InstanceId dimension. Initial collection reads the preceding five minutes; later successful collections use persisted, non-overlapping time windows, with a three-second log-flush delay.

The collector advances its checkpoint only after PutMetricData succeeds. If a network timeout occurs after AWS accepted metrics but before acknowledgment, retry may duplicate samples; CloudWatch PutMetricData does not supply an idempotency key. Container recreation or log rotation can also remove records before collection. This is small-project telemetry, not an exact billing ledger. Preserve raw logs for evaluation and comparative results. The exporter observes requests and does not call Gemini or consume model quota itself.

## Verify after setup

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

```bash
sudo systemctl status residential-metrics.timer --no-pager
```

```bash
sudo journalctl -u residential-metrics.service -n 15 --no-pager
```

Ask the live assistant two invented questions, wait a few minutes, and verify log streams and metric series in the Singapore CloudWatch console. One metric may take longer than others to appear. Successful installation alone does not prove ingestion.

If setup fails, check /opt/aws/amazon-cloudwatch-agent/logs/configuration-validation.log, the agent's log, and the systemd service journal. Do not dump container environments or secret parameters. Source tests run with python3 test_monitoring.py and require only the standard library. Local offline tests do not validate the installed agent's own schema or actual AWS connectivity; those remain runtime checks.

## Controlled alarm delivery test

The student demonstrated all six alarms in the console, each OK with actions enabled. Notification delivery remains a separate check. In the EC2 Session Manager terminal, run this one-line command once:

```bash
sudo docker exec residential-api-1 node -e "fetch('http://gateway:8000/v1/chat/completions',{method:'POST'}).then(r=>console.log('Controlled alarm test HTTP '+r.status)).catch(()=>{console.error('Test could not reach gateway');process.exitCode=1})"
```

Expected HTTP 401: an intentional request without authentication, rejected before Gemini is called. The gateway logs the rejection; the collector includes it in ErrorCount. Wait for the collector and CloudWatch evaluation (typically several minutes, allow about ten), then check Residential-ApplicationErrors and the SNS inbox. Record the real ALARM transition/email time and subsequent OK recovery separately. This is an intentional monitoring test, not an unexpected outage or proof of the separate incident requirement. Do not use these synthetic requests in the quality evaluation or normal latency baseline.

Delivery observed: the student's email screenshot confirmed Residential-ApplicationErrors, OK → ALARM, at 2026-11-08 16:19:47 UTC (2026-11-09 00:19:47 Manila), following the intentional HTTP 401 test. Recovery remains unverified. Screenshot selection and redaction are deferred to deliverable compilation; no image was copied or published.

## Next steps

The student demonstrated both CWAgent series (memory and root disk) and six SAM10/Residential series (request count, errors, response time, database connections, database-probe failures and exporter heartbeat) in CloudWatch for the instance. The agent status reported running/configured and the systemd timer active. A journal entry confirmed metric publication. Actual log ingestion still needs separate verification.

dashboard.json is a console-importable dashboard body for instance i-09ac9cdde1117185b in Singapore. Create a dashboard named Residential-Assistant-Operations, open Actions > View/edit source, replace its JSON with this file, update, and save. It has eight metric widgets and a text explanation. Review the instance ID if the host is replaced. The student's screenshots verified the populated dashboard. This JSON creates no alarms.

### Create six alarms

Use AWS CloudShell while signed into ResidentialProjectSetupRole in Singapore. The EC2 runtime role intentionally lacks alarm-management permissions. In CloudShell choose Actions > Upload file and upload create-alarms.py from this directory. Run `python3 create-alarms.py` to preview, then `python3 create-alarms.py --apply` to create/update the six Residential-prefixed alarms. The script checks the account and that the SNS topic has a confirmed subscriber. It sends ALARM and OK transitions to residential-assistant-alerts. If an AWS call fails, earlier successful changes remain; fix the reported issue and rerun to complete the same six names.

Initial thresholds: CPU average above 85% for two 5-minute periods; EC2 status failure at least 1 in a minute; disk maximum above 85% for three minutes; memory average above 90% for five minutes; at least one application error per 5-minute period; response-time average above 10,000 ms for two 5-minute periods. These are starting assumptions for a small demonstration, not proven production thresholds. Review with representative traffic. Missing data is treated as not breaching, allowing idle response-time intervals; these six alarms do not detect a stopped metric exporter. Monitor its heartbeat separately. Creating alarms does not verify notification delivery. A real metric-triggered transition and received email still need demonstration.

Create a populated dashboard with requests, errors, response time, CPU, disk, memory and database connections. Add at least six alarms, all targeting the confirmed SNS topic, and verify one actual alarm notification arrives. Suggested initial thresholds are CPU above 85% for 10 minutes, failed EC2 status check, disk above 85%, memory above 90%, application errors, and sustained response time above an explained threshold. Final alarm definitions and dashboard are not included in this first monitoring bundle.

Then add scheduled backups and synthetic end-to-end checks, verify two unattended executions of each, and perform an isolated restore. Metric-export timer activity does not replace those planned demonstrations.
