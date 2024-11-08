from io import BytesIO
from unittest.mock import patch

import pytest
from src.app import app


BASE_FILE = "src.app"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_no_file_in_request(client):
    response = client.post("/classify_file")
    assert response.status_code == 400


def test_no_selected_file(client):
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400


@patch(f"{BASE_FILE}.DOC_CLASSIFICATION")
@patch(f"{BASE_FILE}.get_text_from_file")
def test_success(mock_get_text, mock_doc_classification, client):
    mock_doc_classification.predict.return_value = "test_class"
    mock_get_text.return_value = "dummy content"

    data = {"file": (BytesIO(b"dummy content"), "file.pdf")}
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "test_class"}
