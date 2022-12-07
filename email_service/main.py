from scheduler import compiler_scheduler
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.on_event("startup")
async def schedule_poller():
    pass
    # loop = asyncio.get_event_loop()
    # loop.create_task(compiler_scheduler())
