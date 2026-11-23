#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Driver CDP generico para Chrome clonado (porta 9224) — Glassdoor, LinkedIn e sites logados.

Uso no execute_code:
    import sys
    sys.path.insert(0, <diretorio desta skill>/scripts)
    from cdp_extractor import navigate, eval_js, tab_by_url, main_text, scroll, new_tab

Requer: websockets >= 14 (argumento open_timeout, NAO timeout).
Gotcha do kernel: depois de patchar este arquivo, 'del sys.modules["cdp_extractor"]'
antes de importar de novo (o kernel cachia modulos importados).
"""
import asyncio
import json
import urllib.request

CDP = "http://127.0.0.1:9224"


async def _send(ws, _id, method, params):
    await ws.send(json.dumps({"id": _id, "method": method, "params": params}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == _id:
            return msg


async def _cmd(tab_id, method, params, timeout=30):
    tabs = json.loads(urllib.request.urlopen(f"{CDP}/json/list", timeout=5).read())
    tab = next(t for t in tabs if t.get("id") == tab_id)
    import websockets
    async with websockets.connect(tab["webSocketDebuggerUrl"], open_timeout=timeout,
                                  max_size=50 * 1024 * 1024) as ws:
        return await _send(ws, 1, method, params)


def eval_js(tab_id, expr, timeout=30):
    """Avalia expressao JS na aba (expr deve ser IIFE '(() => {...})()')."""
    msg = asyncio.run(_cmd(tab_id, "Runtime.evaluate",
        {"expression": expr, "returnByValue": True, "awaitPromise": True}, timeout))
    r = msg.get("result", {})
    exc = r.get("exceptionDetails")
    if exc:
        return {"_exc": exc.get("exception", {}).get("description", str(exc))[:300]}
    return r.get("result", {}).get("value")


def navigate(tab_id, url, timeout=40):
    return asyncio.run(_cmd(tab_id, "Page.navigate", {"url": url}, timeout))


def tab_by_url(substr):
    """Acha aba existente cujo URL contenha substr (evita abrir abas duplicadas)."""
    tabs = json.loads(urllib.request.urlopen(f"{CDP}/json/list", timeout=5).read())
    for t in tabs:
        if t.get("type") == "page" and substr in t.get("url", ""):
            return t
    return None


def new_tab(url):
    """Abre nova aba (PUT /json/new) e devolve o dict do alvo."""
    req = urllib.request.Request(f"{CDP}/json/new?{url}", method="PUT")
    return json.loads(urllib.request.urlopen(req, timeout=5).read())


def main_text(tab_id, limit=30000):
    """innerText do main (fallback body) — sidebar do Glassdoor/LinkedIn polui body."""
    return eval_js(tab_id,
        f"(() => {{ const m = document.querySelector('main'); "
        f"return (m ? m.innerText : document.body.innerText).slice(0, {limit}); }})()")


def scroll(tab_id, n=4, step=3000):
    eval_js(tab_id, f"(() => {{ for (let i=0;i<{n};i++){{ window.scrollBy(0, {step}); }} "
                     f"return document.body.scrollHeight; }})()")
