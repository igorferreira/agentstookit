# CSS Design Patterns — escritórios TimeAutomático

Validados em 12/09/2026 quando o usuário reportou que a v1 estava "horrível" + "não tá 3d" + "não tá cabendo todo.mundi na tela".

## Avatar 3D com CSS perspective (sem WebGL)

Cubo de 6 faces + cabeça sobreposta usando `transform-style: preserve-3d` + `rotateX/Y/Z` + `translateZ` para profundidade.

```html
<div class="avatar">
  <div class="face3d">
    <div class="cubo">
      <div class="top"></div>
      <div class="front"></div>
      <div class="right"></div>
      <div class="left"></div>
      <div class="back"></div>
      <div class="bottom"></div>
    </div>
    <div class="eye3d"></div>     <!-- translateZ(16px) -->
    <div class="mouth3d"></div>   <!-- translateZ(16px) -->
    <div class="ant3d"></div>     <!-- translateZ(16px) + glow animation -->
  </div>
</div>
```

```css
.avatar{perspective:180px;perspective-origin:50% 80%;width:42px;height:42px}
.face3d{width:30px;height:30px;transform-style:preserve-3d;
        transform:rotateX(15deg) rotateY(-20deg);transition:transform .35s}
.cubo{position:absolute;width:30px;height:30px;transform-style:preserve-3d}
.cubo .top   {transform:rotateX(90deg)  translateZ(15px);background:linear-gradient(135deg,var(--cor) 0%,#fff 100%)}
.cubo .front {transform:translateZ(15px);background:linear-gradient(180deg,var(--cor) 0%,rgba(0,0,0,.4) 100%)}
.cubo .right {transform:rotateY(90deg)  translateZ(15px);background:linear-gradient(90deg,var(--cor) 0%,rgba(0,0,0,.5) 100%)}
.cubo .left  {transform:rotateY(-90deg) translateZ(15px);background:linear-gradient(270deg,var(--cor) 0%,rgba(0,0,0,.5) 100%)}
.cubo .back  {transform:rotateY(180deg) translateZ(15px);background:rgba(0,0,0,.6)}
.cubo .bottom{transform:rotateX(-90deg) translateZ(15px);background:rgba(0,0,0,.5)}
.eye3d  {position:absolute;top:8px;left:8px;width:5px;height:5px;border-radius:50%;background:#0a101c;transform:translateZ(16px);box-shadow:14px 0 0 #0a101c}
.mouth3d{position:absolute;top:18px;left:11px;width:8px;height:2px;background:#0a101c;border-radius:0 0 4px 4px;transform:translateZ(16px)}
.ant3d  {position:absolute;top:-6px;left:13px;width:2px;height:8px;background:rgba(255,255,255,.4);transform:translateZ(16px)}

/* Cor da "personalidade" via CSS var — todas as faces do cubo herdam */
face.style.setProperty('--cor', '#1FD3C4');
```

### Animações por status

```css
[data-status="working"]  .face3d{animation:workingBob 1.4s ease-in-out infinite}
[data-status="tool_call"] .face3d{animation:toolSpin 2.2s linear infinite}
[data-status="idle"]      .face3d{animation:idleBreath 4s ease-in-out infinite;
                                  filter:saturate(.4) brightness(.85)}
[data-status="thinking"]  .face3d{transform:rotateX(20deg) rotateY(-30deg)}
[data-status="error"]     .face3d{filter:hue-rotate(160deg) saturate(.7)}

@keyframes workingBob{50%{translate:0 -2px}}
@keyframes toolSpin{to{transform:rotateX(8deg) rotateY(360deg)}}
@keyframes idleBreath{50%{scale:1.05 1.02}}
```

---

## Grid 12-col responsivo (todos cabem na tela)

Layout que atende **3 cenários** com **1 arquivo CSS**:

```css
.office{display:grid;grid-template-columns:repeat(12,1fr);gap:8px;padding:8px;
        flex:1;overflow:auto;-webkit-overflow-scrolling:touch}
.station{grid-column:span 6}            /* mobile portrait (≤480): 2 cols */

/* tablets retrato: já vem de span 6 (default) → vira span 4 via media menor */
@media (min-width:481px) and (max-width:899px){.station{grid-column:span 4}}

/* desktop paisagem: 6 por linha */
@media (min-width:900px){.station{grid-column:span 2}}
@media (min-width:1200px){.station{grid-column:span 2}}
```

Resultado:
- 390px mobile portrait: 6 agentes em grade 2×3 (todos visíveis sem scroll)
- 768px tablet: 3×2
- 1280px desktop: 6×1 linha

