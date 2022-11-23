from fastapi import APIRouter, Depends, Response
from typing import List, Union
from queries.reminders import ReminderIn, ReminderOut, ReminderUpdate, ReminderRepository
from queries.recipients import RecipientIn
from queries.messages import MessageIn, MessageRepository
from queries.error import Error
from queries.reminder_recipient_mapping_repo import ReminderRecipientMappingRepository

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
    repo: ReminderRepository = Depends()) -> List[ReminderOut]:
    reminders = repo.get_all(user_id)
    if reminders == None or reminders == {"message": "get_all reminder records failed"}:
        response.status_code = 400
    return reminders

@router.get("/reminder/{reminder_id}", response_model=Union[ReminderOut, Error])
def get_one(
    user_id: int,
    reminder_id: int,
    response: Response,
    repo: ReminderRepository = Depends()) -> ReminderOut:
    reminder = repo.get_one(user_id, reminder_id)
    if reminder == None or reminder == {"message": "get_one reminder record failed"}:
        response.status_code = 400
    return reminder

@router.put("/reminder/{reminder_id}", response_model=Union[ReminderUpdate, Error])
def update_reminder(
    user_id: int,
    reminder_id: int,
    reminder: ReminderUpdate,
    # recipients: List[RecipientOut],
    response: Response,
    reminder_repo: ReminderRepository = Depends()) -> ReminderUpdate:
    new_reminder = reminder_repo.update(user_id, reminder_id, reminder) #, recipients)
    if new_reminder == None or new_reminder == {"message": "update reminder record failed"}:
        response.status_code = 400
    return new_reminder

@router.put("/reminder/{reminder_id}/recipients", response_model= bool)
def update_recipient_list(
    user_id: int,
    reminder_id: int,
    recipients: List[int],
    response: Response,
    repo: ReminderRecipientMappingRepository = Depends()) -> bool:
    return repo.update(reminder_id, recipients)

@router.delete("/reminder/{reminder_id}", response_model= bool)
def delete(
    reminder_id: int,
    response: Response,
    repo: ReminderRepository = Depends()):
    return repo.delete(reminder_id)
