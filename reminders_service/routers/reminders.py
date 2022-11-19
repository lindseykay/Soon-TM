from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.reminders import (
    MessageIn,
    MessageOut,
    ReminderIn,
    ReminderOut,
    ReminderRepository,
    MessageRepository,
    Error,
)
from queries.recipients import RecipientIn

router = APIRouter()

@router.post("/reminders", response_model= Union[ReminderOut, Error])
def create_reminder(
    reminder: ReminderIn,
    message: MessageIn,
    recipients: List[RecipientIn],
    response: Response,
    reminder_repo: ReminderRepository = Depends(),
    message_repo: MessageRepository = Depends(),
    user_id = None):
    new_message = message_repo.create(message)
    if new_message == None or new_message == {"message": "No good"}:
        response.status_code = 400
    new_reminder = reminder_repo.create(reminder, new_message, recipients, user_id)
    if new_reminder == None or new_reminder == {"message": "No good"}:
        response.status_code = 400
    return new_reminder


@router.get("/reminders", response_model= Union[List[ReminderOut], Error])
def get_all(
    user_id: int,
    response: Response,
    repo: ReminderRepository = Depends()
):
    return repo.get_all(user_id)
