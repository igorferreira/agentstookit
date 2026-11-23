# Entrega do relatório de rescisão: PDF + e-mail

Quando Igor pedir PDF e/ou envio por e-mail além do Markdown canônico.

## 1. Gerar o PDF (pandoc → HTML → Chrome CDP)

wkhtmltopdf e reportlab não estão instalados nesta máquina. O caminho validado usa o Chrome controlado por CDP (porta 9224; ver `references/linkedin-edit-cdp.md` na skill linkedin-optimization para subir a instância):

**Armadilha da conversão: pares de "R$" no Markdown geram TeX math.** O pandoc interpreta o texto entre dois `R$ ... R$` da mesma linha como fórmula LaTeX e aborta (`unexpected '"'`) — comum em logs com valores ("R$ 10.000, 10x R$ 1.000"). Antes de converter, garantir no máx. um `$` por linha ou reescrever como "mil reais"; verificação rápida: `pandoc X.md -o X.html 2>&1 | grep -i tex`.

```bash
pandoc RELATORIO.md -o /tmp/relatorio.html -s --metadata title="..." -c /tmp/estilo.css
```

CSS mínimo (DejaVu Sans, tabelas com th azul, zebra): escrever conforme o relatório. Depois, via websocket CDP:

1. `Page.navigate` para `file:///tmp/relatorio.html` + sleep ~2s.
2. `Page.printToPDF` com `printBackground: true`, margens ~0.4–0.5in, `paperWidth/paperHeight` 8.5×11.
3. **Decodificar de `response["result"]["data"]`** — o envelope CDP devolve `{id, result:{data}}`; ler `data` direto do nível superior dá KeyError.
4. `Page.printToPDF` funciona sem `Page.enable`; para captura de TELA (`Page.captureScreenshot`) o `Page.enable` é obrigatório.
5. Validar o PDF com `pdftotext ... | grep` dos valores-chave (total geral, prazo) antes de enviar.

## 2. Enviar por e-mail (himalaya, raw MIME com anexo)

`himalaya message send` só aceita mensagem crua; não existe flag --attach. Montar o .eml multipart/mixed à mão (funciona de primeira, sem depender do parse MML):

```
Content-Type: multipart/mixed; boundary="BOUND_UNICO"
[headers From/To/Subject/MIME-Version]
--BOUND_UNICO
Content-Type: text/plain; charset=utf-8

<corpo em PROSA — nunca markdown (tabelas | saem quebradas; ** e # aparecem literais)>
--BOUND_UNICO
Content-Type: application/pdf; name="arquivo.pdf"
Content-Disposition: attachment; filename="arquivo.pdf"
Content-Transfer-Encoding: base64

<base64 -w0 do PDF>
--BOUND_UNICO--
```

```bash
himalaya message send < /tmp/email.eml   # "Message successfully sent!"
```

- O corpo do e-mail reproduz o CÁLCULO (tabelas convertidas em linhas rotuladas `verba ... R$ valor`) e lista o PDF anexo; o PDF carrega o relatório completo.
- **Verificar a chegada** antes de reportar sucesso: `himalaya envelope list` (INBOX padrão) e conferir ID + assunto. O SMTP já entrega antes do índice atualizar — se a lista vier vazia, esperar alguns segundos e relistar.
- Enviar de/para o próprio Igor (`igorferreirabr@gmail.com`) quando ele pede "me envia" sem citar outro destinatário.
