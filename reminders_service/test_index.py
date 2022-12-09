from fastapi.testclient import TestClient
from queries.reminders import ReminderRepository
from queries.messages import MessageRepository
from queries.recipients import RecipientOut, RecipientRepository
from main import app
from pydantic import BaseModel
from routers.reminders import authenticator

client = TestClient(app)


class ReminderInTest(BaseModel):
    email_target: str
    reminder_date: str
    recurring: bool


class CreateMessageRepository:
    def create(self, message):
        print("Message input::", type(message))
        result = {
            "id": 0,
            "template_id": message.template_id,
            "content": message.content,
        }
        print("Message result::", result)
        return result


class CreateReminderRepository:
    def create(self, reminder, message, recipients=[], user_id=None):
        recipient_list = [
            RecipientOut(
                id=0,
                name=recipient.name,
                phone=recipient.phone,
                email=recipient.email,
            ).dict()
            for recipient in recipients
        ]

        result = {
            "id": 0,
            "user_id": user_id,
            "email_target": reminder.email_target,
            "reminder_date": reminder.reminder_date,
            "message": message,
            "sent": False,
            "sent_on": None,
            "recurring": reminder.recurring,
            "created_on": "2022-12-08",
            "recipients": recipient_list,
        }

        return result


def test_create_reminder():
    # Arrange
    app.dependency_overrides[ReminderRepository] = CreateReminderRepository
    app.dependency_overrides[MessageRepository] = CreateMessageRepository

    new_json = {
        "reminder": {
            "email_target": "hackreactor@hackreactor.com",
            "reminder_date": "2022-12-24",
            "recurring": False,
        },
        "message": {"template_id": 0, "content": "This is a test"},
        "recipients": [
            {
                "name": "Test",
                "phone": "9099099090",
                "email": "email@email.com",
                "user_id": 0,
            }
        ],
    }

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

    # Act
    response = client.post("/reminders", json=new_json)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected

    # Clean up
    app.dependency_overrides = {}


----get recipient test---

class EmptyRecipientRepository:
    def get_all_by_user(self, user_id):
        return []

def test_get_all_recipients_by_user():
    fake_account_data = {
        "id": 8,
        "username": "string",
        "email": "string",
        "name": "string"
    }
    app.dependency_overrides[RecipientRepository] = EmptyRecipientRepository
    app.dependency_overrides[authenticator.try_get_current_account_data] = lambda: fake_account_data

    response = client.get("/recipients", cookies={authenticator.cookie_name: "HELLO!"})
    assert response.status_code == 401
    assert response.json() == {}

    app.dependency_overrides = {}
