from fastapi import APIRouter, Depends, Response
from typing import List, Union
from queries.contacts import (
    ContactUpdate,
    ContactIn,
    ContactOut,
    ContactError,
    ContactsRepository
    )
from queries.specialdays import SpecialDayIn


from jwtdown_fastapi.authentication import Authenticator
import os

class MyAuthenticator(Authenticator):
    async def get_account_data(self,username: str,accounts):
        pass
    def get_account_getter(self,accounts):
        pass
    def get_hashed_password(self, account):
        pass
    def get_account_data_for_cookie(self, account):
        pass

authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])

router = APIRouter()

@router.post("/contacts", response_model = Union[ContactOut,ContactError])
def create_contact(
    contact: ContactIn,
    response: Response,
    repo: ContactsRepository=Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
    special_days: List[SpecialDayIn] = []) -> ContactOut:
    new_contact = repo.create(account_data['id'],contact, special_days)
    return new_contact

@router.get("/contacts", response_model = Union[List[ContactOut],ContactError])
def get_all_contacts(
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ContactsRepository=Depends()) -> List[ContactOut]:
    contacts_list = repo.get_all(account_data['id'])
    return contacts_list

@router.get("/contacts/{contact_id}", response_model = Union[ContactOut, ContactError])
def get_contact(
    contact_id: int,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ContactsRepository=Depends()) -> ContactOut:
    contact = repo.get_contact(contact_id, account_data['id'])
    return contact

@router.put("/contacts/{contact_id}", response_model = Union[ContactOut, ContactError])
def update_contact(
    contact_id: int,
    info: ContactUpdate,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ContactsRepository=Depends()) -> ContactOut:
    contact = repo.update_contact(contact_id, account_data['id'], info)
    return contact

@router.delete("/contacts/{contact_id}", response_model = bool)
def delete_contact(
    contact_id: int,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: ContactsRepository=Depends()) -> bool:
    return repo.delete_contact(contact_id, account_data['id'])
