# Fallback: drive the user's real Chrome via raw CDP

Use when the harness browser is stuck on a bot challenge (Cloudflare/Turnstile) or a login wall that the user's own Chrome already passes. The user's Chrome clone (a `--user-data-dir` copy of their default profile, kept for CDP work) has the real fingerprint and cookies — it navigates bot-protected pages without a challenge.

## Find the endpoint

```bash
ss -tlnp | grep -E '92(22|24|25)' ; pgrep -a chrome | grep -o 'remote-debugging-port=[0-9]*'
```

The clone runs on its own port (often 9224). Confirm the port is alive before scripting; it can be down.

## Open a page and extract (Python, `websockets` lib)

```python
import asyncio, json, subprocess, websockets

def open_tab(url):
    r = subprocess.run(['curl','-s','-X','PUT',f'http://127.0.0.1:9224/json/new?{url}'],capture_output=True,text=True)
    return json.loads(r.stdout)['id']            # GET /json/new is rejected in modern Chrome — use PUT

async def cdp(ws, method, params=None, id=[0]):
    id[0] += 1
    await ws.send(json.dumps({'id': id[0], 'method': method, 'params': params or {}}))
    while True:
        m = json.loads(await ws.recv())
        if m.get('id') == id[0]: return m.get('result', m)

async def main():
    tab = open_tab('https://example.com/page')
    async with websockets.connect(f'ws://127.0.0.1:9224/devtools/page/{tab}', max_size=50*1024*1024) as ws:
        await asyncio.sleep(10)                   # let the page settle
        await cdp(ws, 'Page.navigate', {'url': <url>})
        for _ in range(4):                        # scroll to load lazy content
            await cdp(ws, 'Runtime.evaluate', {'expression': 'window.scrollBy(0,2000)', 'returnByValue': True})
            await asyncio.sleep(1.2)
        ev = await cdp(ws, 'Runtime.evaluate',
            {'expression': '(document.querySelector("main")||document.body).innerText', 'returnByValue': True})
        print(ev['result']['value'])
        shot = await cdp(ws, 'Page.captureScreenshot', {'format': 'png'})
        open('/tmp/shot.png','wb').write(__import__('base64').b64decode(shot['data']))
asyncio.run(main())
```

`document.body.innerText` includes huge sidebar noise on portal-style sites — scope to a content container (`main`, a `data-testid`) or slice from a known heading.

## Gotchas

- **List targets first** (`curl -s http://127.0.0.1:9224/json`): tabs, OOPIF iframes, and `browser_ui` omnibox popups all appear; only `type: "page"` entries with the right URL are work targets.
- **Pagination that exists as `_P2.htm`-style links may be an SPA no-op** — navigating to page-2 URLs can return page-1 content. Check whether the extracted text actually changed (compare hashes) before collecting "more pages".
- **Login via the user's SSO**: click the "Entrar com Google"-style button and expect a `accounts.google.com` tab to open. A 2-step-verification notification lands on the user's phone — ask them to approve it. Stop at any password field.
- **Do not enter credentials ever**; SSO continuation with an already-signed-in session is the maximum extent.
- **Check the login state after the SSO tab closes**: the accounts tab disappears on success; verify the original tab shows the signed-in header (e.g. user initials) before harvesting logged-in data.
- This route keeps the user's cookies/profile untouched; nothing is typed into forms except SSO buttons.
