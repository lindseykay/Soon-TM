from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.reminders import (
    ReminderIn,
    ReminderOut,
    ReminderRepository
)
from queries.recipients import RecipientIn
from queries.messages import MessageIn, MessageRepository
from queries.error import Error

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
    if new_message == None or new_message == {"message": "create message record failed"}:
        response.status_code = 400
    new_reminder = reminder_repo.create(reminder, new_message, recipients, user_id)
    if new_reminder == None or new_reminder == {"message": "create reminder record failed"}:
        response.status_code = 400
    return new_reminder


@router.get("/reminders", response_model= Union[List[ReminderOut], Error])
def get_all(
    user_id: int,
    response: Response,
    repo: ReminderRepository = Depends()
):
    reminders = repo.get_all(user_id)
    if reminders == None or reminders == {"message": "get_all reminder records failed"}:
        response.status_code = 400
    return reminders
