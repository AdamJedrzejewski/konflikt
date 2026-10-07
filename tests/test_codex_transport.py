"""Mock-only tests for the local Codex App Server transport."""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from app.adapters import codex_transport  # noqa: E402


def rpc_result(request_id, result):
    return {"id": request_id, "result": result}


class FakeStdout:
    def __init__(self, lines):
        self.lines = lines
        self.closed = False

    def __iter__(self):
        return iter(self.lines)

    def close(self):
        self.closed = True


class FakeStdin:
    def __init__(self):
        self.buffer = []
        self.closed = False

    def write(self, value):
        self.buffer.append(value)

    def flush(self):
        pass

    def close(self):
        self.closed = True

    def messages(self):
        return [json.loads(line) for line in self.buffer]


class FakeProcess:
    def __init__(self, messages):
        lines = [json.dumps(message) for message in messages]
        self.stdout = FakeStdout(lines)
        self.stdin = FakeStdin()
        self.return_code = None
        self.terminated = False
        self.killed = False
        self.wait_calls = []
        self.raise_first_wait_timeout = False

    def poll(self):
        return self.return_code

    def terminate(self):
        self.terminated = True
        self.return_code = -15

    def kill(self):
        self.killed = True
        self.return_code = -9

    def wait(self, timeout=None):
        self.wait_calls.append(timeout)
        if self.raise_first_wait_timeout and len(self.wait_calls) == 1:
            raise subprocess.TimeoutExpired("codex-test", timeout)
        return self.return_code


