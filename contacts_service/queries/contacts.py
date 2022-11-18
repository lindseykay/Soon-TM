from pydantic import BaseModel
from queries.pools import pool
from typing import List, Optional, Union
from queries.specialdays import SpecialDaysRepository, SpecialDayOut, SpecialDayIn

class ContactError(BaseModel):
    message : str

class Recipient(BaseModel):
    id : int
    name : str
    phone : Optional[str]
    email : Optional[str]

class ContactIn(BaseModel):
    recipient_id: int
    notes : str

class ContactOut(BaseModel):
    recipient : Recipient
    special_days : List[SpecialDayOut]
    notes : str

class ContactsRepository:
    def create(self, contact: ContactIn, special_days: List[SpecialDayIn])->Union[ContactOut,ContactError]:
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
                    recipient = self.temp_create_recipient(contact_record[1])

                    s_days = []
                    for day in special_days:
                        new_sd = SpecialDaysRepository.create(None, day, contact_record[0])
                        if isinstance(new_sd,SpecialDayOut):
                            s_days.append(new_sd)


                    return ContactOut(
                        recipient = recipient,
                        special_days = s_days,
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
