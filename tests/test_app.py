import sys
sys.path.insert(0, 'src')
from app import app
def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
def test_add_task():
    client = app.test_client()
    response = client.post('/tasks', json={"title": "Test"})
    assert response.status_code == 201
    assert "id" in response.json
def test_fail_intentional():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
