from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.contacts import (
    ContactIn,
    ContactOut,
    ContactError,
    ContactsRepository
    )
from queries.specialdays import SpecialDayIn

router = APIRouter()

@router.post("/contacts", response_model = Union[ContactOut,ContactError])
def create_contact(contact: ContactIn,
    response: Response,
    repo: ContactsRepository=Depends(),
    special_days: List[SpecialDayIn] = []) -> ContactOut:
    new_contact = repo.create(contact, special_days)
    return new_contact


@router.get("/contacts", response_model = Union[List[ContactOut],ContactError])
def get_all_contacts(user_id: int,
    response: Response,
    repo: ContactsRepository=Depends()) -> List[ContactOut]:
    contacts_list = repo.get_all(user_id)
    return contacts_list


