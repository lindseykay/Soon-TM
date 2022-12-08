from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
)
from typing import Union
from authenticator import authenticator
from jwtdown_fastapi.authentication import Token

from pydantic import BaseModel


from queries.users import (
    UserError,
    UserIn,
    UserUpdate,
    UserOut,
    UserRepository,
)


class AccountForm(BaseModel):
    username: str
    password: str


class AccountToken(Token):
    account: UserOut


class HttpError(BaseModel):
    detail: str


router = APIRouter()


@router.post("/users/", response_model=Union[AccountToken,UserOut])
async def create_user(
    user: UserIn,
    request: Request,
    response: Response,
    repo: UserRepository = Depends(),
):
    hashed_password = authenticator.hash_password(user.password)
    new_user = repo.create(user, hashed_password)

    form = AccountForm(username=user.username, password=user.password)
    if user.username == "CeyF15adHSC4BWoWAQs5wEuM1jaSAwC9":
        return new_user

    token = await authenticator.login(response, request, form, repo)

    return AccountToken(account=new_user, **token.dict())


@router.get("/users/", response_model=Union[UserOut, UserError])
def get_user(
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: UserRepository = Depends(),
) -> UserOut:
    user = repo.get_by_userid(account_data["id"])
    if user is None or user == {"message": "Tough luck"}:
        response.status_code = 400
    return user


@router.put("/users/", response_model=Union[UserOut, UserError])
def update_user(
    user: UserUpdate,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: UserRepository = Depends(),
) -> UserOut:
    if user.password:
        hashed_password = authenticator.hash_password(user.password)
        user.password = hashed_password
    user = repo.update(account_data["id"], user)
    if user is None or user == {"message": "Skill diff"}:
        response.status_code = 400
    return user


@router.get("/token", response_model=AccountToken | None)
async def get_token(
    request: Request,
    account: UserOut = Depends(authenticator.try_get_current_account_data),
) -> AccountToken | None:
    if account and authenticator.cookie_name in request.cookies:
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "token_type": "Bearer",
            "account": account,
        }