---

## Layout flex (sem `calc(100vh - NNNpx)`)

Layout quebrado: `height: calc(100vh - 230px)` depende de magic numbers; qualquer mudança no header quebra.

**Padrão flex correto**:
```css
:root{--header-h:54px;--summary-h:38px}
body{display:flex;flex-direction:column;height:100%;overflow:hidden}
header{height:var(--header-h);flex:none}
.summary{height:var(--summary-h);flex:none}
.office{flex:1;overflow:auto}      /* preenche resto da tela */
.feed{flex:none;max-height:30vh}  /* tamanho próprio, não consome scroll */
```

O feed não tem `position:fixed` (estava quebrando mobile landscape).

---

## Feed colapsável por padrão

**Problema**: feed ocupando 1/3 da tela em mobile. Usuário disse "todo.mundi na tela".

**Solução**: estado inicial collapsed + clique expande.

```html
<div class="feed collapsed" id="feed">
  <h3 id="feedToggle">📡 Atividade <span class="chev">▼</span></h3>
  <div class="events">...</div>
</div>
```

```css
.feed{max-height:30vh;transition:max-height .25s}
.feed.collapsed{max-height:30px}
.feed h3{height:30px;padding:7px 14px;cursor:pointer;user-select:none}
.feed h3 .chev{margin-left:auto;transition:transform .25s}
.feed.collapsed .chev{transform:rotate(180deg)}  /* aponta pra cima quando recolhido */
```

```js
$('#feedToggle').addEventListener('click', () => $('#feed').classList.toggle('collapsed'));
```

---

## Texto longo em card: `line-clamp` + `overflow-wrap`

**Problema**: `delegou para: oswaldo, paulinho, rita, duda, vesna` cortava palavra no meio.

```css
.deleg{
  font-size:.62rem;font-style:italic;color:#ffc266;
  overflow-wrap:anywhere;
  display:-webkit-box;-webkit-line-clamp:1;line-clamp:1;
  -webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis;
  margin-top:2px;
}

.activity{
  overflow-wrap:anywhere;
  display:-webkit-box;-webkit-line-clamp:2;line-clamp:2;
  -webkit-box-orient:vertical;overflow:hidden;
}
```

`overflow-wrap:anywhere` quebra palavras compridas SEM precisar de `&shy;`. `line-clamp` corta com `…`.

---

## Borda colorida por status (sem imagem)

```css
.station[data-status="working"]{border-color:var(--c-green);
  box-shadow:0 0 14px rgba(39,174,96,.3),inset 0 1px 0 rgba(39,174,96,.1)}
.station[data-status="tool_call"]{border-color:var(--c-purple);box-shadow:0 0 14px rgba(142,68,173,.4)}
.station[data-status="delegating"]{border-color:var(--c-orange);box-shadow:0 0 14px rgba(255,140,0,.3)}
.station[data-status="error"]{border-color:var(--c-red)}
.station[data-status="idle"]{opacity:.65}
```

Combinado com `--rc` para cor principal da estação: `node.style.setProperty('--rc', a.cor)`.

---

## Pill de status sem cortar texto

Badge com `max-width:54px` + `flex-shrink:0` + `font-size:.58rem`:

```css
.station .badge{font-size:.58rem;padding:2px 5px;border-radius:4px;
  border:1px solid var(--c-line);color:#9bb;
  display:inline-flex;align-items:center;gap:3px;
  flex-shrink:0;max-width:54px;text-align:center;line-height:1}
```

Texto vira "CONCLUÍDO" → "CONCLUÍD…" automaticamente quando nome/status passa do limite.

---

## Resumo

Checklist antes de aprovar layout de escritório:

- [ ] Avatar tem profundidade real (preserve-3d, múltiplas faces)
- [ ] Todos os agentes visíveis SEM scroll em mobile portrait (390×844)
- [ ] Nenhuma sobreposição de texto (activity/duration/tool/deleg estão em linhas diferentes ou com `-webkit-line-clamp`)
- [ ] Feed colapsado por padrão, chevron ▼ → ▲
- [ ] Border-color muda visivelmente com `data-status`
- [ ] Touch targets ≥ 44px (mas cards não ficam grandes demais)
- [ ] `prefers-reduced-motion: reduce` desativa animações
- [ ] `line-clamp` aplicado em todos os campos com texto variável
- [ ] `overflow-wrap: anywhere` em qualquer campo que pode receber texto longo (delegação, tool name, activity)
