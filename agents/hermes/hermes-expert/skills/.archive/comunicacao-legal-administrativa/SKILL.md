---
name: comunicacao-legal-administrativa
description: E-mails a órgãos públicos, procuradorias e advogados.
version: 1.0.0
metadata:
  hermes:
    tags: [legal, email, administracao-publica, correspondencia, procuradoria, orgaos-publicos]
---

# Comunicação jurídico-administrativa

Use quando Igor precisar redigir e/ou enviar uma **correspondência** (e-mail ou WhatsApp) a um **órgão público, procuradoria, ouvidoria, balcão de atendimento (ex: SIM/Simplifica) ou advogado** relacionada a um processo/caso em andamento (ex: pedido de exclusão de polo passivo, desbloqueio, esclarecimento de cobrança indevida).

Isto NÃO cobre peças processuais formais (petições/Exceção de Pré-Executividade) — para essas, usar as skills de estilo forense (`estilo-diogo-juridico`) e drafting. Esta skill cobre a **correspondência administrativa/amigável ao redor** do processo.

## Fluxo recomendado

1. **Levantar os fatos técnicos antes de escrever** (nº do processo, CDA, CNPJ, CPF, datas de saída da sociedade, endereço de citação errado, datas dos débitos). Nunca chutar.
2. **Abrir com bloco de dados técnicos** em negrito: nome+CPF, empresa+CNPJ, nº do processo. Facilita protocolo e deixa claro do que se trata já no 1º parágrafo.
3. **Depois o texto explicativo** amigável/comovente quando o objetivo é sensibilizar (transtorno real, prejuízo concreto). Separar fato de hipótese.
4. **Pedido claro e humilde** no fim (o que quer que o órgão faça + disposição para comparecer pessoalmente).
5. **Registrar a entrega**: plano de envio + markdown de contatos na pasta do processo.

## Preferências do Igor (validado 03/09/2026)

- **E-mails devem ser FORMATADOS, não texto puro.** Usar HTML com negrito nos dados-chave, títulos de seção (📋 Resumo dos fatos / 📎 Documentos em anexo) e tópicos com marcadores. Se enviado em texto puro, Igor pede reenvio formatado.
- **Assunto do e-mail:** número do processo + descrição curta (ex: `Exclusão de ex-sócio (saída em 2007) – Execução Fiscal 0040223-62.2021.8.19.0031 – ... – CDA 2360961`). Número do processo sempre presente e em destaque.
- **Copiar (Cc) o advogado do caso** nas correspondências administrativas (ele acompanha e fica registrado).
- **Anexar os documentos probatórios** (certidão JUCERJA, QSA da Receita Federal, comprovante CNPJ, CPF). Documentos oficiais do site da RF (QSA) valem mais que relatórios/compilações feitos pela equipe — usar os prints do site oficial.
- **Mensagens WhatsApp quebradas em pedaços curtos**; nunca um bloco gigante.
- E-mails a advogados/terceiros: NUNCA enviar `.md` — converter para PDF.

## Envio por e-mail (himalaya)

- Envio via `himalaya message send --account NAME < /tmp/x.eml` em background (`notify_on_complete=true`).
- **E-mails grandes (>~7MB, muitos anexos) dão timeout SMTP (`request timed out`)**. Manter <~4–6 arquivos e <~7MB; ~3MB/4 arquivos envia com segurança. Se falhar (log mostra `250 OK` repetido mas mensagem não completa), o envio NÃO ocorreu — dividir em 2–3 e-mails menores e reenviar.
- Para apresentação, anexar MIMEText plain + MIMEText html.
- Validar o `.eml` antes (parse de volta com `email.message_from_bytes` para conferir To/Cc/Subject/anexos).

## Arquivo/referências
- `references/caso-marica-sessao-20260903.md` — detalhe da sessão do caso Maricá/Simplifica (contatos, plano de envio, evolução dos textos v1→v3).