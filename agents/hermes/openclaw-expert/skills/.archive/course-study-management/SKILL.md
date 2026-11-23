---
name: course-study-management
description: "Use when saving courses in MEGA. Organize OCR study lists."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [cursos, estudos, educacao, ocr, mega]
---

# Gestão de cursos e estudos

## Objetivo

Organizar cursos, trilhas e listas de estudo do Igor em uma pasta canônica do MEGA, preservando a fonte original, separando OCR de validação e deixando o material pronto para acompanhamento posterior.

## Pasta canônica

Use sempre:

`/home/igorferreira/MEGA/Documentos/educacao_leitura/cursos/`

Arquivos esperados:

- `INDEX.md`: índice geral, status e links para fichas.
- `cursos.txt`: lista legada de links rápidos; preservar o conteúdo existente.
- `YYYYMMDD_<tema>.md`: ficha estruturada de uma lista ou trilha.
- `posts/`: imagens originais de publicações usadas como fonte.

## Procedimento

1. Leia as regras de documentos e cursos aplicáveis antes de escrever.
2. Preserve a imagem/PDF original em `cursos/posts/` ou na pasta temática de origem, usando nome sem espaços.
3. Faça OCR visual da imagem inteira e, quando houver texto pequeno, repita com recorte regional; extraia instituição, título, URL visível, autor e título da publicação.
4. Não invente URLs: registre exatamente o link visível e marque como `OCR — não validado` quando o endereço estiver encurtado, ilegível ou não testado.
5. Crie uma ficha Markdown com tabela contendo número, curso/tema, instituição, link, status e observações.
6. Inclua checklist por curso: link validado, gratuidade, carga horária, idioma, certificado, início, conclusão e aprendizados.
7. Atualize `INDEX.md` com a nova trilha, data de captura, tema, status e link relativo.
8. Acrescente os links a `cursos.txt` sem apagar nem reformatar links legados.
9. Se a lista vier de uma publicação, registre também o post no índice de posts salvos da área de educação, mantendo a ficha de cursos como registro canônico para estudo.
10. Verifique lendo de volta os arquivos e confirme que a imagem original, a ficha e o índice existem.

## Status de estudo

Use apenas estes estados no índice e nas fichas:

- ⬜ A estudar
- 🔵 Em andamento
- ✅ Concluído
- ⏸️ Pausado

Não marque curso como gratuito, certificado ou validado apenas porque o post afirma isso; esses campos permanecem pendentes até consulta à página oficial.

## Preferências do Igor

- Responder em português do Brasil.
- Entregar caminhos dos arquivos salvos.
- Usar listas e tabelas Markdown legíveis, sem esconder a distinção entre OCR e informação confirmada.
- Sugerir uma ordem prática de estudo, mas não transformar a sugestão em status concluído.
- Manter uma pasta geral de cursos no MEGA, em vez de deixar listas espalhadas somente em posts, screenshots ou arquivos temporários.

## Pitfalls

- Classifique o material como curso/trilha salvo, não como curso concluído, até que o progresso seja registrado.
- Preserve a imagem original porque OCR pode perder URLs, acentos ou títulos.
- Não substitua `cursos.txt` por uma nova lista: ele é legado e pode conter links não relacionados à captura atual.
- Não valide disponibilidade, idioma, carga horária ou certificado por inferência do logotipo; abra a fonte oficial quando essa confirmação for solicitada.
- Não misture uma lista de cursos com a pasta de filmes/aulas: a publicação pode permanecer como fonte arquivada, mas a ficha de execução deve ficar em `educacao_leitura/cursos/`.

## Verificação final

- [ ] Imagem original preservada.
- [ ] OCR separado de fatos validados.
- [ ] Ficha Markdown criada.
- [ ] `INDEX.md` atualizado.
- [ ] `cursos.txt` preservado e atualizado quando houver links.
- [ ] Status inicial definido como `⬜ A estudar`.
- [ ] Caminhos relativos conferidos.
