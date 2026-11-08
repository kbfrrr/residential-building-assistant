# Project Tracker

Last updated: 2026-11-09, Asia/Manila.

Personal completion target: November 9, 2026. Submission deadline: November 13, 2026; cutoff time not yet confirmed.

## Session handoff

Development resumed on November 8, 2026 at the student's request. Codex started Docker Desktop and the six local services and verified an HTTP 200 homepage response. Earlier stop and migration actions preserved the data and volumes. Student has since launched EC2 and successfully installed Docker there. See [AWS setup and evidence](aws-setup.md). Codex has not committed or pushed the current tracking updates.

Resume by opening Docker Desktop and running:

```powershell
cd "C:\Users\kobej\Documents\SAM10 Final Project\residential-building-assistant\LibreChat"
docker compose -p librechat up -d
```

The cloud app now answers at the public HTTPS hostname. The student's browser screenshot demonstrated the Residential Building Assistant responding correctly to the Monday pool question with Section 2 cited. Next capture a production request-log sample, verify registration is closed, then begin monitoring and scheduled backups. Initial [architecture](architecture.md) and [baseline/six-pillar review](baseline-review.md) are drafted from observed work. Final MFA, budget, CloudTrail, tags, and running-instance security evidence remain to be confirmed.

## Phase board

| Phase | Suggested branch | Status | Remaining work |
|---|---|---|---|
| 01 Local setup | phase-01-local-setup | Working locally | Retain original-interface and model-connection evidence. |
| 02 Resident assistant | local-build-and-reskin | Working locally and on AWS | Handbook and gateway integration work. Capture actual request logs, complete final branding/conversation starters, run full evaluation, and preserve an actual failure example. |
| 03 AWS preparation | aws-preparation | Partially complete | Region, compute selection and instance-profile setup documented. Confirm account safety, CloudTrail, tags, runtime permissions, and final deployed settings. |
| 04 AWS deployment | aws-deployment | Core deployment verified | Live HTTPS chat, required request-log fields, and anonymous registration rejection (HTTP 403) observed. Architecture and initial six-pillar review drafted. Complete remaining security/baseline evidence as tracked, then commit/merge before monitoring changes. |
| 05 Monitoring and backups | monitoring-and-backups | Core checks verified; ready for phase commit | Dashboard, six alarms, actual alarm email, three log streams with 14-day retention, S3 versioning, retention rule, three unattended validation backups, nightly timer, archive checksum, restored counts for 60 collections and messages unique index verified. Final evidence review and measured full recovery timings remain outstanding. |
| 06 Automation and incident | phase-06-automation-incident | Pending | Two scheduled automations, two unattended runs of each, controlled fault diagnosis, verified prevention, incident timings, and tested runbook. |
| 07 Documentation | phase-07-documentation | Pending | Project website, system card, evidence beside claims, comparable before/after results and graph, costs, final six-pillar review, prioritized next steps, AI disclosure, signed declaration, and embedded 5-8 minute video. |
| 08 Submission | phase-08-submission | Pending | Check live URLs, video playback, secrets and Git history; package repository including .git; student submits; confirm teardown timing. |

At the latest inspection the current branch was aws-deployment with a clean working tree before these documentation updates. Future phase branch names are suggestions. Commit and merge verified phase work into main before starting the next phase branch. Do not recreate past branches merely to imply a historical workflow. Switching branches does not roll back AWS resources or MongoDB state.

## Immediate next actions

- [x] Production gateway log observed with question, timestamp, success, HTTP status, duration, model, app version, and handbook version.
- [x] Student tested an anonymous registration POST at the public HTTPS endpoint; it returned HTTP 403 and Registration is not allowed.
- [ ] Review the initial architecture and six-pillar baseline, commit deployment work, merge into main, and create the monitoring branch before monitoring file changes.

- [ ] Student verifies migrated login, agent, conversations, and handbook response at http://localhost:3080.
- [ ] Confirm AWS budget creation and root MFA from completed settings.
- [ ] Finish creating residential-assistant-operator, enable its MFA, and configure temporary project-role access.
- [ ] Keep the original installation until migrated behavior is verified. Confirm before removing it; its current existence has not been rechecked since migration.
- [ ] Confirm whether the current baseline should be committed locally. Publishing is deferred at the student's request.

## Evidence register

Evidence IDs follow Appendix B of the project brief. Captured images are original user-provided screenshots copied without editing. Local storage is for preparation; the final website must embed evidence beside the relevant claims.

