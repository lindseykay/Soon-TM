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
                        insert into users
                            (username, password, email, name)
                        values
                            (%s, %s, %s, %s)
                        returning id;
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

    def get(self, user_id) -> Union[UserOut,UserError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        select id, username, email, name
                        from users
                        where id = %s;
                        """,
                        [
                            user_id
                        ]
                    )
                    query = result.fetchone()
                    return self.user_query_to_userout(query)
        except Exception:
            return {"message": "We'll get em next time"}

    def user_query_to_userout(self, query) -> UserOut:
        return UserOut(
            id=query[0],
            username=query[1],
            email=query[2],
            name=query[3]
        )
