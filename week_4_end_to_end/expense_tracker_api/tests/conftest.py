import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_expenses.db")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models import Category, User

test_db_url = "sqlite:///./test_expenses.db"

test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    default_user = User(username="testuser", email="testuser@example.com")
    session.add(default_user)
    session.flush()

    seed_categories = [
        Category(category_name="Food"),
        Category(category_name="Transport"),
        Category(category_name="Subscriptions"),
        Category(category_name="Entertainment"),
    ]
    session.add_all(seed_categories)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client

    app.dependency_overrides.clear()
