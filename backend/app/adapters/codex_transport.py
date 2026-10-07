"""Local Codex App Server client. Authentication remains owned by Codex."""
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time


class CodexError(RuntimeError):
    pass


def codex_command(configured: str = "") -> list[str]:
    path = configured or shutil.which("codex.exe") or shutil.which("codex") or shutil.which("codex.cmd")
    if not path:
        raise CodexError("Nie znaleziono Codexa. Zainstaluj Codex CLI i wykonaj codex login.")
    path = Path(path).resolve()
    if path.suffix.lower() in (".cmd", ".ps1"):
        # Avoid cmd.exe and shell quoting entirely on Windows.
        binary = list((path.parent / "node_modules/@openai/codex").glob("node_modules/@openai/codex-win32-*/vendor/*/bin/codex.exe"))
        if len(binary) != 1:
            raise CodexError("Ustaw CODEX_EXECUTABLE na pełną ścieżkę do codex.exe.")
        return [str(binary[0])]
    return [str(path)]


class CodexSession:
    """One process/connection per request; no shared conversational state."""
    def __init__(self, executable="", timeout=300):
        self.command = codex_command(executable)
        self.timeout = timeout
        self.process = None
        self.messages = queue.Queue()
        self.sequence = 0

    def __enter__(self):
        self.deadline = time.monotonic() + self.timeout
        self.directory = tempfile.TemporaryDirectory(prefix="obsil-codex-")
        command = self.command + ["app-server", "--stdio"]
        for key, value in {
            "forced_login_method": '"chatgpt"', "model_provider": '"openai"',
            "approval_policy": '"never"', "sandbox_mode": '"read-only"',
            "web_search": '"disabled"', "project_doc_max_bytes": "0",
            "features.shell_tool": "false", "features.unified_exec": "false",
            "features.multi_agent": "false", "features.hooks": "false",
            "features.memories": "false", "features.apps": "false",
            "apps._default.enabled": "false",
        }.items():
            command += ["-c", f"{key}={value}"]
        env = os.environ.copy()
        for name in ("OPENAI_API_KEY", "CODEX_API_KEY"):
            env.pop(name, None)
        try:
            self.process = subprocess.Popen(command, cwd=self.directory.name, env=env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, encoding="utf-8", bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            self.reader = threading.Thread(target=self._read, daemon=True)
            self.reader.start()
            self.rpc("initialize", {"clientInfo": {"name": "obsil_local", "version": "0.1.0"}})
            self.send({"method": "initialized", "params": {}})
            account = self.rpc("account/read", {"refreshToken": False}).get("account") or {}
            if account.get("type") != "chatgpt":
                raise CodexError("OBSIL wymaga logowania Codexa przez ChatGPT. Wykonaj codex login; nie używaj klucza API.")
            self.plan = account.get("planType")
            return self
        except BaseException:
            self.close()
            raise

    def _read(self):
        try:
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except json.JSONDecodeError:
                    self.messages.put(CodexError("Nieprawidłowy komunikat lokalnego Codexa."))
        finally:
            self.messages.put(CodexError("Codex zakończył połączenie. Sprawdź lokalne logowanie i konfigurację."))

    def send(self, message):
        self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

    def receive(self):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise CodexError("Przekroczono czas oczekiwania na model. Wynik nie został ustalony.")
        try:
            message = self.messages.get(timeout=remaining)
        except queue.Empty:
            raise CodexError("Przekroczono czas oczekiwania na model. Wynik nie został ustalony.") from None
        if isinstance(message, Exception):
            raise message
        if "id" in message and "method" in message:
            # The analysis bridge does not perform tool actions or grant permissions.
            self.send({"id": message["id"], "error": {"code": -32601, "message": "OBSIL does not execute tools or approve actions"}})
            raise CodexError("Model zażądał niedostępnej czynności. Analiza została przerwana.")
        return message

    def rpc(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self.send({"id": request_id, "method": method, "params": params})
        while True:
            message = self.receive()
            if message.get("id") == request_id:
                if "error" in message:
                    raise CodexError(f"Codex odrzucił {method}: {message['error'].get('message', 'błąd protokołu')}")
                if "result" not in message:
                    raise CodexError("Niepełna odpowiedź protokołu Codexa.")
                return message["result"]

    def models(self):
        result = self.rpc("model/list", {"limit": 100})
        return [{"id": m.get("model", m.get("id")), "default": m.get("isDefault", False)} for m in result["data"]]

    def complete(self, instruction, prompt, schema, model, effort="medium"):
        # Read only names to disable any locally configured MCP servers for this thread.
        config = self.rpc("config/read", {"includeLayers": False}).get("config", {})
        overrides = {f"mcp_servers.{name}.enabled": False for name in (config.get("mcp_servers") or {})}
        for name in (config.get("plugins") or {}):
            overrides[f"plugins.{name}.enabled"] = False
        start = self.rpc("thread/start", {
            "model": model, "modelProvider": "openai", "cwd": self.directory.name,
            "approvalPolicy": "never", "sandbox": "read-only", "ephemeral": True,
            "baseInstructions": "You are the OBSIL text analysis engine. Answer only from the supplied input. Do not call tools, access files, browse, or perform actions. Return the requested JSON object.",
            "developerInstructions": instruction, "config": overrides,
        })
        thread_id = start["thread"]["id"]
        self.send({"id": self.sequence + 1, "method": "turn/start", "params": {
            "threadId": thread_id, "input": [{"type": "text", "text": prompt}],
            "model": model, "effort": effort, "outputSchema": schema,
            "sandboxPolicy": {"type": "readOnly"},
        }})
        texts = {}
        usage = None
        while True:
            message = self.receive()
            if "error" in message:
                raise CodexError("Codex nie rozpoczął analizy: " + str(message["error"].get("message", "")))
            method = message.get("method")
            params = message.get("params", {})
            if method == "item/completed":
                item = params["item"]
                if item.get("type") == "agentMessage":
                    texts[item["id"]] = item.get("text", "")
                elif item.get("type") not in ("userMessage", "reasoning", "plan"):
                    raise CodexError("Niedozwolona czynność modelu w analizie tekstowej; wynik odrzucony.")
            if method == "thread/tokenUsage/updated":
                usage = params.get("tokenUsage")
            if method == "turn/completed":
                turn = params["turn"]
                if turn.get("status") != "completed":
                    raise CodexError("Model nie ukończył analizy: " + str((turn.get("error") or {}).get("message", turn.get("status"))))
                if not texts:
                    raise CodexError("Model zakończył bez odpowiedzi. Nie ustalono wyniku.")
                try:
                    parsed = json.loads(list(texts.values())[-1])
                except json.JSONDecodeError:
                    raise CodexError("Odpowiedź modelu nie jest poprawnym JSON; wynik odrzucony.") from None
                return parsed, {"provider": "codex_chatgpt", "model": start["model"],
                    "authentication": "chatgpt", "plan": self.plan, "token_usage": usage}

    def close(self):
        if self.process:
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=5)
            for stream in (self.process.stdin, self.process.stdout):
                if stream:
                    stream.close()
        if hasattr(self, "directory"):
            self.directory.cleanup()

    def __exit__(self, *args):
        self.close()
