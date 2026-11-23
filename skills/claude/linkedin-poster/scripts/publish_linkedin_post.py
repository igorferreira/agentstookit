#!/usr/bin/env python3
"""Publish a post to LinkedIn via the official REST API (personal profile only).

Safety: runs in --dry-run mode by default. Nothing is sent to LinkedIn unless
--publish is passed explicitly.

Usage:
    python3 publish_linkedin_post.py --text "post text" [--image PATH] [--publish]
        [--credentials PATH]
"""
import argparse
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_CREDENTIALS_PATH = Path(__file__).parent / ".credentials.json"
# LinkedIn-Version header (YYYYMM). LinkedIn updates this monthly — confirm the current
# value at https://learn.microsoft.com/en-us/linkedin/marketing/versioning before the
# first real publish, and update this constant if it has moved on.
LINKEDIN_VERSION = "202601"
API_BASE = "https://api.linkedin.com/rest"


class LinkedInAPIError(RuntimeError):
    pass


def load_credentials(path: Path) -> dict:
    if not path.exists():
        raise LinkedInAPIError(
            f"Nenhuma credencial encontrada em {path}. Rode linkedin_oauth_setup.py primeiro."
        )
    data = json.loads(path.read_text())
    for key in ("access_token", "person_urn", "expires_at"):
        if key not in data:
            raise LinkedInAPIError(f"Credencial incompleta: falta '{key}' em {path}")
    if data["expires_at"] < time.time():
        raise LinkedInAPIError(
            "Token de acesso do LinkedIn expirado. Rode linkedin_oauth_setup.py novamente "
            "para reautorizar (tokens de member auth do LinkedIn duram até 60 dias)."
        )
    return data


def build_text_post_payload(author_urn: str, text: str) -> dict:
    return {
        "author": author_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }


def build_image_post_payload(author_urn: str, text: str, image_urn: str) -> dict:
    payload = build_text_post_payload(author_urn, text)
    payload["content"] = {"media": {"id": image_urn}}
    return payload


def _http_request(method: str, url: str, headers: dict, body: bytes | None = None) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _auth_headers(access_token: str, extra: dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }
    if extra:
        headers.update(extra)
    return headers


def initialize_image_upload(access_token: str, author_urn: str) -> dict:
    url = f"{API_BASE}/images?action=initializeUpload"
    body = json.dumps({"initializeUploadRequest": {"owner": author_urn}}).encode("utf-8")
    status, resp_body = _http_request("POST", url, _auth_headers(access_token), body)
    if status not in (200, 201):
        raise LinkedInAPIError(f"Falha ao iniciar upload de imagem ({status}): {resp_body!r}")
    data = json.loads(resp_body)["value"]
    return {"upload_url": data["uploadUrl"], "image_urn": data["image"]}


def upload_image_bytes(upload_url: str, image_bytes: bytes, content_type: str) -> None:
    status, resp_body = _http_request(
        "PUT", upload_url, {"Content-Type": content_type}, image_bytes
    )
    if status not in (200, 201):
        raise LinkedInAPIError(f"Falha ao enviar bytes da imagem ({status}): {resp_body!r}")


def publish_post(access_token: str, payload: dict) -> dict:
    url = f"{API_BASE}/posts"
    body = json.dumps(payload).encode("utf-8")
    status, resp_body = _http_request("POST", url, _auth_headers(access_token), body)
    if status not in (200, 201):
        raise LinkedInAPIError(f"Falha ao publicar post ({status}): {resp_body!r}")
    return {"status": status, "body": resp_body.decode("utf-8") if resp_body else ""}


def run(text: str, image_path, publish: bool, credentials_path: Path) -> dict:
    creds = load_credentials(credentials_path)
    access_token = creds["access_token"]
    author_urn = creds["person_urn"]

    image_urn = None
    if image_path:
        img_path = Path(image_path)
        if not img_path.exists():
            raise LinkedInAPIError(f"Imagem não encontrada: {image_path}")
        content_type = mimetypes.guess_type(img_path.name)[0] or "application/octet-stream"
        if publish:
            upload = initialize_image_upload(access_token, author_urn)
            upload_image_bytes(upload["upload_url"], img_path.read_bytes(), content_type)
            image_urn = upload["image_urn"]
        else:
            image_urn = "urn:li:image:DRY_RUN_PLACEHOLDER"

    payload = (
        build_image_post_payload(author_urn, text, image_urn)
        if image_urn
        else build_text_post_payload(author_urn, text)
    )

    if not publish:
        return {"dry_run": True, "payload": payload}

    result = publish_post(access_token, payload)
    return {"dry_run": False, "payload": payload, "result": result}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, help="Texto final do post")
    parser.add_argument("--image", default=None, help="Caminho de uma imagem opcional")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publica de verdade. Sem essa flag, roda em modo dry-run (nada é enviado).",
    )
    parser.add_argument(
        "--credentials",
        default=str(DEFAULT_CREDENTIALS_PATH),
        help="Caminho do arquivo de credenciais (default: .credentials.json ao lado do script)",
    )
    args = parser.parse_args(argv)

    try:
        result = run(args.text, args.image, args.publish, Path(args.credentials))
    except LinkedInAPIError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    if result["dry_run"]:
        print("[DRY RUN] Nenhuma chamada de rede foi feita. Payload que seria enviado:")
        print(json.dumps(result["payload"], indent=2, ensure_ascii=False))
    else:
        print("Post publicado com sucesso.")
        print(json.dumps(result["result"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
