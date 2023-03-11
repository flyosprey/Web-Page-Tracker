import json
import pytest
import requests_mock
from requests.exceptions import RequestException

from app import create_app


URL = "https://www.muibu.com/"
REDIRECTED_URL = "https://hashanalytic.com/about/"
PAYLOAD = {"url": URL}
MOCK_TEXT = "<html><head><title>Example</title></head><body><h1>Test HTML page</h1></body></html>"


@pytest.fixture
def mock_api_response_200():
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=MOCK_TEXT, status_code=200)
        yield mock


@pytest.fixture
def mock_api_response_302():
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=302, headers={'Location': REDIRECTED_URL})
        mock.get(REDIRECTED_URL, text=MOCK_TEXT)
        yield mock


@pytest.fixture
def mock_api_response_404():
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=MOCK_TEXT, status_code=404)
        yield mock


@pytest.fixture
def mock_api_response_with_exception():
    with requests_mock.Mocker() as mock:
        mock.get(URL, exc=RequestException("Error: Could not connect to server"))
        yield mock


def test_page_200_parser_200(mock_api_response_200):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/pages', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["status_code"] == 200
        assert json_response["title"] == "Example"
        assert json_response["domain_name"] == "www.muibu.com"
        assert json_response["final_status_code"] is None
        assert json_response["final_url"] == PAYLOAD["url"]


def test_page_200_parser_404(mock_api_response_404):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/pages', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["status_code"] == 404
        assert json_response["title"] == "Example"
        assert json_response["domain_name"] == "www.muibu.com"
        assert json_response["final_status_code"] is None
        assert json_response["final_url"] == URL


def test_page_200_parser_302(mock_api_response_302):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/pages', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["status_code"] == 302
        assert json_response["title"] == "Example"
        assert json_response["domain_name"] == "hashanalytic.com"
        assert json_response["final_status_code"] == 200
        assert json_response["final_url"] == REDIRECTED_URL


def test_page_404_parser_error(mock_api_response_with_exception):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/pages', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 404
        assert json_response["status"] == "Not Found"
        assert json_response.get("status_code") is None
        assert json_response.get("title") is None
        assert json_response.get("domain_name") is None
        assert json_response.get("final_status_code") is None
        assert json_response.get("final_url") is None
