from pydantic import BaseModel
from typing import List, Optional, Union
from queries.pools import pool

class UserError(BaseModel):
    message: str

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    name: str

class UserUpdate(BaseModel):
    password: Optional[str]
    email: Optional[str]
    name: Optional[str]

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    name: str

class UserRepository:
    def create(self, user: UserIn) -> Union[UserOut,UserError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO users
                            (username, password, email, name)
                        VALUES
                            (%s, %s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            user.username,
                            user.password,
                            user.email,
                            user.name
                        ]
                    )
                    id = result.fetchone()[0]
                    input = user.dict()
                    input.pop("password")
                    return UserOut(id=id, **input)
        except Exception:
            return {"message": "We'll get em next time"}

    def get(self, user_id: int) -> Union[UserOut,UserError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT id, username, email, name
                        FROM users
                        WHERE id = %s;
                        """,
                        [
                            user_id
                        ]
                    )
                    query = result.fetchone()
                    return self.user_query_to_userout(query)
        except Exception:
            return {"message": "Tough luck"}

    def user_query_to_userout(self, query: tuple) -> UserOut:
        return UserOut(
            id=query[0],
            username=query[1],
            email=query[2],
            name=query[3]
        )

    def update(self, user_id: int, user: UserUpdate) -> Union[UserOut,UserError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        UPDATE users
                        SET password = COALESCE(%s, password)
                            , email = COALESCE(%s, email)
                            , name = COALESCE(%s, name)
                        WHERE id = %s
                        RETURNING id, username, email, name;
                        """,
                        [
                            user.password,
                            user.email,
                            user.name,
                            user_id
                        ]
                    )
                    query = result.fetchone()
                    return self.user_query_to_userout(query)
        except Exception:
            return {"message": "Skill diff"}