class CodexTransportTests(unittest.TestCase):
    def install_process(self, messages):
        process = FakeProcess(messages)
        command_patch = patch.object(codex_transport, "codex_command", return_value=["codex-test"])
        popen_patch = patch.object(codex_transport.subprocess, "Popen", return_value=process)
        command_patch.start()
        popen_patch.start()
        self.addCleanup(command_patch.stop)
        self.addCleanup(popen_patch.stop)
        return process

    @staticmethod
    def handshake(account_type="chatgpt", following=()):
        return [
            rpc_result(1, {"protocolVersion": "test"}),
            rpc_result(2, {"account": {"type": account_type, "planType": "plus"}}),
            *following,
        ]

    def test_complete_parses_json_and_starts_isolated_model_turn(self):
        answer = {"classification": "synthetic"}
        messages = self.handshake(
            following=[
                rpc_result(3, {"config": {
                    "mcp_servers": {"local-server": {}},
                    "plugins": {"local-plugin": {}},
                }}),
                rpc_result(4, {"thread": {"id": "thread-1"}, "model": "gpt-6-astra"}),
                rpc_result(5, {}),
                {"method": "item/completed", "params": {
                    "item": {"id": "answer-1", "type": "agentMessage", "text": json.dumps(answer)},
                }},
                {"method": "turn/completed", "params": {"turn": {"status": "completed"}}},
            ]
        )
        process = self.install_process(messages)

        with codex_transport.CodexSession("codex-test", timeout=3) as session:
            temp_cwd = session.directory.name
            result, metadata = session.complete(
                "instruction", "synthetic prompt", {"type": "object"}, "gpt-6-astra", "high"
            )
            self.assertEqual(result, answer)
            self.assertEqual(metadata["authentication"], "chatgpt")
            self.assertEqual(metadata["model"], "gpt-6-astra")
            self.assertEqual(metadata["plan"], "plus")

        requests = process.stdin.messages()
        thread_start = next(m for m in requests if m.get("method") == "thread/start")
        turn_start = next(m for m in requests if m.get("method") == "turn/start")
        self.assertEqual(thread_start["params"]["cwd"], temp_cwd)
        self.assertTrue(thread_start["params"]["ephemeral"])
        self.assertEqual(thread_start["params"]["sandbox"], "read-only")
        self.assertFalse(thread_start["params"]["config"]["mcp_servers.local-server.enabled"])
        self.assertFalse(thread_start["params"]["config"]["plugins.local-plugin.enabled"])
        self.assertEqual(turn_start["params"]["model"], "gpt-6-astra")
        self.assertEqual(turn_start["params"]["effort"], "high")
        self.assertEqual(turn_start["params"]["sandboxPolicy"], {
            "type": "readOnly",
        })
        self.assertTrue(process.terminated)
        self.assertTrue(process.stdin.closed)
        self.assertTrue(process.stdout.closed)
        self.assertFalse(Path(temp_cwd).exists())

    def test_rpc_server_error_is_reported_and_process_is_cleaned_up(self):
        process = self.install_process([{"id": 1, "error": {"message": "protocol failure"}}])
        session = codex_transport.CodexSession("codex-test", timeout=3)

        with self.assertRaisesRegex(codex_transport.CodexError, "initialize.*protocol failure"):
            session.__enter__()

        self.assertTrue(process.terminated)
        self.assertFalse(Path(session.directory.name).exists())

    def test_incomplete_rpc_response_is_reported_and_process_is_cleaned_up(self):
        process = self.install_process([{"id": 1}])
        session = codex_transport.CodexSession("codex-test", timeout=3)

        with self.assertRaisesRegex(codex_transport.CodexError, "Niepełna odpowiedź protokołu"):
            session.__enter__()

        self.assertTrue(process.terminated)
        self.assertFalse(Path(session.directory.name).exists())

    def test_non_chatgpt_account_is_refused_and_cleaned_up(self):
        process = self.install_process(self.handshake(account_type="apiKey"))
        session = codex_transport.CodexSession("codex-test", timeout=3)

        with self.assertRaisesRegex(codex_transport.CodexError, "wymaga logowania Codexa przez ChatGPT"):
            session.__enter__()

        self.assertTrue(process.terminated)
        self.assertFalse(Path(session.directory.name).exists())

    def test_server_tool_request_is_denied(self):
        tool_request = {"id": "tool-1", "method": "item/commandExecution/requestApproval", "params": {}}
        process = self.install_process(self.handshake(following=[tool_request]))

        with codex_transport.CodexSession("codex-test", timeout=3) as session:
            with self.assertRaisesRegex(codex_transport.CodexError, "niedostępnej czynności"):
                session.receive()

        denial = next(m for m in process.stdin.messages() if m.get("id") == "tool-1")
        self.assertEqual(denial["error"]["code"], -32601)
        self.assertTrue(process.terminated)

    def test_missing_response_times_out_and_context_cleans_up(self):
        process = self.install_process(self.handshake())
        temp_cwd = None

        with codex_transport.CodexSession("codex-test", timeout=3) as session:
            temp_cwd = session.directory.name
            session.deadline = 0
            with self.assertRaisesRegex(codex_transport.CodexError, "czas oczekiwania"):
                session.receive()

        self.assertTrue(process.terminated)
        self.assertFalse(Path(temp_cwd).exists())

    def test_invalid_completed_json_is_rejected_and_context_cleans_up(self):
        messages = self.handshake(following=[
            rpc_result(3, {"config": {}}),
            rpc_result(4, {"thread": {"id": "thread-1"}, "model": "gpt-6-astra"}),
            rpc_result(5, {}),
            {"method": "item/completed", "params": {
                "item": {"id": "answer-1", "type": "agentMessage", "text": "not-json"},
            }},
            {"method": "turn/completed", "params": {"turn": {"status": "completed"}}},
        ])
        process = self.install_process(messages)
        temp_cwd = None

        with self.assertRaisesRegex(codex_transport.CodexError, "nie jest poprawnym JSON"):
            with codex_transport.CodexSession("codex-test", timeout=3) as session:
                temp_cwd = session.directory.name
                session.complete("instruction", "prompt", {"type": "object"}, "gpt-6-astra")

        self.assertTrue(process.terminated)
        self.assertFalse(Path(temp_cwd).exists())

    def test_completed_turn_without_agent_message_is_rejected(self):
        messages = self.handshake(following=[
            rpc_result(3, {"config": {}}),
            rpc_result(4, {"thread": {"id": "thread-1"}, "model": "gpt-6-astra"}),
            rpc_result(5, {}),
            {"method": "turn/completed", "params": {"turn": {"status": "completed"}}},
        ])
        process = self.install_process(messages)
        temp_cwd = None

        with self.assertRaisesRegex(codex_transport.CodexError, "bez odpowiedzi"):
            with codex_transport.CodexSession("codex-test", timeout=3) as session:
                temp_cwd = session.directory.name
                session.complete("instruction", "prompt", {"type": "object"}, "gpt-6-astra")

        self.assertTrue(process.terminated)
        self.assertFalse(Path(temp_cwd).exists())

    def test_cleanup_kills_process_after_terminate_timeout(self):
        process = self.install_process(self.handshake())
        process.raise_first_wait_timeout = True
        temp_cwd = None

        with codex_transport.CodexSession("codex-test", timeout=3) as session:
            temp_cwd = session.directory.name

        self.assertTrue(process.terminated)
        self.assertTrue(process.killed)
        self.assertEqual(process.wait_calls, [5, 5])
        self.assertFalse(Path(temp_cwd).exists())


if __name__ == "__main__":
    unittest.main()
