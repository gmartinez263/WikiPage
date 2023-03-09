from flaskr import create_app
from bs4 import BeautifulSoup


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

def test_home(client):
    response = client.get('/')
    assert len(response.history) == 0
    assert response.request.path == "/"

def test_login_unsuccessful(client):
    # Assuming valid username and password
    response = client.post('/login', data={'Usrname': 'fake_username', 'Password': 'fake_password'})
    redirect = client.get('/')
    soup = BeautifulSoup(redirect.data, 'html.parser')
    visible_text = soup.get_text()
    assert response.status_code == 200
    assert  not 'fake_username' in visible_text


def test_login_successful(client):
    # Assuming valid username and password
    response = client.post('/login', data={'Usrname': 'ale_pagan', 'Password': 'Alejan7901'})
    redirect = client.get("/")
    soup = BeautifulSoup(redirect.data, 'html.parser')
    visible_text = soup.get_text()
    assert response.status_code == 302
    assert  'ale_pagan' in visible_text

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

