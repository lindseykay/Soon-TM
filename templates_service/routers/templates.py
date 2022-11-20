from fastapi import APIRouter, Depends, Response
from typing import List, Optional, Union
from queries.templates import (
    PublicTemplateIn,
    TemplateIn,
    TemplateUpdate,
    TemplateOut,
    TemplatesOut,
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
    new_template = repo.create_user_template(template, user_id)
    return new_template


@router.get("/templates", response_model = Union[TemplatesOut,TemplateError])
def get_all_templates(
    response: Response,
    repo: TemplateRepository = Depends(),
    user_id: int = None
    ) -> TemplatesOut:
    all_templates = repo.get_all(user_id)
    return all_templates


@router.get("/templates/{template_id}", response_model = Union[TemplateOut,TemplateError])
def get_template(
    template_id: int,
    user_id: int,
    response: Response,
    repo: TemplateRepository = Depends(),
    ) -> TemplatesOut:
    template = repo.get_template(template_id, user_id)
    return template


@router.put("/templates/{template_id}", response_model = Union[TemplateOut,TemplateError])
def update_template(
    template_id: int,
    user_id: int,
    info: TemplateUpdate,
    response: Response,
    repo: TemplateRepository = Depends()
    ) -> TemplateOut:
    updated_template = repo.update_template(template_id, user_id, info)
    return updated_template


@router.delete("/templates/{template_id}", response_model = bool)
def delete_template(
    template_id: int,
    user_id: int,
    response: Response,
    repo: TemplateRepository = Depends()
    ) -> bool:
    deleted_flag = repo.delete_template(template_id, user_id)
    return deleted_flag
