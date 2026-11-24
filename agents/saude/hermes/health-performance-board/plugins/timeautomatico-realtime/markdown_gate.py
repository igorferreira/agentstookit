"""Gate determinístico de Markdown externo — conteúdo nunca ganha autoridade."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

MAX_BYTES = 1_048_576
ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff]")
SUSPICIOUS = {
    "instruction_override": re.compile(r"(?i)(ignore|disregard|forget).{0,40}(instruction|system|previous)"),
    "authority_claim": re.compile(r"(?i)(system prompt|developer message|you are now|role\s*:)"),
    "tool_directive": re.compile(r"(?i)(call|execute|run|invoke).{0,30}(tool|terminal|shell|sudo)"),
    "secret_request": re.compile(r"(?i)(api[_ -]?key|token|password|credential|\.env|config\.yaml)"),
    "active_markup": re.compile(r"(?is)<\s*(script|iframe|object|embed|form)\b|javascript\s*:"),
    "dangerous_shell": re.compile(r"(?i)\b(rm\s+-rf|curl\s+[^\n]*\|\s*(sh|bash)|wget\s+[^\n]*\|\s*(sh|bash))\b"),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _emit(callback: Callable[..., None] | None, event_type: str, **fields: Any) -> None:
    if callback:
        callback(event_type, **fields)


def inspect_markdown(source: str, emit: Callable[..., None] | None = None) -> dict[str, Any]:
    """Quarentena, normaliza e analisa. Nunca devolve conteúdo bruto ao agente."""
    source_path = Path(source).expanduser().resolve(strict=True)
    file_id = str(uuid.uuid4())
    _emit(emit, "file.received", fileId=file_id, activity="Markdown externo recebido")

    if not source_path.is_file() or source_path.suffix.lower() not in {".md", ".markdown"}:
        _emit(emit, "file.blocked", fileId=file_id, activity="Tipo de arquivo não permitido")
        return {"verdict": "BLOCKED", "fileId": file_id, "reason": "tipo não permitido"}
    size = source_path.stat().st_size
    if size > MAX_BYTES:
        _emit(emit, "file.blocked", fileId=file_id, activity="Arquivo excede 1 MiB")
        return {"verdict": "BLOCKED", "fileId": file_id, "reason": "arquivo grande demais"}

    root = Path.home() / ".cache" / "timeautomatico" / "markdown-gate" / file_id
    quarantine = root / "quarantine"
    sanitized_dir = root / "sanitized"
    quarantine.mkdir(parents=True, mode=0o700)
    sanitized_dir.mkdir(parents=True, mode=0o700)
    quarantined = quarantine / "source.md"
    shutil.copyfile(source_path, quarantined)
    os.chmod(quarantined, 0o400)
    _emit(emit, "file.quarantined", fileId=file_id, activity="Cópia imutável em quarentena")

    raw = quarantined.read_text(encoding="utf-8", errors="strict")
    normalized = unicodedata.normalize("NFKC", ZERO_WIDTH.sub("", raw)).replace("\r\n", "\n").replace("\r", "\n")
    _emit(emit, "file.scanning", fileId=file_id, activity="Static scan e normalização")

    findings = []
    for rule, pattern in SUSPICIOUS.items():
        for match in pattern.finditer(normalized):
            findings.append({"rule": rule, "line": normalized.count("\n", 0, match.start()) + 1})
            if len(findings) >= 100:
                break

    verdict = "SAFE_WITH_WARNINGS" if not findings else "MANUAL_REVIEW"
    # Sanitização de exibição, não de confiança: neutraliza tags e bidi; não executa Markdown/HTML.
    safe_text = normalized.replace("<", "&lt;").replace(">", "&gt;")
    sanitized = sanitized_dir / "content.txt"
    sanitized.write_text(safe_text, encoding="utf-8")
    os.chmod(sanitized, 0o400)

    manifest = {
        "schemaVersion": 1,
        "fileId": file_id,
        "receivedAt": _now(),
        "sourceName": source_path.name,
        "sha256": hashlib.sha256(quarantined.read_bytes()).hexdigest(),
        "sizeBytes": size,
        "verdict": verdict,
        "securityStatus": "UNTRUSTED_EXTERNAL_CONTENT",
        "authorityGranted": False,
        "findings": findings,
        "taint": {"fileId": file_id, "chunkId": None, "lineStart": 1, "lineEnd": normalized.count("\n") + 1},
        "sanitizedDisplayPath": str(sanitized),
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(manifest_path, 0o400)

    if verdict == "MANUAL_REVIEW":
        _emit(emit, "file.blocked", fileId=file_id, activity="Aguardando revisão humana/segurança")
    else:
        _emit(emit, "file.approved", fileId=file_id, activity="Liberado somente como dado não confiável")
    return manifest
