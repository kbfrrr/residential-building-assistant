# Residential Building Assistant

A SAM10 Systems Administration and Maintenance school project adapting LibreChat into an informational assistant for a fictional residential building.

## Review the project

- [Project site source](site/index.html) is a single HTML file. Open it directly in your browser to view the system card, architecture, operations evidence, restore incident, and evaluation chart.
- [Live AWS chatbot](https://residential-assistant.54.179.56.26.sslip.io/) is the separate deployed application.
- [AWS architecture](docs/architecture.md) and [EC2 deployment instructions](deployment/app/README.md) explain how the system runs. The [monitoring](deployment/monitoring/README.md), [backup](deployment/backup/README.md), and [answer-check](deployment/quality/README.md) folders contain operational setup and automation.
- [Resident handbook](content/resident-handbook.md), [restore test and runbook](deployment/backup/restore-test.md), [baseline evaluation](docs/evaluation-test-plan.md), and [formal retest](docs/evaluation-retest.md) accompany the site.

## Project folders

- `content/` contains the fictional resident handbook.
- `LibreChat/` contains the upstream application source and its original license and documentation.
- `docs/` contains the project tracker and captured evidence.
- `deployment/` contains deployment configuration, monitoring, backup automation, and operational runbooks.
- `site/` contains the project website.

To start the local application, open a terminal at the repository root with Docker Desktop running and the required local configuration in place:

```powershell
cd LibreChat
docker compose -p librechat up -d
```

Open [http://localhost:3080](http://localhost:3080) after the containers start. Keep credentials, private configuration, and runtime data excluded from Git.

## Attribution

Based on LibreChat by Danny Avila and the LibreChat contributors.

- Source: https://github.com/LibreChat-AI/LibreChat
- License: MIT. See `LibreChat/LICENSE` for the original copyright and license notices.

This repository has independent Git history. The imported LibreChat code is credited to its original authors. Project-specific changes and operational results will be documented as they are completed.

## Current project work

- Fictional resident handbook and agent instructions.
- Local LibreChat installation connected to Gemini.
- Manual tests for handbook answers, missing information, and unsupported actions.

The saved agent and conversations are held in the running installation's MongoDB database. Their local files were migrated, but Git does not back them up. They require a separate export or backup.

## Credentials and runtime data

Keep API keys, passwords, private environment files, database files, logs, and backups out of Git. Use sanitized examples for deployment documentation.

## Project Progress Record

Dates use Asia/Manila time. This record separates observed results from work that still needs verification. Detailed tasks, branch names, and evidence status are maintained in [the project tracker](docs/project-tracker.md).

| Phase | Date | Work performed | Evidence and verification |
|---|---|---|---|
| Local setup | 2026-11-08 | Student installed WSL, enabled SVM, installed Docker, and installed LibreChat using Docker Compose. Created a fictional local demo account and connected Gemini. Codex supplied setup guidance and verified the Docker engine. | [Original interface](docs/evidence/E-05-original-interface.png). A shared screenshot showed a successful Gemini 3.6 Flash response. |
| Resident assistant and initial reskin | 2026-11-08 | Codex drafted the fictional handbook and agent instructions. Student created the Residential Building Assistant agent, attached the handbook through File Context, and tested resident questions. Configuration guidance covered the app title, footer, and conversation starters; final appearance still needs verification. | [Handbook answer](docs/evidence/E-01-resident-agent.png) and [boundary tests](docs/evidence/E-03-boundary-tests.png). Pool closure, missing parking-sticker fee, and inability to reserve the elevator were demonstrated. Full evaluation and an actual failure example remain pending. |
| Repository organization and migration | 2026-11-08 | Student created an independent local repository. Codex organized the source under LibreChat/ and the handbook under content/, retained the MIT license and attribution, and migrated the stopped local runtime. Fixed the admin panel's missing private session secret. | Local checks confirmed new mount paths, matching database counts (1 user, 1 agent, 1 file, 3 conversations, 12 messages), successful app/config responses, and a healthy admin panel. Student verification of login and chat after migration is still pending. |
| AWS account safety | 2026-11-08, in progress | Student began MFA, budget, and IAM user setup with guidance. Screenshots show a budget form and the permissions step for residential-assistant-operator. | Final confirmation of budget creation, root MFA, IAM user creation, operator MFA, and role permissions is pending. Setup forms alone do not prove completion. |
| AWS role setup and session pause | 2026-11-08 | Guided configuration of ResidentialProjectSetupRole with an operator-only, MFA-required trust policy and temporary AdministratorAccess. Screenshot showed the role permissions selection page; final creation and role-switch test remain unverified. At the student's request, Codex stopped all six local project containers and confirmed their exited states. | Application data and Docker volumes preserved. No commit or push performed by Codex. Resume with the local startup commands, then verify operator sign-in and role switching. |
| AWS server provisioning and Docker | 2026-11-08 | Student launched the EC2 server, connected using Session Manager, verified Ubuntu, memory and disk space, and installed Docker Engine and Compose. Codex guided setup and organized the evidence. Local development was also restarted on request and its homepage verified. | [AWS setup record](docs/aws-setup.md), [server checks](docs/evidence/aws-server-environment.png), and [Docker hello-world](docs/evidence/aws-docker-verification.png). Application deployment and HTTPS on AWS are pending. Current branch observed as aws-deployment. |
| Runtime key storage | 2026-11-08 | Student created /sam10/residential/gemini-api-key as a Standard SecureString in Parameter Store. Codex prepared a scoped EC2 runtime policy for the chosen handbook object and parameter, including a restriction on other parameter reads. | [Parameter creation screenshot](docs/evidence/E-13-parameter-created.png). Policy attachment, handbook upload verification, and runtime access tests are pending. The secret value was not shown. |
| Runtime access verification | 2026-11-08 | Student attached ResidentialRuntimeAccess, installed AWS CLI, confirmed the EC2 role identity, successfully downloaded the handbook, and retrieved the SecureString with decryption while displaying only metadata. Corrected an initial S3 object-path mismatch. | [Text verification record](docs/aws-setup.md). Successful S3-download screenshot excluded at the student's request. Gemini key acceptance and full application deployment remain pending. |
| HTTPS checkpoint and app-secrets preparation | 2026-11-08 | Student started Caddy, demonstrated certificate issuance and the temporary setup page, and reported creating the app-secrets SecureString. Codex prepared the runtime-policy revision for the additional parameter. | HTTPS is serving a setup response; AI app deployment is pending. Revised-policy attachment and app-secrets validation are pending. Secret values have not been shared. |
| App-secrets validation and deployment bundle | 2026-11-08 | Student successfully validated all six required app-secret fields without displaying values. Codex drafted the private app stack, authenticated Gemini gateway, in-memory secret-loading launcher, database-user initialization, and HTTPS handover instructions. | Five offline gateway tests and static syntax/Compose checks passed. Runtime policy now also includes a private deployment-bundle object; applying that revision and running the cloud app remain pending. No evidence images or credentials are included in the bundle. |
| Private app startup on EC2 | 2026-11-08 | Student downloaded and started the app deployment. Terminal output showed MongoDB, the resident gateway, and LibreChat healthy. Codex reviewed the reported result and updated the progress record. | Text record only. Cloud demo login creation, public proxy handover, and actual Gemini answer remain pending. |
| Live resident assistant on AWS | 2026-11-08 | Student demonstrated a logged-in browser session at the public HTTPS hostname and a correct Gemini-backed answer about Monday pool closure and other-day hours. Codex recorded the milestone and drafted the current architecture and initial six-pillar review. | [Architecture](docs/architecture.md) and [initial baseline review](docs/baseline-review.md). Production request-log capture, registration test, formal quality score, monitoring and backups remain pending. Evidence images remain local for later selection. |
| Deployment acceptance checks | 2026-11-08 | Student showed production JSON request logs with question, timestamp, outcome, duration, model, app version and handbook version. An anonymous registration request returned HTTP 403 and Registration is not allowed. | [Baseline observations](docs/baseline-review.md). The observed successful request took 1977 ms; no overall quality, latency, or availability score is claimed. Ready to move to monitoring and recovery work. |
| Monitoring preparation | 2026-11-08 | Student created and confirmed an SNS email subscription, received a direct test notification, installed CloudWatch agent 1.300074.1b2005-1, and identified the three production container log paths. Codex prepared automatic agent configuration and a scheduled app-metric collector. | [Monitoring setup](deployment/monitoring/README.md). Offline collector tests run locally; server activation, ingestion, dashboard, alarms, and actual alarm email remain pending. SNS confirmation/test is distinct from CloudWatch alarm evidence. |
| Monitoring activation | 2026-11-08 | Student activated the CloudWatch agent and metric timer, showed a successful metric-publication journal entry, and demonstrated CWAgent memory/disk series and six application metric series in the console. Codex prepared dashboard JSON for the observed EC2 instance. | Dashboard application/populated graphs, log ingestion, six alarms, and an actual alarm email still need verification. Evidence image publication remains deferred. |

Dashboard verification: the student's CloudWatch screenshots showed Residential-Assistant-Operations populated with application and host metrics. Codex prepared create-alarms.py for six SNS-linked alarms; AWS execution and actual alarm email are still pending. Evidence images remain deferred.

Alarm verification (2026-11-09, Manila): the student ran create-alarms.py in CloudShell and demonstrated six alarms in CloudWatch, all OK with actions enabled. Actual metric-triggered notification delivery remains pending. Codex prepared a controlled unauthorized internal request to exercise the application-error metric without calling Gemini or stopping the app.

Alarm delivery test verified (2026-11-09, Manila): the student ran one controlled unauthorized gateway request (HTTP 401), showed Residential-ApplicationErrors in ALARM, and demonstrated its matching SNS email showing OK → ALARM at 2026-11-08 16:19:47 UTC / November 9 00:19:47 Manila. This verifies the request-error metric, alarm and email path. Recovery notification remains unverified. The test is synthetic and excluded from normal quality/performance results; screenshot copying/publication remains deferred.

Log ingestion verified (2026-11-09, Manila): student demonstrated gateway request events and MongoDB connection events in their CloudWatch log streams. Both captures show six alarms OK, confirming state recovery after the controlled error test; recovery email remains unverified. Codex organized both original captures locally with hash verification. Log retention and API-log ingestion still need console confirmation. No evidence was committed or pushed.

Log retention verified (2026-11-09, Manila): the student demonstrated gateway, API and MongoDB log groups with two-week retention. A populated stream supplied for the API check has its group name cropped out; final evidence should include the group name. Codex preserved both original images locally with checksums. Evidence remains ignored by Git and unpublished. Next work is versioning verification and scheduled database backups with isolated restore.

API log identity verified (2026-11-09, Manila): the student's follow-up capture explicitly showed /sam10/residential/api with populated LibreChat events. Gateway, API and MongoDB ingestion and two-week retention are now verified. Codex preserved the original in the ignored local evidence library and updated the index; no commit or push was performed.

Content versioning check (2026-11-09, Manila): student supplied the Bucket Versioning panel showing Enabled during the sam10-residential-content-1229 check. The crop does not include bucket identity; obtain a full identity capture for final evidence. Codex organized the original locally. Scheduled database backup, retention and restore remain pending; versioning alone does not fulfill them.

Backup permissions attached (2026-11-09, Manila): student demonstrated ResidentialBackupAccess created on ResidentialAssistantEC2Role. Codex prepared the scoped backups-prefix policy and preserved the confirmation screenshot locally with a checksum. Actual upload/download, scheduled backup, retention and restore remain unverified. No evidence was committed or pushed.

Backup preparation (2026-11-09, Manila): student demonstrated mongodump 100.16.0 and successful S3 listing of backups/ (zero-byte folder marker). Codex prepared a write-locked logical database backup script with finally-based unlock, private temporary storage, collection-count manifest, explicit SSE-S3 and SHA-256 upload checksums. Three offline failure-path tests passed. First actual database backup, scheduling, retention and restore are still pending. Source-only backup-bundle.zip is prepared outside the repository; no credentials or evidence images are included.

First backup attempt troubleshooting (2026-11-09, Manila): student reported backup_failed; a direct check confirmed MongoDB ping 1 and writeLocked false. Detailed traceback identified the post-unlock validation. Codex corrected numeric comparison of mongosh BSON Long lockCount (which may serialize as text) and added a regression test. Four offline tests passed and the local source bundle was refreshed. Applying the correction on EC2 and verifying S3 backup success remain pending; no successful backup is claimed.

First database backup uploaded (2026-11-09, Manila): after correcting the BSON lock-count conversion inside mongosh, the student demonstrated backup_uploaded for 20261108T172036Z-b98a2319 with collection counts and S3 manifest location; completion around 01:20:40 Manila. Codex preserved the screenshot locally. S3 object-list verification, scheduling, retention and isolated restore remain pending; no recoverability or unattended-run result is claimed.

Backup object listing verified (2026-11-09, Manila): student showed LibreChat.archive.gz (13.2 KB) and manifest.json (2.0 KB) in S3, both last modified 01:20:40 UTC+08. The screenshot was preserved locally with a checksum. Retention, scheduled runs and isolated restore remain pending. This confirms object presence, not restore success.

Backup retention enabled (2026-11-09, Manila): student demonstrated Residential-Backup-Retention successfully created and Enabled. Prior setup screens showed backups/daily/ prefix, seven-day current expiration and seven-day noncurrent expiration, with newer-version count blank. Codex prepared a temporary five-minute timer for two unattended validation runs before nightly scheduling; installation and unattended execution remain pending.

Unattended backup validation (2026-11-09, Manila): student demonstrated the enabled active systemd timer and three backup_uploaded entries with successful service completion. UTC completion times November 8 17:37:16, 17:42:17 and 17:47:18 correspond to November 9 01:37:16, 01:42:17 and 01:47:18 Manila. These are genuine unattended runs under the temporary five-minute test schedule, not three nightly runs. Codex prepared the final nightly timer for 02:00 Manila and retained the validation timer source separately. Nightly activation, second automation and isolated restore remain pending. Evidence images remain local and unpublished.

Nightly backup schedule activated (2026-11-09, Manila): student replaced the temporary validation interval with OnCalendar=*-*-* 18:00:00 UTC and Persistent=true, reloaded systemd and restarted the timer. The timer listing showed its next trigger at November 8 18:00 UTC / November 9 02:00 Manila. Three earlier unattended validation backups remain recorded separately. A completed nightly execution, isolated restore and second automation remain pending. Screenshot preserved locally only.

Isolated restore attempt (2026-11-09, Manila): archive checksum verified against the downloaded manifest. Student restored into a separate network-isolated test MongoDB container. The first attempt reported 75 documents restored but failed creating an index: available temporary disk 59,717,440 bytes versus required 524,288,000. Codex's initial 256 MiB tmpfs sizing was insufficient; corrected test sizing is 1 GiB. Retry, index verification and collection-count comparison remain pending. This is not recorded as a successful restore.

Restore retry completed (2026-11-09, Manila): after increasing only the isolated test container's temporary database filesystem to 1 GiB, student demonstrated index restoration output ending with 75 documents restored and zero document failures at 02:12:16 Manila. Codex preserved the original locally. Explicit restored collection-count and index verification, cleanup and measured recovery timing remain pending. The initial index disk-space failure is retained in the record.

Restore data-count verification (2026-11-09, Manila): student compared the isolated restored database with the downloaded backup manifest and demonstrated all 60 collection counts match. Archive checksum and 75-document restore result were already observed. Codex organized the screenshot locally. Explicit messages-index verification and test cleanup remain pending; no field-by-field equivalence or full-service recovery-time claim is made.

Messages index verified (2026-11-09, Manila): student demonstrated messageId_1_user_1_tenantId_1 with unique true in the restored test database. Together with matching archive SHA-256, 75 restored documents and matching counts for all 60 collections, this completes the demonstrated database restore checks. Test-container cleanup and a measured full recovery exercise remain pending. Full index-definition and field-by-field comparison were not performed.

Post-restore live-system check (2026-11-09, Manila): student demonstrated docker ps with residential-proxy running and residential-api-1, residential-mongodb-1 and residential-gateway-1 healthy. Restore-test container was absent from the running list after cleanup instructions; the removal command output itself was not captured. Monitoring/backup core checks are ready for a local phase commit and transition to automation/incident work. Codex has not committed or pushed files or evidence.

Second automation preparation (2026-11-09, Manila): student demonstrated ResidentialQualityAlertAccess created on the EC2 role. Codex prepared a three-question heuristic answer regression check, private raw-response reports, SNS summary emails, and validation/nightly systemd schedule installer on automation-incident. Three offline tests passed and installer syntax was checked. Source-only quality-bundle.zip is ready for manual upload. Live execution, inbox delivery and two unattended runs remain pending; this is distinct from the formal 15-question evaluation.

Second automation manual check verified (2026-11-09, Manila): student demonstrated quality_check_completed for run 20261108T184856Z-20e6c563, completed 02:49:08 Manila, with 3/3 heuristic checks and notification_sent true. Matching SNS summary email was received. Raw answers are stored privately on EC2. This is one manual regression check, not an unattended run or formal project quality score. Two unattended validation executions and nightly schedule activation remain pending. Originals preserved locally only.

Second automation unattended runs verified (2026-11-09, Manila): student showed two successful systemd-triggered answer checks: 20261108T185751Z-8debecd7 completed November 8 18:57:59 UTC / November 9 02:57:59 Manila, and 20261108T190252Z-aaaf8e26 completed 19:02:59 UTC / 03:02:59 Manila. Both recorded 3/3 heuristic passes, notification_sent true and successful service completion. The earlier manual email proves inbox delivery for that manual run; these journal entries prove SNS acceptance, not separately observed inbox receipt. Both required automations now have at least two unattended validation runs. Final nightly answer-check activation remains pending. Evidence preserved locally, not published.

Development paused (2026-11-09, Manila): at the student's request Codex stopped the six local LibreChat containers while preserving data. AWS EC2 was left running for the live website, monitoring and schedules. Current branch is automation-incident; no changes were committed or pushed. Requested answer-check schedule is 19:00 Manila / 11:00 UTC, but cloud application has not yet been demonstrated and the repository installer still needs reconciliation with the verified setting. Resume with that check; handbook edits remain deferred.

### AI assistance record

Codex assisted with planning, setup instructions, handbook and prompt drafting, repository organization, migration commands, local checks, and documentation. The student performed the installations, account setup, agent setup, and manual question tests. Review and update this record as work continues. The final submission declaration must describe AI assistance and how the output was verified.
