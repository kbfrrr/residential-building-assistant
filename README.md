# Residential Building Assistant

A SAM10 Systems Administration and Maintenance school project adapting LibreChat into an informational assistant for a fictional residential building.

## Project folders

- `content/` contains the fictional resident handbook.
- `LibreChat/` contains the upstream application source and its original license and documentation.

Run application commands from `LibreChat/`. This repository is a source copy. The existing local demonstration is currently running from the separate original installation at `../LibreChat/`, whose database, secrets, and saved agent have not been migrated into this copy.

## Attribution

Based on LibreChat by Danny Avila and the LibreChat contributors.

- Source: https://github.com/LibreChat-AI/LibreChat
- License: MIT. See `LibreChat/LICENSE` for the original copyright and license notices.

This repository has independent Git history. The imported LibreChat code is credited to its original authors. Project-specific changes and operational results will be documented as they are completed.

## Current project work

- Fictional resident handbook and agent instructions.
- Local LibreChat installation connected to Gemini.
- Manual tests for handbook answers, missing information, and unsupported actions.

The saved agent and conversations are held in the running installation's MongoDB database. They require a separate export or backup.

## Credentials and runtime data

Keep API keys, passwords, private environment files, database files, logs, and backups out of Git. Use sanitized examples for deployment documentation.
