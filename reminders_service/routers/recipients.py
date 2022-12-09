from fastapi import APIRouter, Depends, Response
from typing import List, Union, Optional
from queries.recipients import RecipientIn, RecipientOut, RecipientRepository
from queries.error import Error

from jwtdown_fastapi.authentication import Authenticator
import os


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


@router.put("/recipients", response_model=Union[List[RecipientOut], Error])
def update_recipients(
    reminder_id: int,
    recipients: List[RecipientOut],
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: RecipientRepository = Depends(),
):
    recipient_list = []
    for recipient in recipients:
        updated_recipient = repo.update(
            account_data["id"], reminder_id, recipient
        )
        recipient_list.append(updated_recipient)
    return recipient_list


@router.post("/recipients", response_model=Union[int, Error])
def create(
    recipient: RecipientIn,
    response: Response,
    account_data: Optional[dict] = Depends(
        authenticator.try_get_current_account_data
    ),
    repo: RecipientRepository = Depends(),
):
    return repo.create(recipient, account_data["id"]).id


@router.get("/recipients", response_model=Union[List[RecipientOut], Error])
def get_all_by_user(
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: RecipientRepository = Depends(),
):
    print(account_data)
    return repo.get_all_by_user(account_data["id"])


@router.get("/recipients/{recipient_id}")
def get_by_id(recipient_id: int, repo: RecipientRepository = Depends()):
    return repo.get_by_id(recipient_id)
