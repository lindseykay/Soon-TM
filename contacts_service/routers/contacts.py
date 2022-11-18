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
