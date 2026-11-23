# Buser — extração de preços reais por data

O site da Buser (Nuxt/Vue + SPA) tem datepicker quebrado e um formulário React controlado que ignora eventos sintéticos. Scraping visual dos cards é lento e sujeito a pegar a data errada. O caminho confiável é a URL com datas ISO + leitura do estado interno da página.

## Passo 1 — Navegar pela URL com datas ISO

Formato que o servidor RESPEITA (a data só vale em ISO `YYYY-MM-DD`, separada por hífen):

```
https://www.buser.com.br/onibus/rio-de-janeiro-rj/sao-paulo-sp?ida=2026-11-26&volta=2026-11-28
```

- Trocar slugs pelo trecho desejado (`rio-de-janeiro-rj`/`sao-paulo-sp` e o inverso).
- O parâmetro em `dd-mm-aaaa` (`ida=26-11-2026`) é IGNORADO silenciosamente: a página renderiza resultados do dia corrente com cara de busca válida. Sempre confirme a data efetiva lendo o estado (Passo 2) antes de confiar no que está na tela.
- Remeter origem/destino via query (`?fromCity=` etc.) não funciona — o form é slug-only.

## Passo 2 — Ler os resultados do estado interno (não dos cards)

Depois do `wait_for_load()` + ~3s, extrair o payload do Pinia que hidrata a página:

```python
payload = js("""
(() => {
  const s = window.__NUXT__.pinia.search;
  const gb = s.gruposByDate;
  const keys = Array.isArray(gb) ? gb.map((_, i) => String(i)) : Object.keys(gb);
  const out = {};
  for (const k of keys) out[k] = gb[k];
  return {meta: {dep: s.departureDate, ret: s.returnDate}, data: out};
})()""")
```

- Validar `meta.dep` == data pedida. `gruposByDate['N'].datetime_ida` deve bater com a data alvo (ex.: `2026-11-26`); se vier a data de hoje, a URL não foi respeitada — volte ao Passo 1.
- Salvar o JSON inteiro em arquivo antes de parsear (o estado é volátil a cada navegação).

## Passo 3 — Interpretar os campos de cada grupo

Campos úteis por item de `grupos[]`:

| Campo | Significado |
|---|---|
| `datetime_ida` / `chegada_ida` | Partida/chegada ISO-3 (`2026-11-26T00:10:00-03:00` → hora = `dt[11:16]`) |
| `origem.nickname` / `destino.nickname` | Ponto de embarque/desembarque (ex.: "Ponto Estação Afonso Pena", "Barra Funda") |
| `company_friendly_name` | Operadora do ônibus |
| `tipo_assento` | `semi leito` / `leito` / `leito individual` |
| `vagas` | Assentos restantes |
| **`ref_split_value`** | **PREÇO COBRADO na Buser — usar este, nunca `preco_base`** |
| `preco_rodoviaria` | Referência concorrente (não é o preço Buser) |
| `closed` / `grupo_classe_closed` | Filtrar fora quando `true` |
| `parcelamento` | `valor_por_parcela` × `quantidade_de_parcelas` |

**Validação do campo de preço:** cruzar um card visível (texto do body, `R$ XX,XX`) com o grupo correspondente pelo horário de partida — `ref_split_value` bate com o valor exibido; `preco_base` é maior. Validar essa correspondência a cada extração, pois a API interna pode mudar.

## Passo 4 — Montar o comparativo

- Filtrar janelas de horário (ex.: partidas `00:00–01:00` para "saída à meia-noite") e o top-N mais barato geral.
- Combinar ida × volta por classe de assento e apresentar o total por combo (econômico / conforto / plano anterior), com ponto de embarque de cada trecho — o Usuário decide por horário+ponto, não só por preço.
- Registrar tudo no arquivo canônico do plano de viagem (pasta da viagem no Drive) com a data da consulta — os preços mudam; a pesquisa anterior fica obsoleta e é sempre substituída por nova seção datada, nunca apagada.

## Pitfalls

- **Não setar datas sinteticamente no input** (`ada-input-*` com value + dispatchEvent): o componente React aceita a string na tela mas o estado interno segue `Invalid Date` e a busca volta ao dia corrente.
- **Não confiar em performance entries** para achar a API de busca: os resultados vêm SSR no payload, não por XHR/fetch visível.
- **`window.__NUXT__` só existe após a hidratação** — espere o load completo antes de ler.
- Uma viagem de madrugada sai do dia ANTERIOR nos sites 23:5x (ex.: volta listada como `23:59 dia 28 → 29/11`): interpretar 'sair às 00h do dia X' como partida `X 00:00-00:59`, nunca `X-1 23:59`.
