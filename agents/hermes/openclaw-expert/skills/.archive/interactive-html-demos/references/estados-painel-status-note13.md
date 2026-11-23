# Lições da sessão 11/09 — estados, painel de status, Note 13 (retrato+paisagem)

## Estados + painel de status em tempo real (validado)

- **Estados por agente**: 🔨 Trabalhando (se mexe, micro-ajuste na cadeira) · ☕ Café (xícara com vapor animada, `display:block` só nesse estado) · 😴 Parado (imóvel, `opacity:.75; filter:saturate(.6)`). Troca aleatória a cada 8–22s por agente.
- **Painel fixo `#painelStatus`** (bottom:64px, acima do rodapé): linha por agente com dot colorido + estado + tarefa, `atualizarPainel()` a cada 3s. Vem **minimizado no mobile** (`W()<700` → classe `min`), aberto no desktop.

## Note 13 — retrato E paisagem (exigência do Igor)

- Espaçamento adaptativo por orientação: `ESP_X = MOBILE() ? (W()<H()?100:118) : 130`, `ESP_Y = MOBILE() ? (W()<H()?96:84) : 118`.
- `window.addEventListener('orientationchange', ()=>setTimeout(relayout, 350))` — cadeiras se reorganizam ao girar.
- Validar em **384×814 E 814×384** (não só 390×844 retrato).

## Pitfalls novos (custaram várias rodadas de debug)

1. **Feature criada via `setTimeout` (ex: painel após 400ms) NÃO aparece em screenshot headless** — a captura roda antes do timer. Provar existência via CDP (`!!document.getElementById(...)` + contar linhas do painel), não por print. NÃO "consertar" o que já funciona só porque o print não mostra.

2. **Helper chamado dentro do `AGENTES.map` com assinatura errada ou definido fora de escopo** (ex: `addXicara(el)` recebendo `a.el` quando o caller passa o elemento DOM direto) mata o `.map` inteiro → "0 agentes" no header, sem erro visível em print. Sintoma: estações renderizam mas humanos não. Declarar o helper no MESMO `<script>`, antes do uso, e conferir a assinatura.

3. **`onclick` inline com aspas simples aninhadas dentro de string innerHTML** (`'...onclick="x.toggle('min')"'`) = SyntaxError silencioso que mata o bloco JS inteiro. Usar `el.onclick = ()=>...` via `querySelector` depois do innerHTML.

4. **Prova funcional de estado**: `typeof cicloEstados`, `agents[0].estadoAg`, contar `#listaStatus .linha` via CDP — o painel pode existir e estar correto sem nunca aparecer num screenshot headless.