"""
Shared pytest setup for the backend tests.

Two things happen here, and the order matters:

1. PERSONAL_LLM_DB is pointed at an in-memory SQLite database BEFORE any
   backend module is imported. backend/db/__init__.py builds the connection
   from that variable at import time, so this guard is what keeps the tests
   away from the real storage/app/data.db. Nothing is written to disk, so
   there is nothing to clean up.

2. The `fresh_db` fixture below runs automatically for every test and gives it
   its own brand-new, empty database file under pytest's tmp_path.
"""
import os

os.environ["PERSONAL_LLM_DB"] = ":memory:"

import pytest  # noqa: E402  (must come after the environment guard above)

from db import db_instance  # noqa: E402
from db.utils import setup as db_setup  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db(tmp_path):
    """Give every test an empty database of its own."""
    db_instance.init(str(tmp_path / "test.db"))
    db_setup()  # same function main.py uses: connect + create tables
    yield db_instance
    db_instance.close()
