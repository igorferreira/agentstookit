# Playbook de Negociação → Envio ao Advogado

Fluxo completo para atualizar e enviar o playbook de negociação ao Dr. Israel.

## Quando ativar

- "atualiza o playbook" / "envia o playbook pro advogado" / "manda pro Israel"

## Passos

1. Ler `2026_07_JULHO/2026-07-31_PLAYBOOK-NEGOCIACAO-CARTOES.md`
2. Ler ebook do Dr. Israel: `~/MEGA/Documentos/CARREIRA/2026-07-24_EBOOK-NEGOCIACAO-DIVIDA-CARTAO-CREDITO.pdf` → `pdftotext`
3. Cruzar playbook vs ebook — verificar se tem:
   - Metodologia 280 dias com passo a passo Consumidor.gov.br
   - Perfil de risco por banco (com cartões do Igor mapeados)
   - Tabela "O que bancos NÃO podem fazer" com base legal
   - ⚠️ Riscos assumidos (SPC/Serasa, score, juros, ação judicial)
4. Atualizar valores com status real de pagamento (CONTROLE_PAGAMENTOS.md)
5. Reorganizar grupos se houve absorções (Inter, Dígio)
6. Gerar PDF: `pandoc → HTML → wkhtmltopdf`
7. Enviar via himalaya na thread "Dossiê financeiro — Igor Ferreira (26 cartões, dívida R$ 89 mil)" — **manter esse subject literal** para o e-mail cair na thread certa; não é uma contagem/valor atual (ver `ENDIVIDAMENTO.md`/`CONTROLES.md` para os números vigentes), é só o identificador da conversa original com o Dr. Israel
8. Confirmar envio verificando `himalaya envelope list -f "[Gmail]/E-mails enviados" | grep -i dossiê`

## Pitfalls

- O ebook usa **280 dias** (não meses) e **Consumidor.gov.br** (não Procon)
- O perfil de risco do PAN não está no ebook — marcar como ❓
- RecargaPay não é banco — tratamento jurídico diferente
- Sempre confirmar que o email caiu na thread certa (subject "Re: Dossiê financeiro...")
