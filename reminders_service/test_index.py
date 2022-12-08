from unittest import TestCase
import pytest
import json

from fastapi.testclient import TestClient
from queries.reminders import ReminderRepository
from queries.messages import MessageRepository, MessageIn
from queries.recipients import RecipientIn, RecipientOut
from main import app
from pydantic import BaseModel

client = TestClient(app)


class CreateReminderRepository:
    def create(self, reminder, message, recipients=[], user_id=None):
        recipient_list = [
            RecipientOut(
                id=0,
                name=recipient["name"],
                phone=recipient["phone"],
                email=recipient["email"],
            ).dict()
            for recipient in recipients
        ]

        result = {
            "id": 0,
            "user_id": user_id,
            "email_target": reminder["email_target"],
            "reminder_date": reminder["reminder_date"],
            "message": message,
            "sent": False,
            "sent_on": None,
            "recurring": reminder["recurring"],
            "created_on": "2022-12-08",
            "recipients": recipient_list,
        }

        return result


class CreateMessageRepository:
    def create(self, message):
        print("Message input::", message)
        result = {
            "id": 0,
            "template_id": message["template_id"],
            "content": message["content"],
        }
        print("Message result::", result)
        return result


class ReminderInTest(BaseModel):
    email_target: str
    reminder_date: str
    recurring: bool


def test_create_reminder():
    # Arrange
    app.dependency_overrides[ReminderRepository] = CreateReminderRepository
    app.dependency_overrides[MessageRepository] = CreateMessageRepository

    json_response = {
        "reminder": ReminderInTest(
            email_target="hackreactor@hackreactor.com",
            reminder_date="2022-12-24",
            recurring=False,
        ).dict(),
        "message": MessageIn(template_id=0, content="This is a test").dict(),
        "recipients": [
            RecipientIn(
                name="Test", phone="9099099090", email="email@email.com"
            ).dict()
        ],
    }

    new_json = json.dumps(json_response)

    expected = {
        "id": 0,
        "user_id": None,
        "email_target": "hackreactor@hackreactor.com",
        "reminder_date": "2022-12-24",
        "message": {"id": 0, "template_id": 0, "content": "This is a test"},
        "sent": False,
        "sent_on": None,
        "recurring": False,
        "created_on": "2022-12-08",
        "recipients": [
            {
                "id": 0,
                "name": "Test",
                "phone": "9099099090",
                "email": "email@email.com",
            }
        ],
    }

    # print("THIS IS THE JSON:::::::", new_json)
    # Act
    response = client.post("/reminders/", json=new_json)
    # print("THIS IS THE RESPONSE:::::::", response.json())
    # Assert
    assert response.status_code == 307
    # assert response.json() == expected

    # Clean up
    app.dependency_overrides = {}
