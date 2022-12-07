from fastapi import APIRouter, Depends, Response
from typing import Union
from queries.specialdays import (
    SpecialDayIn,
    SpecialDayOut,
    SpecialDayError,
    SpecialDaysRepository,
)

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


@router.post(
    "/specialdays", response_model=Union[SpecialDayOut, SpecialDayError]
)
def create_special_day(
    specialday: SpecialDayIn,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: SpecialDaysRepository = Depends(),
) -> SpecialDayOut:
    new_special_day = repo.create(specialday)
    return new_special_day
