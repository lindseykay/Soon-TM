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
    user_id: int
    recipient_id: int
    notes : str

class ContactOut(BaseModel):
    id : int
    user_id: int
    recipient : Recipient
    special_days : List[SpecialDayOut]
    notes : str

class ContactUpdate(BaseModel):
    notes: str

class ContactsRepository:
    def create(self, contact: ContactIn, special_days: List[SpecialDayIn])->Union[ContactOut,ContactError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO contacts
                            (user_id, recipient_id, notes)
                        VALUES
                            (%s, %s, %s)
                        RETURNING *;
                        """,
                        [contact.user_id, contact.recipient_id, contact.notes]
                    )
                    contact_record = result.fetchone()
                    recipient = temp_create_recipient(contact_record[1])

                    s_days = []
                    for day in special_days:
                        new_sd = SpecialDaysRepository.create(SpecialDaysRepository, day, contact_record[0])
                        if isinstance(new_sd,SpecialDayOut):
                            s_days.append(new_sd)
                    return ContactOut(
                        id = contact_record[0],
                        user_id = contact_record[1],
                        recipient = recipient,
                        special_days = s_days,
                        notes = contact_record[3]
                    )
        except Exception:
            return {"message": "hello error town"}

    def get_all(self, user_id: int)-> Union[List[ContactOut],ContactError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM CONTACTS
                        WHERE user_id = %s
                        """,
                        [user_id]
                    )
                    query = result.fetchall()

                    return [query_to_contactout(record) for record in query]


        except Exception:
            return {"message": "hello Can't find all contacts"}

    def get_contact(self, contact_id: int, user_id: int) -> Union[ContactOut,ContactError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM CONTACTS
                        WHERE user_id = %s and id = %s
                        """,
                        [
                            user_id,
                            contact_id
                        ]
                    )
                    query = result.fetchone()
                    return query_to_contactout(query)


        except Exception:
            return {"message": "Can't find contact"}




#____________________HELP FUNCTIONS_________________________________
def temp_create_recipient(id:int):
    return Recipient(
        id = id,
        name = "Mom",
        phone = None,
        email = None
    )


def query_to_contactout(query:tuple) -> ContactOut:
    with pool.connection() as conn:
        with conn.cursor() as db:
            result = db.execute(
                """
                SELECT *
                FROM special_days
                WHERE contact_id = %s
                """,
                [query[0]]
            )
            sd_query = result.fetchall()
            specialdays = [query_to_specialdayout(record) for record in sd_query]
            recipient = temp_create_recipient(query[2])
            return ContactOut(
                id = query[0],
                user_id = query[1],
                recipient = recipient,
                special_days = specialdays,
                notes = query[3]
            )

def query_to_specialdayout(query:tuple) -> SpecialDayOut:
    return SpecialDayOut(
        id = query[0],
        contact_id = query[1],
        name = query[2],
        date = query[3]
    )


#____________________HELP FUNCTIONS_________________________________


