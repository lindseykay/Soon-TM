from unittest import TestCase
import pytest

from fastapi.testclient import TestClient
from queries.users import UserIn, UserRepository
from main import app


client = TestClient(app)


class CreateUserRepository:
    def create(self, user, password=None):
        result = {
            "access_token": "abc",
            "token_type": "Bearer",
            "account": {"id": 21},
        }
        result["account"].update(user)
        result["account"].pop("password")
        return result


def test_create_user():
    # Arrange
    app.dependency_overrides[UserRepository] = CreateUserRepository

    json = UserIn(
        username="CeyF15adHSC4BWoWAQs5wEuM1jaSAwC9",
        password="hack",
        email="hacker@hack.com",
        name="hacker",
    ).dict()

    expected = {
        "access_token": "abc",
        "token_type": "Bearer",
        "account": {
            "id": 21,
            "username": "CeyF15adHSC4BWoWAQs5wEuM1jaSAwC9",
            "email": "hacker@hack.com",
            "name": "hacker",
        },
    }

    # Act
    response = client.post("/users/", json=json)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected

    # Clean up
    app.dependency_overrides = {}
