# Isolated restore test record

Messages index verification completed: the student showed messageId_1_user_1_tenantId_1 with unique true in the isolated database. This is the compound index implicated in the initial failure. Archive SHA-256, all 60 collection counts and this index are now verified. Temporary test-container cleanup and a timed full recovery exercise remain pending.

Latest verification: student ran the manifest comparison against the isolated restored database and received `Restore verified: all 60 collection counts match backup manifest.` Combined with the archive SHA-256 check and 75-document restore result, this verifies restored collection counts. It does not verify every field value, all index definitions or full application recovery. Explicit messages-index check and cleanup are next. End-to-end recovery time remains unmeasured.

November 9, 2026 (Manila): downloaded archive and manifest for backup 20261108T172036Z-b98a2319 from S3 into /tmp/residential-restore-check. Student verified archive SHA-256 equals manifest archive.sha256. A separate MongoDB 8.0.20 test container was created with --network none and a temporary /data/db mount; no live database volume was attached.

First restore attempt at November 8 18:09:28 UTC / November 9 02:09:28 Manila was incomplete. mongorestore reported 75 documents restored and zero document failures, but also Failed: LibreChat.messages, OutOfDiskSpace during index creation: 59,717,440 bytes available versus a required minimum 524,288,000 bytes. The final document-count summary alone does not establish success. The initial 256 MiB temporary filesystem was too small for data, journal files and the index-build free-space reserve.

Correction: recreate only residential-restore-check with a 1 GiB temporary /data/db mount. The tmpfs limit is a maximum rather than fully preallocated memory; watch host memory during testing. Never remove residential-mongodb-1 or use its volume for this test. Corrected command:

```bash
sudo docker run -d --name residential-restore-check --network none --tmpfs /data/db:rw,size=1g mongo:8.0.20 --bind_ip 127.0.0.1 --wiredTigerCacheSizeGB 0.25
```

After confirming test-container readiness, repeat mongorestore into this container and require exit status zero with no index failures. Then compare restored collection counts to the manifest and verify indexes. The student demonstrated retry output ending at November 8 18:12:16 UTC / November 9 02:12:16 Manila with index restoration entries and 75 documents restored, zero document failures. A separately captured exit code and explicit count/index checks remain pending, as does cleanup. No end-to-end recovery-time measurement has been captured. This test validates database restoration only, not full host/application recovery.
