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

# Skill: Diário de Atividades e Pensamentos (com Memória Infinita)

## Visão Geral

Esta skill orienta o registro contínuo de atividades realizadas, pensamentos, reflexões, fotos, mídias e links web no cofre do Obsidian do Igor em:

`/home/usuario/MEGA/Documentos/obsidian/NotasDiarias`

Pasta para fotos e anexos:
`/home/usuario/MEGA/Documentos/obsidian/NotasDiarias/anexos`

Perfil recomendado:
`diario`

## Protocolo de Memória Infinita
- O histórico de todas as notas `.md` em `/home/usuario/MEGA/Documentos/obsidian/NotasDiarias/` funciona como a memória persistente e infinita de longo prazo.
- Sempre que Igor perguntar sobre fatos do passado, resuma hábitos, busque padrões ou queira recuperar uma anotação antiga, use busca textual (grep/read) nos arquivos `.md` do diário ou no histórico do banco `state.db` (via `session_search`).

## Regra de Ouro do Formato de Arquivos
- **Formatos Textuais**: Todos os arquivos de texto criados pelo agente DEVEM ser obrigatoriamente no formato Markdown (`.md`).
- **Exceção**: Apenas utilize a extensão `.txt` se Igor solicitar expressamente na mensagem.

## Quando Usar

Use quando Igor enviar ou mencionar:
- O que fez no dia (tarefas, reuniões, treinos, entregas);
- Pensamentos, desabafos, ideias ou reflexões;
- Imagens ou fotos para anexar no diário;
- Links de sites, artigos ou vídeos que quer salvar com anotações;
- Perguntas sobre eventos passados, ideias antigas ou memórias salvas no diário;
- Pedidos de fechamento diário ou retrospectiva semanal.

## Estrutura da Nota Diária (`AAAA-MM-DD.md`)

Template padrão de uma nova nota diária:

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
