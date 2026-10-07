"""Etap 2: logowanie przez Cloudflare Access, role i dostęp do cudzych analiz."""

import asyncio
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from app.api import analysis as analysis_api  # noqa: E402
from app.core import auth, database, deps  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.main import app  # noqa: E402

TEAM = "obsil-test.cloudflareaccess.com"
AUD = "aud-test"
KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
OTHER_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
CASE = "Fikcyjny kazus testowy: radca prowadził sprawę spółki A przeciwko B, teraz B prosi o poradę."


def token(email, key=KEY, aud=AUD, sub=None, expires_in=600):
    claims = {"email": email, "sub": sub or f"sub-{email}", "aud": aud, "iss": f"https://{TEAM}",
              "exp": int(time.time()) + expires_in}
    return jwt.encode(claims, key, algorithm="RS256")


class FakeJwks:
    def get_signing_key_from_jwt(self, _token):
        return SimpleNamespace(key=KEY.public_key())


class AuthAccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        engine = create_async_engine(f"sqlite+aiosqlite:///{self.tmp.name}/test.sqlite3")
        sessions = async_sessionmaker(engine, expire_on_commit=False)
        asyncio.run(self._create_tables(engine))
        self.engine = engine

        async def override_db():
            async with sessions() as session:
                yield session
                await session.commit()

        app.dependency_overrides[deps.get_db] = override_db
        app.dependency_overrides[database.get_db] = override_db
        self.patches = [
            patch.object(settings, "auth_mode", "cloudflare"),
            patch.object(settings, "cf_access_team_domain", TEAM),
            patch.object(settings, "cf_access_aud", AUD),
            patch.object(settings, "operator_email_list", "Operator@Kancelaria.pl"),
            patch.object(auth, "_jwks_client", lambda _team: FakeJwks()),
            patch.object(analysis_api, "_run_orchestrator", self._no_analysis),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        app.dependency_overrides.clear()
        asyncio.run(self.engine.dispose())
        self.tmp.cleanup()

    @staticmethod
    async def _create_tables(engine):
        async with engine.begin() as connection:
            await connection.run_sync(database.Base.metadata.create_all)

    @staticmethod
    async def _no_analysis(*_args):
        return None

    def request(self, method, path, email=None, raw_token=None, **kwargs):
        headers = {}
        if email or raw_token:
            headers["Cf-Access-Jwt-Assertion"] = raw_token or token(email)

        async def run():
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                return await client.request(method, path, headers=headers, **kwargs)
        return asyncio.run(run())

    def test_request_without_valid_token_is_refused(self):
        self.assertEqual(self.request("GET", "/api/v1/history").status_code, 401)
        bad = [token("a@x.pl", key=OTHER_KEY), token("a@x.pl", aud="inna"), token("a@x.pl", expires_in=-60)]
        for raw in bad:
            self.assertEqual(self.request("GET", "/api/v1/history", raw_token=raw).status_code, 401)

    def test_roles_from_operator_list(self):
        self.assertEqual(self.request("GET", "/api/v1/me", "pawel@test.pl").json()["role"], "tester")
        self.assertEqual(self.request("GET", "/api/v1/me", "operator@kancelaria.pl").json()["role"], "operator")

    def test_tester_sees_only_own_analyses(self):
        created = self.request("POST", "/api/v1/analyze", "pawel@test.pl", json={"fact_pattern": CASE})
        self.assertEqual(created.status_code, 202)
        aid = created.json()["id"]

        self.assertEqual(self.request("GET", f"/api/v1/analyze/{aid}", "pawel@test.pl").status_code, 200)
        self.assertEqual(self.request("GET", f"/api/v1/history/{aid}", "pawel@test.pl").status_code, 200)
        self.assertEqual(self.request("GET", "/api/v1/history", "pawel@test.pl").json()["total"], 1)

        other = "inny@test.pl"
        self.assertEqual(self.request("GET", f"/api/v1/analyze/{aid}", other).status_code, 404)
        self.assertEqual(self.request("GET", f"/api/v1/history/{aid}", other).status_code, 404)
        self.assertEqual(self.request("POST", f"/api/v1/analyze/{aid}/clarify", other,
                                      json={"analysis_id": aid, "answers": []}).status_code, 404)
        self.assertEqual(self.request("GET", "/api/v1/history", other).json()["total"], 0)

        operator = "operator@kancelaria.pl"
        self.assertEqual(self.request("GET", f"/api/v1/analyze/{aid}", operator).status_code, 200)
        self.assertEqual(self.request("GET", "/api/v1/history", operator).json()["total"], 1)

    def test_audit_only_for_operator(self):
        self.assertEqual(self.request("GET", "/api/v1/admin/audit", "pawel@test.pl").status_code, 403)
        self.assertEqual(self.request("GET", "/api/v1/admin/audit", "operator@kancelaria.pl").status_code, 200)

    def test_feedback_register(self):
        tester, other, operator = "pawel@test.pl", "inny@test.pl", "operator@kancelaria.pl"
        aid = self.request("POST", "/api/v1/analyze", tester, json={"fact_pattern": CASE}).json()["id"]
        body = {"kind": "podstawa", "description": "Brak odwołania do art. 22 KERP.", "expected": "Konflikt", "source": "WO-134/19"}

        created = self.request("POST", f"/api/v1/analyze/{aid}/feedback", tester, json=body)
        self.assertEqual(created.status_code, 201)
        item = created.json()
        self.assertEqual(item["number"], "U-0001")
        self.assertEqual(item["author_email"], tester)
        self.assertEqual(item["status"], "NOWA")
        self.assertTrue(item["app_version"])

        # Nieznany rodzaj i pusty opis są odrzucane.
        self.assertEqual(self.request("POST", f"/api/v1/analyze/{aid}/feedback", tester,
                                      json={"kind": "xyz", "description": "abcdef"}).status_code, 422)
        self.assertEqual(self.request("POST", f"/api/v1/analyze/{aid}/feedback", tester,
                                      json={"kind": "inne", "description": ""}).status_code, 422)

        # Inny tester nie dopisze uwagi do cudzej analizy ani jej nie zobaczy.
        self.assertEqual(self.request("POST", f"/api/v1/analyze/{aid}/feedback", other, json=body).status_code, 404)
        self.assertEqual(self.request("GET", "/api/v1/feedback", other).json(), [])
        self.assertEqual(len(self.request("GET", "/api/v1/feedback", tester).json()), 1)
        self.assertEqual(len(self.request("GET", f"/api/v1/analyze/{aid}/feedback", tester).json()), 1)

        # Operator widzi wszystko i eksportuje CSV; tester nie eksportuje.
        self.assertEqual(len(self.request("GET", "/api/v1/feedback", operator).json()), 1)
        self.assertEqual(self.request("GET", "/api/v1/feedback/export.csv", tester).status_code, 403)
        export = self.request("GET", "/api/v1/feedback/export.csv", operator)
        self.assertEqual(export.status_code, 200)
        self.assertIn("U-0001;", export.text)
        self.assertIn("WO-134/19", export.text)

    def test_local_mode_needs_no_token_and_is_operator(self):
        with patch.object(settings, "auth_mode", "local"):
            me = self.request("GET", "/api/v1/me")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["role"], "operator")


if __name__ == "__main__":
    unittest.main()
