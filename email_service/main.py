from scheduler import compiler_scheduler
from fastapi import FastAPI
from routers import prodder
import asyncio

app = FastAPI()
app.include_router(prodder.router)

@app.on_event("startup")
async def schedule_poller():
    loop = asyncio.get_event_loop()
    loop.create_task(compiler_scheduler())
