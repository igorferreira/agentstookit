---
name: diario-registro
description: "Use para registrar atividades, pensamentos, ideias, fotos, arquivos e links no diário do Igor sob /home/usuario/MEGA/Documentos/obsidian/NotasDiarias com suporte a memoria infinita."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [diario, obsidian, notas, pensamentos, fotos, links, memoria-infinita, markdown]
---

# Skill: Diário de Atividades e Pensamentos

## Visão Geral

Registro contínuo de atividades, pensamentos, reflexões e eventos do dia em formato estruturado Markdown.

## Caminhos de Diário

## Caminhos de Diário

Dois caminhos disponíveis (escolha o mais adequado ao contexto):

1. **Diário Canônico (novo):** `/home/usuario/MEGA/Documentos/diario/AAAA-MM-DD.md`
   - Template limpo, agrupado por domínio (Saúde, Tecnologia, Relacionamento, etc.)
   - Sincroniza automaticamente pro Google Drive via Insync (`usuariobr`)
   - Ideal para registro de eventos factuais do dia

2. **Notas Diárias (legado):** `/home/usuario/MEGA/Documentos/obsidian/NotasDiarias/AAAA-MM-DD.md`
   - Template Obsidian-friendly com anexos, links e reflexões
   - Ideal para pensamentos mais introspectivos e mídia

## Estrutura da Nota Canônica (`Diario/AAAA-MM-DD.md`)

```markdown
# Diário — AAAA-MM-DD (Dia da Semana)

## 🩺 Saúde
- Eventos de saúde: exames, treinos, alimentação, peso

## 💻 Tecnologia
- Eventos tech: agentes, notebooks, sistemas, ferramentas

## ❤️ Relacionamento
- Eventos de relacionamento: conversas, crises, decisões

## 🏠 Infraestrutura / Casa
- Casa, contas, insync, nuvem, etc.

---

*Registrado por Hermes em AAAA-MM-DD HH:MM*
```

## Estrutura da Nota Diária (`obsidian/NotasDiarias/AAAA-MM-DD.md`)

```markdown
# 📅 Diário - AAAA-MM-DD

## 🎯 Destaques do Dia
- [HH:MM] 

## 🛠️ O que fiz hoje (Atividades & Tarefas)
- [HH:MM] 

## 💡 Pensamentos, Ideias & Reflexões
- [HH:MM] 

## 📸 Fotos, Mídias & Anexos
- [HH:MM] 

## 🔗 Links & Referências Web
- [HH:MM] 

## 📌 Pendências para Amanhã
- [ ] 
```

## Protocolo de Manipulação de Imagens e Anexos

1. Quando uma foto/imagem for enviada (via Telegram/Gateway ou caminho de arquivo local):
   - Mover ou salvar a imagem em `/home/usuario/MEGA/Documentos/obsidian/NotasDiarias/anexos/`.
   - Nomear como: `AAAA-MM-DD_HHMMSS_<descricao-curta>.<ext>`.
   - Inserir a imagem na seção `📸 Fotos, Mídias & Anexos` do arquivo `AAAA-MM-DD.md` com a sintaxe:
     `![[anexos/AAAA-MM-DD_HHMMSS_descricao-curta.ext]]` ou `![descrição](anexos/AAAA-MM-DD_HHMMSS_descricao-curta.ext)`.
   - Adicionar legenda explicando o contexto do arquivo.

## Protocolo de Links Web

1. Quando um link/URL for enviado:
   - Tentar obter o título e contexto do link.
   - Adicionar na seção `🔗 Links & Referências Web` do arquivo `AAAA-MM-DD.md`:
     `- [HH:MM] [Título do Link](URL) - Descrição em 1 linha sobre o conteúdo ou interesse de Igor.`

## Regras de Atualização Incremental (Append)

1. Verificar a data atual usando `date`.
2. Verificar se a nota `AAAA-MM-DD.md` já existe em `/home/usuario/MEGA/Documentos/obsidian/NotasDiarias/`.
3. Se NÃO existir: criar o arquivo com o cabeçalho e estrutura completa do template (extensão `.md`).
4. Se JÁ existir: ler o conteúdo atual, localizar a seção adequada (Fatos, Pensamentos, Fotos, Links, etc.) e adicionar a nova linha no final dessa seção mantendo o horário `[HH:MM]`.
5. NUNCA apagar ou sobrescrever anotações anteriores da nota diária.
