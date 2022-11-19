from pydantic import BaseModel
from typing import Optional, Union
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