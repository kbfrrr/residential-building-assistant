"""Offline checks for write-lock cleanup and manifest completion ordering."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("backup", Path(__file__).with_name("backup.py"))
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


class BackupTests(unittest.TestCase):
    def test_text_zero_lock_count_is_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            def dump(command, **kwargs):
                kwargs["stdout"].write(b"dummy archive")
            with patch.object(backup, "mongo", side_effect=[False, {"ok": 1}, {"users": 1}, {"ok": 1, "lockCount": "0"}]):
                with patch.object(backup, "run", side_effect=dump):
                    counts = backup.dump_locked(Path(temporary) / "dump.gz")
            self.assertEqual(counts, {"users": 1})

    def test_dump_failure_unlocks(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(backup, "mongo", side_effect=[False, {"ok": 1}, {"users": 1}, {"ok": 1, "lockCount": 0}]) as mongo:
                with patch.object(backup, "run", side_effect=RuntimeError("dump failed")):
                    with self.assertRaises(RuntimeError):
                        backup.dump_locked(Path(temporary) / "dump.gz")
            self.assertIn("fsyncUnlock", mongo.call_args.args[0])
            self.assertIn("Number(r.lockCount)", mongo.call_args.args[0])

    def test_existing_lock_is_not_released(self):
        with patch.object(backup, "mongo", return_value=True) as mongo:
            with self.assertRaises(RuntimeError):
                backup.dump_locked(Path("unused.gz"))
            self.assertEqual(mongo.call_count, 1)

    def test_failed_archive_upload_does_not_publish_manifest(self):
        def dump(path):
            path.write_bytes(b"dummy archive")
            return {"users": 1}
        with patch.object(backup, "dump_locked", side_effect=dump):
            with patch.object(backup, "upload", side_effect=RuntimeError("upload failed")) as upload:
                with self.assertRaises(RuntimeError):
                    backup.backup()
                self.assertEqual(upload.call_count, 1)
                self.assertTrue(upload.call_args.args[1].endswith("LibreChat.archive.gz"))


if __name__ == "__main__":
    unittest.main()
