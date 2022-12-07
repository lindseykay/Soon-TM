from pydantic import BaseModel
from queries.pools import conn
from typing import Union
from datetime import date

class SpecialDayError(BaseModel):
    message : str


class SpecialDayIn(BaseModel):
    contact_id : int
    name : str
    date : date


class SpecialDayOut(BaseModel):
    id: int
    contact_id : int
    name : str
    date : date


class SpecialDaysRepository:
    def create(self, specialday: SpecialDayIn, contact_id: int = None) -> Union[SpecialDayOut,SpecialDayError]:
        try:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO special_days
                            (contact_id, name, date)
                        VALUES
                            (%s, %s, %s)
                        RETURNING *;
                        """,
                        [
                            specialday.contact_id if contact_id == None else contact_id,
                            specialday.name,
                            specialday.date
                        ]
                    )
                    query = result.fetchone()
                    return query_to_specialdayout(query)
        except Exception:
            return {"message": "not so special of a day huh"}


def query_to_specialdayout(query: tuple) -> SpecialDayOut:
    output = SpecialDayOut(
        id = query[0],
        contact_id = query[1],
        name = query[2],
        date = query[3]
    )
    return output
