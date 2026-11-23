import time
import json
import pytest
from pathlib import Path
from unittest.mock import patch

import publish_linkedin_post as mod
from publish_linkedin_post import (
    build_text_post_payload,
    build_image_post_payload,
    load_credentials,
    LinkedInAPIError,
)


def test_build_text_post_payload_shape():
    payload = build_text_post_payload("urn:li:person:abc123", "Hello LinkedIn")
    assert payload["author"] == "urn:li:person:abc123"
    assert payload["commentary"] == "Hello LinkedIn"
    assert payload["visibility"] == "PUBLIC"
    assert payload["lifecycleState"] == "PUBLISHED"
    assert "content" not in payload


def test_build_image_post_payload_includes_media():
    payload = build_image_post_payload(
        "urn:li:person:abc123", "Look at this", "urn:li:image:xyz"
    )
    assert payload["content"]["media"]["id"] == "urn:li:image:xyz"
    assert payload["commentary"] == "Look at this"


def test_load_credentials_missing_file(tmp_path):
    missing = tmp_path / "nope.json"
    with pytest.raises(LinkedInAPIError, match="Nenhuma credencial"):
        load_credentials(missing)


def test_load_credentials_expired(tmp_path):
    creds_path = tmp_path / "creds.json"
    creds_path.write_text(json.dumps({
        "access_token": "tok",
        "person_urn": "urn:li:person:abc123",
        "expires_at": time.time() - 3600,
    }))
    with pytest.raises(LinkedInAPIError, match="expirado"):
        load_credentials(creds_path)


def test_load_credentials_valid(tmp_path):
    creds_path = tmp_path / "creds.json"
    creds_path.write_text(json.dumps({
        "access_token": "tok",
        "person_urn": "urn:li:person:abc123",
        "expires_at": time.time() + 3600,
    }))
    creds = load_credentials(creds_path)
    assert creds["access_token"] == "tok"


def _write_valid_creds(tmp_path):
    creds_path = tmp_path / "creds.json"
    creds_path.write_text(json.dumps({
        "access_token": "tok",
        "person_urn": "urn:li:person:abc123",
        "expires_at": time.time() + 3600,
    }))
    return creds_path


def test_run_dry_run_text_only_makes_no_network_call(tmp_path):
    creds_path = _write_valid_creds(tmp_path)
    with patch.object(mod, "_http_request") as mock_http:
        result = mod.run("Hello", None, False, creds_path)
    mock_http.assert_not_called()
    assert result["dry_run"] is True
    assert result["payload"]["commentary"] == "Hello"
    assert "content" not in result["payload"]


def test_run_dry_run_with_image_uses_placeholder_and_no_network_call(tmp_path):
    creds_path = _write_valid_creds(tmp_path)
    fake_image = tmp_path / "photo.jpg"
    fake_image.write_bytes(b"fake-bytes")
    with patch.object(mod, "_http_request") as mock_http:
        result = mod.run("Look", str(fake_image), False, creds_path)
    mock_http.assert_not_called()
    assert result["payload"]["content"]["media"]["id"] == "urn:li:image:DRY_RUN_PLACEHOLDER"


def test_run_missing_image_raises(tmp_path):
    creds_path = _write_valid_creds(tmp_path)
    with pytest.raises(LinkedInAPIError, match="Imagem não encontrada"):
        mod.run("Hello", str(tmp_path / "nope.jpg"), False, creds_path)


def test_run_publish_calls_publish_post_with_built_payload(tmp_path):
    creds_path = _write_valid_creds(tmp_path)
    with patch.object(mod, "publish_post", return_value={"status": 201, "body": "{}"}) as mock_pub:
        result = mod.run("Hello", None, True, creds_path)
    mock_pub.assert_called_once()
    called_access_token, called_payload = mock_pub.call_args[0]
    assert called_access_token == "tok"
    assert called_payload["commentary"] == "Hello"
    assert result["dry_run"] is False
    assert result["result"]["status"] == 201
