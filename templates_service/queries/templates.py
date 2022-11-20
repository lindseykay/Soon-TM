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
    user_id: int
    name: str
    content: str

class TemplateOut(BaseModel):
    id: int
    public: bool
    theme_id: Optional[int]
    user_id: Optional[int]
    name: str
    content: str

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

    def create_user_template(self, template: TemplateIn) -> Union[TemplateOut,TemplateError]:
        pass

    def get_all(self, user_id: int) -> Union[List[TemplateOut],TemplateError]:
        pass

    def get_template(self, template_id: int, user_id: int) -> Union[TemplateOut,TemplateError]:
        pass
