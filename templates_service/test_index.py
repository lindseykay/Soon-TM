from fastapi.testclient import TestClient
from main import app
from queries.templates import TemplateRepository

client = TestClient(app)

class GetAllTemplatesRepository:
    def get_all(self, user_id):
        return {
            "public_templates": {
                "themes": []
            },
            "user_templates": []
        }

def test_get_all_templates():

    app.dependency_overrides[TemplateRepository] = GetAllTemplatesRepository


    expected = {
            "public_templates": {
                "themes": []
            },
            "user_templates": []
        }
    response = client.get("/templates")

    assert response.status_code == 200
    assert response.json() == expected

    app.dependency_overrides = {}


class CreatePublicTempRepo:
    def create_public_templates(self, templates):
        result = [{
            "id": 1,
            "public": True,
            "theme_id": template.theme_id,
            "user_id": None,
            "name": template.name,
            "content": template.content
        } for template in templates]
        return result

def test_create_public_templates():

    app.dependency_overrides[TemplateRepository] = CreatePublicTempRepo

    input = [
        {
            "theme_id": 0,
            "name": "string",
            "content": "string"
        }
        ]

    expected = [
        {
            "id": 1,
            "public": True,
            "theme_id": 0,
            "user_id": None,
            "name": "string",
            "content": "string"
        }
        ]

    response = client.post("/public/templates/", json=input)

    assert response.status_code == 200
    assert response.json() == expected

    app.dependency_overrides = {}
