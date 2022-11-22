from pydantic import BaseModel
from typing import List, Optional, Union
from queries.pools import pool
from datetime import date
from queries.recipients import RecipientIn, RecipientOut, RecipientRepository
from queries.messages import MessageOut
from queries.error import Error
from queries.reminder_recipient_mapping_repo import ReminderRecipientMappingRepository

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


class ReminderUpdate(BaseModel):
    email_target: str
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
                    for recipient in recipients:
                        new_recipient = RecipientRepository.create(RecipientRepository, recipient)
                        recipient_list.append(new_recipient)
                    recipient_ids = [recipient.id for recipient in recipient_list]
                    for id in recipient_ids:
                        ReminderRecipientMappingRepository.create(ReminderRecipientMappingRepository, query[0], id)
                    return self.reminder_query_to_reminder_out(query, recipient_list)
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
                            ORDER BY r.id;
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

                            [user_id,
                            reminder_id]
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

    def update(self, user_id: int, reminder_id: int, reminder: ReminderOut, recipients: List[RecipientOut]) -> Union[ReminderOut, Error]:
            try:
                with pool.connection() as conn:
                    with conn.cursor() as db:
                        result = db.execute(
                            """
                            UPDATE reminders
                            SET email_target = COALESCE(%s, email_target)
                                , reminder_date = COALESCE(%s, reminder_date)
                                , recurring = COALESCE(%s, recurring)
                            WHERE id = %s
                            AND user_id = %s
                            RETURNING *
                            """,
                            [
                                reminder.email_target,
                                reminder.reminder_date,
                                reminder.recurring,
                                reminder_id,
                                user_id
                            ]
                        )
                        query = result.fetchone()
                        print(query)
                        recipient_list = []
                        for recipient in recipients:
                            print("RECIPIENT::::" , recipient)
                            updated_recipient = RecipientRepository.update(RecipientRepository, recipient.id, recipient)
                            print("UPDATED RECIPIENT::::", updated_recipient)
                            recipient_list.append(updated_recipient)
                        recipient_ids = [recipient.id for recipient in recipient_list]
                        ReminderRecipientMappingRepository.delete(reminder_id)
                        print("RECIPIENT LIST::::", recipient_list)
                        for id in recipient_ids:
                            ReminderRecipientMappingRepository.create(ReminderRecipientMappingRepository, query[0], id)
                        return self.reminder_query_to_reminder_out(query, recipient_list)
            except Exception:
                return {"message": "update reminder record failed"}

#HELPER FUNCTIONS
    def reminder_query_to_reminder_out(self, query: tuple, recipient_list: List[RecipientOut]) -> ReminderOut:
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
