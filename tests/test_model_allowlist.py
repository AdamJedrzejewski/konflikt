"""Model limit: the adapter factory refuses models outside LLM_ALLOWED_MODELS."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from app.adapters.llm_adapter import create_adapter  # noqa: E402
from app.core.config import settings  # noqa: E402


class ModelAllowlistTests(unittest.TestCase):
    def test_model_outside_list_is_refused(self):
        with patch.object(settings, "llm_model_name", "gpt-6-astra"), \
                patch.object(settings, "llm_allowed_models", "gpt-6-luna"):
            with self.assertRaisesRegex(ValueError, "nie jest dozwolony"):
                create_adapter("codex_chatgpt")

    def test_model_on_list_is_accepted(self):
        with patch.object(settings, "llm_model_name", "gpt-6-luna"), \
                patch.object(settings, "llm_allowed_models", " gpt-6-luna , gpt-6-mini "):
            self.assertEqual(create_adapter("codex_chatgpt").model, "gpt-6-luna")

    def test_empty_list_means_no_limit(self):
        with patch.object(settings, "llm_model_name", "gpt-6-astra"), \
                patch.object(settings, "llm_allowed_models", ""):
            self.assertEqual(create_adapter("codex_chatgpt").model, "gpt-6-astra")


if __name__ == "__main__":
    unittest.main()
