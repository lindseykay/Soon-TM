from fastapi import APIRouter, Depends, Response
from typing import Union
from queries.messages import MessageIn, MessageRepository
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
