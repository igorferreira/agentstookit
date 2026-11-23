---
name: snapinsta-downloader
description: Baixar mídia pública do Instagram e gerar MD de metadata.
---

# Snapinsta Downloader Skill

**Baixa videos, fotos, reels e stories do Instagram via [snapinsta.com.br](https://snapinsta.com.br) — salva na pasta sync (Google Drive) e gera arquivo MD com metadata.**

## Endpoint Principal

```
POST https://snapinsta.com.br/api/download.php
Content-Type: application/json; charset=utf-8
Accept: application/json
Origin: https://snapinsta.com.br
Referer: https://snapinsta.com.br/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

{ "url": "<instagram_url>" }
```

### Resposta Esperada

```json
{
  "status": true,
  "service": "Instagram",
  "media": [
    {
      "fileType": "video/mp4",
      "url": "https://scontent.cdninstagram.com/o1/v/t2/f2/m86/...mp4?...?...",
      "thumbnail": "https://scontent.cdninstagram.com/o1/v/...jpg"
    }
  ]
}
```

Se `status` é `false`, o campo `message` contem a mensagem de erro.

## Formatando URLs Instagram

Aceita formatos comuns — **remover sempre parâmetros extra** (`utm_source`, `utm_medium`, `utm_campaign`, `igshid`, `fbclid`, `cplk`) antes do POST:

| Tipo | Exemplo | Suporte |
|------|---------|---------|
| Reel (singular) | `https://www.instagram.com/reel/<ID>/` | Total |
| Reel (plural) | `https://www.instagram.com/reels/<ID>/` | Total |
| Post feed | `https://www.instagram.com/p/<ID>/` | Total |
| IGTV | `https://www.instagram.com/tv/<ID>/` | Parcial |
| Story | `https://www.instagram.com/stories/<USER>/<ID>/` | Limitado |

### Extraindo Shortcode

Regex canonical: `(?:reel[s]?|p|tv)/\K[A-Za-z0-9_-]+` ou stories pattern `(?:stories)/[^/]+/\K[A-Za-z0-9_-]+`.

> **PITFALL:** O URL padrão é `/reels/` (plural). A regex `(?:reel|p|tv)` sem o `[s]?` **falha silenciosamente** retornando `instagram` como shortcode fallback. Sempre usar `(?:reel[s]?)` para cobrir ambas as variantes.

## Formato Nome do Arquivo

Nome estrito em **snake_case**: `{perfil}_{descrição_contexto}_{shortcode}.{ext}`.

Regras:
- Tudo minusculo
- Espacos viram underscores
- Caracteres especiais removidos/substituidos por `_`
- Sequencias multiples de `_` colapsadas em um unico
- Sem underscore no inicio ou fim

> **PITFALL:** passar `--profile`/`--description` com vários termos separados por underscore produz nome letra-por-letra (`tech_ia` vira `t_e_c_h_i_a_...`) — usar termos simples sem underscore e, logo após o download, **conferir o nome do arquivo gerado**; veio mutilado, renomear com `mv` (vídeo e .md juntos) antes de continuar. Cuidado ao renomear: o nome mutilado tem underscore ENTRE os caracteres, então o glob de busca tem que bater com o nome real na pasta (`ls` primeiro, nunca assumir o padrão).

Exemplos:
- Perfil `empreendedorismo` + Descricao `dicas_redes_sociais` + Shortcode `DdCzlolRqwq` → `empreendedorismo_dicas_redes_sociais_DdCzlolRqwq.mp4`
- Perfil `cristao` + Descricao `testemunho_transformacao_pessoal` + Shortcode `DenBhOAxQr6` → `cristao_testemunho_transformacao_pessoal_DenBhOAxQr6.mp4`

## Pastas de Destino por Categoria

Todas as pastas sincronizam automaticamente via **Insync** com a conta Google Drive `igorferreira08`:

| Categoria | Pasta Base | Subpastas Disponíveis | Uso |
|-----------|------------|----------------------|-----|
| `empreendedorismo` | `~/Insync/GoogleDrive/igorferreira08/Documentos/empreendedorismo/` | `vendas`, `estoque`, `localizacao`, `contratacao`, `fornecedores` | Conteudos de negocio, vendas, mindset, renda extra |
| `cristao` | `~/Insync/GoogleDrive/igorferreira08/Documentos/Cristao/` | `testemunhos`, `drogados`, `prostituicao`, `prosperidade` | Testemunhos, devocionais, pregações, conteudo cristao |

### Uso da Flag `--subpasta`

Quando especificada, o video vai para: `<categoria>/<subpasta>/`. Exemplos:

```bash
# Vai para empreendedorismo/vendas/
--categoria empreendedorismo --subpasta vendas

# Vai para Cristao/testemunhos/
--categoria cristao --subpasta testemunhos

# Sem --subpasta → vai direto na pasta base da categoria
--categoria empreendedorismo (sem --subpasta)
```

## Script Bash Completo

Script canonical em `.hermes/scripts/snapinsta_downloader.sh`:

```bash
bash ~/.hermes/scripts/snapinsta_downloader.sh \
  "<instagram_url>" \
  [--profile "nome"] \
  [--description "descricao_snake_case"] \
  [--categoria empreendedorismo|cristao] \
  [--subpasta <nome>]
```

### Exemplos completos

```bash
# Video empreendedorismo → vendas/
bash ~/.hermes/scripts/snapinsta_downloader.sh \
  "https://www.instagram.com/reel/DdCzlolRqwq/" \
  --profile empreendedorismo --description dicas_redes_sociais --categoria empreendedorismo --subpasta vendas

# Video cristao → testemunhos/
bash ~/.hermes/scripts/snapinsta_downloader.sh \
  "https://www.instagram.com/reels/DenBhOAxQr6/" \
  --profile cristao --description testemunho_transformacao_pessoal --categoria cristao --subpasta testemunhos
```

## Geracao de Arquivo MD (Novo!)

**Sempre** que baixar, o script gera automaticamente um `.md` com metadata e descricao do post:

```markdown
# <nome_do_arquivo_sem_extensao>

## Metadata do Post

- **URL:** <url_original>
- **Shortcode:** <shortcode>
- **Data de download:** <data>
- **Arquivo:** <nome>.mp4
- **Tamanho:** <N> MB

## Conteúdo

### Título
<og:title capturado da pagina>

### Descrição / Legenda
<og:description ou legendo do post>

## Tags e Contexto

- Perfil: <profile>
- Categoria: <categoria>
- Descrição: <description>

## Notas

<adicionar aqui observacoes>

---
*Gerado automaticamente pelo snapinsta_downloader.sh*
```

## Fluxo Completo (via script)

1. **LIMPAR URL** — remove params extras (UTM, fbclid, etc.) mas mantém base valida
2. **EXTRAIR SHORTCODE** — regex `(?:reel[s]?|p|tv)/\K[A-Za-z0-9_-]+` ou stories
3. **CONSTRUIR NOME SNAKE_CASE** — concatena perfil+descricao+shortcode → minusculas → limpa caracteres → colapsa `_` multiplos
4. **ESCOLHER PASTA** baseado em `--categoria` (empreendedorismo ou cristao)
5. **POST /api/download.php** com body JSON `{"url":"<clean_url>"}`
6. **PARSE RESPOSTA** — extrai `media[].url` e `media[].thumbnail`
7. **DOWNLOAD DIRETO** via curl (User-Agent + Referer Instagram, max 120s por arquivo)
8. **VALIDAR** — verifica arquivo existe e >0 bytes
9. **CAPTURAR METADADOS** — tenta extrair og:title e og:description da pagina Instagram
10. **GERAR .MD** — salva metadata completa no mesmo diretorio
11. **SALVAR** tudo no diretorio de output correto

Para carrossel, baixa cada imagem separadamente (`nome_base.mp4`, `nome_base_2.jpg`, etc.).

## Limitações

- **Limite diario:** ~30 downloads por IP/dia. Se falhar, ver mensagens de erro abaixo e aplicar workaround.
- **Conteudo privado/não público:** nao funciona.
- **URLs com parâmetros extra:** script limpa automaticamente, mas a URL base deve ser válida.
- **Metadados Instagram:** og:title/description podem nao estar disponíveis para todos os posts (depende do tipo e configuracao da conta).

## Fallback Quando API Bloqueia

Quando a API retorna erro (limite atingido, link invalido, ou qualquer outro), usar browser_exec:

```python
from browser_helpers import new_tab, wait_for_load, fill_input, click_at_xy, js, capture_screenshot

new_tab('https://snapinsta.com.br/')
wait_for_load()
fill_input('.input-box', 'https://www.instagram.com/reel/XXXX/')
# ENCONTRAR BOTAO DINAMICAMENTE — NUNCA usar coordenadas fixas
btn_rect = js('''(() => {
  const b = [...document.querySelectorAll("button")].find(x => x.textContent.includes("Download"));
  return {x: Math.round(b.getBoundingClientRect().x + b.offsetWidth/2), y: Math.round(b.getBoundingClientRect().y + b.offsetHeight/2)};
})()''')
click_at_xy(btn_rect.x, btn_rect.y)
wait_for_load()
capture_screenshot()  # verificar resultado
```

> **PITFALL:** NUNCA usar coordenadas fixas (ex.: `click_at_xy(852, 281)`) para o botao Download — mudam conforme largura da tela e responsividade. Sempre encontrar o botao dinamicamente via JS filtrando pelo texto ("Download" ou "Baixar").

### Mensagens de Erro Comuns

| Mensagem | Causa | Ação |
|----------|-------|------|
| `"Insira um link válido"` | URL inválida ou formato nao suportado | Verificar URL, remover params extras |
| Rate limit | Limite diario atingido (~30 downloads/IP/dia) | Esperar ~24h ou usar browser_exec |
| Conteúdo privado | Conta privada ou post removido | Impossível baixar via API |
| Timeout/Erro inesperado | Insta instável ou rede lenta | Retry com delay de 5-10s |
