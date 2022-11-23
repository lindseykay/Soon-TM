from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.users import (
    UserError,
    UserIn,
    UserUpdate,
    UserOut,
    UserRepository,
)

router = APIRouter()

@router.post("/users", response_model=Union[UserOut,UserError])
def create_user(
    user: UserIn,
    response: Response,
    repo: UserRepository = Depends()):
    new_user = repo.create(user)
    if new_user == None or new_user == {"message": "We'll get em next time"}:
        response.status_code = 400
    return new_user

@router.get("/users/{user_id}", response_model=Union[UserOut,UserError])
def get_user(
    user_id: int,
    response: Response,
    repo: UserRepository = Depends()) -> UserOut:
    user = repo.get(user_id)
    if user == None or user == {"message": "Tough luck"}:
        response.status_code = 400
    return user

@router.put("/users/{user_id}", response_model=Union[UserOut,UserError])
def update_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
    repo: UserRepository = Depends()) -> UserOut:
    user = repo.update(user_id, user)
    if user == None or user == {"message": "Skill diff"}:
        response.status_code = 400
    return user
