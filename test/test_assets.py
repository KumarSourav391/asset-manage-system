import pytest
from entrypoint import create_app
from extensions import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
    yield app.test_client()

def test_create_asset(client):
    response = client.post('/api/assets', json={
        "name": "Test",
        "service_time": "2025-01-01",
        "expiration_time": "2026-01-01"
    })
    assert response.status_code == 201

def test_get_assets(client):
    client.post('/api/assets', json={
        "name": "A",
        "service_time": "2025-01-01",
        "expiration_time": "2026-01-01"
    })
    response = client.get('/api/assets')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_asset(client):
    resp = client.post('/api/assets', json={
        "name": "B",
        "service_time": "2025-01-01",
        "expiration_time": "2026-01-01"
    })
    assert resp.status_code == 201

    asset_id = resp.get_json()["id"]

    response = client.patch(f'/api/assets/{asset_id}', json={"serviced": True})
    assert response.status_code == 200
    assert response.get_json()["serviced"] is True

def test_run_checks(client):
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    soon = now + timedelta(minutes=10)
    past = now - timedelta(minutes=1)

    client.post('/api/assets', json={
        "name": "Soon",
        "service_time": soon.isoformat(),
        "expiration_time": soon.isoformat()
    })
    client.post('/api/assets', json={
        "name": "Past",
        "service_time": past.isoformat(),
        "expiration_time": past.isoformat()
    })

    response = client.post('/api/run-checks')
    assert response.status_code == 200
