import json
from unittest.mock import patch

import linkedin_oauth_setup as mod


def test_build_authorization_url_contains_required_params():
    url = mod.build_authorization_url(
        client_id="abc", redirect_uri="http://localhost:8765/callback", state="xyz"
    )
    assert url.startswith("https://www.linkedin.com/oauth/v2/authorization?")
    assert "client_id=abc" in url
    assert "state=xyz" in url
    assert "redirect_uri=http%3A%2F%2Flocalhost%3A8765%2Fcallback" in url
    assert "scope=" in url


def test_exchange_code_for_token_parses_response():
    fake_response = json.dumps({"access_token": "tok123", "expires_in": 5184000}).encode()
    with patch.object(mod, "_http_request", return_value=(200, fake_response)) as mock_http:
        result = mod.exchange_code_for_token(
            client_id="abc",
            client_secret="secret",
            code="authcode",
            redirect_uri="http://localhost:8765/callback",
        )
    assert result["access_token"] == "tok123"
    assert result["expires_in"] == 5184000
    mock_http.assert_called_once()


def test_fetch_person_urn_builds_urn_from_userinfo():
    fake_response = json.dumps({"sub": "abc123XYZ"}).encode()
    with patch.object(mod, "_http_request", return_value=(200, fake_response)):
        urn = mod.fetch_person_urn("tok123")
    assert urn == "urn:li:person:abc123XYZ"
