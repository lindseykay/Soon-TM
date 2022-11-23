from pydantic import BaseModel
from typing import Optional, Union, List
from queries.pools import pool
from queries.error import Error

class RecipientIn(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]
    user_id: Optional[int]


class RecipientOut(BaseModel):
    id: Optional[int]
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]


class RecipientRepository:
    def create(self, user_id: int, recipient: RecipientIn) -> Union[RecipientOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    check_exists = db.execute(
                        """
                        SELECT *
                        FROM recipients
                        WHERE recipients.name = %s
                        AND recipients.phone = %s
                        AND recipients.email = %s
                        AND recipients.user_id = %s
                        """,
                        [
                            recipient.name,
                            recipient.phone,
                            recipient.email,
                            user_id
                        ]
                    )
                    existing_recipient = check_exists.fetchone()
                    if existing_recipient:
                        return RecipientOut(
                            id = existing_recipient[0],
                            name = existing_recipient[1],
                            phone = existing_recipient[2],
                            email = existing_recipient[3]
                        )
                    result = db.execute(
                        """
                        INSERT INTO recipients(
                            name
                            , phone
                            , email
                            , user_id
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            recipient.name,
                            recipient.phone,
                            recipient.email,
                            user_id
                        ]
                    )
                    recipient_id = result.fetchone()[0]
                    input = recipient.dict()
                    input.pop("user_id")
                    return RecipientOut(id=recipient_id, **input)
        except Exception:
            return {"message": "create recipient record failed"}

    def update(self, user_id: int, reminder_id: int, recipient = RecipientOut) -> Union[RecipientOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        UPDATE recipients
                        SET name = COALESCE(%s, recipients.name)
                            , phone = COALESCE(%s, recipients.phone)
                            , email = COALESCE(%s, recipients.email)
                            FROM recipients AS rec
                            JOIN reminders_recipients_mapping_table as rrmt
                                on (rec.id = rrmt.recipient_id)
                            JOIN reminders as re
                                on (rrmt.reminder_id = re.id)
                        WHERE recipients.id = %s
                        AND re.id = %s
                        RETURNING recipients.id, recipients.name, recipients.phone, recipients.email;
                        """,
                        [
                            recipient.name,
                            recipient.phone,
                            recipient.email,
                            recipient.id,
                            reminder_id,
                        ]
                    )
                    query = result.fetchone()
                    return RecipientOut(
                        id = query[0],
                        name = query[1],
                        phone = query[2],
                        email = query[3]
                    )
        except Exception:
            return {"message": "update recipient record failed"}

    def get_all_by_user(self, user_id: int) -> Union[List[RecipientOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM recipients
                        WHERE user_id = %s
                        """,
                        [user_id]
                    )
                    query = result.fetchall()
                    return [RecipientOut(
                        id = record[0],
                        name = record[1],
                        phone = record[2],
                        email = record[3]
                    ) for record in query]
        except Exception:
            return {"message": "get_all_by_user recipient record failed"}
