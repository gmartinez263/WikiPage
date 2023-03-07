from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data

def test_home():
    response = client.get('/')

    assert len(response.history) == 1
    assert response.request.path == "/"

def test_login():
    response = client.get('/login')

    assert len(response.history) == 1
    assert response.request.path == "/login"

def test_about():
    response = client.get('/about')

    assert len(response.history) == 1
    assert response.request.path == "/about"

def test_pages():
    response = client.get('/pages')

    assert len(response.history) == 1
    assert response.request.path == "/pages"

def test_signup():
    response = client.get('/signup')

    assert len(response.history) == 1
    assert response.request.path == "/signup"
