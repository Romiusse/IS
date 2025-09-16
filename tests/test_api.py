import pytest
import json
import os
import sys
from pathlib import Path
from werkzeug.security import generate_password_hash

sys.path.append(str(Path(__file__).parent.parent))

os.environ['FLASK_SECRET_KEY'] = 'test-secret-key'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

@pytest.fixture
def app():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        from app.database import get_db
        db = get_db()
        db.execute("DELETE FROM users")
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ('testuser', generate_password_hash('testpass'))
        )
        db.commit()
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    response = client.post(
        '/auth/login',
        data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
        content_type='application/json'
    )
    return json.loads(response.data)['token']

def test_register(client):
    response = client.post(
        '/auth/register',
        data=json.dumps({'username': 'newuser', 'password': 'newpass'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_login(client):
    response = client.post(
        '/auth/login',
        data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert 'token' in json.loads(response.data)

def test_protected_endpoint(client, auth_token):
    response = client.post(
        '/api/items',
        data=json.dumps({'item': 'test data'}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    
    response = client.get(
        '/api/items',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert b'test data' in response.data

def test_sqli_protection(client, auth_token):
    response = client.post(
        '/api/items',
        data=json.dumps({'item': "test'; DROP TABLE items; --"}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    
    response = client.get(
        '/api/items',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
