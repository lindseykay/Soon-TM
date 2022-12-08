from pydantic import BaseModel
from typing import Optional, Union

# from queries.pools import conn
from queries.error import Error
import os
from psycopg import connect


class MessageIn(BaseModel):
    template_id: Optional[int]
    content: str


class MessageOut(BaseModel):
    id: int
    template_id: Optional[int]
    content: str


DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    kwargs = {"autocommit": True}
    return connect(conninfo=DATABASE_URL, **kwargs)


class MessageRepository:
    def create(self, message: MessageIn) -> Union[MessageOut, Error]:
        try:
            conn = get_conn()
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
                    [message.template_id, message.content],
                )
                id = result.fetchone()[0]
                input = message.dict()
                print("this is the message input in the message repo:", input)
                return MessageOut(id=id, **input)
        except Exception:
            return {"message": "create message record failed"}

    def update(
        self, reminder_id: int, message: MessageIn
    ) -> Union[MessageIn, Error]:
        try:
            conn = get_conn()
            with conn.cursor() as db:
                result = db.execute(
                    """
                        UPDATE messages
                        SET template_id = COALESCE(%s, template_id)
                            ,   content = COALESCE(%s, content)
                        WHERE id = %s
                        RETURNING template_id, content
                        """,
                    [
                        message.template_id,
                        message.content,
                        reminder_id,
                    ],
                )
            conn.close()
            query = result.fetchone()

            return MessageIn(template_id=query[0], content=query[1])
        except Exception:
            return {"message": "update message record failed"}

    def get_one(self, message_id: int) -> Union[MessageOut, Error]:
        try:
            conn = get_conn()
            with conn.cursor() as db:
                result = db.execute(
                    """
                        SELECT *
                        FROM messages
                        WHERE id = %s
                        """,
                    [message_id],
                )
            conn.close()
            query = result.fetchone()
            return MessageOut(
                id=query[0], template_id=query[1], content=query[2]
            )
        except Exception:
            return {"message": "get message record failed"}
