# Igor — formato de mensagens para WhatsApp

## Correção de 13/08/2026

Igor pediu explicitamente:

> "Toda vez q eu te pedir uma resposta por whatsapp melhor vc colocar em formato texto com o botão de copiar"

## Implementação

- Envolver cada mensagem pronta em um bloco cercado com a linguagem `text`.
- Manter fora do bloco qualquer explicação destinada somente a Igor.
- Se houver alternativas, usar um bloco por alternativa.
- O texto copiado deve continuar usando apenas formatação compatível com WhatsApp.

## Exemplo

````markdown
**Mensagem pronta:**

```text
Oi! Passando para confirmar nosso combinado de amanhã às 15h.
```
````

## Escopo

A preferência vale para qualquer classe de conteúdo preparada para WhatsApp: respostas pessoais, explicações, negociações, mensagens profissionais, transcrições e textos para encaminhamento.
