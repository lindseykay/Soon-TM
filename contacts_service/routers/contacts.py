from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union



from queries.contacts import (
    ContactIn,
    ContactOut,
    ContactError,
    SpecialDay,
    ContactsRepository
    )



router = APIRouter()


@router.post("/contacts", response_model = Union[ContactOut,ContactError])
def create_contact(contact: ContactIn,
    response: Response,
    repo: ContactsRepository=Depends())->ContactOut:
    new_contact = repo.create(contact)
    return new_contact



