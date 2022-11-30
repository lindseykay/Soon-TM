from fastapi import APIRouter, Depends, Response
from typing import Union
from queries.messages import MessageIn, MessageRepository
from queries.error import Error

from jwtdown_fastapi.authentication import Authenticator
import os

class MyAuthenticator(Authenticator):
    async def get_account_data(self, username: str, accounts):
        pass
    def get_account_getter(self,accounts):
        pass
    def get_hashed_password(self, account):
        pass
    def get_account_data_for_cookie(self, account):
        pass

authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])

router = APIRouter()

@router.put("/reminders/{reminder_id}/messages", response_model=Union[MessageIn, Error])
def update_message(
    reminder_id: int,
    message: MessageIn,
    response: Response,
    repo: MessageRepository = Depends()):
    return repo.update(reminder_id, message)
