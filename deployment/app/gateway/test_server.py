"""Offline compatibility tests, with AWS and Gemini replaced by test doubles."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import threading
import types
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen


spec = importlib.util.spec_from_file_location("gateway_server", Path(__file__).with_name("server.py"))
gateway = importlib.util.module_from_spec(spec)
with patch.dict("sys.modules", {
    "boto3": types.ModuleType("boto3"),
    "botocore": types.ModuleType("botocore"),
    "botocore.config": types.SimpleNamespace(Config=object),
}):
    spec.loader.exec_module(gateway)


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {"RESIDENT_GATEWAY_KEY": "test-only"})
        self.environment.start()
        self.logs = contextlib.redirect_stdout(io.StringIO())
        self.logs.__enter__()
        self.server = gateway.ThreadingHTTPServer(("127.0.0.1", 0), gateway.Handler)
        self.server.resources = types.SimpleNamespace(load=lambda: ("Test handbook", "test-secret", "v1"))
        self.server.slots = threading.BoundedSemaphore(4)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.logs.__exit__(None, None, None)
        self.environment.stop()

    def request(self, payload, token="test-only"):
        request = Request(
            "http://127.0.0.1:" + str(self.server.server_port) + "/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        )
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, response.read().decode()
        except HTTPError as error:
            return error.code, error.read().decode()

    def test_json_completion(self):
        with patch.object(gateway, "generate_answer", return_value=("Closed Monday.", {})):
            status, body = self.request({"messages": [{"role": "user", "content": "Pool hours?"}]})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["choices"][0]["message"]["content"], "Closed Monday.")

    def test_stream_completion(self):
        with patch.object(gateway, "generate_answer", return_value=("Closed Monday.", {})):
            status, body = self.request({"stream": True, "messages": [{"role": "user", "content": "Pool hours?"}]})
        self.assertEqual(status, 200)
        events = [line[6:] for line in body.splitlines() if line.startswith("data: ")]
        self.assertEqual(events[-1], "[DONE]")
        self.assertEqual(json.loads(events[0])["choices"][0]["delta"]["content"], "Closed Monday.")

    def test_unauthorized_request_never_calls_provider(self):
        with patch.object(gateway, "generate_answer") as provider:
            status, _ = self.request({"messages": []}, token="incorrect")
        self.assertEqual(status, 401)
        provider.assert_not_called()

    def test_rejects_non_text_requests(self):
        with patch.object(gateway, "generate_answer") as provider:
            status, _ = self.request({"messages": [{"role": "user", "content": [{"type": "image_url"}]}]})
        self.assertEqual(status, 400)
        provider.assert_not_called()

    def test_provider_errors_do_not_expose_secrets(self):
        with patch.object(gateway, "generate_answer", side_effect=ValueError("test-secret upstream payload")):
            status, body = self.request({"messages": [{"role": "user", "content": "Hello"}]})
        self.assertEqual(status, 502)
        self.assertNotIn("test-secret", body)


if __name__ == "__main__":
    unittest.main()
