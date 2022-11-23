from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.themes import (
    ThemeIn,
    ThemeOut,
    ThemesOut,
    ThemeRepository
)

router = APIRouter()

@router.post("/public/themes/", response_model = bool)
def create_public_themes(
    themes: List[ThemeIn],
    response: Response,
    repo: ThemeRepository = Depends()
    ) -> bool:
    success_flag = repo.create_public_themes(themes)
    return success_flag

@router.get("/public/themes/", response_model = ThemesOut)
def get_themes(
    response: Response,
    repo: ThemeRepository = Depends()
    ) -> ThemesOut:
    themes = repo.get_themes()
    return themes
