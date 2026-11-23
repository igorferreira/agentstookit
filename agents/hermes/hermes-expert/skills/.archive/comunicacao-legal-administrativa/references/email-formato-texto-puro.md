# E-mails a órgãos públicos/advogados — preferência de formato (atualizada 03/09/2026)

## Importante: a preferência MUDOU. Texto puro, NÃO HTML.
Na sessão de 03/09/2026 (caso Maricá/Simplifica) Igor **rejeitou explicitamente** o corpo em
HTML: "nao quero formato html, quero formato texto com negrito, lista enumeradas e espacamentos
e quebras de linhas para destacar itens importantes".

> ⚠️ A versão anterior da skill dizia "usar HTML com negrito". Isso está SUPERADO. O que o Igor
> quer agora é texto puro (`MIMEText(body, "plain")`), formatado para legibilidade.

## Como formatar um corpo em TEXTO PURO (sem negrito/HTML real)
1. **Quebras de linha frequentes** — uma ideia por parágrafo; nunca bloco contínuo.
2. **Espaçamento entre blocos** (linha em branco) para separar seções e dar respiro.
3. **Listas enumeradas** `1. 2. 3.` para fatos e lista de documentos; `•` para subtipos.
4. **Destaque em MAIÚSCULAS** para os pontos-chave — é o "negrito" do texto puro:
   INDEVIDAMENTE, BLOQUEIO, NÃO CONSTA, LIBERAÇÃO, etc.
5. **Títulos de seção em MAIÚSCULAS**, separados por linha de travessão `---`:
   `---`, `RESUMO DOS FATOS`, `1. ...`, `---`, `DOCUMENTOS EM ANEXO`, etc.
6. **Humanizar** — incluir um trecho genuíno do impacto emocional/transtorno real
   ("tenho passado noites mal dormidas e uma angústia constante porque é injusto pagar por algo
    que não fiz"). Igor pede explicitamente para "humanizar o email e ficar menos IA".
7. **Dados técnicos logo no início** — nome+CPF, empresa+CNPJ, nº do processo (+ valor da causa).
8. Detalhar as dívidas/valores executados em seção própria quando relevante.

## Exemplo de abertura (texto puro, formatado)
```
Prezada equipe do Simplifica Maricá Empresas,

Meu nome é Igor dos Santos Ferreira (CPF XXX.XXX.XXX-XX).

Fui incluído INDEVIDAMENTE na CDA nº 2360961 e no polo passivo da
Execução Fiscal nº 0040223-62.2021.8.19.0031 ..., movida pelo Município
contra o Restaurante Salada de Sabores Ltda ME (CNPJ 07.801.460/0001-68).
O valor da causa é de R$ 2.544,00.
```

## Comparação para decisão rápida
| Formato | Status |
|---|---|
| HTML (MIMEText html) com negrito/📋/📎 | ❌ REJEITADO por Igor (03/09) |
| Texto puro com quebras + listas + MAIÚSCULAS + humanização | ✅ Preferência atual |