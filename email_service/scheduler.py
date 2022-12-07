import schedule
from datetime import date
from emailer import formatter, send_emails
import requests
import json
import os
import asyncio

def reminder_compiler():
    url = f'{os.environ["REMINDERS_HOST"]}{os.environ["COMPILER_ROUTE"]}'
    response = requests.get(url)
    content = json.loads(response.content)
    return content

def job():
    x = reminder_compiler()
    try:
        y = formatter(x)
        send_emails(y)
    except Exception:
        print("You have no reminders or crashed")

#   ----SCHEDULER----

async def compiler_scheduler():
    schedule.every().day.at("14:00:00").do(job)
    schedule.every().day.at("15:00:00").do(job)
    schedule.every().day.at("19:00:00").do(job)
    while True:
        schedule.run_pending()
        await asyncio.sleep(10)
        print("Waiting for emails..", flush=True)
