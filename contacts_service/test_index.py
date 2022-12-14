from fastapi.testclient import TestClient
from queries.contacts import ContactsRepository
from main import app
from routers.contacts import authenticator

client = TestClient(app)


class CreateContactRepository:
    def create(self, user_id, contact, special_days):
        return {
            "id": 0,
            "user_id": user_id,
            "recipient": {
                "id": 0,
                "name": "string",
                "phone": "string",
                "email": "string",
            },
            "special_days": special_days,
            "notes": contact.notes,
        }


def test_create_reminder():
    # Arrange
    acc = {
        "id": "12345",
    }

    app.dependency_overrides[ContactsRepository] = CreateContactRepository
    app.dependency_overrides[
        authenticator.try_get_current_account_data
    ] = lambda: acc

    json = {
        "contact": {"recipient_id": 0, "notes": "string"},
        "special_days": [],
    }

    expected = {
        "id": 0,
        "user_id": 12345,  # what id is in the acc defined above
        "recipient": {
            "id": 0,
            "name": "string",
            "phone": "string",
            "email": "string",
        },
        "special_days": [],
        "notes": "string",
    }

    headers = {"Authorization": "Bearer z1232131"}

    # Act
    response = client.post("/contacts", json=json, headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected

    # Clean up
    app.dependency_overrides = {}
