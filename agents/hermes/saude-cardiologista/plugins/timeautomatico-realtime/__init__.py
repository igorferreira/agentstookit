"""Plugin oficial Hermes → TimeAutomatico realtime.

Publica apenas metadados de lifecycle. Nunca grava prompt, argumentos, resultados,
respostas, reasoning ou segredos. Eventos carregam ``origin=hermes-plugin``.
"""

from __future__ import annotations

import json
import hashlib
import hmac
import os
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .markdown_gate import inspect_markdown

PLUGIN_NAME = "timeautomatico-realtime"
OFFICE_ID = "banca-saude"
CACHE_DIR = Path.home() / ".cache" / "timeautomatico"
EVENTS_PATH = CACHE_DIR / "events.jsonl"
PRODUCERS_DIR = CACHE_DIR / "producers"
SECRET_PATH = Path(os.environ.get("TIMEAUTOMATICO_REALTIME_SECRET", CACHE_DIR / "realtime.key"))
_PROCESS_ID = os.getpid()
_SESSION_AGENT: dict[str, str] = {}
_CHILD_AGENT: dict[str, str] = {}
_HEARTBEAT_STARTED = False

MARKDOWN_GATE_SCHEMA = {
    "name": "timeautomatico_markdown_gate",
    "description": "Coloca um Markdown externo em quarentena e devolve apenas metadados/veredito; nunca concede autoridade ao conteúdo.",
    "parameters": {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "Caminho local do arquivo .md ou .markdown"}},
        "required": ["path"],
    },
}

PROFILE_TO_AGENT = {
    "saude": "angelica",
    "saude-master": "angelica",
    "health-performance-board": "angelica",
    "saude-endocrinologista": "duda",
    "saude-clinico-geral": "duda",
    "saude-nutrologo": "paulinho",
    "saude-cardiologista": "vesna",
    "saude-reumatologista": "rita",
    "saude-ortopedista": "rita",
}

