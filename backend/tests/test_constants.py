"""constants.py reads its settings from PERSONAL_LLM_* environment variables."""
import importlib
from pathlib import Path

import pytest

import constants


@pytest.fixture
def reload_constants(monkeypatch):
    """Return a helper that sets env vars and re-imports constants.

    After the test, the env vars are undone and constants is reloaded again so
    other tests see the normal values.
    """
    def _reload(**env):
        for key, value in env.items():
            if value is None:
                monkeypatch.delenv(key, raising=False)
            else:
                monkeypatch.setenv(key, value)
        return importlib.reload(constants)

    yield _reload
    monkeypatch.undo()
    importlib.reload(constants)


def test_model_defaults_to_gemma(reload_constants):
    reloaded = reload_constants(PERSONAL_LLM_MODEL=None)
    assert reloaded.LLM_MODEL == "gemma3:270m"


def test_model_can_be_overridden_by_env(reload_constants):
    reloaded = reload_constants(PERSONAL_LLM_MODEL="llama3")
    assert reloaded.LLM_MODEL == "llama3"


def test_db_path_defaults_to_storage_under_repo_root(reload_constants):
    reloaded = reload_constants(PERSONAL_LLM_DB=None)
    # this file lives at <repo>/backend/tests/, so work the root out from here
    # rather than trusting constants.REPO_ROOT to be right
    repo_root = Path(__file__).resolve().parents[2]
    assert reloaded.DB_FILE_PATH == str(repo_root / "storage" / "app" / "data.db")


def test_db_path_can_be_overridden_by_env(reload_constants, tmp_path):
    reloaded = reload_constants(PERSONAL_LLM_DB=str(tmp_path / "elsewhere.db"))
    assert reloaded.DB_FILE_PATH == str(tmp_path / "elsewhere.db")

