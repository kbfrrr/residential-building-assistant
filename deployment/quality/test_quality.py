import unittest
from unittest.mock import patch
from types import SimpleNamespace
import quality_check as quality


class QualityTests(unittest.TestCase):
    def test_expected_answers_and_http_failure(self):
        self.assertTrue(quality.judge("pool_monday", 200, "The pool is closed every Monday for cleaning."))
        self.assertTrue(quality.judge("gym_hours", 200, "Daily from 6:00 AM to 10:00 PM."))
        self.assertTrue(quality.judge("unknown_parking_fee", 200, "The handbook does not specify that fee. Contact the building office."))
        self.assertFalse(quality.judge("pool_monday", 500, "The pool is closed Monday."))

    def test_invented_fee_and_wrong_facts_fail(self):
        self.assertFalse(quality.judge("unknown_parking_fee", 200, "The handbook does not list it, but pay 100 pesos at the office."))
        self.assertFalse(quality.judge("gym_hours", 200, "Open 9 AM to 5 PM."))
        self.assertFalse(quality.judge("pool_monday", 200, "It is closed sometimes but open on Monday."))

    def test_request_failure_does_not_expose_stderr(self):
        with patch.object(quality.subprocess, "run", return_value=SimpleNamespace(returncode=1, stderr="private diagnostic")):
            result = quality.ask("Pool hours?")
        self.assertEqual(result["status"], 0)
        self.assertNotIn("private", str(result))


if __name__ == "__main__":
    unittest.main()
