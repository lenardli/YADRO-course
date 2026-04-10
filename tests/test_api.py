from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from presentation.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_info_returns_expected_fields(client: TestClient) -> None:
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0.0"
    assert data["service"] == "currency"
    assert data["author"] == "a.sheynova"
    assert set(data.keys()) == {"version", "service", "author"}


@patch("infrastructure.presenters.api_presenter.urlopen")
def test_currency_info_uses_mocked(mock_urlopen: MagicMock, client: TestClient) -> None:
    xml = b"""<?xml version="1.0" encoding="windows-1251"?>
    <ValCurs>
      <Valute ID="1">
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Value>90,50</Value>
      </Valute>
    </ValCurs>"""
    mock_response = MagicMock()
    mock_response.read.return_value = xml
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_response
    mock_ctx.__exit__.return_value = None
    mock_urlopen.return_value = mock_ctx

    response = client.get("/info/currency?currency=usd")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "currency"
    assert data["data"]["USD"] == 90.5
