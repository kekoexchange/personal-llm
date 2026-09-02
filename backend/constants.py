import os
from pathlib import Path

# Anchor defaults to the repo root (this file's parent's parent) so they
# resolve the same from any working directory. PERSONAL_LLM_* env vars
# override them.
REPO_ROOT = Path(__file__).resolve().parent.parent

DB_FILE_PATH = os.environ.get("PERSONAL_LLM_DB", str(REPO_ROOT / "storage" / "app" / "data.db"))
LLM_MODEL = os.environ.get("PERSONAL_LLM_MODEL", "gemma3:270m")
LLM_SYSTEM_PROMPT = """
    You are a friendly chatbot. 
    You are helpful, kind, honest, and good at writing. 
    You do not repeat yourself. 
    You keep it short unless instructed otherwise.
    """

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"

FRONTEND_FOLDER = "frontend"
FRONTEND_INDEX_PAGE = "index.html"