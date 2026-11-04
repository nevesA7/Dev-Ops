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
    assert b"Dashboard" in response.data

def test_api_stats(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_visits" in data
    assert "visits_per_minute" in data
    assert "recent_visits" in data

def test_healthz_endpoint(client):
    response = client.get('/healthz')
    assert response.status_code in [200, 503]