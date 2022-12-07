from pydantic import BaseModel
from typing import Optional, Union
from queries.pools import conn

class DuplicateAccountError(BaseModel):
    pass

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

class UserOutWithPassword(UserOut):
    hashed_password: str

class UserRepository:
    def create(self, user: UserIn, hashed_password: str) -> Union[UserOut,UserError]:
        try:
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
                            hashed_password,
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

    def get_by_userid(self, user_id: int) -> Union[UserOut,UserError]:
        try:
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

    def get_by_username(self, username: str) -> Union[UserOutWithPassword,UserError]:
        try:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT id, username, email, name, password
                        FROM users
                        WHERE username = %s;
                        """,
                        [
                            username
                        ]
                    )
                    query = result.fetchone()
                    return UserOutWithPassword(
                        id = query[0],
                        username = query[1],
                        email = query[2],
                        name = query[3],
                        hashed_password = query[4]
                    )

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
