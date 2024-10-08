import pytest
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', data=dict(
        username='testuser', password='password', confirm_password='password'
    ), follow_redirects=True)
    assert b'Registration successful' in response.data

def test_login_logout(client):
    client.post('/register', data=dict(
        username='testuser', password='password', confirm_password='password'
    ))
    response = client.post('/login', data=dict(
        username='testuser', password='password'
    ), follow_redirects=True)
    assert b'Welcome, testuser' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data
