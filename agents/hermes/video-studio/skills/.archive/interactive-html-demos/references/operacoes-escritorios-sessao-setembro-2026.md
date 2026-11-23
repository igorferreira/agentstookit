# Operações de escritórios multi-agente — padrões da sessão 12–13/09/2026

Este arquivo captura padrões operacionais descobertos ou validados nesta sessão. Não são regras duras — são lições aprendidas em tempo real.

---

## 1. Nome único DE AGENTE no sistema todo

**Pitfall:** quando gera múltiplos escritórios (ex. Escape Room, Espetinho, Política, Portões) a partir de um mesmo template, papéis compartilhados como "Dono/Igor/Manager" ficam repetidos em TODOS os arquivos. Mesmo que cada escritório tenha seu próprio array `agents = [...]`, o Igor visualiza tudo num painel unificado — nomes duplicados confundem.

**Regra:**
- Cada nome de agente deve ser **único no projeto inteiro**, não só dentro do escritório.
- Papéis compartilhados (donos, gerentes) devem receber apelidos diferenciados por contexto: `"Mestre Igor"`, `"Chefão Igor"`, `"Investidor Igor"`, `"Sócio Igor"` — nunca repetir "Igor" puro.
- Nomes comuns (Cris, Bia, Rita) verificar contra lista global antes de criar novo escritório.

**Validação:** script que escaneia todos `.html` e `.js` da pasta `clientes/`, extrai `{id, nome}`, conta duplicatas cruzadas entre escritórios. Se >1 ocorrência do mesmo nome → alerta.

---

## 2. Função de zoom NUNCA vazia

**Pitfall:** ambos Escritório Escape Room Infantil e Portões Luís tinham `function aplicarZoom(){}` VAZIA. Os handlers dos botões usavam `document.body.style.zoom` que funciona NO CHROME APENAS. No Firefox/Safari mobile, zoom simplesmente não aplicava — os botões clicavam mas nada acontecia visualmente.

**Fix correto:** usar CSS `transform: scale(N)` aplicado ao container do floor/stage:
```js
function aplicarZoom() {
    const f = document.getElementById('floor');
    if (f) f.style.transform = 'scale(' + zoom + ')';
    f.style.transformOrigin = 'center center';
    // Atualizar label se existir
    const v = document.getElementById('zoomValue');
    if (v) v.textContent = Math.round(zoom * 100) + '%';
}
// Handlers: chamar aplicarZoom(), NUNCA body.style.zoom
document.getElementById('btnMais').onclick = () => {
    zoom = Math.min(2, zoom + 0.1);
    aplicarZoom();
};
```

**Verificação pré-entrega:** `grep -rn 'body.style.zoom' demos/clientes/` deve retornar nada. Se encontrar → corrigir imediatamente.

---

## 3. Normalização de mapeamento de grupos temáticos

**Pitfall encontrado com 54 agentes jurídicos:** ao mapear folders como `direitos-humanos`, `execucao_penal`, `financas_publicas` para grupos temáticos, os keys do dicionário Python precisam corresponder aos nomes NORMALIZADOS (underscores, não hífens).

```python
folder_normalized = agent['folder'].replace('juris-', '').replace('-', '_')
group = mapeamento.get(folder_normalized, 'especial')
```

Sem o `.replace('-', '_')`, 16 de 54 mapeamentos falham silenciosamente (todos caem no fallback 'especial'), criando distribuição totalmente desbalanceada (um grupo com 23+ agentes, outros com 1).

**Regra fixa:** sempre normalizar hífens para underscores antes de lookup em qualquer dicionário de mapeamento.

---

## 4. Docker cache de COPY stages

**Padrão recorrente:** `docker compose build` CACHEia COPY stages mesmo quando novos arquivos foram adicionados à pasta de contexto. Sintoma: container roda HTTP 200 mas conteúdo é antigo/arquivos existem no host mas não dentro do container.

**Fix:** reconstruir sem cache:
```bash
docker compose stop && docker compose build && docker compose up -d
```
Ou forçar recriação service-a-service.

**Verificação pós-build:** `docker exec <painel> ls /path/<office>/` deve listar todos os arquivos esperados antes de confiar no HTTP 200.

---

## 5. Patch rápido para escritórios já publicados com zoom quebrado

Se detectar durante QA posterior que algum escritório existente usa `body.style.zoom`:

1. Substituir `function aplicarZoom(){}` pela versão com `transform:scale()`
2. Trocar cada handler de botão: de `document.body.style.zoom=zoom` para `aplicarZoom()`
3. No reset: `zoom=1; aplicarZoom()` ANTES de limpar cookies e reload
4. Adicionar label `%` na função

Esses 4 patches resolvem 100% dos casos de zoom quebrado identificados.
