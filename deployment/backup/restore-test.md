# Isolated restore test record

November 9, 2026 (Manila): downloaded archive and manifest for backup 20261108T172036Z-b98a2319 from S3 into /tmp/residential-restore-check. Student verified archive SHA-256 equals manifest archive.sha256. A separate MongoDB 8.0.20 test container was created with --network none and a temporary /data/db mount; no live database volume was attached.

First restore attempt at November 8 18:09:28 UTC / November 9 02:09:28 Manila was incomplete. mongorestore reported 75 documents restored and zero document failures, but also Failed: LibreChat.messages, OutOfDiskSpace during index creation: 59,717,440 bytes available versus a required minimum 524,288,000 bytes. The final document-count summary alone does not establish success. The initial 256 MiB temporary filesystem was too small for data, journal files and the index-build free-space reserve.

Correction: recreate only residential-restore-check with a 1 GiB temporary /data/db mount. The tmpfs limit is a maximum rather than fully preallocated memory; watch host memory during testing. Never remove residential-mongodb-1 or use its volume for this test. Corrected command:

```bash
sudo docker run -d --name residential-restore-check --network none --tmpfs /data/db:rw,size=1g mongo:8.0.20 --bind_ip 127.0.0.1 --wiredTigerCacheSizeGB 0.25
```

The retry completed at November 9 02:12:16 Manila with 75 documents restored and zero document failures. The archive checksum matched, all 60 collection counts matched the manifest, and the compound messages index was present with the unique option. The first logged failure and the retry completion were 2 minutes 48 seconds apart. The restore start, first human observation, and full application recovery time were not captured.

## Runbook for an index build that runs out of space

1. Read the entire restore output. An `OutOfDiskSpace` error during index creation requires action even when the final document summary reports zero failures.
2. Verify the backup archive against its manifest. Check free space in the isolated test container using `sudo docker exec residential-restore-check df -h /data/db`. Account for database files, journal files, and the index-build free-space requirement.
3. Recreate the isolated test container using the command above. The 1 GiB limit worked for this archive. Check available space and size the mount for larger archives before restoring.
4. Once the test MongoDB instance responds to a ping, restore into the test container:

   ```bash
   sudo docker exec -i residential-restore-check mongorestore --archive --gzip --nsInclude='LibreChat.*' < /tmp/residential-restore-check/LibreChat.archive.gz
   ```

5. Check the exit status and the index output. Compare restored collection counts with the manifest and confirm that `messageId_1_user_1_tenantId_1` appears in `db.messages.getIndexes()` with `unique: true`.
6. Remove the test container once evidence is captured. If the retry fails, preserve its output and repeat from a fresh test container after correcting the identified cause.

For the recording, use the saved E-11 captures of the disk error, successful retry, collection comparison, and restored index. The production containers were shown running after the exercise.
