from fastapi import APIRouter, Depends, Response
from typing import Union
from queries.specialdays import (
    SpecialDayIn,
    SpecialDayOut,
    SpecialDayError,
    SpecialDaysRepository
    )

router = APIRouter()

@router.post("/specialdays", response_model = Union[SpecialDayOut,SpecialDayError])
def create_special_day(specialday: SpecialDayIn,
    response: Response,
    repo: SpecialDaysRepository=Depends())->SpecialDayOut:
    new_special_day = repo.create(specialday)
    return new_special_day
