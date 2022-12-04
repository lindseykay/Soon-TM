from pydantic import BaseModel
from typing import List, Optional, Union
from queries.pools import pool
from datetime import date
from queries.recipients import RecipientIn, RecipientOut, RecipientRepository
from queries.messages import MessageOut, MessageRepository
from queries.error import Error
from queries.reminder_recipient_mapping_repo import ReminderRecipientMappingRepository

class ReminderIn(BaseModel):
    email_target: str
    reminder_date: date
    recurring: bool


class ReminderOut(BaseModel):
    id: int
    user_id: Optional[int]
    email_target: str
    reminder_date: date
    message: MessageOut
    sent: bool
    sent_on: Optional[date]
    recurring: bool
    created_on: date
    recipients: List[RecipientOut]


class ReminderUpdate(BaseModel):
    reminder_date: date
    recurring: bool

class ReminderRepository:
    def create(self, reminder: ReminderIn, message: MessageOut, recipients: List[RecipientIn] = [], user_id = None) -> Union[ReminderOut, Error]:
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
                            , recurring)
                        VALUES
                            (%s, %s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [
                            user_id,
                            reminder.email_target,
                            reminder.reminder_date,
                            message.id,
                            reminder.recurring
                        ]
                    )
                    query = result.fetchone()
                    recipient_list = []
                    for recipient in recipients:
                        new_recipient = RecipientRepository.create(RecipientRepository, recipient, user_id)
                        recipient_list.append(new_recipient)
                    recipient_ids = [recipient.id for recipient in recipient_list]
                    for id in recipient_ids:
                        ReminderRecipientMappingRepository.create(ReminderRecipientMappingRepository, query[0], id)
                    return self.reminder_query_to_reminder_out(query, recipient_list, message)
        except Exception:
            return {"message": "create reminder record failed"}

    def get_all(self, user_id:int) -> Union[List[ReminderOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                            """
                            SELECT
                                    r.id,
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
                            ORDER BY r.reminder_date ASC;
                            """,
                            [user_id]
                    )
                    query = result.fetchall()
                    new_dict = {}
                    for record in query:
                        if record[0] not in new_dict:
                            new_dict[record[0]] = ReminderOut(
                                id= record[0],
                                user_id= record[1],
                                email_target= record[2],
                                reminder_date= record[3],
                                message= MessageRepository.get_one(MessageRepository, record[4]),
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
                            new_dict[record[0]].recipients.append(RecipientOut(
                                    id = record[9],
                                    name = record[10],
                                    phone = record[11],
                                    email = record[12])
                                    )
                    returns = list(new_dict.values())
                    return returns
        except Exception:
            return {"message": "get_all reminder records failed"}

    def get_one(self, user_id: int, reminder_id: int) -> Union[ReminderOut, Error]:
            try:
                with pool.connection() as conn:
                    with conn.cursor() as db:
                        result = db.execute(
                             """
                            SELECT
                                    r.id,
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
                            AND r.id = %s;
                            """,
                            [
                                user_id,
                                reminder_id
                            ]
                        )
                        query = result.fetchall()
                        new_dict = {}
                        for record in query:
                            if record[0] not in new_dict:
                                new_dict[record[0]] = ReminderOut(
                                    id= record[0],
                                    user_id= record[1],
                                    email_target= record[2],
                                    reminder_date= record[3],
                                    message= MessageRepository.get_one(MessageRepository, record[4]),
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
                                new_dict[record[0]].recipients.append(RecipientOut(
                                        id = record[9],
                                        name = record[10],
                                        phone = record[11],
                                        email = record[12])
                                        )
                    returns = new_dict[reminder_id]
                    return returns
            except Exception:
                return {"message": "get_one reminder record failed"}

    def update(self, user_id: int, reminder_id: int, reminder: ReminderUpdate) -> Union[ReminderUpdate, Error]:
            try:
                with pool.connection() as conn:
                    with conn.cursor() as db:
                        result = db.execute(
                            """
                            UPDATE reminders
                            SET reminder_date = COALESCE(%s, reminder_date)
                                , recurring = COALESCE(%s, recurring)
                            WHERE id = %s
                            AND user_id = %s
                            RETURNING email_target, reminder_date, recurring
                            """,
                            [
                                reminder.reminder_date,
                                reminder.recurring,
                                reminder_id,
                                user_id
                            ]
                        )
                        query = result.fetchone()
                        return ReminderUpdate(email_target = query[0], reminder_date = query[1], recurring = query[2])
            except Exception:
                return {"message": "update reminder record failed"}

    def delete(self, reminder_id: int, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        DELETE FROM reminders
                        WHERE id = %s
                        AND user_id = %s
                        RETURNING message_id
                        """,
                        [
                            reminder_id,
                            user_id
                        ]
                    )
                    message_id = result.fetchone()[0]
                    db.execute(
                        """
                        DELETE FROM messages
                        WHERE id = %s
                        """,
                        [message_id]
                    )
                    db.execute(
                        """
                        DELETE FROM reminders_recipients_mapping_table
                        WHERE reminder_id = %s
                        """,
                        [reminder_id]
                    )
                    return True
        except Exception:
            return False

#HELPER FUNCTIONS
    def reminder_query_to_reminder_out(self, query: tuple, recipient_list: List[RecipientOut], message: MessageOut) -> ReminderOut:
        return ReminderOut(
            id= query[0],
            user_id= query[1],
            email_target= query[2],
            reminder_date= query[3],
            message= message,
            sent= query[5],
            sent_on= query[6],
            recurring= query[7],
            created_on= query[8],
            recipients= recipient_list
            )
