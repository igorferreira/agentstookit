#!/usr/bin/env python3
"""One-time interactive OAuth setup for LinkedIn's official personal-profile posting API.

Requires a LinkedIn Developer app with the "Share on LinkedIn" product added (Open Permission
self-serve — no partner approval needed for posting to your own profile). Run this once; it
writes .credentials.json next to this script.

Usage:
    python3 linkedin_oauth_setup.py --client-id ID --client-secret SECRET
"""
import argparse
import http.server
import json
import secrets
import stat
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

from publish_linkedin_post import LinkedInAPIError, _http_request

REDIRECT_PORT = 8765
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/callback"
SCOPES = "openid profile w_member_social"
CREDENTIALS_PATH = Path(__file__).parent / ".credentials.json"


def build_authorization_url(client_id: str, redirect_uri: str, state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": SCOPES,
    }
    return "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(params)


def exchange_code_for_token(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict:
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    status, resp_body = _http_request(
        "POST", "https://www.linkedin.com/oauth/v2/accessToken", headers, body
    )
    if status != 200:
        raise LinkedInAPIError(f"Falha ao trocar código por token ({status}): {resp_body!r}")
    return json.loads(resp_body)


def fetch_person_urn(access_token: str) -> str:
    headers = {"Authorization": f"Bearer {access_token}"}
    status, resp_body = _http_request(
        "GET", "https://api.linkedin.com/v2/userinfo", headers
    )
    if status != 200:
        raise LinkedInAPIError(f"Falha ao buscar identidade do usuário ({status}): {resp_body!r}")
    data = json.loads(resp_body)
    return f"urn:li:person:{data['sub']}"


def _wait_for_callback_code(expected_state: str) -> str:
    """Spin up a local HTTP server to capture LinkedIn's OAuth redirect and return the code."""
    captured = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if qs.get("state", [None])[0] != expected_state:
                self.send_response(400)
                self.end_headers()
                return
            captured["code"] = qs.get("code", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Autorizado! Pode fechar esta aba e voltar ao terminal.")

        def log_message(self, *args):
            pass  # silence default request logging

    server = http.server.HTTPServer(("localhost", REDIRECT_PORT), Handler)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    thread.join(timeout=300)
    server.server_close()
    if "code" not in captured or captured["code"] is None:
        raise LinkedInAPIError("Timeout ou state inválido esperando o redirect do LinkedIn.")
    return captured["code"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    args = parser.parse_args(argv)

    state = secrets.token_urlsafe(16)
    auth_url = build_authorization_url(args.client_id, REDIRECT_URI, state)
    print("Abrindo o navegador para você autorizar o app no LinkedIn...")
    print(auth_url)
    webbrowser.open(auth_url)

    code = _wait_for_callback_code(state)
    token_data = exchange_code_for_token(args.client_id, args.client_secret, code, REDIRECT_URI)
    person_urn = fetch_person_urn(token_data["access_token"])

    creds = {
        "access_token": token_data["access_token"],
        "person_urn": person_urn,
        "expires_at": time.time() + token_data.get("expires_in", 5184000),
    }
    CREDENTIALS_PATH.write_text(json.dumps(creds, indent=2))
    CREDENTIALS_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)
    print(f"Credenciais salvas em {CREDENTIALS_PATH} (permissão 600).")
    print(f"Identidade confirmada: {person_urn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
