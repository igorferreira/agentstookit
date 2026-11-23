---
name: openrouter-account-operations
description: "Check OpenRouter credit and switch model; compare prices."
tags: [openrouter, llm, model-management, account]
related_skills: [hermes-agent]
---

# OpenRouter Account & Model Operations

Operaciones de cuenta de OpenRouter para el usuario (Igor): consultar crédito/límite/uso, comparar precios de modelos y cambiar el modelo activo del Hermes. Estas tareas se repiten (chequeos de crédito, ajustes de costo, cambio a un modelo que se comporte bien en idioma).

## Reglas de seguridad al tocar la clave

- **NUNCA imprimir el valor de la API key** (regla absoluta del usuario). Leer la clave del `.env` global y usarla en el comando sin eco; jamás exponerla en salida.
- Patrón seguro para extraerla del `.env` **sin mostrarla**:
  ```bash
  KEY=$(grep -oE 'OPENROUTER_API_KEY=.*' /home/igorferreira/.hermes/.env | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")
  ```
- Evitar el pipe directo `curl | python3` → dispara aprobación de seguridad [HIGH]. Mejor: guardar el JSON a archivo con `curl -o /tmp/or_models.json` y luego leerlo con `python3`. (Ver `references/openrouter-api.md`.)

## Crédito / límite / uso

Consultar el endpoint de auth de la key:

```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $KEY" -o /tmp/or_key.json
python3 -c "import json; d=json.load(open('/tmp/or_key.json'))['data']; print('label:', d.get('label')); print('limite US$:', d.get('limit')); print('usado US$:', round(d.get('usage',0),4))"
```

Interpretación importante:
- `limit: None` + label `sk-or-v1-...` = la key **no tiene tope de crédito fijo** (funciona por consumo, no monto precomprado). NO reportar "restante X" inventado cuando no hay tope.
- `usage` = consumo acumulado. Restante solo tiene sentido si existe `limit`.

## Comparar precios de modelos

```bash
curl -s https://openrouter.ai/api/v1/models -H "Authorization: Bearer $KEY" -o /tmp/or_models.json
```
Luego parsear por `m['id']` y `m['pricing']['prompt']` / `['completion']` (US$/token). Para comparar al nivel "por millón de tokens" multiplicar ×1e6. Precios tipo flash son ~$0.03–0.07/M entrada.

## Cambiar el modelo activo del Hermes

```bash
hermes config set model.default "PROVIDER/MODELO"
hermes config set model.provider "openrouter"   # si el proveedor es openrouter
# verificar:
hermes config   # o leer ~/.hermes/config.yaml
```

- `hermes config set` puede advertir que **4 cron jobs guardan su propio model_snapshot** y "fallarán cerrado" si difieren del nuevo modelo. **NO es un error**: esos jobs (karate, rescisión, resumen diario) conservan su modelo a propósito. No tocarlos a menos que el usuario lo pida. Verificar con `hermes cron list`.
- El cambio aplica a **nuevas sesiones/chat**, no a la sesión en curso.

## Pragmática del cambio de sesión activa

Si el problema de idioma ocurre DURANTE una conversación, `hermes config set` no afecta la sesión en marcha. Avisar al usuario y abrir sesión nueva; no prometer cambio en caliente a la sesión actual.

## Pitfall: modelo que se sale del idioma

Si un modelo activo empieza a emitir respuestas en idioma equivocado (ej. español aunque el usuario exige pt-BR), **la causa raíz es el modelo**, no las instrucciones. Solución: cambiar de modelo (ver arriba). Modelo de referencia estable en idioma y económico para esta cuenta: `qwen/qwen3.7-flash` (openrouter). Los "flash" baratos de DeepSeek han mostrado alternancia involuntaria de idioma. Aviso: al delegar traducción a un subagente, verificar el archivo resultante — un modelo idéntico puede dejar el texto igual de contaminado por idioma.

## Verificación

- Tras configurar: `python3 -c "import yaml; print(yaml.safe_load(open('/home/igorferreira/.hermes/config.yaml')).get('model'))"` muestra `{'default': ..., 'provider': ...}` correctos.
- Tras consultar crédito: confirmar campos `label/limit/usage` antes de reportar.

## Referencias
- `references/openrouter-api.md` — endpoints exactos y formato de respuesta.