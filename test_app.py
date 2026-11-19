import pytest
from app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["service"] == "shop-api"


def test_products_endpoint(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.get_json()) == 2
