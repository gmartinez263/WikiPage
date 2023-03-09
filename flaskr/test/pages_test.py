from flaskr import create_app
from backend import Backend
import unittest.mock as mock
from bs4 import BeautifulSoup
import json


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


def test_about(client):
    response = client.get('/about')
    assert len(response.history) == 0
    assert response.request.path == "/about"

def test_pages(client):
    response = client.get('/pages')
    assert len(response.history) == 0
    assert response.request.path == "/pages"

def test_signup_unsuccessful(client):
    response = client.post('/signup',data={"Usrname":"ale_pagan","Password":"Alejan7901"}) #this user already exists
    soup = BeautifulSoup(response.data, 'html.parser')
    visible_text = soup.get_text()
    assert response.status_code == 200
    assert "Signup failed! Please select another username." in visible_text 

def test_signup_successful(client):
    with mock.patch.object(Backend, 'sign_up') as mock_save_user_data:
        # Assuming valid username and password
        response = client.post('/signup', data={"Usrname": "pedro", "Password": "432"})

        # Check that the function to save user data was called with the correct arguments
        mock_save_user_data.assert_called_once_with("pedro", "432")

    # Replace the mock object with a real object
    response.data = json.dumps({'message': 'Signup successful'}).encode('utf-8')

    # Check that the server redirected to the homepage after successful signup
    redirect = client.get("/")
    soup = BeautifulSoup(redirect.data, 'html.parser')
    visible_text = soup.get_text()
    assert response.status_code == 302
    assert "pedro" in visible_text

