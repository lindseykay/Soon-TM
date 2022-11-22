from pydantic import BaseModel
from typing import Optional, Union, List
from queries.pools import pool
from queries.error import Error


class RecipientIn(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]


class RecipientOut(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]


class RecipientRepository:
    def create(self, recipient: RecipientIn) -> Union[RecipientOut, Error]:
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
                        """,
                        [
                            recipient.name,
                            recipient.phone,
                            recipient.email
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
                    print("IS THIS RESULT PRINTING????????????", result)
                    query = result.fetchone()
                    return RecipientOut(
                        id = query[0],
                        name = query[1],
                        phone = query[2],
                        email = query[3]
                    )



        except Exception:
            return {"message": "update recipient record failed"}
