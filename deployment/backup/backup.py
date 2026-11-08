"""Root-only, single-host MongoDB backup; AWS uses the EC2 instance role."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

BUCKET = "sam10-residential-content-1229"
REGION = "ap-southeast-1"
CONTAINER = "residential-mongodb-1"
AWS = "/usr/local/bin/aws"
AUTH = 'const a=db.getSiblingDB("admin"); if(!a.auth(process.env.MONGO_INITDB_ROOT_USERNAME,process.env.MONGO_INITDB_ROOT_PASSWORD)) throw Error("Authentication failed"); '


def run(command, **kwargs):
    result = subprocess.run(command, stderr=subprocess.PIPE, timeout=180, **kwargs)
    if result.returncode:
        # Never forward database-tool stderr: it may contain private records or credentials.
        raise RuntimeError("Operation failed: " + Path(command[0]).name)
    return result


def mongo(js):
    result = run(["docker", "exec", CONTAINER, "mongosh", "--quiet", "--eval", AUTH + js],
                 stdout=subprocess.PIPE, text=True)
    return json.loads(result.stdout)


def dump_locked(archive):
    if mongo('print(JSON.stringify(Boolean(a.currentOp().fsyncLock)))'):
        raise RuntimeError("Database already write-locked; investigate before retrying.")
    # Mark before acquiring so a timeout after server-side acquisition still attempts unlock.
    try:
        lock = mongo('print(JSON.stringify(a.fsyncLock()))')
        if lock.get("ok") != 1:
            raise RuntimeError("Could not acquire database write lock")
        database = 'const d=db.getSiblingDB("LibreChat"); '
        counts = mongo(database + 'print(JSON.stringify(Object.fromEntries(d.getCollectionInfos({type:"collection"}).map(c=>[c.name,d.getCollection(c.name).countDocuments({})]))))')
        with archive.open("wb") as output:
            run(["docker", "exec", CONTAINER, "sh", "-c",
                 'exec mongodump --username "$MONGO_INITDB_ROOT_USERNAME" --password "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --db LibreChat --gzip --archive'],
                stdout=output)
        if archive.stat().st_size == 0:
            raise RuntimeError("Empty archive")
        return counts
    finally:
        released = mongo('const r=a.fsyncUnlock(); print(JSON.stringify({ok:Number(r.ok),lockCount:Number(r.lockCount)}))')
        # BSON Long values may serialize as strings in mongosh JSON output.
        if released.get("ok") != 1 or int(released.get("lockCount", -1)) != 0:
            raise RuntimeError("Database unlock needs operator attention; see README")


def upload(path, key):
    digest = hashlib.sha256(path.read_bytes()).digest()
    result = run([AWS, "s3api", "put-object", "--bucket", BUCKET, "--key", key,
                  "--body", str(path), "--server-side-encryption", "AES256",
                  "--checksum-algorithm", "SHA256", "--checksum-sha256",
                  base64.b64encode(digest).decode(), "--region", REGION, "--no-cli-pager"],
                 stdout=subprocess.PIPE, text=True)
    response = json.loads(result.stdout)
    return {"key": key, "sha256": digest.hex(), "bytes": path.stat().st_size,
            "version_id": response.get("VersionId")}


def backup():
    started = datetime.now(timezone.utc)
    identifier = started.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    prefix = "backups/daily/" + identifier + "/"
    with tempfile.TemporaryDirectory(prefix="residential-backup-") as temporary:
        archive = Path(temporary) / "LibreChat.archive.gz"
        counts = dump_locked(archive)
        archive_record = upload(archive, prefix + archive.name)
        manifest = {
            "format": 1, "backup_id": identifier, "database": "LibreChat",
            "started_utc": started.isoformat(),
            "consistency": "fsync write lock held during counts and mongodump; released before upload",
            "collections": counts, "archive": archive_record,
            "scope": "LibreChat database only; no filesystem uploads, container images, secrets or AWS configuration",
        }
        manifest_path = Path(temporary) / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        upload(manifest_path, prefix + "manifest.json")
    print(json.dumps({"event": "backup_uploaded", "backup_id": identifier,
                      "manifest": "s3://" + BUCKET + "/" + prefix + "manifest.json",
                      "archive_bytes": archive_record["bytes"], "collections": counts,
                      "completed_utc": datetime.now(timezone.utc).isoformat()}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unlock", action="store_true", help="Recovery only: release one database fsync lock")
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit("Run with sudo python3 backup.py")
    os.umask(0o077)
    import fcntl
    with open("/run/residential-backup.lock", "w") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.unlock:
            print(json.dumps(mongo('const r=a.fsyncUnlock(); print(JSON.stringify({ok:Number(r.ok),lockCount:Number(r.lockCount)}))')))
        else:
            backup()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"event": "backup_failed", "reason": str(error) if isinstance(error, RuntimeError) else type(error).__name__,
                          "next": "Check database write-lock state and follow backup README recovery steps."}))
        raise SystemExit(1)
