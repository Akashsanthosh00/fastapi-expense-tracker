import os
import pytest

from alembic.config import Config
from alembic import command

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.database import Base, get_db
from backend.app.main import app
from fastapi.testclient import TestClient


load_dotenv(".env")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not configured")

alembic_cfg = Config("backend/alembic.ini")
alembic_cfg.set_main_option(
    "sqlalchemy.url",
    TEST_DATABASE_URL.replace("%", "%%"),
)

command.upgrade(alembic_cfg, "head")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())

    db.commit()
    db.close()

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)