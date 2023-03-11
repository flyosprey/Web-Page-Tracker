import json
import pytest
import requests_mock

from app import create_app


URL = "https://www.muibu.com/"
URL_EXAMPLE_1 = "https://www.muibu.com/1"
URL_EXAMPLE_2 = "https://www.muibu.com/2"
URL_EXAMPLE_3 = "https://www.muibu.com/3"
URL_EXAMPLE_4 = "https://www.muibu.com/4"
URL_EXAMPLE_5 = "https://www.muibu.com/5"
PAYLOAD = {"domain": "www.muibu.com"}
MOCK_TEXT = f"""<html><head><title>Example</title></head><body><h1>Test HTML domain</h1>
                <a href={URL_EXAMPLE_1}"></a><a href="{URL_EXAMPLE_1}"></a>
                <a href="{URL_EXAMPLE_2}"></a><a href="{URL_EXAMPLE_2}"></a>
                <a href="{URL_EXAMPLE_3}"></a>
                <a href="{URL_EXAMPLE_4}"></a><a href="{URL_EXAMPLE_5}"></a>
                </body></html>"""


@pytest.fixture
def mock_api_response_200_with_200():
    with requests_mock.Mocker() as mock:
        mock.get(URL, text=MOCK_TEXT, status_code=200)
        mock.get(URL_EXAMPLE_1, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_2, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_3, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_4, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_5, text=MOCK_TEXT)
        yield mock


@pytest.fixture
def mock_api_response_302_with_200():
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=302, headers={'Location': URL_EXAMPLE_1})
        mock.get(URL_EXAMPLE_1, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_2, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_3, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_4, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_5, text=MOCK_TEXT)
        yield mock


@pytest.fixture
def mock_api_response_302_with_404():
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=302, headers={'Location': URL_EXAMPLE_1})
        mock.get(URL_EXAMPLE_1, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_2, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_3, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_4, text=MOCK_TEXT, status_code=404)
        mock.get(URL_EXAMPLE_5, text=MOCK_TEXT, status_code=404)
        yield mock


@pytest.fixture
def mock_api_response_200_with_404():
    with requests_mock.Mocker() as mock:
        mock.get(URL, status_code=200, headers={'Location': URL})
        mock.get(URL_EXAMPLE_1, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_2, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_3, text=MOCK_TEXT)
        mock.get(URL_EXAMPLE_4, text=MOCK_TEXT, status_code=404)
        mock.get(URL_EXAMPLE_5, text=MOCK_TEXT, status_code=404)
        yield mock


def test_domain_parser_with_200(mock_api_response_200_with_200):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/stats', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["active_page_count"] == 6
        assert json_response["total_page_count"] == 6
        assert len(json_response["url_list"]) == json_response["total_page_count"]


def test_domain_parser_with_302(mock_api_response_302_with_200):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/stats', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["active_page_count"] == 6
        assert json_response["total_page_count"] == 6
        assert len(json_response["url_list"]) == json_response["total_page_count"]


def test_domain_parser_with_404(mock_api_response_302_with_404):
    app = create_app()
    with app.test_client() as client:
        response = client.post('/stats', data=json.dumps(PAYLOAD), content_type='application/json')
        json_response = response.json

        assert response.status_code == 200
        assert json_response["active_page_count"] == 4
        assert json_response["total_page_count"] == 6
        assert len(json_response["url_list"]) == json_response["total_page_count"]

