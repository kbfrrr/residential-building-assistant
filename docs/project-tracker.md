# Project Tracker

Last updated: 2026-11-08, Asia/Manila.

Personal completion target: November 9, 2026. Submission deadline: November 13, 2026; cutoff time not yet confirmed.

## Session handoff

Development paused at the student's request on November 8, 2026. All six local Compose services were stopped and verified exited. Databases, uploaded files, private configuration, and named Docker volumes were retained. Local tracking changes remain available for review; Codex has not committed or pushed them.

Resume by opening Docker Desktop and running:

```powershell
cd "C:\Users\kobej\Documents\SAM10 Final Project\residential-building-assistant\LibreChat"
docker compose -p librechat up -d
```

Then open http://localhost:3080 and verify the migrated login and resident agent. The next AWS checkpoint is to confirm ResidentialProjectSetupRole was created and test an MFA-authenticated sign-in as residential-assistant-operator followed by switching into that role. The latest screenshot showed selection of AdministratorAccess during role creation; successful role creation and switching have not been observed. No AWS workload has been deployed through this chat. AWS console state and any resources created independently have not been audited during this pause.

## Phase board

| Phase | Suggested branch | Status | Remaining work |
|---|---|---|---|
| 01 Local setup | phase-01-local-setup | Working locally | Retain original-interface and model-connection evidence. |
| 02 Resident assistant | phase-02-resident-assistant | Partially complete | Verify final branding and conversation starters; export agent configuration without credentials; build the planned gateway and request logging; run the full evaluation; capture an actual incorrect or incomplete answer. |
| 03 AWS preparation | phase-03-aws-preparation | Current phase | Confirm account safety steps; enable operator MFA; configure temporary role access, CloudTrail, resource tags, and deployment configuration; resolve region, instance size, and HTTPS hostname. |
| 04 AWS deployment | phase-04-aws-deployment | Pending | Deploy over HTTPS; use private database access, versioned S3 content, runtime Parameter Store secrets; capture infrastructure design, baseline measurements, and initial six-pillar review. |
| 05 Monitoring and backups | phase-05-monitoring-backups | Pending | Dashboard, six alarms, SNS email delivery, request/database logs and retention, backup inventory, seven-day backup retention, S3 versioning, and verified restore with measured RPO/RTO. |
| 06 Automation and incident | phase-06-automation-incident | Pending | Two scheduled automations, two unattended runs of each, controlled fault diagnosis, verified prevention, incident timings, and tested runbook. |
| 07 Documentation | phase-07-documentation | Pending | Project website, system card, evidence beside claims, comparable before/after results and graph, costs, final six-pillar review, prioritized next steps, AI disclosure, signed declaration, and embedded 5-8 minute video. |
| 08 Submission | phase-08-submission | Pending | Check live URLs, video playback, secrets and Git history; package repository including .git; student submits; confirm teardown timing. |

These are proposed branch names, not claims that branches exist. At the latest inspection the current branch was main. Commit the current baseline when ready, then create phase branches from main and merge verified work back into main. Do not recreate past branches merely to imply a historical workflow. Switching branches does not roll back AWS resources or MongoDB state.

## Immediate next actions

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
| E-02 | Deployed system URL | Pending AWS deployment. |
| E-03 | Three test questions and answers including a failure | [Two boundary tests](evidence/E-03-boundary-tests.png) captured, plus the E-01 pool question. All three demonstrated expected behavior; actual failure evidence remains pending. |
| E-04 | Quality measurement script and result | Pending; no evaluation score claimed. |
| E-05 | Original interface for reskin comparison | [Original LibreChat interface](evidence/E-05-original-interface.png) captured. |
| E-06 | Populated dashboard | Pending. |
| E-07 | Alarms | Pending. |
| E-08 | Received alert email with timestamp | Pending. |
| E-09 | Request-log sample | Pending. |
| E-10 | Backup settings and output | Pending. Local migration copying does not count as the scheduled backup requirement. |
| E-11 | Restore output and verification | Pending. Local folder migration does not count as the required restore test. |
| E-12 | MFA and IAM user list | Pending completed-settings screenshots. |
| E-13 | Parameter Store or Secrets Manager setup | Pending. Never show secret values. |
| E-14 | Two automations with unattended timestamps | Pending. |
| E-15 | Fault investigation logs and commands | Pending assessed incident. Local setup troubleshooting is documented separately. |
| E-16 | Cost before and after | Pending. Budget configuration is separate from cost-comparison evidence. |
| E-17 | Six-pillar review and highest-priority gap | Pending initial and final reviews. |
| E-18 | AWS infrastructure design | Planned architecture discussed; final diagram pending actual deployment. |

## Recording rules

- Add dated entries to the README's Project Progress Record when work is completed or a result is verified.
- Identify student actions and Codex assistance accurately.
- Mark a task complete only after the result is observed. A form, intention, or configuration draft is insufficient evidence of execution.
- Preserve actual results and failures. Do not invent timestamps, scores, screenshots, branch history, or unattended executions.
- Keep API keys, passwords, MFA setup material, and personal records out of evidence and Git.
- Keep updates local until the student requests publishing.
