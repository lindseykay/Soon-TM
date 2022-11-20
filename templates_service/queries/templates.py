from pydantic import BaseModel
from queries.pools import pool
from typing import List, Optional, Union

class ThemeOut(BaseModel):
    id: int
    name: str
    picture_url: str

class PublicTemplateIn(BaseModel):
    theme_id: int
    name: str
    content: str

class TemplateIn(BaseModel):
    name: str
    content: str

class TemplateUpdate(BaseModel):
    name: Optional[str]
    content: Optional[str]

class TemplateOut(BaseModel):
    id: int
    public: bool
    theme_id: Optional[int]
    user_id: Optional[int]
    name: str
    content: str

class TemplatesOut(BaseModel):
    public_templates: List[TemplateOut]
    user_templates: List[TemplateOut]

class TemplateError(BaseModel):
    message: str

class TemplateRepository:
    def create_public_templates(self, templates: List[PublicTemplateIn]) -> Union[List[TemplateOut],TemplateError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    themes = [template.theme_id for template in templates]
                    names = [template.name for template in templates]
                    contents = [template.content for template in templates]

                    result = db.execute(
                        """
                        INSERT INTO templates
                            (public, theme_id, name, content)
                        VALUES
                            (%s, unnest(cast(%s as int[])), unnest(cast(%s as text[])), unnest(cast(%s as text[])))
                        RETURNING *;
                        """,
                        [
                            True,
                            themes,
                            names,
                            contents
                        ]
                    )
                    query = result.fetchall()

                    output = [TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]) for record in query]
                    return output

        except Exception:
            return {"message": "My disappointment is immeasurable and my day is ruined"}

    def create_user_template(self, template: TemplateIn, user_id: int) -> Union[TemplateOut,TemplateError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO templates
                            (public, user_id, name, content)
                        VALUES
                            (%s, %s, %s, %s)
                        RETURNING *;
                        """,
                        [
                            False,
                            user_id,
                            template.name,
                            template.content
                        ]
                    )
                    record = result.fetchone()
                    print(record)

                    output = TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]
                    )
                    return output

        except Exception:
            return {"message": "My disappointment is immeasurable and my day is ruined"}

    def get_all(self, user_id: Optional[int]) -> Union[TemplatesOut,TemplateError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM templates
                        WHERE user_id = %s OR user_id IS NULL
                        ORDER BY public DESC
                        """,
                        [
                            user_id
                        ]
                    )
                    query = result.fetchall()

                    public_templates = [TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]) for record in query if record[1]]
                    user_templates = [] if not user_id else [TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]) for record in query if not record[1]]

                    return TemplatesOut(
                        public_templates = public_templates,
                        user_templates = user_templates
                    )

        except Exception:
            return {"message": "My disappointment is immeasurable and my day is ruined"}

    def get_template(self, template_id: int, user_id: int) -> Union[TemplateOut,TemplateError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM templates
                        WHERE user_id = %s AND id = %s
                        """,
                        [
                            user_id,
                            template_id
                        ]
                    )
                    record = result.fetchone()

                    return TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]
                    )
        except Exception:
            return {"message": "My disappointment is immeasurable and my day is ruined"}

    def update_template(self, template_id: int, user_id: int, info: TemplateUpdate) -> Union[TemplateOut, TemplateError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        UPDATE templates
                        SET name = COALESCE(%s, name)
                            , content = COALESCE(%s, content)
                        WHERE user_id = %s AND id = %s
                        RETURNING *;
                        """,
                        [
                            info.name,
                            info.content,
                            user_id,
                            template_id
                        ]
                    )
                    record = result.fetchone()

                    return TemplateOut(
                        id = record[0],
                        public = record[1],
                        theme_id = record[2],
                        user_id = record[3],
                        name = record[4],
                        content = record[5]
                    )
        except Exception:
            return {"message": "My disappointment is immeasurable and my day is ruined"}

    def delete_template(self, template_id: int, user_id: int) -> bool:
        try:
            if not user_id:
                return False

            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM templates
                        where user_id = %s AND id = %s
                        """,
                        [
                            user_id,
                            template_id
                        ]
                    )
                    return True
        except Exception:
            return False
