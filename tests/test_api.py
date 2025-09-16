import pytest
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Очистка после тестов
    if os.path.exists('data.db'):
        os.remove('data.db')

def test_full_flow(client):
    # Регистрация
    resp = client.post('/auth/register', json={'username': 'testuser', 'password': 'testpass'})
    assert resp.status_code == 201
    
    # Логин
    resp = client.post('/auth/login',json={'username': 'testuser', 'password': 'testpass'})
    assert resp.status_code == 200
    token = resp.json['token']
    
    # Добавление item
    resp = client.post('/api/items',json={'item': 'test item'},headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 201
    
    # Получение items
    resp = client.get('/api/items',headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    assert 'test item' in resp.json

def test_sqli_protection(client):
    # Регистрация и логин
    client.post('/auth/register', json={'username': 'testuser', 'password': 'testpass'})
    resp = client.post('/auth/login',иjson={'username': 'testuser', 'password': 'testpass'})
    token = resp.json['token']
    
    # Попытка SQL-инъекции
    malicious_input = "test'; DROP TABLE items; --"
    resp = client.post('/api/items',json={'item': malicious_input},headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 201
    
    # Проверяем что таблица не была удалена
    resp = client.get('/api/items',headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
