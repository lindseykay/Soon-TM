from pydantic import BaseModel
from typing import Optional, Union
from queries.pools import pool
from queries.error import Error


class MessageIn(BaseModel):
    template_id: Optional[int]
    content: str


class MessageOut(BaseModel):
    id: int
    template_id: Optional[int]
    content: str


class MessageRepository:
    def create(self, message: MessageIn) -> Union[MessageOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO messages(
                            template_id
                            , content
                        )
                        VALUES (%s, %s)
                        RETURNING id;
                        """,
                        [
                            message.template_id,
                            message.content
                        ]
                    )
                    id = result.fetchone()[0]
                    input = message.dict()
                    return MessageOut(id=id, **input)
        except Exception:
            return {"message": "create message record failed"}