SPECIALTY_RULES = (
    (re.compile(r"\b(exame|laborator|horm|endocrin)", re.I), "duda"),
    (re.compile(r"\b(nutri|dieta|aliment|composi[cç][aã]o corporal)", re.I), "paulinho"),
    (re.compile(r"\b(cardio|cora[cç][aã]o|press[aã]o|lip[ií]d)", re.I), "vesna"),
    (re.compile(r"\b(reumat|articula|inflama|ortoped)", re.I), "rita"),
    (re.compile(r"\b(aws|infra|ferramenta|tool)", re.I), "oswaldo"),
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _secret() -> bytes | None:
    try:
        value = SECRET_PATH.read_bytes().strip()
        return value if len(value) >= 32 else None
    except OSError:
        return None


def _sign(payload: dict[str, Any]) -> bool:
    secret = _secret()
    if not secret:
        return False
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["auth"] = hmac.new(secret, data, hashlib.sha256).hexdigest()
    return True


def _profile() -> str:
    try:
        from hermes_cli.profiles import get_active_profile_name
        return get_active_profile_name() or "default"
    except Exception:
        return "default"


def _explicit_health_request(message: Any) -> bool:
    text = str(message or "").lstrip().lower()
    return text.startswith(("saude", "saúde"))


def _agent_for_session(session_id: str = "", user_message: Any = None) -> str | None:
    # A correlação explícita da sessão prevalece sobre o perfil do processo.
    # Isso evita atribuir chamadas de um subagente à coordenadora Angélica.
    if session_id in _CHILD_AGENT:
        return _CHILD_AGENT[session_id]
    if session_id in _SESSION_AGENT:
        return _SESSION_AGENT[session_id]
    profile_agent = PROFILE_TO_AGENT.get(_profile())
    if profile_agent:
        return profile_agent
    if _profile() == "default" and _explicit_health_request(user_message):
        return "angelica"
    return None


def _append(event_type: str, agent_id: str | None = None, **fields: Any) -> None:
    """Append atômico de evento curto, sem payload sensível."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    event = {
        "v": 1,
        "eventId": str(uuid.uuid4()),
        "timestamp": _now(),
        "officeId": OFFICE_ID,
        "agentId": agent_id,
        "type": event_type,
        "origin": "hermes-plugin",
        "producer": PLUGIN_NAME,
        "producerPid": _PROCESS_ID,
        "profile": _profile(),
        **{k: v for k, v in fields.items() if v not in (None, "")},
    }
    if not _sign(event):
        return
    data = (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    fd = os.open(EVENTS_PATH, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def _write_heartbeat() -> None:
    PRODUCERS_DIR.mkdir(parents=True, exist_ok=True)
    path = PRODUCERS_DIR / f"producer-{_PROCESS_ID}.json"
    payload = {
        "origin": "hermes-plugin",
        "plugin": PLUGIN_NAME,
        "pid": _PROCESS_ID,
        "profile": _profile(),
        "heartbeatAt": _now(),
    }
    if not _sign(payload):
        return
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)


def _heartbeat_loop() -> None:
    while True:
        try:
            _write_heartbeat()
        except Exception:
            pass
        time.sleep(5)


def _start_heartbeat() -> None:
    global _HEARTBEAT_STARTED
    if _HEARTBEAT_STARTED:
        return
    _HEARTBEAT_STARTED = True
    threading.Thread(target=_heartbeat_loop, name="ta-realtime-heartbeat", daemon=True).start()


def _session_key(kwargs: dict[str, Any]) -> str:
    return str(kwargs.get("session_id") or kwargs.get("task_id") or "")


def on_pre_llm_call(*, session_id: str = "", user_message: Any = None, **kwargs: Any) -> None:
    agent = _agent_for_session(session_id, user_message)
    if not agent:
        return
    _SESSION_AGENT[session_id] = agent
    _append("banca.started", taskId=session_id, activity="Pedido real recebido pelo Hermes")
    _append("agent.thinking", agent, taskId=session_id, status="thinking", activity="Analisando pedido real")


def on_post_llm_call(*, session_id: str = "", **kwargs: Any) -> None:
    agent = _agent_for_session(session_id)
    if not agent:
        return
    _append("agent.completed", agent, taskId=session_id, status="completed", activity="Resposta real concluída")
    _append("banca.completed", taskId=session_id, activity="Turno real concluído")


def on_pre_tool_call(*, tool_name: str = "", session_id: str = "", task_id: str = "", **kwargs: Any) -> None:
    key = session_id or task_id
    agent = _agent_for_session(key)
    if not agent:
        return
    # Oswaldo representa a execução real de ferramentas/infra, nunca simulação.
    _SESSION_AGENT[key] = agent
    _append("agent.tool.started", "oswaldo", taskId=key, status="tool_call", tool=tool_name, activity=f"Executando {tool_name}")


def on_post_tool_call(*, tool_name: str = "", session_id: str = "", task_id: str = "", status: str = "", **kwargs: Any) -> None:
    key = session_id or task_id
    if not _agent_for_session(key):
        return
    if status in {"error", "blocked"}:
        _append("agent.error", "oswaldo", taskId=key, status="error", tool=tool_name, activity=f"Falha em {tool_name}")
    else:
        _append("agent.tool.completed", "oswaldo", taskId=key, status="thinking", tool=tool_name, activity=f"{tool_name} concluída")


def on_api_error(*, session_id: str = "", task_id: str = "", **kwargs: Any) -> None:
    key = session_id or task_id
    agent = _agent_for_session(key)
    if agent:
        _append("agent.error", agent, taskId=key, status="error", activity="Erro real na chamada do modelo")


def _classify_specialty(goal: Any) -> str | None:
    text = str(goal or "")[:1000]
    for pattern, agent in SPECIALTY_RULES:
        if pattern.search(text):
            return agent
    return None


def on_subagent_start(*, parent_session_id: Any = None, child_session_id: Any = None,
                      child_goal: Any = None, **kwargs: Any) -> None:
    parent = str(parent_session_id or "")
    if not _agent_for_session(parent):
        return
    child_agent = _classify_specialty(child_goal)
    if not child_agent:
        return
    child = str(child_session_id or uuid.uuid4())
    _CHILD_AGENT[child] = child_agent
    _append("agent.delegated", "angelica", taskId=parent, status="delegating", to=child_agent,
            activity=f"Delegando para {child_agent}")
    _append("agent.task.started", child_agent, taskId=child, status="working", delegatedBy="angelica",
            activity="Subagente real iniciado")


def on_subagent_stop(*, child_session_id: Any = None, child_status: Any = None, **kwargs: Any) -> None:
    child = str(child_session_id or "")
    agent = _CHILD_AGENT.pop(child, None)
    if not agent:
        return
    failed = str(child_status or "").lower() not in {"completed", "success", "ok"}
    _append("agent.error" if failed else "agent.completed", agent, taskId=child,
            status="error" if failed else "completed",
            activity="Subagente real falhou" if failed else "Subagente real concluiu")


def on_session_end(*, session_id: str = "", completed: bool = False, failed: bool = False, **kwargs: Any) -> None:
    agent = _SESSION_AGENT.pop(session_id, None)
    if not agent:
        return
    succeeded = bool(completed) and not bool(failed)
    _append("agent.completed" if succeeded else "agent.error", agent, taskId=session_id,
            status="completed" if succeeded else "error",
            activity="Turno real encerrado" if succeeded else "Turno real falhou ou foi interrompido")


def markdown_gate_tool(args: dict[str, Any], **kwargs: Any) -> str:
    path = str(args.get("path") or "").strip()
    if not path:
        return json.dumps({"verdict": "BLOCKED", "reason": "path obrigatório"}, ensure_ascii=False)
    try:
        result = inspect_markdown(path, emit=lambda event_type, **fields: _append(event_type, **fields))
    except (OSError, UnicodeError, ValueError) as exc:
        return json.dumps({"verdict": "BLOCKED", "reason": type(exc).__name__}, ensure_ascii=False)
    # Conteúdo bruto/sanitizado não retorna ao LLM; só metadados e caminho auditável.
    public = {key: value for key, value in result.items() if key != "sanitizedDisplayPath"}
    return json.dumps(public, ensure_ascii=False)


def register(ctx) -> None:
    _start_heartbeat()
    ctx.register_hook("pre_llm_call", on_pre_llm_call)
    ctx.register_hook("post_llm_call", on_post_llm_call)
    ctx.register_hook("pre_tool_call", on_pre_tool_call)
    ctx.register_hook("post_tool_call", on_post_tool_call)
    ctx.register_hook("api_request_error", on_api_error)
    ctx.register_hook("on_session_end", on_session_end)
    ctx.register_hook("subagent_start", on_subagent_start)
    ctx.register_hook("subagent_stop", on_subagent_stop)
    ctx.register_tool(
        name="timeautomatico_markdown_gate",
        toolset="file",
        schema=MARKDOWN_GATE_SCHEMA,
        handler=markdown_gate_tool,
        emoji="🛡️",
    )
