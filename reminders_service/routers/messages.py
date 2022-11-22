from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.reminders import ReminderIn, ReminderOut, ReminderUpdate, ReminderRepository
from queries.recipients import RecipientIn, RecipientOut, RecipientRepository
from queries.messages import MessageIn, MessageOut, MessageRepository
from queries.error import Error

router = APIRouter()


@router.put("/reminders/{reminder_id}/messages", response_model=Union[MessageIn, Error])
def update_message(
    user_id: int,
    reminder_id: int,
    message: MessageIn,
    response: Response,
    repo: MessageRepository = Depends()):
    return repo.update(user_id, reminder_id, message)
