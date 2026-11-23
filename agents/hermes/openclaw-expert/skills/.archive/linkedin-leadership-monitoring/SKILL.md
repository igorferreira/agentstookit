---
name: linkedin-leadership-monitoring
description: Use for public LinkedIn leadership monitoring.
---
# Monitoramento de liderança no LinkedIn

## Objetivo

Monitorar publicações públicas de presidentes, vice-presidentes, diretores e superintendentes de uma empresa, catalogando o conteúdo e alertando o usuário quando houver publicação nova. O escopo é conteúdo público; nunca presumir acesso a pensamentos, intenções privadas, mensagens diretas ou conteúdo restrito.

## Procedimento obrigatório

1. **Defina o escopo institucional.** Separe país, empresa, grupo econômico e período. Para liderança da HDI, começar pela liderança atual do Grupo HDI Brasil/HDI Seguros Brasil; incluir presidente quando solicitado.
2. **Crie a pasta canônica antes da coleta.** Use uma pasta de trabalho com `INDEX.md`, `WATCHLIST.md`, `perfis/`, `posts/`, `analises/` e `relatorios/`. No ambiente do Igor, a pasta de LinkedIn corporativo fica em `~/MEGA/Documentos/trabalho_projetos_ti/ia_corporativa/linkedin_hdi/`.
3. **Monte e valide a watchlist.** Para cada pessoa, registre nome, cargo, organização, URL pública, fonte de confirmação, data da validação e status `confirmado`, `provável` ou `pendente`. Não transforme snippet de mecanismo de busca em confirmação definitiva.
4. **Descubra publicações sem ultrapassar acesso.** Priorize URLs públicas indexadas, página pública do perfil e fontes oficiais. Use `social-fetch` para posts por URL, `web-research` para descoberta/validação e `browser-use` apenas quando a página pública exigir JavaScript. Não contorne login, CAPTCHA, paywall, bloqueio ou perfil privado.
5. **Capture antes de interpretar.** Salve um registro por post com URL, ID, autor, cargo no momento da coleta, data de publicação, data de coleta, texto disponível, mídia pública, fonte de captura e limitações. Deduplicate por ID/URL; se o texto mudar, preserve a versão anterior.
6. **Analise em camadas.** Separe sempre: (a) texto literal ou transcrição fiel; (b) tema; (c) fatos verificáveis; (d) posicionamentos explicitamente publicados; (e) inferências/hipóteses; (f) relevância para estratégia, IA, tecnologia, seguros e operações. Nunca escreva “o executivo pensa X” quando a fonte só permite dizer “publicou/defendeu X”.
7. **Alerte somente novidade verificável.** O alerta deve conter pessoa, cargo, data, link, resumo curto, tema, grau de confiança e eventual limitação de acesso. Não enviar alerta duplicado e não afirmar que não houve postagem se a plataforma não permitiu verificar o perfil.
8. **Faça consolidações periódicas.** Relatórios podem agrupar temas, recorrências, mudanças de vocabulário, prioridades declaradas e lacunas de evidência. Não transformar frequência de postagem em diagnóstico de personalidade ou intenção.
9. **Verifique a watchlist após mudanças organizacionais.** Cargo atual, empresa e liderança mudam; marque perfis antigos como históricos em vez de continuar tratando-os como liderança atual.

## Formato mínimo do registro de post

```markdown
# POST-AAAA-MM-DD-autor-id

- Autor:
- Cargo na coleta:
- Publicado em:
- Coletado em:
- URL:
- Fonte/método:
- Status de acesso: público / parcial / indisponível

## Conteúdo disponível

## Fatos e posicionamentos explícitos

## Análise e hipóteses

## Temas e tags

## Limitações
```

## Regras específicas do Igor

- Entregar os caminhos absolutos dos registros e dos relatórios no MEGA.
- Responder em português do Brasil, com linguagem direta.
- Manter a distinção entre HDI Seguros Brasil e Grupo HDI internacional.
- Incluir o presidente na watchlist quando o escopo for a liderança da HDI.
- Não misturar publicações pessoais irrelevantes com posicionamento corporativo sem marcar essa diferença.
- Não usar dados reais internos da HDI, sistemas corporativos ou informações não públicas.
- Não publicar, comentar, curtir, seguir ou enviar mensagens em nome do Igor.

## Alertas automatizados

Quando houver vigia agendado, o job deve ler a watchlist e os registros anteriores, buscar somente conteúdo público novo, deduplicar e enviar o alerta ao canal de origem. Se a coleta falhar, informar “verificação inconclusiva” em vez de “nenhuma publicação”. Preferir um script/estado local para deduplicação e uma etapa de análise separada, evitando que cada execução repita todo o histórico.

## Limitações e ética

“Tudo que eles pensam” não é um resultado tecnicamente ou eticamente obtível. O produto é um arquivo auditável do que foi publicado publicamente e das interpretações explicitamente marcadas como hipóteses. Minimizar dados pessoais e excluir conteúdo privado, familiar ou não relacionado ao papel profissional.

## Relação com outras skills

- `social-fetch`: captura normalizada de um post por URL.
- `web-research`: descoberta, validação e fontes externas.
- `linkedin-optimization`: contexto de linguagem e posicionamento no LinkedIn, não substitui o monitoramento.
- `browser-use`: fallback para páginas públicas renderizadas por JavaScript.

Não confundir este monitoramento com `linkedin-post-specialist`, que é voltado à redação/publicação de posts do Igor e não à vigilância de liderança externa.
