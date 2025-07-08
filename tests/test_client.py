import pytest
from youtrack.client import YouTrackClient, YouTrackError
import requests

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
        self._raise = status_code >= 400
        self.text = str(json_data)
    def json(self):
        return self._json
    def raise_for_status(self):
        if self._raise:
            raise requests.HTTPError("HTTP error", response=self)

@pytest.fixture
def client():
    return YouTrackClient(token="dummy", base_url="https://example.com")

def test_headers(client):
    headers = client._headers()
    assert headers["Authorization"].startswith("Bearer ")
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"

def test_handle_response_success(client):
    resp = DummyResponse({"ok": True})
    assert client._handle_response(resp) == {"ok": True}

def test_handle_response_error(client):
    resp = DummyResponse({"message": "fail"}, status_code=400)
    with pytest.raises(YouTrackError):
        client._handle_response(resp)

def test_init():
    c = YouTrackClient(token="abc", base_url="https://yt")
    assert c.token == "abc"
    assert c.base_url == "https://yt"
