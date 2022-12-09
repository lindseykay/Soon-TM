from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import reminders, messages, recipients
import os

app = FastAPI()
app.include_router(reminders.router)
app.include_router(messages.router)
app.include_router(recipients.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.environ.get("CORS_HOST", "http://localhost:3000"),
        os.environ["EMAIL_HOST"],
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/launch-details")
def launch_details():
    return {
        "launch_details": {
            "year": 2022,
            "month": 12,
            "day": "9",
            "hour": 19,
            "min": 0,
            "tz:": "PST",
        }
    }
