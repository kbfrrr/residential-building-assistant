# Residential Building Assistant

A SAM10 Systems Administration and Maintenance school project adapting LibreChat into an informational assistant for a fictional residential building.

## Project folders

- `content/` contains the fictional resident handbook.
- `LibreChat/` contains the upstream application source and its original license and documentation.
- `docs/` contains the project tracker and captured evidence.

Run application commands from `LibreChat/`. The local demonstration now runs from this repository. Its configuration, MongoDB files, uploads, and other local runtime files were copied from the original installation while its containers were stopped. Existing Docker named volumes were retained using the Compose project name `librechat`.

```powershell
cd "C:\Users\kobej\Documents\SAM10 Final Project\residential-building-assistant\LibreChat"
docker compose -p librechat up -d
```

Open http://localhost:3080. Keep private configuration and runtime data ignored by Git. The original installation remains outside this repository as a temporary migration fallback pending manual verification.

Local development was stopped at the student's request on November 8, 2026. All six project containers are stopped; data and Docker volumes were preserved. Use the startup commands above to resume.

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

### AI assistance record

Codex assisted with planning, setup instructions, handbook and prompt drafting, repository organization, migration commands, local checks, and documentation. The student performed the installations, account setup, agent setup, and manual question tests. Review and update this record as work continues. The final submission declaration must describe AI assistance and how the output was verified.
