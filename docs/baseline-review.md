# Deployment Baseline and Initial Well-Architected Review

Checkpoint date: November 8, 2026, Asia/Manila. This is the initial review after the first working cloud response and before the monitoring/recovery phases. Revisit the same pillars after the assessed incident. Evidence images remain local until deliverable compilation.

## Observed baseline

| Item | Current observation |
|---|---|
| Live endpoint | https://residential-assistant.54.179.56.26.sslip.io |
| Platform | Ubuntu 24.04.5 LTS on one m7i-flex.large EC2 server in Singapore |
| App components | Caddy, LibreChat, resident gateway, and one MongoDB database |
| Cloud app health | Student demonstrated healthy MongoDB, gateway, and LibreChat containers before public activation |
| User flow | Student demonstrated a logged-in browser chat at the public hostname |
| Public registration | Anonymous POST to /api/auth/register returned HTTP 403 with Registration is not allowed |
| Smoke question | Can I use the swimming pool on Monday? |
| Observed answer | Correctly stated Monday closure for cleaning and Tuesday-Sunday hours of 7:00 AM-8:00 PM, citing Section 2 |
| Handbook and secret access | EC2 role downloaded the handbook and read the encrypted Gemini parameter; app-secrets structure validated |
| Request logging | Production JSON log observed for the pool question: status 200, success true, duration_ms 1977, model gemini-3.6-flash, version sam10-deployment-v1, request ID, UTC timestamp, and handbook version. This single observation is not a representative latency baseline. |
| Monitoring | No populated CloudWatch dashboard, application metrics ingestion, or tested alarm email yet |
| Backups | No scheduled cloud database backup or tested cloud restore yet |
| Automations | No two-run unattended evidence yet |
| Quality score | Not measured; a successful smoke answer is not a full evaluation |
| Performance | Not measured; the UI's single-response time is not a comparable baseline |
| Cost | Launch form showed $0.1197/hour compute; actual before/after billing comparison remains unmeasured |

## Six-pillar review

| Pillar | What it asks for | Current setup and verdict | Next improvement |
|---|---|---|---|
| Operational Excellence | Operate visibly and improve through documented procedures | **Gap.** The app is working, code and setup records exist, and gateway logging is implemented. No operating dashboard or scheduled-check evidence yet. | Capture logs, publish metrics, test alerts, and automate routine checks. |
| Security | Protect access, credentials, and data | **Adequate provisionally.** HTTPS, private container ports, authenticated database user, closed public registration in config, instance role, scoped object access, and SecureString retrieval are implemented. Final MFA, CloudTrail, budget, tags, running security groups, and encryption evidence need confirmation. Setup-role AdministratorAccess is still broader than final operating needs. | Audit running controls, test unauthorized registration and out-of-scope runtime access, confirm CloudTrail, and reduce setup permissions. |
| Reliability | Detect faults and restore service and data | **Gap.** Restart policies, startup health checks and certificate persistence exist. One host remains a single point of failure. Backups and recovery have not been demonstrated. | Add monitoring, schedule database dumps, perform an isolated restore, and measure RPO/RTO. |
| Performance Efficiency | Match resources to measured workload | **Gap.** An 8 GiB host was selected for the small stack and only one live response is observed. No representative load or comparative latency measurements exist. | Measure request durations under a repeatable workload before changing resources. |
| Cost Optimization | Make spending visible and avoid unused resources | **Gap.** A small single-host design and free hostname are in use. Budget setup was guided but final creation evidence and actual costs need confirmation. | Verify the budget, resource tags and billing data, then plan stop/teardown timing. |
| Sustainability | Avoid unnecessary resource use | **Adequate provisionally.** Model inference is external, deployment uses one host and one database, and unneeded local services can be stopped. Compute has not yet been right-sized using measurements. | Measure utilization, avoid duplicate idle services, and stop or remove resources when assessment permits. |

Highest-priority gap: failure detection. A live system can currently fail without a verified email alert. Add CloudWatch request/error/latency and host metrics with a tested alert route, then back it with scheduled backups and a performed restore. CloudWatch role permissions alone are not proof that monitoring is operating.

## Measurement plan

The before/after measurement windows are not yet established. Define equal windows, run the same fixed questions at the same cadence, record exact start/end timestamps, and retain the raw log records. Compare request count, success/error rate, response-time summary, and attributable cost using the same definitions. Report the small sample honestly. Do not invent availability or quality scores from this single smoke test.

Use docs/evaluation-test-plan.md for the separate 15-question quality evaluation and preserve actual responses. The AWS gateway already supplies the S3 handbook, so the cloud user does not need to attach it manually.
