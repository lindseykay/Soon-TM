from pydantic import BaseModel
from queries.pools import conn
from typing import List, Optional, Union
from queries.specialdays import (
    SpecialDaysRepository,
    SpecialDayOut,
    SpecialDayIn,
)
import os
import requests
import json


class ContactError(BaseModel):
    message: str


class Recipient(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]


class ContactIn(BaseModel):
    recipient_id: int
    notes: str


class ContactOut(BaseModel):
    id: int
    user_id: int
    recipient: Optional[Recipient]
    special_days: Optional[List[SpecialDayOut]]
    notes: str


class ContactUpdate(BaseModel):
    notes: Optional[str]


class ContactsRepository:
    def create(
        self,
        user_id: int,
        contact: ContactIn,
        special_days: List[SpecialDayIn],
    ) -> Union[ContactOut, ContactError]:
        try:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    INSERT INTO contacts
                        (user_id, recipient_id, notes)
                    VALUES
                        (%s, %s, %s)
                    RETURNING *;
                    """,
                    [user_id, contact.recipient_id, contact.notes],
                )
                contact_record = result.fetchone()
                recipient = find_recipient(contact_record[2])

                s_days = []
                for day in special_days:
                    new_sd = SpecialDaysRepository.create(
                        SpecialDaysRepository, day, contact_record[0]
                    )
                    if isinstance(new_sd, SpecialDayOut):
                        s_days.append(new_sd)
                return ContactOut(
                    id=contact_record[0],
                    user_id=contact_record[1],
                    recipient=recipient,
                    special_days=s_days,
                    notes=contact_record[3],
                )
        except Exception:
            return {"message": "hello error town"}

    def get_all(self, user_id: int) -> Union[List[ContactOut], ContactError]:
        try:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT *
                    FROM CONTACTS c
                    LEFT JOIN special_days sd on c.id = sd.contact_id
                    WHERE user_id = %s
                    """,
                    [user_id],
                )
                query = result.fetchall()

                recipients = find_all_recipients(user_id)
                recipients_dict = {}
                for recipient in recipients:
                    recipients_dict[recipient["id"]] = recipient

                q_dict = {}
                for record in query:
                    if q_dict.get(record[0]):
                        q_dict[record[0]][4].append(SpecialDayOut(
                            id = record[4],
                            contact_id = record[5],
                            name = record[6],
                            date = record[7]
                        ))
                    else:
                        q_dict[record[0]] = (
                            record[0],
                            record[1],
                            Recipient(**recipients_dict[record[2]]),
                            record[3],
                            [SpecialDayOut(
                                id = record[4],
                                contact_id = record[5],
                                name = record[6],
                                date = record[7])
                            ] if record[4] else [])

                output = [ContactOut(
                    id = rec[0],
                    user_id = rec[1],
                    recipient = rec[2],
                    special_days = rec[4],
                    notes = rec[3]
                ) for rec in q_dict.values()]

                return output
        except Exception:
            return {"message": "hello Can't find all contacts"}

    def get_contact(
        self, contact_id: int, user_id: int
    ) -> Union[ContactOut, ContactError]:
        try:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT *
                    FROM CONTACTS
                    WHERE user_id = %s AND id = %s
                    """,
                    [user_id, contact_id],
                )
                query = result.fetchone()
                return query_to_contactout(query)

        except Exception:
            return {"message": "Can't find contact"}

    def update_contact(
        self, contact_id: int, user_id: int, info: ContactUpdate
    ) -> Union[ContactOut, ContactError]:
        try:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    UPDATE contacts
                    SET notes = COALESCE(%s,notes)
                    WHERE user_id = %s AND id=%s
                    RETURNING *
                    """,
                    [info.notes, user_id, contact_id],
                )
                query = result.fetchone()
                return query_to_contactout(query)

        except Exception:
            return {"message": "Can't find contact"}

    def delete_contact(self, contact_id: int, user_id: int) -> bool:
        try:
            with conn.cursor() as db:
                db.execute(
                    """
                        DELETE
                        FROM contacts
                        WHERE user_id = %s AND id = %s
                        """,
                    [user_id, contact_id],
                )
            return True
        except Exception:
            return False


# ____________________HELP FUNCTIONS_________________________________
def find_recipient(id: int):
    url = f'{os.environ["REMINDERS_HOST"]}recipients/{id}'
    response = requests.get(url)
    content = json.loads(response.content)
    return content


def find_all_recipients(user_id: int):
    url = f'{os.environ["REMINDERS_HOST"]}contacts/recipients/'
    params = {"user_id": user_id}
    response = requests.get(url, params)
    content = json.loads(response.content)
    return content


def query_to_contactout(query: tuple) -> ContactOut:
    with conn.cursor() as db:
        result = db.execute(
            """
                SELECT *
                FROM special_days
                WHERE contact_id = %s
                """,
            [query[0]],
        )
        sd_query = result.fetchall()
        specialdays = [query_to_specialdayout(record) for record in sd_query]
        recipient = find_recipient(query[2])
        return ContactOut(
            id=query[0],
            user_id=query[1],
            recipient=recipient,
            special_days=specialdays,
            notes=query[3],
        )


def query_to_specialdayout(query: tuple) -> SpecialDayOut:
    return SpecialDayOut(
        id=query[0], contact_id=query[1], name=query[2], date=query[3]
    )


# ____________________HELP FUNCTIONS_________________________________
