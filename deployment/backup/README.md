# Database backup preparation

Run on the project EC2 host under sudo. Python standard library, Docker and AWS CLI are already present; no new software installation is needed. The instance role needs deployment/iam/backup-access.json. Do not run this script in Windows or CloudShell. Read source before running.

## First manual execution

Upload backup-bundle.zip to sam10-residential-content-1229/backups/setup/ using the S3 console. That path is permitted by the backup role policy. In Session Manager download it, create /opt/residential-assistant/backup, extract there, then run:

```bash
sudo python3 /opt/residential-assistant/backup/backup.py
```

Do not send chat messages while testing the backup. The script briefly locks MongoDB writes while collecting collection counts and a compressed logical dump, then unlocks before contacting S3. Reads remain possible, but operations that write can wait. This is a single-host demo maintenance tradeoff, not a zero-downtime backup design. See MongoDB's [mongodump guidance](https://www.mongodb.com/docs/database-tools/mongodump/mongodump-examples/) and [write-lock behavior](https://www.mongodb.com/docs/manual/reference/method/db.fsynclock/).

Uploads are under backups/daily/<UTC-time-and-random-ID>/: LibreChat.archive.gz and manifest.json. Explicit SSE-S3 encryption and SHA-256 upload checksums are used. The manifest is uploaded last; a backup is a candidate for restore only when both files are present. A successful upload is not proof of recoverability. Verify downloaded archive digest, isolated restore and document counts before making that claim.

Root-only temporary files are removed at completion or ordinary exception. No database content, password or raw tool error is printed. The archive contains private application data including user password hashes and chats; never put it in Git or the public website. The manifest contains collection names and counts, not records. Host/root administrators can inspect running processes; no API key is needed by this script. Keep runtime secret parameters available separately for application recovery.

Scope: LibreChat database only. Filesystem uploads, secrets, proxy certificate volumes, images and infrastructure are not part of this database dump. Handbook content is separately versioned in S3. A full host recovery needs those dependencies and the deployment runbook.

## Failure recovery

The script attempts fsyncUnlock in a finally block on dump/count errors. An abrupt process kill, server failure, or power loss may leave MongoDB write-locked. Do not run another locking tool concurrently. If a backup fails or chat writes hang, inspect the job and recover the project-owned lock once:

```bash
sudo python3 /opt/residential-assistant/backup/backup.py --unlock
```

Expected lockCount is zero. If no lock exists, MongoDB may report an error; inspect the running service and database state before further actions. Do not repeatedly force-unlock locks owned by another operator. Retest the app after recovery. Partial uploads may remain after failure; no remote object deletion is performed by this script.

First manual execution verified: backup 20261108T172036Z-b98a2319 completed around November 9 01:20:40 Manila. S3 listing showed the archive (13.2 KB) and manifest (2.0 KB). Initial unlock validation failed because BSON lockCount needed conversion inside mongosh; the corrected source converts it with Number before JSON serialization. The failure-path tests are offline and do not replace restore verification.

Retention rule Residential-Backup-Retention was demonstrated enabled for the project bucket. Setup captures show prefix backups/daily/, current expiration after 7 days and noncurrent expiration 7 days after becoming noncurrent, with no newer-version count specified. This is not an immutable retention lock. Lifecycle timing is asynchronous, not deletion exactly to the second. The setup bundle and handbook are outside the scoped prefix. Observing the rule does not prove aged-object expiration has run.

## Schedule validation

The source service and timer run the same backup.py as root. The temporary validation timer source is residential-backup-validation.timer; install it as residential-backup.timer only during validation. It first triggers after two minutes, then approximately every five minutes after a service start. This schedule is intentionally temporary to demonstrate two genuine unattended runs without claiming two days of history. Jobs may briefly block database writes. Avoid manual concurrent backup runs.

Verify timer activity, journal timestamps and distinct backup IDs for at least two successful timer-triggered runs. Manual invocations do not count as unattended runs. Three successes were demonstrated: November 8 17:37:16, 17:42:17 and 17:47:18 UTC (November 9 01:37:16, 01:42:17 and 01:47:18 Manila). The main residential-backup.timer source now contains OnCalendar=*-*-* 18:00:00 UTC and Persistent=true (02:00 Manila daily). Install that final timer, reload and restart it, then verify its next trigger. The pending transition must not be described as already activated. Persistent=true permits a catch-up run when a missed calendar schedule is detected after reactivation.

Nightly scheduling is now verified: the student showed the rewritten timer and its next trigger at November 8 18:00 UTC / November 9 02:00 Manila after daemon-reload and restart. The next-trigger listing does not prove that nightly execution completed. Isolated restore remains unverified. Daily backups imply an intended RPO up to 24 hours only while successful daily runs are maintained; actual RPO and RTO remain unmeasured.
