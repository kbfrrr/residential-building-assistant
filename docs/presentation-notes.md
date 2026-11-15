# Presentation notes

## Why database backups run at 2:00 AM Manila

The daily database backup is scheduled for 02:00 Manila (18:00 UTC). This was chosen as an intended low-traffic maintenance window because the implementation briefly pauses MongoDB writes while collecting a consistent logical backup. Lower overnight traffic is a design assumption for the fictional residential system, not measured production usage. The project guidelines do not require 2:00 AM; it is configurable. EC2 runs independently of the student's PC, so the student does not need to remain awake or keep the PC on.

The answer check runs at 02:15 Manila (18:15 UTC). The student confirmed the next trigger for November 15, 2026. Explain that the 15-minute gap gives the 02:00 backup time to finish. The 19:00 journals show 3/3 on November 11 and 14 and 2/3 on November 12 and 13. Use the two dated 3/3 entries to demonstrate unattended execution and acknowledge the two flagged results. Check the overnight results before recording.

Include this rationale when creating presentation slides or the demonstration narration, as explicitly requested by the student on November 9, 2026.

## Restore incident for the recording

Show the first restore's `OutOfDiskSpace` line. MongoDB had about 57 MiB free in the isolated test container and required at least 500 MiB free for the index build. Show the retry with a 1 GiB temporary mount, the matching counts for all 60 collections, and the rebuilt unique messages index. Explain that the runbook now calls for checking free space and verifying indexes. The error and retry-completion logs were 2 minutes 48 seconds apart.

Source: [Restore test and runbook](../deployment/backup/restore-test.md).