| ID | Required evidence | Current state |
|---|---|---|
| E-01 | Reskinned interface with realistic question and answer | [Resident agent test](evidence/E-01-resident-agent.png) captured. Replace or supplement with final branding. |
| E-02 | Deployed system URL | Live browser chat observed at https://residential-assistant.54.179.56.26.sslip.io. Preserve selected evidence during deliverable compilation. |
| E-03 | Three test questions and answers including a failure | [Two boundary tests](evidence/E-03-boundary-tests.png) captured, plus the E-01 pool question. All three demonstrated expected behavior; actual failure evidence remains pending. |
| E-04 | Quality measurement script and result | Pending; no evaluation score claimed. |
| E-05 | Original interface for reskin comparison | [Original LibreChat interface](evidence/E-05-original-interface.png) captured. |
| E-06 | Populated dashboard | Student screenshots verified Residential-Assistant-Operations with populated request, error, latency, CPU, disk, memory, database and heartbeat graphs. Image selection/publication deferred. |
| E-07 | Alarms | Student demonstrated all six Residential-prefixed alarms in CloudWatch, each OK with actions enabled. Actual metric-triggered email delivery remains pending. Image selection/publication deferred. |
| E-08 | Received alert email with timestamp | Student demonstrated the Residential-ApplicationErrors SNS email with OK → ALARM at 2026-11-08 16:19:47 UTC (2026-11-09 00:19:47 Manila). Trigger was one intentional unauthorized gateway request returning HTTP 401. Recovery notification remains unverified. Screenshot not copied or published; select/redact during deliverable compilation. |
| E-09 | Request-log sample | Student demonstrated the successful pool-question JSON log with duration_ms 1977 and required fields. November 9 screenshots verified named gateway, API and MongoDB streams with populated log events, plus all three groups with two-week retention. Originals preserved only in the ignored local library. |
| E-10 | Backup settings and output | Manual backup and S3 archive/manifest listing verified; seven-day current/seven-day noncurrent lifecycle rule Enabled. Three successful five-minute timer-triggered uploads observed November 9 around 01:37, 01:42 and 01:47 Manila. Nightly schedule transition and restore verification pending. Screenshots preserved locally only. |
| E-11 | Restore output and verification | Downloaded archive checksum verified. Initial isolated restore failed index creation because test tmpfs was too small; retry with 1 GiB restored 75 documents. All 60 collection counts match the manifest; the previously failing compound messages index is present and unique. After the cleanup instruction, running-container list excludes the test container and shows production containers up. Container deletion itself was not shown. Measured full recovery timing remains pending. Original captures remain local. |
| E-12 | MFA and IAM user list | Pending completed-settings screenshots. |
| E-13 | Parameter Store or Secrets Manager setup | [SecureString creation](evidence/E-13-parameter-created.png) confirmed. Student demonstrated decrypted retrieval with only metadata displayed; key acceptance by Gemini remains untested on EC2. |
| E-14 | Two automations with unattended timestamps | Backup automation demonstrated three unattended successes under the disclosed temporary five-minute validation schedule: November 9 around 01:37, 01:42 and 01:47 Manila. Second distinct automation with two unattended runs remains pending. Nightly backup schedule not yet verified. |
| E-15 | Fault investigation logs and commands | Pending assessed incident. Local setup troubleshooting is documented separately. |
| E-16 | Cost before and after | Pending. Budget configuration is separate from cost-comparison evidence. |
| E-17 | Six-pillar review and highest-priority gap | [Initial review](baseline-review.md) drafted; final review after incident remains pending. |
| E-18 | AWS infrastructure design | [Current app diagram](architecture.md) drafted; update after monitoring/backup changes. |

## Recording rules

Local evidence organization authorized November 9, 2026: 28 original screenshot copies organized under docs/evidence/organized/ with an evidence-ID index and SHA-256 manifest. This ignored directory remains local. No evidence images were staged, committed or pushed. Original files and the three historical tracked images were retained. The explicitly excluded successful S3-download screenshot was not copied. Email captures need redaction review before publication. This supersedes the earlier deferral of local organization, but publication remains deferred.

Evidence publishing preference, November 8, 2026: keep evidence images local and defer their selection, organization for submission, and GitHub publication until deliverable compilation. New files under docs/evidence/ are ignored by Git. Three earlier screenshots (E-01, E-03 and E-05) are already tracked in local history; ignore rules do not remove those historical copies. Review those commits before any first publication, and do not push branches containing them before resolving the student's evidence-publication preference. No history rewrite or image deletion has been performed.

- Add dated entries to the README's Project Progress Record when work is completed or a result is verified.
- Identify student actions and Codex assistance accurately.
- Mark a task complete only after the result is observed. A form, intention, or configuration draft is insufficient evidence of execution.
- Preserve actual results and failures. Do not invent timestamps, scores, screenshots, branch history, or unattended executions.
- Keep API keys, passwords, MFA setup material, and personal records out of evidence and Git.
- Keep updates local until the student requests publishing.
