from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.reminders import (
    RecipientIn,
    RecipientOut,
    MessageIn,
    MessageOut,
    ReminderIn,
    ReminderOut,
    ReminderRepository,
    MessageRepository
)

router = APIRouter()

@router.post("/reminders")
def create_reminder(
    reminder: ReminderIn,
    message: MessageIn,
    response: Response,
    reminder_repo: ReminderRepository = Depends(),
    message_repo: MessageRepository = Depends(),
    user_id = None):
    print(user_id)
    new_message = message_repo.create(message)
    if new_message == None or new_message == {"message": "No good"}:
        response.status_code = 400
    new_reminder = reminder_repo.create(reminder, new_message, user_id)
    if new_reminder == None or new_reminder == {"message": "No good"}:
        response.status_code = 400
    return new_reminder