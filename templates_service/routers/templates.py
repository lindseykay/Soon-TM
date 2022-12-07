from fastapi import APIRouter, Depends, Response
from typing import List, Union, Optional
from queries.templates import (
    PublicTemplateIn,
    TemplateIn,
    TemplateUpdate,
    TemplateOut,
    TemplatesOut,
    TemplateError,
    TemplateRepository,
)

from jwtdown_fastapi.authentication import Authenticator
import os


class MyAuthenticator(Authenticator):
    async def get_account_data(self, username: str, accounts):
        pass

    def get_account_getter(self, accounts):
        pass

    def get_hashed_password(self, account):
        pass

    def get_account_data_for_cookie(self, account):
        pass


authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])


router = APIRouter()


@router.post(
    "/public/templates/",
    response_model=Union[List[TemplateOut], TemplateError],
)
def create_public_templates(
    templates: List[PublicTemplateIn],
    response: Response,
    repo: TemplateRepository = Depends(),
) -> List[TemplateOut]:
    new_public_templates = repo.create_public_templates(templates)
    return new_public_templates


@router.post("/templates", response_model=Union[TemplateOut, TemplateError])
def create_template(
    template: TemplateIn,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: TemplateRepository = Depends(),
) -> TemplateOut:
    new_template = repo.create_user_template(template, account_data["id"])
    return new_template


@router.get("/templates", response_model=Union[TemplatesOut, TemplateError])
def get_all_templates(
    response: Response,
    repo: TemplateRepository = Depends(),
    account_data: Optional[dict] = Depends(
        authenticator.try_get_current_account_data
    ),
) -> TemplatesOut:
    if account_data:
        all_templates = repo.get_all(account_data["id"])
        return all_templates
    all_templates = repo.get_all(None)
    return all_templates


@router.get(
    "/templates/{template_id}",
    response_model=Union[TemplateOut, TemplateError],
)
def get_template(
    template_id: int,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: TemplateRepository = Depends(),
) -> TemplatesOut:
    template = repo.get_template(template_id, account_data["id"])
    return template


@router.put(
    "/templates/{template_id}",
    response_model=Union[TemplateOut, TemplateError],
)
def update_template(
    template_id: int,
    info: TemplateUpdate,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: TemplateRepository = Depends(),
) -> TemplateOut:
    updated_template = repo.update_template(
        template_id, account_data["id"], info
    )
    return updated_template


@router.delete("/templates/{template_id}", response_model=bool)
def delete_template(
    template_id: int,
    response: Response,
    account_data: dict = Depends(authenticator.get_current_account_data),
    repo: TemplateRepository = Depends(),
) -> bool:
    deleted_flag = repo.delete_template(template_id, account_data["id"])
    return deleted_flag
