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
    assert b"Home Page" in resp.data

def test_home(client):
    response = client.get('/')
    assert len(response.history) == 0
    assert response.request.path == "/"

def test_login(client):
    response = client.get('/login')
    # print(response.url)
    print(response.history)
    assert len(response.history) == 0
    assert response.request.path == "/login"

def test_about(client):
    response = client.get('/about')
    assert len(response.history) == 0
    assert response.request.path == "/about"

def test_pages(client):
    response = client.get('/pages')
    assert len(response.history) == 0
    assert response.request.path == "/pages"

def test_signup(client):
    response = client.get('/signup')
    assert len(response.history) == 0
    assert response.request.path == "/signup"
