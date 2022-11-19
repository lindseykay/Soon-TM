from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.contacts import (
    ContactUpdate,
    ContactIn,
    ContactOut,
    ContactError,
    ContactsRepository
    )
from queries.specialdays import SpecialDayIn

router = APIRouter()

@router.post("/contacts", response_model = Union[ContactOut,ContactError])
def create_contact(
    contact: ContactIn,
    response: Response,
    repo: ContactsRepository=Depends(),
    special_days: List[SpecialDayIn] = []) -> ContactOut:
    new_contact = repo.create(contact, special_days)
    return new_contact


@router.get("/contacts", response_model = Union[List[ContactOut],ContactError])
def get_all_contacts(
    user_id: int,
    response: Response,
    repo: ContactsRepository=Depends()) -> List[ContactOut]:
    contacts_list = repo.get_all(user_id)
    return contacts_list


@router.get("/contacts/{contact_id}", response_model = Union[ContactOut, ContactError])
def get_contact(
    contact_id: int,
    user_id: int,
    response: Response,
    repo: ContactsRepository=Depends()) -> ContactOut:
    contact = repo.get_contact(contact_id, user_id)
    return contact


# @router.put("/contacts/{contact_id}", response_model = Union[ContactOut, ContactError])
# def update_contact(
#     contact_id: int,
#     user_id: int,
#     info: ContactUpdate,
#     response: Response,
#     repo: ContactsRepository=Depends()) -> ContactOut:
#     contact = repo.update_contact(contact_id, user_id)
#     return contact







