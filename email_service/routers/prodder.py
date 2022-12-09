from fastapi import APIRouter
import os
import requests

router = APIRouter()

@router.get("/marco-polo")
def prodder():
    url = f'{os.environ["REMINDERS_HOST"]}/marco-polo'
    response = requests.get(url)