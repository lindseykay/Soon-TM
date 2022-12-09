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