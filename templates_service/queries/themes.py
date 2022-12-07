from pydantic import BaseModel
from queries.pools import conn
from typing import List, Optional

class TemplateOut(BaseModel):
    id: int
    public: bool
    theme_id: Optional[int]
    user_id: Optional[int]
    name: str
    content: str


class ThemeIn(BaseModel):
    name: str
    picture_url: str


class ThemeOut(BaseModel):
    id: int
    name: str
    picture_url: str
    templates: List[TemplateOut]


class ThemesOut(BaseModel):
    themes: List[ThemeOut]


class ThemeRepository:
    def create_public_themes(self, themes: List[ThemeIn]) -> bool:
        try:
                with conn.cursor() as db:
                    names = [theme.name for theme in themes]
                    picture_urls = [theme.picture_url for theme in themes]
                    db.execute(
                        """
                        INSERT INTO themes
                            (name, picture_url)
                        VALUES
                            (UNNEST(CAST(%s AS TEXT[])), UNNEST(CAST(%s AS TEXT[])))
                        """,
                        [
                            names,
                            picture_urls
                        ]
                    )
                    return True
        except Exception:
            return False

    def get_themes(self) -> ThemesOut:
        try:
                with conn.cursor() as db:
                    results = db.execute(
                        """
                        SELECT *
                        FROM themes th
                        LEFT JOIN templates AS te
                        ON th.id = te.theme_id
                        ORDER BY th.id
                        """
                    )
                    query = results.fetchall()
                    tdict = {}
                    for record in query:
                        if record[0] not in tdict:
                            tdict[record[0]] = ThemeOut(
                                id = record[0],
                                name = record[1],
                                picture_url = record[2],
                                templates = [] if not record[3] else [TemplateOut(
                                    id = record[3],
                                    public = record[4],
                                    theme_id = record[5],
                                    user_id = record[6],
                                    name = record[7],
                                    content = record[8]
                                )]
                            )
                        else:
                            if record[3]:
                                tdict[record[0]].templates.append(TemplateOut(
                                        id = record[3],
                                        public = record[4],
                                        theme_id = record[5],
                                        user_id = record[6],
                                        name = record[7],
                                        content = record[8]
                                    ))
                    return ThemesOut(
                        themes = list(tdict.values())
                    )
        except Exception:
            return None
