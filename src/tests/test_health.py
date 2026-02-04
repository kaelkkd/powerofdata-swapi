from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check(): #teste de health
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["healthy", "degraded"]
    assert "service" in data
    assert data["service"] == "star-wars-api"


def test_root(): #teste da raiz
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "version" in data


def test_get_people_list(): #teste para a listagem de pessoas
    response = client.get("/people?page=1")

    assert response.status_code == 200
    data = response.json()

    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    if data["results"]:
        person = data["results"][0]
        assert "id" in person
        assert "name" in person
