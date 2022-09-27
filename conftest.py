import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app import token_listener

from app import app as application


async def generate_dummy_auth():
    pass


'''Sets up testing environment. Overrides the JWTBearer dependency such that token authentication is bypassed for
specific endpoints and dummy data is provided.
'''


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {token_listener: generate_dummy_auth}
    return application


'''Sets up the Test Client for initiating requests within the application.
'''


@pytest.fixture
def client(app) -> TestClient:
    with TestClient(app=app, base_url="http://localhost:8080/") as client:
        yield client
