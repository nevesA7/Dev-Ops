import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_api_stats_multi_sources(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert "series" in data
    assert "dolar" in data["series"]
    assert "euro" in data["series"]
    assert "bitcoin" in data["series"]
    assert "clima" in data["series"]

def test_healthz_endpoint(client):
    response = client.get('/healthz')
    assert response.status_code in [200, 503]