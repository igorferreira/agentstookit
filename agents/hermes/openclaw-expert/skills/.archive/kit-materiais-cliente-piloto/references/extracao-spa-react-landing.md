# Extração de conteúdo de landing pages SPA React (validado 04/09/2026)

Caso real: extrair TODO o conteúdo do workshop-ia.techleads.club/v3 para documentação.
A página é uma SPA React (Vite) — `curl` retorna só o shell HTML (~28 KB, quase sem texto).

## Escada de extração (da mais barata para a mais cara)

1. **curl + parse do HTML**: às vezes o shell já traz hero/meta (title, description, headline). Extrair texto com regex tag-stripping — mas esperar pouco.
2. **Ler o final do HTML**: apps Vite injetam a lista de bundles num `<script>` inline (padrão `var tags=["<link... /assets/index-XXXX.js">", "<link ... /assets/Section-YYYY.js">"]`). Esse é o mapa do tesouro.
3. **Baixar os chunks JS de conteúdo**: nomes autoexplicativos (`WorkshopSection-*`, `workshopSpeakers-*`, `InstructorsSectionContent-*`, `PainPointsSection-*`, `FAQSection-*`, `TestimonialsSection-*`, `RealProblemSection-*`, `CTASection-*`).
4. **Extrair strings de texto dos bundles** (ver script abaixo), filtrando lixo de CSS/JS.
5. **Estruturas tipadas**: procurar `name:`/`title:`/`role:`/`day:`/`tab:` nos bundles para pegar objetos estruturados (professores, módulos, agenda).
6. **web_search para completar bios** de pessoas citadas (LinkedIn, GitHub, imprensa).

## Script de extração de strings pt-BR de um bundle

```python
import re
raw = open('/tmp/bundle.js', encoding='utf-8', errors='ignore').read()
strs = re.findall(r'"((?:[^"\\]|\\.){12,900})"', raw)
out, seen = [], set()
for s in strs:
    t = s.encode().decode('unicode_escape', errors='ignore')
    # texto plausível em pt: palavras minúsculas acentuadas separadas por espaço
    if re.search(r'[a-z\u00e0-\u00ff]{3}\s[a-z\u00e0-\u00ff]', t, re.I):
        # filtrar lixo técnico
        if not re.match(r'^(http|assets/|function|const |var |import)', t) \
           and not re.search(r'(className|fixed |flex |grid |absolute|relative|rounded|text-\[|px-|py-|mb-|mt-|border|bg-|w-\d|h-\d)', t) \
           and not re.search(r'[{};()]', t):
            if t not in seen:
                seen.add(t); out.append(t)
print('\n'.join(out))
```

## Pitfalls

- **Filtro regex**: cuidado com classes de caractere acentuado literais (usar `\u00e0-\u00ff`, não caracteres colados no fonte — um erro `bad character range` quebra o heredoc inteiro).
- **Bundles de biblioteca** (embla-carousel, radix) geram centenas de strings inúteis — filtrar por palavras-pt de conteúdo (`\b(de|da|do|para|com|que|como)\b`) e excluir `[{};()]`.
- **O texto dos módulos pode estar no chunk da SEÇÃO**, não no bundle raiz da variante — baixar todos os chunks nomeados por seção.
- **Objetos estruturados** (bios com nome/cargo) são mais confiáveis via regex `name\s*:\s*"..."` do que por heurística de texto.
- **Wayback/archive.today não ajudam** se a página nunca foi crawlada — ir direto para os chunks.

## Resultado comprovado
Com essa escada extraíram-se: 7 módulos completos, 7 professores com cargos, materiais bônus, dores de marketing e posicionamento — sem browser (CDP) e sem paywall.
