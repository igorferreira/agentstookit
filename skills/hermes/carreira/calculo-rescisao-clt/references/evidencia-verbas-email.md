# Varredura de evidência de verbas por e-mail (Noorden/HDI)

Quando uma verba da rescisão estiver em disputa (Igor afirma que não existe / empresa pode não ter pago), PROVAR por documento antes de decidir. Ordem:

## 1. Mapear as pastas do Gmail do empregador

`himalaya folder list --output json` (filtrar linhas WARN). Pastas típicas: `Carreira/<empresa>`, `Clientes/<empresa>` (+ subpastas Contracheques, Comunicados, Correspondencia, ControleHoras, Recisao). Filtrar em Python: `from` contendo domínio da empresa, RH, ou nomes de contato.

## 2. Dump paginado, filtro em Python (nunca confiar no IMAP search)

```python
# por pasta: paginar até voltar < page-size, acumular, filtrar
out = himalaya envelope list -f <pasta> --page-size 250 --page N --output json
# filtrar subject lower() contendo termos SEM acento: 'feri', 'decimo', 'rescis', 'aviso'
# IMAP search com termo acentuado aborta; com termo sem acento PODE falhar silenciosamente — o dump paginado é a fonte confiável
```

Pitfall JSON: `from` pode virar dict (name/addr) — normalizar com função `sender_str(e)` antes de `.lower()`.

## 3. Classificar as evidências típicas de férias

- **ZapSign** (`Noorden via ZapSign <ola@zapsign.com.br>`): cada lote = um período aquisitivo liquidado. "Assinar documento" = convite; "Comprovante de assinatura" / "está finalizado" / "Assinaturas finalizadas" = concluído. O ASSUNTO data o lote (ex.: "Documentos Ferias - Igor Ferreira - Março 2026.pdf"); cruzar com os contracheques do(s) mesmo(s) mês(es) para identificar QUAL período aquisitivo foi liquidado (gozo + abono/venda). Prova mínima sem login no serviço: abrir o link `/verificar/<uuid>` da variante "está finalizado" — mostra SEM LOGIN o nome do documento e a contagem de assinaturas ("Assinaturas 2/2"); o PDF em si exige conta no serviço e os comprovantes não trazem anexo. URLs de rastreador vêm dobradas no quoted-printable — decodificar com `email.message_from_string(raw, policy=policy.default)` antes de regex.
- **Contracheques PDF**: baixar via `himalaya attachment download -f <pasta> -d /tmp/hol <id>`; extrair texto (`pdftotext -layout` ou fitz) e grepar `éri` (férias/abono). Rúbrica ausente no(s) mês(es) após o vencimento do período aquisitivo = período NÃO pago pela folha → entra como vencidas no TRCT.
- **Informativos de RH** (13º, FGTS, benefícios) ficam em Comunicados/Correspondencia — úteis para prazos e regras, não para valores.

## 4. Veredicto

- Documentos CONFIRMAM a afirmação do Igor → aplicar a correção e marcar a pendência como resolvida com a fonte.
- Documentos CONTRADIZEM → manter a verba CONDICIONAL com o valor exato, registrar as duas leituras (com/sem) nos totais, e apontar ao Igor exatamente o que falta (ex.: "contracheques jul–out não mostram pagamento do período vencido em <data>"). O TRCT oficial é a fonte final.
