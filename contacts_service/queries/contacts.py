from pydantic import BaseModel
from queries.pools import pool
from typing import List, Optional, Union
from datetime import date

class ContactError(BaseModel):
    message : str


class Recipient(BaseModel):
    id : int
    name : str
    phone : Optional[str]
    email : Optional[str]

class SpecialDay(BaseModel):
    name : str
    date : date


class ContactIn(BaseModel):
    recipient_id: int
    notes : str


class ContactOut(BaseModel):
    recipient : Recipient
    special_days : list
    notes : str

class ContactsRepository:
    def create(self, contact: ContactIn)->Union[ContactOut,ContactError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO contacts
                            (recipient_id, notes)
                        VALUES
                            (%s, %s)
                        RETURNING *;
                        """,
                        [contact.recipient_id, contact.notes]
                    )
                    contact_record = result.fetchone()
                    recipient =self.temp_create_recipient(contact_record[1])
                    special = []
                    return ContactOut(
                        recipient = recipient,
                        special_days = special,
                        notes = contact_record[2]
                    )
        except Exception:
            return {"message": "hello error town"}




    def temp_create_recipient(self, id:int):
        return Recipient(
            id = id,
            name = "Mom",
            phone = None,
            email = None
        )






