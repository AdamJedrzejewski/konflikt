"""Persistence tests for failures before the analysis orchestrator starts."""

import asyncio
from enum import Enum
import importlib.util
import sys
import types
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))


def load_analysis_module():
    """Load the API module with import-time framework/database dependencies stubbed."""
    class AnalysisStatus(str, Enum):
        pending = "pending"
        error = "error"

    class Column:
        def __eq__(self, _other):
            return self

    class Statement:
        def where(self, _condition):
            return self

    class Router:
        def __init__(self, *_args, **_kwargs):
            pass

        def post(self, *_args, **_kwargs):
            return lambda function: function

        def get(self, *_args, **_kwargs):
            return lambda function: function

    class Analysis:
        id = Column()

    class AnalysisOrchestrator:
        @staticmethod
        def _build_error_fallback(exc, _extraction):
            return {
                "conflict_classification": "UNKNOWN",
                "risk_level": "nieznane",
                "confidence_level": "niski",
                "source": "error_fallback",
                "mode": "error_fallback",
                "error": {"type": type(exc).__name__, "message": str(exc)},
            }

    def make_module(name, **attributes):
        result = types.ModuleType(name)
        result.__dict__.update(attributes)
        result.__path__ = []
        return result

    fastapi = make_module(
        "fastapi",
        APIRouter=Router,
        BackgroundTasks=type("BackgroundTasks", (), {}),
        Depends=lambda dependency: dependency,
        HTTPException=type("HTTPException", (Exception,), {}),
    )
    sqlalchemy = make_module("sqlalchemy", select=lambda _model: Statement())
    sqlalchemy_async = make_module("sqlalchemy.ext.asyncio", AsyncSession=type("AsyncSession", (), {}))
    sqlalchemy_ext = make_module("sqlalchemy.ext")
    database = make_module("app.core.database", get_db=lambda: None, AsyncSessionLocal=None)
    adapters = make_module("app.adapters.llm_adapter", create_adapter=lambda: None)
    db_models = make_module(
        "app.models.db_models",
        Analysis=Analysis,
        AnalysisStatus=AnalysisStatus,
        Clarification=type("Clarification", (), {}),
    )
    schemas = make_module(
        "app.models.schemas",
        AnalysisCreateRequest=type("AnalysisCreateRequest", (), {}),
        AnalysisResponse=type("AnalysisResponse", (), {}),
        ClarificationAnswerRequest=type("ClarificationAnswerRequest", (), {}),
    )
    auth = make_module(
        "app.core.auth",
        CurrentUser=type("CurrentUser", (), {}),
        get_current_user=lambda: None,
        get_owned_analysis=lambda *_args: None,
    )
    rules = make_module("app.rules.engine", RuleEngine=type("RuleEngine", (), {}))
    orchestrator = make_module("app.services.orchestrator", AnalysisOrchestrator=AnalysisOrchestrator)
    replacements = {
        "fastapi": fastapi,
        "sqlalchemy": sqlalchemy,
        "sqlalchemy.ext": sqlalchemy_ext,
        "sqlalchemy.ext.asyncio": sqlalchemy_async,
        "app.core.database": database,
        "app.core.auth": auth,
        "app.adapters.llm_adapter": adapters,
        "app.models.db_models": db_models,
        "app.models.schemas": schemas,
        "app.rules.engine": rules,
        "app.services.orchestrator": orchestrator,
    }
    missing = object()
    previous = {name: sys.modules.get(name, missing) for name in replacements}
    sys.modules.update(replacements)
    try:
        source = Path(__file__).resolve().parents[1] / "backend" / "app" / "api" / "analysis.py"
        spec = importlib.util.spec_from_file_location("analysis_api_under_test", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        for name, old_module in previous.items():
            if old_module is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old_module
    return module, AnalysisStatus, database


analysis_api, AnalysisStatus, database_module = load_analysis_module()


class FakeResult:
    def __init__(self, analysis):
        self.analysis = analysis

    def scalar_one_or_none(self):
        return self.analysis


class FakeDatabase:
    def __init__(self, analysis, commit_error=None):
        self.analysis = analysis
        self.commit_error = commit_error
        self.commit_calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def execute(self, _statement):
        return FakeResult(self.analysis)

    async def commit(self):
        self.commit_calls += 1
        if self.commit_error:
            raise self.commit_error


class AnalysisStartFailureTests(unittest.TestCase):
    def make_analysis(self):
        return SimpleNamespace(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            status=AnalysisStatus.pending,
            final_result=None,
            conflict_classification=None,
            risk_level=None,
            confidence_level=None,
        )

    def test_adapter_factory_failure_is_persisted_as_error(self):
        analysis = self.make_analysis()
        db = FakeDatabase(analysis)
        database_module.AsyncSessionLocal = lambda: db

        with (
            patch.dict(sys.modules, {"app.core.database": database_module}),
            patch.object(analysis_api, "create_adapter", side_effect=RuntimeError("adapter unavailable")),
        ):
            asyncio.run(analysis_api._run_orchestrator(analysis.id, "synthetic fact pattern"))

        self.assertEqual(db.commit_calls, 1)
        self.assertEqual(analysis.status, AnalysisStatus.error)
        self.assertIsInstance(analysis.final_result, dict)
        self.assertEqual(analysis.final_result["mode"], "error_fallback")
        self.assertEqual(analysis.final_result["conflict_classification"], "UNKNOWN")
        self.assertNotEqual(analysis.final_result["conflict_classification"], "NO_CONFLICT")
        self.assertEqual(analysis.final_result["error"]["type"], "RuntimeError")

    def test_failure_to_persist_start_error_is_propagated(self):
        analysis = self.make_analysis()
        db = FakeDatabase(analysis, commit_error=OSError("sqlite write failed"))
        database_module.AsyncSessionLocal = lambda: db

        with (
            patch.dict(sys.modules, {"app.core.database": database_module}),
            patch.object(analysis_api, "create_adapter", side_effect=RuntimeError("adapter unavailable")),
        ):
            with self.assertRaisesRegex(OSError, "sqlite write failed"):
                asyncio.run(analysis_api._run_orchestrator(analysis.id, "synthetic fact pattern"))


if __name__ == "__main__":
    unittest.main()
