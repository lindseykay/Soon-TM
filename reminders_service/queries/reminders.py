from pydantic import BaseModel
from typing import List, Optional, Union
from queries.pools import pool
from datetime import date

class Error(BaseModel):
    message: str


class RecipientIn(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]


class RecipientOut(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]


class MessageIn(BaseModel):
    template_id: Optional[int]
    content: str


class MessageOut(BaseModel):
    id: int
    template_id: Optional[int]
    content: str


class ReminderIn(BaseModel):
    email_target: str
    reminder_date: date
    sent: bool
    sent_on: Optional[date]
    recurring: bool
    created_on: date


class ReminderOut(BaseModel):
    id: int
    user_id: Optional[int]
    email_target: str
    reminder_date: date
    message_id: int
    sent: bool
    sent_on: Optional[date]
    recurring: bool
    created_on: date

class ReminderRepository:
    def create(self, reminder: ReminderIn, message: MessageOut, user_id = None) -> Union[ReminderOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO reminders(
                            user_id
                            , email_target
                            , reminder_date
                            , message_id
                            , sent
                            , sent_on
                            , recurring
                            , created_on)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [
                            user_id,
                            reminder.email_target,
                            reminder.reminder_date,
                            message.id,
                            reminder.sent,
                            reminder.sent_on,
                            reminder.recurring,
                            reminder.created_on
                        ]
                    )
                    query = result.fetchone()
                    return self.reminder_query_to_reminderout(query)
        except Exception:
            return {"message": "No good"}
    
    def reminder_query_to_reminderout(self, query: tuple) -> ReminderOut:
        return ReminderOut(
            id= query[0],
            user_id= query[1],
            email_target= query[2],
            reminder_date= query[3],
            message_id= query[4],
            sent= query[5],
            sent_on= query[6],
            recurring= query[7],
            created_on= query[8]
        )


class MessageRepository:
    def create(self, message: MessageIn) -> Union[MessageOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO messages(
                            template_id
                            , content
                        )
                        VALUES (%s, %s)
                        RETURNING id;
                        """,
                        [
                            message.template_id,
                            message.content
                        ]
                    )
                    id = result.fetchone()[0]
                    input = message.dict()
                    return MessageOut(id=id, **input)
        except Exception:
            return {"message": "No good"}