# Áudio/voz apresentando-se a uma pessoa (pitch em voz)

Workflow validado em 03/09/2026: gerar um áudio (text_to_speech / Piper pt-BR) do
agente apresentando-se a um contato do Igor (família, figura pública, cliente).
É da mesma classe de "conteúdo pronto para um destinatário" que as mensagens de
WhatsApp deste skill — muda o canal (voz) e exige qualidade de roteiro como produto.

## Quando usar
- O usuário pede um "áudio" de apresentação, pitch, agradecimento ou mensagem de voz
  a um contato. Entregue como `[[audio_as_voice]] MEDIA:<path>` (voice bubble).
- Mesmr `text_to_speech` p/ voz em pt-BR local (Piper).

## Fluxo que funciona
1. **Pesquisar a pessoa antes** (web_search: nome + papel). Traça perfil real
   (cargo, história, bandeiras) p/ citar fatos verdadeiros e conectar-se com o que
   a pessoa valoriza. Ex: líder público → agenda/discurso/pauta; líder de núcleo
   etário → inclusão digital/proteção/educação financeira.
2. **Salvar perfil + estratégia em Markdown** (pasta pessoas_clientes/<nome>/) antes
   do roteiro — base verificável.
3. **Ajustar o TOM à relacão** — família/amigo = afetuoso e simples ("meu querido",
   "como a gente é família"); profissional = formal. Clarificar a relação; não assumir.
4. **PROOFREAD o roteiro antes de gerar** — palavras inventadas/gírias entram no
   áudio e forçam regravação.
5. **Pausa no nome** — abrir com o nome ("Zé Augusto.") e nova frase, p/ o TTS
   pronunciar o nome limpo e pausado.
6. **Entregar MEDIA:** + resumo do conteúdo + o que NÃO inclui.

## Restrições de conteúdo (sensíveis)
- Respeitar sigilo/não-confirmações do usuário (ex.: NÃO citar candidatura não
  confirmada pela pessoa — falar "atuação pública" de forma ampla).
- Exemplo prático real do que o agente já fez (resolução concreta de problema) dá
  credibilidade; citar caso real, não generalidade vazia.

## Pitfalls (vistos em uso)
- **"machuco"**: palavra-sem-sentido entrou no roteiro TTS e o usuário reclamou
  ("que machuco é esse cara?"). Sempre reler o roteiro caçando gírias/neologismos
  antes de gerar; trocar por frase natural.
- **Tom errado por relação assumida**: regravei formal quando era relação familiar.
  Clarificar relação antes de gravar economiza iteração.
- **Mencionar fato sensível**: só falar de posições/planos não confirmados com
  autorização explícita do Igor.