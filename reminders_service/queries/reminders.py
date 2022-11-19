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
    recipients: List[RecipientOut]

class ReminderRepository:
    def create(self, reminder: ReminderIn, message: MessageOut, new_recipient_list: List[RecipientIn] = [], user_id = None) -> Union[ReminderOut, Error]:
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

                    recipient_list = []
                    for recipient in new_recipient_list:
                        new_recipient = RecipientRepository.create(RecipientRepository, recipient)
                        recipient_list.append(new_recipient)

                    recipient_ids = [recipient.id for recipient in recipient_list]
                    for id in recipient_ids:
                        ReminderRecipientMappingRepository.create(ReminderRecipientMappingRepository, query[0], id)

                    return self.reminder_query_to_reminderout(query, recipient_list)
        except Exception:
            return {"message": "No good"}

    def reminder_query_to_reminderout(self, query: tuple, recipient_list: List[RecipientOut]) -> ReminderOut:
        return ReminderOut(
            id= query[0],
            user_id= query[1],
            email_target= query[2],
            reminder_date= query[3],
            message_id= query[4],
            sent= query[5],
            sent_on= query[6],
            recurring= query[7],
            created_on= query[8],
            recipients= recipient_list
        )


    def get_all(self, user_id:int) -> Union[List[ReminderOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                            """
                            SELECT r.id,
                                    r.user_id,
                                    r.email_target,
                                    r.reminder_date,
                                    r.message_id,
                                    r.sent,
                                    r.sent_on,
                                    r.recurring,
                                    r.created_on,
                                    re.id as recipient_id,
                                    re.name,
                                    re. phone,
                                    re. email
                            FROM reminders as r
                            LEFT JOIN reminders_recipients_mapping_table as rrmt
                            ON (r.id = rrmt.reminder_id)
                            LEFT JOIN recipients as re
                            ON (rrmt.recipient_id = re.id )
                            WHERE r.user_id = %s
                            ORDER BY r.id;
                            """,

                            [user_id]

                    )

                    query = result.fetchall()

                    new_dict = {}
                    for record in query:
                        if record[0] not in new_dict:
                            print("If statement ran")
                            new_dict[record[0]] = ReminderOut(
                                id= record[0],
                                user_id= record[1],
                                email_target= record[2],
                                reminder_date= record[3],
                                message_id= record[4],
                                sent= record[5],
                                sent_on= record[6],
                                recurring= record[7],
                                created_on= record[8],
                                recipients= [RecipientOut(
                                    id = record[9],
                                    name = record[10],
                                    phone = record[11],
                                    email = record[12])
                                    ]
                            )

                        else:
                            print(new_dict[record[0]].recipients)
                            new_dict[record[0]].recipients.append(RecipientOut(
                                    id = record[9],
                                    name = record[10],
                                    phone = record[11],
                                    email = record[12])
                                    )
                    return(list(new_dict.values()))


        except Exception:
            return {"message": "Get_all fetch failed"}

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


class RecipientRepository:
    def create(self, recipient: RecipientIn) -> Union[RecipientOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO recipients(
                            name
                            , phone
                            , email
                        )
                        VALUES (%s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            recipient.name,
                            recipient.phone,
                            recipient.email,
                        ]
                    )
                    recipient_id = result.fetchone()[0]
                    input = recipient.dict()
                    return RecipientOut(id=recipient_id, **input)
        except Exception:
            return {"message": "No good"}


class ReminderRecipientMappingRepository:
    def create(self, reminder_id: int, recipient_id: int):
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        INSERT INTO reminders_recipients_mapping_table(
                            reminder_id
                            , recipient_id
                        )
                        VALUES (%s, %s);
                        """,
                        [
                            reminder_id,
                            recipient_id
                        ]
                    )
        except Exception:
            return {"message": "Failed to insert mapping table"}
