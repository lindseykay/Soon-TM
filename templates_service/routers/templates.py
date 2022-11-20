from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.templates import (
    PublicTemplateIn,
    TemplateIn,
    TemplateOut,
    TemplateError,
    TemplateRepository,
    ThemeOut
)

router = APIRouter()

### FOR CREATION OF PUBLIC TEMPLATES, API ENDPOINT NOT TO BE CALLED ON FRONT END
@router.post("/public/templates/", response_model = Union[List[TemplateOut],TemplateError])
def create_public_templates(
    templates: List[PublicTemplateIn],
    response: Response,
    repo: TemplateRepository = Depends()
    ) -> List[TemplateOut]:
    new_public_templates = repo.create_public_templates(templates)
    return new_public_templates


@router.post("/templates", response_model = Union[TemplateOut,TemplateError])
def create_template(
    template: TemplateIn,
    user_id: int,
    response: Response,
    repo: TemplateRepository = Depends()
    ) -> TemplateOut:
    pass


@router.get("/templates", response_model = Union[List[TemplateOut],TemplateError])
def get_all_templates(
    response: Response,
    repo: TemplateRepository = Depends(),
    user_id: int = None
    ) -> List[TemplateOut]:
    pass
