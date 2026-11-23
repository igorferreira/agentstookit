---
name: envio-de-comandos
description: Use ao enviar comandos executáveis ao Igor.
---

# Envio de comandos ao Igor

Regra canônica definida pelo Igor (espelhada em ~/MEGA/Regras/comunicacao.md): toda mensagem que tiver comando para executar precisa ter o comando em bloco de código copiável — com botão de copiar no Telegram.

## Regras (sempre)

- **Um comando por bloco de código.** Nunca comando solto no meio de texto corrido — o botão de copiar só aparece por bloco, e Igor não copia blocos individuais de uma mensagem com vários.
- Passos sequenciais dependentes: entregar **um por vez, numerados na conversa**, e aguardar a confirmação antes do próximo quando o resultado de um muda o comando seguinte (porta de túnel, URL, token, sessão criada).
- Caminhos/paths que serão colados numa UI (campo "Open folder" de IDE, formulário) também vão em bloco — a mecânica de copiar/colar é a mesma.
- Se o Telegram não renderizar o botão de copiar, enviar **um bloco por mensagem** até funcionar.
- Comando com placeholder sensível (senha, chave) nunca vai no bloco com valor real colado pelo assistente — instruir onde o Igor digita o valor (terminal pede senha, campo de formulário, .env).

## Por quê

Igor executa no Termux (Redmi Note 13) ou no desktop e cola sem revisar; bloco copiável elimina erro de transcrição de caractere — pontos, underscores e espaços somem quando o comando vem dentro de texto corrido ou de instrução paragrafada.