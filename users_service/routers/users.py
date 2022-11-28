from fastapi import APIRouter, Depends, Response, status, HTTPException, Request
from typing import List, Optional, Union
from authenticator import authenticator
from jwtdown_fastapi.authentication import Token

from pydantic import BaseModel


from queries.users import (
    UserError,
    UserIn,
    UserUpdate,
    UserOut,
    UserRepository,
    DuplicateAccountError
)

class AccountForm(BaseModel):
    username: str
    password: str

class AccountToken(Token):
    account: UserOut

class HttpError(BaseModel):
    detail: str



router = APIRouter()

@router.post("/users", response_model=AccountToken)
async def create_user(
    user: UserIn,
    request: Request,
    response: Response,
    repo: UserRepository = Depends()):
    hashed_password = authenticator.hash_password(user.password)
    new_user = repo.create(user, hashed_password)

    form = AccountForm(username=user.username, password=user.password)
    token = await authenticator.login(response, request, form, repo)

    return AccountToken(account=new_user, **token.dict())



@router.get("/users/{user_id}", response_model=Union[UserOut,UserError])
def get_user(
    user_id: int,
    response: Response,
    repo: UserRepository = Depends()) -> UserOut:
    user = repo.get_by_userid(user_id)
    if user == None or user == {"message": "Tough luck"}:
        response.status_code = 400
    return user

@router.put("/users/{user_id}", response_model=Union[UserOut,UserError])

def update_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: UserRepository = Depends()) -> UserOut:
    if user.password:
        hashed_password = authenticator.hash_password(user.password)
        user.password = hashed_password
    user = repo.update(user_id, user)
    if user == None or user == {"message": "Skill diff"}:
        response.status_code = 400
    return user
