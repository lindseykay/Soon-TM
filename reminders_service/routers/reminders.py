from fastapi import APIRouter, Depends, Response
from typing import List, Union, Optional
from queries.reminders import (
    ReminderIn,
    ReminderOut,
    ReminderUpdate,
    ReminderRepository,
)
from queries.recipients import RecipientIn
from queries.messages import MessageIn, MessageRepository
from queries.error import Error
from queries.reminder_recipient_mapping_repo import (
    ReminderRecipientMappingRepository,
)
from jwtdown_fastapi.authentication import Authenticator
import os
import requests


class MyAuthenticator(Authenticator):
    async def get_account_data(self, username: str, accounts):
        pass

    def get_account_getter(self, accounts):
        pass

    def get_hashed_password(self, account):
        pass

    def get_account_data_for_cookie(self, account):
        pass


authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])

router = APIRouter()


@router.post("/reminders", response_model=Union[ReminderOut, Error])
def create_reminder(
    reminder: ReminderIn,
    message: MessageIn,
    recipients: List[RecipientIn],
    response: Response,
    account_data: Optional[dict] = Depends(
        authenticator.try_get_current_account_data
    ),
    reminder_repo: ReminderRepository = Depends(),
    message_repo: MessageRepository = Depends(),
):
    new_message = message_repo.create(message)
    if new_message is None or new_message == {
        "message": "create message record failed"
    }:
        response.status_code = 400
    if account_data:
        reminder.email_target = account_data["email"]
        new_reminder = reminder_repo.create(
            reminder, new_message, recipients, account_data["id"]
        )
    else:
        new_reminder = reminder_repo.create(
            reminder, new_message, recipients, None
        )
    if new_reminder is None or new_reminder == {
        "message": "create reminder record failed"
    }:
        response.status_code = 400
    return new_reminder


@router.get("/reminders", response_model=Union[List[ReminderOut], Error])
def get_all(
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ReminderRepository = Depends(),
) -> List[ReminderOut]:
    reminders = repo.get_all(account_data["id"])
    if reminders is None or reminders == {
        "message": "get_all reminder records failed"
    }:
        response.status_code = 400
    return reminders


@router.get(
    "/reminder/{reminder_id}", response_model=Union[ReminderOut, Error]
)
def get_one(
    reminder_id: int,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ReminderRepository = Depends(),
) -> ReminderOut:
    reminder = repo.get_one(account_data["id"], reminder_id)
    if reminder is None or reminder == {
        "message": "get_one reminder record failed"
    }:
        response.status_code = 400
    return reminder


@router.put(
    "/reminder/{reminder_id}", response_model=Union[ReminderUpdate, Error]
)
def update_reminder(
    reminder_id: int,
    reminder: ReminderUpdate,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    reminder_repo: ReminderRepository = Depends(),
) -> ReminderUpdate:
    new_reminder = reminder_repo.update(
        account_data["id"], reminder_id, reminder
    )
    if new_reminder is None or new_reminder == {
        "message": "update reminder record failed"
    }:
        response.status_code = 400
    return new_reminder


@router.put("/reminder/{reminder_id}/recipients", response_model=bool)
def update_recipient_list(
    reminder_id: int,
    recipients: List[int],
    response: Response,
    repo: ReminderRecipientMappingRepository = Depends(),
) -> bool:
    return repo.update(reminder_id, recipients)


@router.delete("/reminder/{reminder_id}", response_model=bool)
def delete(
    reminder_id: int,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ReminderRepository = Depends(),
):
    return repo.delete(reminder_id, account_data["id"])


@router.get(f'/{os.environ["COMPILER_ROUTE"]}')
def compile(repo: ReminderRepository = Depends()):
    reminders = repo.reminder_compiler()
    if reminders:
        repo.mark_complete()
    return reminders


@router.get("/marco-polo")
def prodder():
    url = f'{os.environ["EMAIL_HOST"]}/marco-polo'
    response = requests.get(url)