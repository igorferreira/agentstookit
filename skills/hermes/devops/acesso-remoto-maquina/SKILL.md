---
name: acesso-remoto-maquina
description: Use quando Usuário pedir acesso remoto à máquina via túnel.
category: devops
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ngrok, ssh, tailscale, termux, t3-code, tunel]
    related_skills: [public-preview, browser-act]
---

# Acesso remoto à máquina do Usuário

## When to Use
- Usuário pede acessar a máquina de casa do celular (Termux) ou de outro PC.
- Usuário pede liberar ngrok/túnel/URL pública para app local (T3 Code, dashboards, OpenBot).
- Usuário está fora de casa e precisa de terminal ou interface da máquina.

## Regras permanentes (sempre)
- TODO comando entregue ao Usuário vai em bloco de código isolado, UM COMANDO POR BLOCO, para ter botão de copiar no Telegram (Termux). Passos sequenciais = blocos separados. Se o botão não renderizar, mandar um bloco por mensagem até funcionar.
- Antes de entregar qualquer URL ao Usuário, TESTAR o caminho de ponta a ponta (banner/porta/HTTP 200) a partir da máquina. Nunca entregar túnel não verificado.
- Qualquer UI administrativa exposta via ngrok PRECISA de `--basic-auth "usuario:senha"`: em apps single-user, quem alcança a porta É o admin — túnel sem auth = admin público.
- Túnel ngrok do plano free morre a cada restart do processo/máquina e a porta é aleatória. Regenerar quando o Usuário pedir, mantendo um log persistente (--log /tmp/ngrok_*.log) para recuperar a URL atual.
- Tailscale é o caminho preferido quando disponível (IP fixo, sem porta pública); ngrok é o caminho quando o Usuário pede URL na hora.

## Procedimento A — acesso ao terminal via ngrok tcp (validado)
1. Subir o túnel em background: `ngrok tcp 22 --log /tmp/ngrok_ssh.log --log-format json`
2. Ler a URL do log (linha JSON `"msg":"started tunnel"`): `tcp://0.tcp.sa.ngrok.io:PORTA`.
3. VERIFICAR antes de entregar: o DNS local da máquina pode estar sob adblock/sinkhole e responder `0.0.0.0`/`::` para domínios ngrok — testar `getent hosts <domínio>`; se vier 0.0.0.0/::, resolver o IP real via DoH (`curl -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=<domínio>&type=A'`) e testar a conexão no IP direto. UDP 53 externo pode estar bloqueado (só o resolvedor local responde) — não insistir no dig direto.
4. Prova final: handshake SSH — `ssh -p PORTA -o BatchMode=yes -o StrictHostKeyChecking=no usuario@<IP>` deve retornar `Permission denied (publickey,password)` (chegou ao sshd; BatchMode não manda senha, a negativa é esperada).
5. Entregar ao Usuário (Termux):
   ```
   pkg install -y openssh
   ```
   ```
   ssh -p PORTA usuario@<IP-ou-domínio>
   ```

## Procedimento B — interface de app local (T3 Code etc.) no navegador do celular (validado)
Apps locais escutam em loopback (T3 Code: 127.0.0.1:3773); o caminho é túnel SSH do celular:
1. No celular, o túnel `-L` tem que rodar numa SESSÃO LOCAL do Termux (gaveta lateral → New session), NUNCA dentro da sessão SSH já aberta: o `-L` escuta no aparelho onde o comando roda, e dentro do SSH o listener nasceria na máquina (loop inútil).
2. Na sessão local:
   ```
   ssh -fN -p PORTA -L 3773:127.0.0.1:3773 usuario@<IP-ou-domínio>
   ```
3. Na máquina, gerar o código de pareamento (`t3 pair`) e entregar a URL `http://127.0.0.1:3773/pair#token=...` — ela expira em ~5 MINUTOS: gerar na hora da entrega, nunca adiantado. Usuário abre no navegador do próprio celular (o túnel já mapeia o 127.0.0.1 do celular).
- Pitfall: `bind [127.0.0.1]:3773: Address already in use` na 2ª tentativa = o túnel da 1ª tentativa ESTÁ no ar. Não é erro — informar sucesso.
- T3 Code: o serviço `t3 up --lan` falha com `ServerAlreadyRunningError` enquanto o app desktop é dono de ~/.t3/userdata. NÃO matar o desktop do Usuário para liberar o dono — o caminho validado é usar o servidor existente (loopback 3773) via túnel do passo 2.

## Procedimento C — Tailscale (preferido)
- Tailnet ativa com dois nós: `isfconsultpc` (100.93.59.85, a máquina) e `redmi-note-13` (Android). Pareamento = entrar com a MESMA conta em cada dispositivo novo; nada a configurar por device.
- SSH direto de qualquer nó: `ssh usuario@100.93.59.85`.
- `tailscale serve` (HTTPS na tailnet) exige operator/root: o Usuário roda UMA VEZ `sudo tailscale set --operator=usuario`; depois o CLI funciona sem sudo. Sem isso o comando trava em vez de falhar rápido — não interpretar o travamento como falha do túnel.

## Expor app web com allowlist de Host via ngrok
- Apps servidos por vite dev (ex.: OpenBot/OpenDuet em :3010) bloqueiam Host header que não seja localhost/loopback (403 'Blocked request'). O rewrite resolve sem patch no app: `ngrok http 3010 --host-header="localhost:3010" --basic-auth ...`. Se o app validar CORS/origem (TRUSTED_ORIGINS, BETTER_AUTH_URL), acrescentar a URL https do ngrok nessas variáveis e reiniciar o processo do app.
