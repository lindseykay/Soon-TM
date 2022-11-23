from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.reminders import ReminderIn, ReminderOut, ReminderUpdate, ReminderRepository
from queries.recipients import RecipientIn, RecipientOut, RecipientRepository
from queries.messages import MessageIn, MessageOut, MessageRepository
from queries.error import Error

router = APIRouter()


@router.put("/recipients", response_model=Union[List[RecipientOut], Error])
def update_recipients(
    reminder_id: int,
    user_id: int,
    recipients: List[RecipientOut],
    response: Response,
    repo: RecipientRepository = Depends()):
    recipient_list = []
    for recipient in recipients:
        updated_recipient = repo.update(user_id, reminder_id, recipient)
        recipient_list.append(updated_recipient)
    return recipient_list

@router.post("/recipients", response_model=Union[int, Error])
def create(
    user_id: int,
    recipient: RecipientIn,
    response: Response,
    repo: RecipientRepository = Depends()):
    return repo.create(user_id, recipient).id

@router.get("/recipients", response_model=Union[List[RecipientOut], Error])
def get_all_by_user(
    user_id: int,
    response: Response,
    repo: RecipientRepository = Depends()):
    return repo.get_all_by_user(user_id)