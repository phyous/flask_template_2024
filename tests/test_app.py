import pytest
from src.app import app
from src.models import Base, engine, SessionLocal

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Create tables
        Base.metadata.create_all(bind=engine)
        yield client
        # Drop tables after tests
        Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post('/users', json={
        "email": "test@example.com",
        "name": "Test User"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data
    assert "created_at" in data

def test_get_user(client):
    # First create a user
    create_response = client.post('/users', json={
        "email": "test@example.com",
        "name": "Test User"
    })
    user_id = create_response.get_json()["id"]
    
    # Then get the user
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"

def test_get_nonexistent_user(client):
    response = client.get('/users/999')
    assert response.status_code == 404